from utils import *


def test_guess_the_weight():
    # Guess More! Right
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card2.put_on_top()
    card1.put_on_top()
    game.player1.give("DMF_075").play()
    assert card1.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert card2.zone == Zone.HAND
    # Guess More! Wrong
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card2.put_on_top()
    card1.put_on_top()
    game.player1.give("DMF_075").play()
    assert card1.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[1])
    assert card2.zone == Zone.DECK
    # Guess Less! Right
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card1.put_on_top()
    card2.put_on_top()
    game.player1.give("DMF_075").play()
    assert card2.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[1])
    assert card1.zone == Zone.HAND
    # Guess Less! Wrong
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card1.put_on_top()
    card2.put_on_top()
    game.player1.give("DMF_075").play()
    assert card2.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert card1.zone == Zone.DECK
