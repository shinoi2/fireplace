from utils import *


def test_xhilag_of_the_abyss():
    game = prepare_game()
    game.player1.summon("TSC_219")
    assert game.player1.field == [
        "TSC_219t",
        "TSC_219t2",
        "TSC_219",
        "TSC_219t3",
        "TSC_219t4",
    ]
    game.skip_turn()
    assert game.player2.hero.damage == 2 * 4
    game.skip_turn()
    assert game.player2.hero.damage == 2 * 4 + 3 * 4
