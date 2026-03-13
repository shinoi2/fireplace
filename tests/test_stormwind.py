from utils import *


def test_flightmaster_dungar_1():
    game = prepare_game()
    dungar = game.player1.give("SW_079").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert dungar.dormant
    assert len(game.player1.field) == 1
    game.skip_turn()
    assert not dungar.dormant
    assert len(game.player1.field) == 2


def test_flightmaster_dungar_2():
    game = prepare_game()
    dungar = game.player1.give("SW_079").play()
    game.player1.choice.choose(game.player1.choice.cards[1])
    game.player1.hero.hit(20)
    for _ in range(3):
        assert game.player1.hero.health == 10
        assert dungar.dormant
        game.skip_turn()
    assert not dungar.dormant
    assert game.player1.hero.health == 20


def test_flightmaster_dungar_3():
    game = prepare_game()
    dungar = game.player1.give("SW_079").play()
    game.player1.choice.choose(game.player1.choice.cards[2])
    for _ in range(5):
        assert dungar.dormant
        game.skip_turn()
    assert not dungar.dormant
    assert game.player2.hero.damage == 12
