from utils import *


def test_reckoning():
    game = prepare_game()
    reckoning = game.player1.give("CS3_016")
    reckoning.play()
    assert reckoning in game.player1.secrets
    game.end_turn()

    boar = game.player2.give("CS2_171").play()
    boar.attack(game.player1.hero)
    assert not boar.dead
    assert reckoning in game.player1.secrets

    wolf = game.player2.give("CS2_124").play()
    wolf.attack(game.player1.hero)
    assert wolf.dead
    assert reckoning not in game.player1.secrets
