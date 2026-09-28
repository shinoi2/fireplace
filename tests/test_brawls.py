from utils import *
from utils import _empty_mulligan


def _brawl_game(game_class, deck1=(), deck2=(), hero1=None, hero2=None, mana=10):
    """A game of a Tavern Brawl (a Game subclass of fireplace.brawls), started,
    mulligan kept, both players at `mana` mana."""
    player1 = Player("Player1", list(deck1), hero1 or CardClass.MAGE.default_hero)
    player2 = Player("Player2", list(deck2), hero2 or CardClass.WARRIOR.default_hero)
    player1.cant_fatigue = not deck1
    player2.cant_fatigue = not deck2
    game = game_class(players=(player1, player2))
    game.start()
    _empty_mulligan(game)
    player1.max_mana = mana
    player2.max_mana = mana
    return game


def test_great_summoner_brawl():
    # "When you cast a spell, a random minion of the same cost is summoned for you!"
    # (a summoned minion may summon more: Kolkar Pack Runner, after the spell)
    game = _brawl_game(GreatSummonerBrawl)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.field) >= 1
    assert game.player1.field[0].cost == 0
    assert len(game.player2.field) == 0
    before = list(game.player1.field)
    game.player1.give("CS2_023").play()  # Arcane Intellect, 3
    new = [m for m in game.player1.field if m not in before]
    assert new and new[0].cost == 3
    assert len(game.player2.field) == 0
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert len(game.player2.field) >= 1
    assert game.player2.field[0].controller is game.player2
    # A minion is not a spell
    count = len(game.player2.field)
    game.player2.give(WISP).play()
    assert len(game.player2.field) == count + 1


def test_masked_ball_brawl():
    # "When a minion dies, its disguise is revealed, showing the minion to
    # actually be a different random minion"
    game = _brawl_game(MaskedBallBrawl)
    yeti = game.player1.give("CS2_182")
    yeti.play()
    assert yeti.buffs[0].id == "TB_Pilot1"
    assert yeti.buffs[0].controller is game.player1
    wisp = game.player1.give(WISP)
    wisp.play()
    assert not wisp.buffs  # costs less than (2)
    yeti.destroy()
    assert len(game.player1.field) == 2
    pilot = game.player1.field[-1]
    assert pilot is not yeti
    assert pilot.controller is game.player1
    assert len(game.player2.field) == 0


def test_masked_ball_pilot_costs_two_less():
    # The wiki: "it will summon in its place a random minion that costs 2
    # mana less"; the minion it summons has no disguise.
    game = _brawl_game(MaskedBallBrawl)
    for i in range(2):
        yeti = game.player1.give("CS2_182")
        yeti.play()
        yeti.destroy()
        assert len(game.player1.field) == i + 1
        pilot = game.player1.field[-1]
        assert pilot.cost == 4 - 2
        assert "TB_Pilot1" not in [buff.id for buff in pilot.buffs]


def _drawn_decks(game_class, hero1, hero2, seed=None):
    """The decks a brawl draws, as it gives them to the players: before the
    game starts, and a card transforms in the deck or in the hand (Transfer
    Student)."""
    drawn = []

    class Recording(game_class):
        def pick_first_player(self):
            drawn.extend(list(player.starting_deck) for player in self.players)
            return super().pick_first_player()

    game = Recording(
        players=(Player("Player1", [], hero1), Player("Player2", [], hero2)),
        seed=seed,
    )
    game.start()
    return [
        (player.hero.card_class, [fireplace.cards.db[id] for id in deck])
        for player, deck in zip(game.players, drawn)
    ]


def _check_fixed_and_spells(decks, fixed):
    for card_class, deck in decks:
        assert len(deck) == 30
        assert [c.id for c in deck].count(fixed) == 23
        others = [c for c in deck if c.id != fixed]
        assert len(others) == 7
        for card in others:
            assert card.type == CardType.SPELL
            assert card.collectible
            assert card_class in card.classes


def test_spiders_everywhere_brawl():
    # "your deck will be TEEMING with Webspinners": 23 Webspinners and seven
    # spells of your class
    _check_fixed_and_spells(
        _drawn_decks(SpidersEverywhereBrawl, "HERO_05", "HERO_08"), "FP1_011"
    )
    game = _brawl_game(SpidersEverywhereBrawl, hero1="HERO_05", hero2="HERO_08")
    assert len(game.player1.deck) + len(game.player1.hand) >= 30


def test_too_many_portals_brawl():
    # "a few spells and a WHOLE lot of portals"
    _check_fixed_and_spells(
        _drawn_decks(TooManyPortalsBrawl, "HERO_02", "HERO_09"), "GVG_003"
    )


def test_crossroads_encounter_brawl():
    # "Pick a class. Let's see what's in your deck this time!": fifteen
    # cards of your class, fifteen neutral cards (a card of two classes
    # counts as neutral and of its classes)
    for card_class, deck in _drawn_decks(CrossroadsEncounterBrawl, "HERO_06", "HERO_01"):
        assert len(deck) == 30
        assert all(c.collectible for c in deck)
        assert len([c for c in deck if card_class in c.classes]) >= 15
        assert len([c for c in deck if c.card_class == CardClass.NEUTRAL]) >= 15
        assert [
            c
            for c in deck
            if card_class not in c.classes and c.card_class != CardClass.NEUTRAL
        ] == []


def test_brawl_fixed_decks():
    for deck, hero in (
        GrandTournamentBrawl.ALLERIA_DECK,
        GrandTournamentBrawl.MEDIVH_DECK,
        BlackrockShowdownBrawl.NEFARIAN_DECK,
        BlackrockShowdownBrawl.RAGNAROS_DECK,
    ):
        assert len(deck) == 30
        assert [id for id in deck if id not in fireplace.cards.db] == []
        assert fireplace.cards.db[hero].type == CardType.HERO
    assert GrandTournamentBrawl.ALLERIA_DECK[0].count("AT_103") == 1
    assert GrandTournamentBrawl.ALLERIA_DECK[0].count("AT_108") == 2


def test_grand_tournament_brawl():
    # Alleria and Medivh, each with their own deck, drawn between the seats
    for _ in range(4):
        game = GrandTournamentBrawl.new_game(
            Player("Player1", [], "HERO_01"), Player("Player2", [], "HERO_01")
        )
        game.start()
        heroes = sorted(player.hero.id for player in game.players)
        assert heroes == ["HERO_05a", "HERO_08a"]
        for player in game.players:
            assert len(player.deck) + len(player.hand) == 30 + (
                1 if player.hand.filter(id=THE_COIN) else 0
            )


def test_brawl_decks_follow_the_seed():
    decks = [
        [[c.id for c in deck] for _, deck in _drawn_decks(TooManyPortalsBrawl, "HERO_05", "HERO_08", seed=7)]
        for _ in range(2)
    ]
    assert decks[0] == decks[1]


def test_double_deathrattler_battler():
    # "minions with Deathrattle now rattle twice", for both players
    game = _brawl_game(
        DoubleDeathrattlerBattler, deck1=[WISP] * 10, deck2=[WISP] * 10
    )
    for player in game.players:
        hand = len(player.hand)
        hoarder = player.summon("EX1_096")  # Loot Hoarder: Deathrattle: draw
        hoarder.destroy()
        assert len(player.hand) == hand + 2
    game.end_turn()
    hand = len(game.player2.hand)
    game.player2.summon("EX1_096").destroy()
    assert len(game.player2.hand) == hand + 2


def test_pick_your_fate_coin():
    # Fate: Coin: "When a minion dies, its owner gets a Coin.", for the
    # minions in play and for those summoned later
    game = prepare_empty_game()
    wisp1 = game.player1.summon(WISP)
    game.player1.give("TB_PickYourFate_7").play()
    assert "TB_PickYourFate_7_EnchMinion" in [b.id for b in wisp1.buffs]
    for player in game.players:
        assert "TB_PickYourFate_7Ench" in [b.id for b in player.buffs]
    wisp2 = game.player1.summon(WISP)
    assert "TB_PickYourFate_7_EnchMinion" in [b.id for b in wisp2.buffs]
    wisp1.destroy()
    assert game.player1.hand[-1].id == "TB_011"
    wisp2.destroy()
    assert game.player1.hand[-1].id == "TB_011"


def _fate(fate, game=None):
    game = game or prepare_empty_game()
    game.player1.give(fate).play()
    return game


def _buff_ids(entity):
    return [b.id for b in entity.buffs]


def test_pick_your_fate_is_the_same_for_both_players():
    # A fate is a rule of the game: the opponent of the player who picks it
    # lives under it too, and nobody gets it twice.
    game = _fate("TB_PickYourFate_7")
    wisp = game.player2.summon(WISP)
    assert _buff_ids(wisp).count("TB_PickYourFate_7_EnchMinion") == 1
    mine = game.player1.summon(WISP)
    assert _buff_ids(mine).count("TB_PickYourFate_7_EnchMinion") == 1
    hand1, hand2 = len(game.player1.hand), len(game.player2.hand)
    wisp.destroy()
    assert len(game.player1.hand) == hand1
    assert game.player2.hand[-1].id == "TB_011"
    assert len(game.player2.hand) == hand2 + 1

    # Fate: Bananas
    game = _fate("TB_PickYourFate_2")
    for player in game.players:
        wisp = player.summon(WISP)
        assert _buff_ids(wisp).count("TB_PickYourFate_2_EnchMinion") == 1
        hand = len(player.hand)
        wisp.destroy()
        assert len(player.hand) == hand + 1

    # Fate: Armor
    game = _fate("TB_PickYourFate_8rand")
    game.end_turn()
    assert (game.player1.hero.armor, game.player2.hero.armor) == (0, 2)
    game.end_turn()
    assert (game.player1.hero.armor, game.player2.hero.armor) == (2, 2)

    # Fate: Spells
    game = _fate("TB_PickYourFate_5")
    for player in game.players:
        assert player.give(FIREBALL).cost == 4 - 1

    # Dire Fate: Taunt and Charge
    game = _fate("TB_PickYourFate_1")
    game.end_turn()
    wisp = game.player2.give(WISP)
    wisp.play()
    assert wisp.taunt and wisp.charge
    assert _buff_ids(wisp).count("TB_AllMinionsTauntCharge") == 1

    # Fate: Confusion, at the end of each turn
    game = _fate("TB_PickYourFate_12")
    yeti = game.player1.summon("CS2_182")
    game.end_turn()
    assert (yeti.atk, yeti.health) == (5, 4)
    game.end_turn()
    assert (yeti.atk, yeti.health) == (4, 5)


def _blingtron_game():
    game = prepare_empty_game()
    for player in game.players:
        game.queue_actions(player, [Buff(player, "TB_BlingBrawl_Blade2e")])
    return game


def test_blingtron_blade_hero():
    # Blingtron's Beauteous Brawl: the rule on each player gives Blingtron's
    # Blade to the weapons they equip
    game = _blingtron_game()
    for player in game.players:
        assert "TB_BlingBrawl_Blade2e" in [b.id for b in player.buffs]
    axe = game.player1.give("CS2_106")
    axe.play()
    assert [b.id for b in axe.buffs] == ["TB_BlingBrawl_Blade1e"]
    game.end_turn()
    axe = game.player2.summon("CS2_106")
    assert [b.id for b in axe.buffs] == ["TB_BlingBrawl_Blade1e"]


def test_blingtron_blade_breaks_into_a_new_weapon():
    # Blingtron's Blade: "When this breaks, randomly summon a new weapon.";
    # the new one has the Blade too. Cash In: "Destroy your weapon, gaining
    # a random one."
    game = _blingtron_game()
    axe = game.player1.give("CS2_106")
    axe.play()
    axe.destroy()
    weapon = game.player1.weapon
    assert weapon is not None and weapon is not axe
    assert [b.id for b in weapon.buffs] == ["TB_BlingBrawl_Blade1e"]
    assert game.player2.weapon is None
    game.player1.summon("TP_Bling_HP2")
    before = game.player1.weapon
    game.player1.hero.power.use()
    assert game.player1.weapon is not None
    assert game.player1.weapon is not before


def test_gift_exchange_stolen_gift():
    # The wiki (Gift Exchange): the destroyed Winter Veil Gift gives the
    # current player a Stolen Gift: "Discover a card belonging to the class
    # of the player who controlled the Winter Veil Gift minion, with its mana
    # cost reduced by 5"; spells and minions of 5 or more only, no neutral.
    for _ in range(5):
        game = _brawl_game(Game, hero1="HERO_08", hero2="HERO_01")  # Mage, Warrior
        assert game.player1.hero.card_class != game.player2.hero.card_class
        gift = game.player2.summon("TB_GiftExchange_Treasure")
        game.player1.give(FIREBALL).play(target=gift)
        stolen = game.player1.hand[-1]
        assert stolen.id == "TB_GiftExchange_Treasure_Spell"
        assert not game.player2.hand.filter(id="TB_GiftExchange_Treasure_Spell")
        stolen.play()
        choice = game.player1.choice
        assert len(choice.cards) == 3
        for card in choice.cards:
            assert game.player2.hero.card_class in card.classes
            assert card.type in (CardType.MINION, CardType.SPELL)
            assert card.data.cost >= 5
        picked = choice.cards[0]
        choice.choose(picked)
        assert game.player1.hand[-1] is picked
        assert picked.cost == max(picked.data.cost - 5, 0)
        assert picked.controller is game.player1

def test_gift_exchange_gift_for_everyone():
    # "If a player has no gifts at the start of their turn, Greatfather
    # Winter delivers a fresh one."
    game = _brawl_game(Game)
    for player in game.players:
        game.queue_actions(player, [Buff(player, "TB_GiftExchange_Rule")])
    game.end_turn()
    assert len(game.player2.field.filter(id="TB_GiftExchange_Treasure")) == 1
    assert len(game.player1.field) == 0
    game.end_turn()
    gift = game.player1.field.filter(id="TB_GiftExchange_Treasure")[0]
    game.end_turn()
    game.end_turn()
    assert game.player1.field == [gift]
    gift.destroy()
    game.end_turn()
    game.end_turn()
    assert len(game.player1.field.filter(id="TB_GiftExchange_Treasure")) == 1


def _miniature_game():
    game = _brawl_game(Game, deck1=["CS2_182", FIREBALL] * 10, deck2=["CS2_182"] * 20)
    for player in game.players:
        game.queue_actions(player, [Buff(player, "TB_Mini_Rule")])
    return game


def _mini(card):
    return (card.atk, card.health, card.cost) == (1, 1, 1)


def test_miniature_warfare():
    # The wiki (Miniature Warfare): the Miniature enchantment ("Mini-sized,
    # set to 1/1", and it costs (1)) "is granted to all minions while still
    # in the hand, and affects all minions whether played from the hand, or
    # summoned by spells, Hero Powers, or other minions' effects"; only
    # minions.
    game = _miniature_game()
    for player in game.players:
        for card in list(player.hand) + list(player.deck):
            if card.type == CardType.MINION:
                assert _mini(card), card
                assert "TB_Mini_1e" in [b.id for b in card.buffs]
            elif card.id == FIREBALL:
                assert card.cost == 4
    yeti = game.player1.hand.filter(id="CS2_182")[0]
    yeti.play()
    assert _mini(yeti)
    tidehunter = game.player1.give("EX1_506")  # Battlecry: summon a 2/1 Murloc Scout
    tidehunter.play()
    assert _mini(tidehunter)
    assert _mini(game.player1.field[-1]) and game.player1.field[-1].id == "EX1_506a"
    wolf = game.player2.summon("CS2_boar")
    assert _mini(wolf)
    assert [b.id for b in yeti.buffs].count("TB_Mini_1e") == 1


def test_miniature_cannot_be_silenced():
    # "applied through a game-wide aura, and as a result cannot be removed
    # through Silences"; a buff still counts on top of it.
    game = _miniature_game()
    yeti = game.player1.summon("CS2_182")
    game.player1.give(SILENCE).play(target=yeti)
    assert _mini(yeti)
    game.player1.give("CS2_092").play(target=yeti)  # Blessing of Kings, +4/+4
    assert (yeti.atk, yeti.health) == (5, 5)
    # back in hand, it is still mini
    game.end_turn()
    game.player2.give("EX1_581").play(target=yeti)  # Sap
    assert yeti.zone == Zone.HAND
    assert _mini(yeti)


BANANAS = ("EX1_014t", "TB_006", "TB_007", "TB_008")


def test_banana_brawl():
    # Banana Brawl!: "Whenever one of your minions dies, he gives you a
    # Banana to celebrate!" (the Game no longer calls _schedule_death)
    game = _brawl_game(BananaBrawl)
    hand1, hand2 = len(game.player1.hand), len(game.player2.hand)
    game.player1.summon(WISP).destroy()
    assert len(game.player1.hand) == hand1 + 1
    assert game.player1.hand[-1].id in BANANAS
    assert len(game.player2.hand) == hand2
    game.player2.summon(WISP).destroy()
    assert len(game.player2.hand) == hand2 + 1
    assert game.player2.hand[-1].id in BANANAS
    # Not for a spell, nor for a hero
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.hand) == hand1 + 1


LEEROY = "EX1_116"  # 5 mana, Legendary
ONYXIA = "EX1_562"  # 9 mana, Legendary


def test_cloneball_offensive_play():
    # Offensive Play: "The next Legendary minion you play and all your other
    # copies cost (3) less." The wiki (Cloneball!): it "lasts until the player
    # plays a legendary minion card, and can stack multiple times".
    game = prepare_empty_game()
    player = game.player1
    player.max_mana = 10
    leeroys = [player.give(LEEROY) for _ in range(3)]
    in_deck = player.card(LEEROY, zone=Zone.DECK)
    onyxia = player.give(ONYXIA)
    yeti = player.give("CS2_182")
    player.give("TB_Superfriends001").play()
    assert [c.cost for c in leeroys] == [2, 2, 2]
    assert (onyxia.cost, yeti.cost) == (6, 4)
    leeroys[0].play()
    assert player.used_mana == 2
    # The other copies keep the discount, the next legendary no longer has it
    assert [c.cost for c in leeroys[1:]] == [2, 2]
    assert in_deck.cost == 2
    assert onyxia.cost == 9
    assert "TB_Superfriends001e" not in [b.id for b in player.buffs]
    # A minion that is not legendary does not use it up; two stack
    player.give("TB_Superfriends001").play()
    player.give("TB_Superfriends001").play()
    assert onyxia.cost == 3
    yeti.play()
    assert onyxia.cost == 3
    onyxia.play()
    assert [c.cost for c in leeroys[1:]] == [2, 2]
    # The opponent is untouched
    other = game.player2.give(LEEROY)
    assert other.cost == 5
