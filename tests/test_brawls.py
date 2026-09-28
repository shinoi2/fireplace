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
    game = _brawl_game(GreatSummonerBrawl)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.field) == 1
    assert game.player1.field[0].cost == 0
    assert len(game.player2.field) == 0
    game.player1.give("CS2_023").play()  # Arcane Intellect, 3
    assert len(game.player1.field) == 2
    assert game.player1.field[1].cost == 3
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert len(game.player2.field) == 1
    assert game.player2.field[0].controller is game.player2
    # A minion is not a spell
    game.player2.give(WISP).play()
    assert len(game.player2.field) == 2


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
