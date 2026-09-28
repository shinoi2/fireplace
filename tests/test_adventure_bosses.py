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
