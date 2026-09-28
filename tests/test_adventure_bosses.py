from utils import *
from utils import _empty_mulligan


def _boss_game(hero1, hero2="HERO_01", deck=None):
    """A game where player1 (the first to play) is the boss `hero1`, 10 mana each."""
    deck = deck if deck is not None else [WISP] * 20
    player1 = Player("Player1", list(deck), hero1)
    player2 = Player("Player2", list(deck), hero2)
    game = BaseTestGame(players=(player1, player2))
    game.start()
    _empty_mulligan(game)
    if game.player1 is not player1:
        game.end_turn()
    return game, player1, player2


def test_magmatron():
    # Magmatron (Omnotron Defense System): "Whenever a player plays a card,
    # Magmatron deals 2 damage to them."
    for magmatron in ("BRMA14_9", "BRMA14_9H"):
        game = prepare_empty_game()
        game.player1.summon(magmatron)
        game.player1.give(WISP).play()
        assert game.player1.hero.damage == 2
        assert game.player2.hero.damage == 0
        game.end_turn()
        game.player2.give(WISP).play()
        assert game.player2.hero.damage == 2
        assert game.player1.hero.damage == 2


def test_omnotron_defense_system():
    # Activate Arcanotron, then Toxitron, Electron, Magmatron, Activate!
    for hero in ("BRMA14_1", "BRMA14_1H"):
        game, boss, _ = _boss_game(hero)
        powers = []
        for turn in range(5):
            powers.append(boss.hero.power.id)
            boss.hero.power.use()
            game.end_turn()
            game.end_turn()
        h = "H" if hero.endswith("H") else ""
        assert powers == [
            "BRMA14_2" + h,
            "BRMA14_4" + h,
            "BRMA14_6" + h,
            "BRMA14_8" + h,
            "BRMA14_10" + h,
        ]
        assert boss.field.filter(id="BRMA14_9" + h)


def test_the_alchemist():
    # Maloriak: "Passive Hero Power: Whenever a minion is summoned, swap its
    # Attack and Health."; heroic: "Your minions have +2/+2."
    game, boss, other = _boss_game("BRMA15_1")
    yeti = other.summon("CS2_182")
    assert (yeti.atk, yeti.health) == (5, 4)
    mine = boss.summon("CS2_182")
    assert (mine.atk, mine.health) == (5, 4)
    game, boss, other = _boss_game("BRMA15_1H")
    yeti = other.summon("CS2_182")
    assert (yeti.atk, yeti.health) == (5, 4)
    mine = boss.summon("CS2_182")
    assert (mine.atk, mine.health) == (5 + 2, 4 + 2)


def test_ancient_power():
    # Skelesaurus Hex: "Give each player a random card. It costs (0)."
    game, boss, other = _boss_game("LOEA13_1", deck=[])
    hands = len(boss.hand), len(other.hand)
    boss.hero.power.use()
    assert (len(boss.hand), len(other.hand)) == (hands[0] + 1, hands[1] + 1)
    for player in (boss, other):
        card = player.hand[-1]
        assert card.cost == 0
        assert "LOEA13_2e" in [b.id for b in card.buffs]
    # the Skelesaurus Hex minion of Rafaam's fight does it at the end of turn
    game, boss, other = _boss_game("HERO_08", deck=[])
    boss.summon("LOEA16_26")
    game.end_turn()
    assert other.hand[-1].cost == 0 and boss.hand[-1].cost == 0
