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


def test_school_teacher():
    game = prepare_game()
    teacher = game.player1.give("TSC_052")
    moonfire = game.player1.card(MOONFIRE)
    with mock(RandomSpell, [moonfire]):
        teacher.play()
    game.player1.choice.choose(moonfire)
    nagaling = game.player1.hand[-1]
    assert nagaling == "TSC_052t"
    nagaling.play(target=game.player2.hero)
    assert game.player2.hero.damage == 1
