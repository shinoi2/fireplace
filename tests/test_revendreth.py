from utils import *


def test_suspicious_alchemist():
    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    coin = game.player1.card(THE_COIN)
    fireball = game.player1.card(FIREBALL)
    pyroblast = game.player1.card(PYROBLAST)
    with mock(RandomSpell, [coin, fireball, pyroblast]):
        game.player1.give("REV_000").play()
    game.player1.choice.choose(coin)
    game.end_turn()
    game.player2.choice.choose(coin)
    assert game.player1.hand == [THE_COIN]
    assert game.player2.hand == [THE_COIN]


def test_suspicious_alchemist_2():
    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    coin = game.player1.card(THE_COIN)
    fireball = game.player1.card(FIREBALL)
    pyroblast = game.player1.card(PYROBLAST)
    with mock(RandomSpell, [coin, fireball, pyroblast]):
        game.player1.give("REV_000").play()
    game.player1.choice.choose(coin)
    game.end_turn()
    game.player2.choice.choose(fireball)
    assert game.player1.hand == [THE_COIN]
    assert game.player2.hand == []
