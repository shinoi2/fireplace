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
    for card_class, deck in _drawn_decks(
        CrossroadsEncounterBrawl, "HERO_06", "HERO_01"
    ):
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
        [
            [c.id for c in deck]
            for _, deck in _drawn_decks(
                TooManyPortalsBrawl, "HERO_05", "HERO_08", seed=7
            )
        ]
        for _ in range(2)
    ]
    assert decks[0] == decks[1]


def test_double_deathrattler_battler():
    # "minions with Deathrattle now rattle twice", for both players
    game = _brawl_game(DoubleDeathrattlerBattler, deck1=[WISP] * 10, deck2=[WISP] * 10)
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


def _game_with_rule(rule, deck1=(), deck2=()):
    """A game whose rule (an enchantment) is on both players before the
    mulligan, applied as the Hearthstone wrapper does (no action queued
    during the mulligan)."""
    player1 = Player("Player1", list(deck1), CardClass.MAGE.default_hero)
    player2 = Player("Player2", list(deck2), CardClass.WARRIOR.default_hero)
    player1.cant_fatigue = not deck1
    player2.cant_fatigue = not deck2
    game = Game(players=(player1, player2))
    game.start()
    for player in game.players:
        player.card(rule, source=player.hero).apply(player)
    _empty_mulligan(game)
    return game


def test_wacky_waxy_large_waxy_gift():
    # Large Waxy Gift: "Deathrattle: Add a random Legendary minion to your
    # opponent's hand. It costs (3) less."
    game = prepare_empty_game()
    gift = game.player1.summon("TB_KoboldGiftMinion")
    assert (gift.atk, gift.health) == (0, 4)
    hand1, hand2 = len(game.player1.hand), len(game.player2.hand)
    gift.destroy()
    assert len(game.player1.hand) == hand1
    assert len(game.player2.hand) == hand2 + 1
    legend = game.player2.hand[-1]
    assert legend.type == CardType.MINION and legend.rarity == Rarity.LEGENDARY
    assert legend.cost == max(0, legend.data.cost - 3)
    game.end_turn()
    game.player2.max_mana = 10
    legend.play()
    assert legend.cost == legend.data.cost


def test_wacky_waxy_presents_drop_on_turns_1_and_7():
    # "All gifts are summoned on turn 1" (four on each side), "At Turn 7, 4
    # more presents will drop on each side of the board", as many as fit.
    game = _game_with_rule("TB_KoboldGiftEnch")
    assert game.turn == 1
    for player in game.players:
        assert [m.id for m in player.field] == ["TB_KoboldGiftMinion"] * 4
    for _ in range(5):
        game.end_turn()
    assert game.turn == 6
    for player in game.players:
        assert len(player.field) == 4
    game.player2.field[0].destroy()
    game.player2.field[0].destroy()
    game.end_turn()
    assert game.turn == 7
    assert len(game.player1.field) == 7
    assert len(game.player2.field) == 6
    for _ in range(4):
        game.end_turn()
    assert len(game.player2.field) == 6
    # The spell drops four presents on its player's side
    game = prepare_empty_game()
    game.player1.give("TB_KoboldGiftSpell").play()
    assert [m.id for m in game.player1.field] == ["TB_KoboldGiftMinion"] * 4
    assert not game.player2.field


def test_yellow_brick_dorothee():
    # Dorothee: "Minions to the left have Charge. Minions to the right have
    # Taunt." The wiki (Yellow-Brick Brawl): a permanent; "She cannot be
    # targeted or attacked", "will not be affected by auras", "is not affected
    # by AoE effects", "does not count as a minion for effects that require a
    # certain number of minions", "She does however still take up a minion
    # space"; "Silence does not remove the Charge or Taunt effects".
    game = prepare_empty_game()
    p1, p2 = game.player1, game.player2
    p1.max_mana = p2.max_mana = 10
    dorothee = p1.summon("TB_Dorothee_001")
    assert dorothee.dormant
    left = p1.give(WISP)
    left.play(index=0)
    right = p1.give("CS2_182")
    right.play(index=2)
    assert [m.id for m in p1.field] == [WISP, "TB_Dorothee_001", "CS2_182"]
    assert left.charge and not left.taunt and left.can_attack()
    assert right.taunt and not right.charge and not right.can_attack()
    assert not dorothee.charge and not dorothee.taunt
    # Silence does not take the aura away
    p1.give(SILENCE).play(target=right)
    assert right.taunt
    # Not a target, not attackable, not hit by an area of effect, not
    # counted, not buffed by an aura
    fireball = p1.give(FIREBALL)
    assert dorothee not in fireball.targets
    assert dorothee not in left.attack_targets
    game.end_turn()
    wolf = p2.summon("CS2_boar")
    wolf.turns_in_play = 1
    assert dorothee not in wolf.attack_targets
    p2.give("CS2_032").play()  # Flamestrike: 4 damage to all enemy minions
    assert dorothee.zone == Zone.PLAY and dorothee.health == 10
    game.end_turn()
    p1.give("CS2_222").play()  # Stormwind Champion: other friendly minions +1/+1
    assert (dorothee.atk, dorothee.health) == (0, 10)
    p1.used_mana = 0
    p1.give("EX1_312").play()  # Twisting Nether: destroy all minions
    assert dorothee.zone == Zone.PLAY
    assert len(p1.field) == 1
    game.end_turn()
    p2.summon(WISP)
    tech = p2.give("EX1_085")  # Mind Control Tech: 4 or more enemy minions
    for _ in range(3):
        p1.summon(WISP)
    tech.play()
    assert dorothee.controller is p1 and len(p1.field) == 4
    # She takes up a space
    for _ in range(3):
        p1.summon(WISP)
    assert len(p1.field) == 7


def test_clockwork_card_dealer():
    # "the card draw at the start of each turn will always try to draw a card
    # whose mana cost matches the turn number [...] If the deck lacks an
    # appropriate on-curve draw on a given turn, a random card will be drawn
    # instead"; only the draw at the start of the turn.
    curve = ["CS2_189", "CS2_172", "CS2_122", "CS2_182", "CS2_131", "CS2_200"]  # 1 to 6
    deck = [WISP] * 24 + curve
    game = _game_with_rule("TB_GreatCurves_01", deck, deck)
    on_curve = 0
    for _ in range(12):
        player = game.current_player.opponent
        costs = [c.cost for c in player.deck]
        turn = len(player.turns) + 1
        game.end_turn()
        drawn = player.hand[-1]
        if turn in costs:
            assert drawn.cost == turn, (turn, drawn)
            on_curve += 1
        for card in list(player.hand):
            if card.cost:
                card.discard()
    assert on_curve >= 4
    # Another draw is a normal draw: the top of the deck
    top = game.current_player.deck[-1]
    game.current_player.draw()
    assert game.current_player.hand[-1] is top


def test_visions_of_sayge():
    # "At the start of each turn, the player is offered a choice between two
    # cards to add to their hand. The card they don't choose is given to the
    # opponent." and "Cards are still drawn from the deck at the start of the
    # turn."
    deck = [WISP] * 30
    game = _game_with_rule("TB_VisionsOfSayge_Rule", deck, deck)
    for _ in range(4):
        player = game.current_player
        opponent = player.opponent
        choice = player.choice
        assert choice is not None and len(choice.cards) == 2
        assert all(c.data.collectible for c in choice.cards)
        kept, given = choice.cards
        deck_before = len(player.deck)
        hand, other_hand = len(player.hand), len(opponent.hand)
        choice.choose(kept)
        assert player.choice is None
        assert kept.zone == Zone.HAND and kept.controller is player
        assert given.zone == Zone.HAND and given.controller is opponent
        assert given in opponent.hand
        # The draw of the turn came after the choice
        assert len(player.deck) == deck_before - 1
        assert len(player.hand) == hand + 2
        assert len(opponent.hand) == other_hand + 1
        for card in list(player.hand) + list(opponent.hand):
            card.discard()
        game.end_turn()


EGG = "TB_Noblegarden_002"
BUNNY = "TB_Noblegarden_002t1"
DYES = ["TB_Noblegarden_003t%i" % n for n in range(1, 9)]


def _two_turns(game):
    game.end_turn()
    game.end_turn()


def test_everybunny_egg_hatches_into_a_bunny():
    # Noblegarden Egg: "Stealth. At the start of your turn, hatch this into
    # something cute." The wiki: "Without any dyes applied, it will always
    # spawn a Bunny".
    game = prepare_empty_game()
    egg = game.player1.summon(EGG)
    assert egg.stealthed and Race.EGG in egg.races
    game.end_turn()
    assert game.player1.field[0].id == EGG
    game.end_turn()
    bunny = game.player1.field[0]
    assert bunny.id == BUNNY and (bunny.atk, bunny.health) == (1, 3)
    assert not bunny.stealthed


def test_everybunny_dyes():
    # "Dye an Egg. When it hatches, it grants <keyword>." (Red: +2/+2); the
    # dyes of one egg stack; a dye needs an Egg.
    game = prepare_empty_game()
    p1 = game.player1
    p1.max_mana = 10
    wisp = p1.summon(WISP)
    blue = p1.give("TB_Noblegarden_003t1")
    assert not blue.is_playable()
    egg1 = p1.summon(EGG)
    egg2 = p1.summon(EGG)
    assert blue.targets == [egg1, egg2] or set(blue.targets) == {egg1, egg2}
    assert wisp not in blue.targets
    blue.play(target=egg1)
    assert "TB_Noblegarden_003t1e" in [b.id for b in egg1.buffs]
    p1.give("TB_Noblegarden_003t8").play(target=egg2)
    p1.give("TB_Noblegarden_003t7").play(target=egg2)
    p1.give("TB_Noblegarden_003t4").play(target=egg2)
    _two_turns(game)
    first, second = p1.field[1], p1.field[2]
    assert first.id == BUNNY and first.windfury and (first.atk, first.health) == (1, 3)
    assert second.id == BUNNY and (second.atk, second.health) == (3, 5)
    assert second.divine_shield and second.stealthed and not second.windfury
    for n, keyword in ((2, "lifesteal"), (3, "poisonous"), (5, "rush"), (6, "taunt")):
        egg = p1.summon(EGG)
        p1.used_mana = 0
        p1.give("TB_Noblegarden_003t%i" % n).play(target=egg)
        p1.give("TB_Noblegarden_004").play()  # Noblegarden Spoon
        assert egg.morphed.id == BUNNY and getattr(egg.morphed, keyword), keyword
        egg.morphed.destroy()


def test_everybunny_shifting_dye():
    # Shifting Dye: "Each turn this is in your hand, transform it into a
    # random dye." The wiki: it "can change on the same turn it's drawn".
    game = prepare_empty_game()
    p1 = game.player1
    p1.card("TB_Noblegarden_003", zone=Zone.DECK)
    p1.draw()
    dye = p1.hand[-1]
    assert dye.id in DYES
    assert "TB_Noblegarden_003e" in [b.id for b in dye.buffs]
    _two_turns(game)
    shifted = p1.hand[-1]
    assert shifted.id in DYES and shifted is not dye
    # In the starting hand, it shifts at the start of the turn
    game = prepare_empty_game()
    shifting = game.player1.give("TB_Noblegarden_003")
    _two_turns(game)
    assert game.player1.hand[-1].id in DYES


def test_everybunny_spoon_carrots_hen():
    game = prepare_empty_game()
    p1 = game.player1
    p1.max_mana = 10
    eggs = [p1.summon(EGG), p1.summon(EGG)]
    enemy_egg = game.player2.summon(EGG)
    # Noblegarden Spoon: "Hatch your Noblegarden Eggs!"
    p1.give("TB_Noblegarden_004").play()
    assert [m.id for m in p1.field] == [BUNNY, BUNNY]
    assert enemy_egg.zone == Zone.PLAY and enemy_egg.id == EGG
    # Carrots: "Give friendly minions +1/+1 or +2/+2 if it's a Bunny."
    wisp = p1.summon(WISP)
    p1.give("TB_Noblegarden_005").play()
    assert [(m.atk, m.health) for m in p1.field] == [(3, 5), (3, 5), (2, 2)]
    assert (enemy_egg.atk, enemy_egg.health) == (0, 2)
    # Hawkstrider Hen: "Battlecry and Deathrattle: Summon a Noblegarden Egg."
    p1.used_mana = 0
    hen = p1.give("TB_Noblegarden_006")
    hen.play()
    assert [m.id for m in p1.field][-2:] == ["TB_Noblegarden_006", EGG]
    hen.destroy()
    assert [m.id for m in p1.field].count(EGG) == 2


class _FirstPlayerFirst(BaseTestGame):
    def pick_first_player(self):
        return self.players[0], self.players[1]


def _monster(hero):
    """An empty game where player1 (the first player) is the Monster Smash
    hero `hero`, with its own hero power (HERO_POWER of CardDefs.xml), at 10
    mana."""
    player1 = Player("Player1", [], hero)
    player2 = Player("Player2", [], CardClass.WARRIOR.default_hero)
    player1.cant_fatigue = player2.cant_fatigue = True
    game = _FirstPlayerFirst(players=(player1, player2))
    game.start()
    _empty_mulligan(game)
    player1.max_mana = player2.max_mana = 10
    return game


def test_monster_smash_heroes_have_their_powers():
    # The nine heroes of Monster Smash, and the power each one's HERO_POWER
    # names (Brushwood Centurion: "Axe Around" on the wiki, GILA_BOSS_41p).
    powers = {
        "TB_BountyHunt_Chupacabran": "TB_Chupacabran_HP",
        "TB_BountyHunt_Winslow": "GILA_BOSS_64p",
        "TB_BountyHunt_Experiment3C": "GILA_BOSS_27p",
        "TB_BountyHunt_Wharrgarbl": "GILA_BOSS_37p",
        "TB_BountyHunt_Azalina": "GILA_BOSS_55p",
        "TB_BountyHunt_BloodWitch": "GILA_BOSS_30p",
        "TB_BountyHunter_Plaguemaster": "GILA_BOSS_68p",
        "TB_BountyHunt_Shudderwock": "GILA_BOSS_47p",
        "TB_BountyHunt_Brushwood": "GILA_BOSS_41p",
    }
    for hero, power in powers.items():
        game = _monster(hero)
        assert game.player1.hero.power.id == power, hero


def test_monster_smash_bloodthirst_consume_hypnotize():
    # Bloodthirst: "Give a friendly minion +1/+1 and Lifesteal."
    game = _monster("TB_BountyHunt_Chupacabran")
    p1 = game.player1
    wisp = p1.summon(WISP)
    assert game.player2.summon(WISP) not in p1.hero.power.targets
    p1.hero.power.use(target=wisp)
    assert (wisp.atk, wisp.health) == (2, 2) and wisp.lifesteal
    # Consume: "Destroy a friendly minion, then draw 3 cards." (both ids)
    for power in ("GILA_BOSS_27p", "TB_BountyHunt_Consume"):
        game = _monster("TB_BountyHunt_Experiment3C")
        p1 = game.player1
        p1.summon(power)
        for _ in range(5):
            p1.card(WISP, zone=Zone.DECK)
        wisp = p1.summon(WISP)
        hand = len(p1.hand)
        p1.hero.power.use(target=wisp)
        assert wisp.dead or wisp.zone == Zone.GRAVEYARD
        assert len(p1.hand) == hand + 3
    # Hypnotize: "Each player shuffles their hand into their deck and draws
    # that many cards." (both ids)
    for power in ("GILA_BOSS_64p", "TB_BountyHunt_Hypnotize"):
        game = _monster("TB_BountyHunt_Winslow")
        p1, p2 = game.player1, game.player2
        p1.summon(power)
        for player in game.players:
            for _ in range(10):
                player.card("CS2_182", zone=Zone.DECK)
        mine = [p1.give(WISP), p1.give(WISP)]
        theirs = [p2.give(FIREBALL)]
        hands = (len(p1.hand), len(p2.hand))
        decks = (len(p1.deck), len(p2.deck))
        p1.hero.power.use()
        assert (len(p1.hand), len(p2.hand)) == hands
        assert (len(p1.deck), len(p2.deck)) == decks
        assert all(c.zone == Zone.DECK or c in p1.hand for c in mine)
        assert theirs[0].zone in (Zone.DECK, Zone.HAND)


def test_monster_smash_boss_powers():
    # It's Raining Fin: "Draw 3 Murlocs from your deck."
    game = _monster("TB_BountyHunt_Wharrgarbl")
    p1 = game.player1
    for _ in range(4):
        p1.card("CS2_168", zone=Zone.DECK)  # Murloc Raider
    for _ in range(4):
        p1.card("CS2_182", zone=Zone.DECK)
    p1.hero.power.use()
    assert [c.id for c in p1.hand].count("CS2_168") == 3
    # Unfinished Business: "Summon three 1/1 Wisps."
    game = _monster("TB_BountyHunt_Azalina")
    game.player1.hero.power.use()
    assert [(m.id, m.atk, m.health) for m in game.player1.field] == [
        ("GILA_BOSS_55t", 1, 1)
    ] * 3
    # Blood Red Apple: "Passive Hero Power: Spells cost Health instead of Mana."
    game = _monster("TB_BountyHunt_BloodWitch")
    p1 = game.player1
    assert not p1.hero.power.is_usable()
    p1.give(FIREBALL).play(target=game.player2.hero)
    assert p1.used_mana == 0 and p1.hero.health == 30 - 4
    # Frumiousity: "Passive Hero Power: All Battlecries trigger twice."
    game = _monster("TB_BountyHunt_Shudderwock")
    p1, p2 = game.player1, game.player2
    p1.give("CS2_189").play(target=p2.hero)  # Elven Archer: 1 damage
    assert p2.hero.health == 30 - 2
    game.end_turn()
    p2.give("CS2_189").play(target=p1.hero)
    assert p1.hero.health == 50 - 2
    # Poison Flask: "Deal 2 damage to a minion. If it survives, give it
    # Poisonous."
    game = _monster("TB_BountyHunter_Plaguemaster")
    p1 = game.player1
    yeti = game.player2.summon("CS2_182")
    p1.hero.power.use(target=yeti)
    assert yeti.health == 3 and yeti.poisonous
    game.end_turn()
    game.end_turn()
    wisp = game.player2.summon(WISP)
    p1.hero.power.use(target=wisp)
    assert wisp.dead or wisp.zone == Zone.GRAVEYARD
    # Survival of the Fittest: "All minions attack random enemy minions."
    game = _monster("TB_BountyHunt_Brushwood")
    p1, p2 = game.player1, game.player2
    mine = p1.summon("CS2_182")
    theirs = p2.summon("CS2_182")
    p1.hero.power.use()
    # Each yeti attacked the other one: 4 damage twice
    assert mine.dead and theirs.dead


def test_monster_smash_boss_cards():
    game = _monster("TB_BountyHunt_Experiment3C")
    p1, p2 = game.player1, game.player2
    # Witchwood's Touch: "Draw a card. Gain 6 Armor."
    p1.card(WISP, zone=Zone.DECK)
    touch = p1.give("GILA_BOSS_99t")
    hand = len(p1.hand)
    touch.play()
    assert len(p1.hand) == hand and p1.hand[-1].id == WISP and p1.hero.armor == 6
    # Amalgamate: "Destroy all minions. Summon an Amalgamation with the
    # combined Attack and Health."
    p1.used_mana = 0
    p1.summon("CS2_182")  # 4/5
    p2.summon("CS2_120")  # 2/3
    p1.give("GILA_BOSS_27t").play()
    assert [m.id for m in p1.field] == ["GILA_BOSS_27t2"] and not p2.field
    amalgamation = p1.field[0]
    assert (amalgamation.atk, amalgamation.health) == (6, 8)
    # Hack: "Deal 1 damage to a minion. Then do it four more times."
    p1.used_mana = 0
    ogre = p2.summon("CS2_200")  # 6/7
    p1.give("GILA_BOSS_41t").play(target=ogre)
    assert ogre.health == 2
    # Infected Quillflinger: "Whenever this minion takes damage, deal 1
    # damage to a random enemy minion."
    quill = p1.summon("GILA_BOSS_68t")
    p1.give(MOONFIRE).play(target=quill)
    assert ogre.health == 1
    # Soul Assimilation: "Destroy your Wisps. Gain control of a random enemy
    # minion for each Wisp destroyed."
    game = _monster("TB_BountyHunt_Azalina")
    p1, p2 = game.player1, game.player2
    wisps = [p1.summon("GILA_BOSS_55t"), p1.summon(WISP)]
    enemies = [p2.summon("CS2_182") for _ in range(3)]
    p1.give("GILA_BOSS_55t2").play()
    assert all(w.zone == Zone.GRAVEYARD for w in wisps)
    assert len(p1.field) == 2 and len(p2.field) == 1
    assert all(m.controller is p1 for m in p1.field)
