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


def test_cthun_the_shattered():
    game = prepare_game(include=tuple(["DMF_254"] + [WISP] * 29))
    all_card = list(game.player1.deck + game.player1.hand)
    assert "DMF_254" not in all_card
    pieces = ["DMF_254t3", "DMF_254t4", "DMF_254t5", "DMF_254t7"]
    for piece in pieces:
        assert piece in all_card
        card = all_card[all_card.index(piece)]
        card.zone = Zone.HAND
        game.player1.used_mana = 0
        if card == "DMF_254t7":
            card.play(target=game.player1.field[0])
        else:
            card.play()
    assert "DMF_254" in list(game.player1.deck)
