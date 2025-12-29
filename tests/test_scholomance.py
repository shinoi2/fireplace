from utils import *

def test_sphere_of_sapience():
    game = prepare_game()
    weapon = game.player1.give("SCH_259").play()
    hand_len = len(game.player1.hand)
    game.skip_turn()
    first_card = game.player1.deck[-1]
    second_card = game.player1.deck[-2]
    assert game.player1.choice.cards == ["SCH_259t", first_card]
    assert len(game.player1.hand) == hand_len
    game.player1.choice.choose(first_card)
    hand_len += 1
    assert game.player1.hand[-1] == first_card
    assert len(game.player1.hand) == hand_len
    assert weapon.damage == 0
    
    game.skip_turn()
    first_card = game.player1.deck[-1]
    second_card = game.player1.deck[-2]
    assert game.player1.choice.cards == ["SCH_259t", first_card]
    assert len(game.player1.hand) == hand_len
    game.player1.choice.choose(game.player1.choice.cards[0])
    hand_len += 1
    assert game.player1.deck[0] == first_card
    assert game.player1.hand[-1] == second_card
    assert len(game.player1.hand) == hand_len
    assert weapon.damage == 1


def test_sphere_of_sapience_empty():
    game = prepare_empty_game()
    weapon = game.player1.give("SCH_259").play()
    game.skip_turn()
    assert game.player1.choice is None
    assert weapon.damage == 0


def test_potion_of_illusion():
    game = prepare_empty_game()
    game.player1.give("SCH_352").play()
    assert len(game.player1.hand) == 0
    for _ in range(7):
        game.player1.give(TARGET_DUMMY).play()
    assert len(game.player1.hand) == 0
    game.player1.give("SCH_352").play()
    assert len(game.player1.hand) == 7
    for card in game.player1.hand:
        assert card == TARGET_DUMMY
        assert card.cost == 1
        assert card.atk == 1
        assert card.health == 1
