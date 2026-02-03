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


def test_horrendous_growth():
    game = prepare_empty_game()
    growth = game.player1.give("DMF_124")
    assert growth.cost == 2
    assert growth.atk == 2
    assert growth.max_health == 2
    game.player1.give("CS2_127").play()
    corrputed = game.player1.hand[0]
    assert corrputed.id == "DMF_124t"
    assert corrputed.atk == 3
    assert corrputed.max_health == 3
    game.player1.give("CS2_127").play()
    corrputed = game.player1.hand[0]
    assert corrputed.atk == 4
    assert corrputed.max_health == 4
    game.player1.give("CS2_127").play()
    corrputed = game.player1.hand[0]
    assert corrputed.atk == 5
    assert corrputed.max_health == 5
