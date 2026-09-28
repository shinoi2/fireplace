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


def _whole_deck(player):
    return [c.id for c in player.deck] + [c.id for c in player.hand if c.id != THE_COIN]


def _check_fixed_and_spells(game, fixed):
    for player in game.players:
        deck = _whole_deck(player)
        assert len(deck) == 30
        assert deck.count(fixed) == 23
        others = [fireplace.cards.db[id] for id in deck if id != fixed]
        assert len(others) == 7
        for card in others:
            assert card.type == CardType.SPELL
            assert player.hero.card_class in card.classes


def test_spiders_everywhere_brawl():
    # "your deck will be TEEMING with Webspinners": 23 Webspinners and seven
    # spells of your class
    game = _brawl_game(SpidersEverywhereBrawl, hero1="HERO_05", hero2="HERO_08")
    _check_fixed_and_spells(game, "FP1_011")


def test_too_many_portals_brawl():
    # "a few spells and a WHOLE lot of portals"
    game = _brawl_game(TooManyPortalsBrawl, hero1="HERO_02", hero2="HERO_09")
    _check_fixed_and_spells(game, "GVG_003")


def test_crossroads_encounter_brawl():
    # "Pick a class. Let's see what's in your deck this time!": fifteen
    # cards of your class, fifteen neutral cards
    game = _brawl_game(CrossroadsEncounterBrawl, hero1="HERO_06", hero2="HERO_01")
    for player in game.players:
        deck = [fireplace.cards.db[id] for id in _whole_deck(player)]
        assert len(deck) == 30
        assert all(c.collectible for c in deck)
        assert len([c for c in deck if player.hero.card_class in c.classes]) >= 15
        assert len([c for c in deck if c.card_class == CardClass.NEUTRAL]) >= 15
        assert all(
            player.hero.card_class in c.classes or c.card_class == CardClass.NEUTRAL
            for c in deck
        )


def test_brawl_decks_follow_the_seed():
    decks = []
    for _ in range(2):
        player1 = Player("Player1", [], "HERO_05")
        player2 = Player("Player2", [], "HERO_08")
        game = TooManyPortalsBrawl(players=(player1, player2), seed=7)
        game.start()
        decks.append(sorted(_whole_deck(player1)) + sorted(_whole_deck(player2)))
    assert decks[0] == decks[1]
