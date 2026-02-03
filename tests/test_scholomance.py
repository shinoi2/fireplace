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


def test_mindrender_illucia():
    game = prepare_game()
    player1_hand = game.player1.hand[:]
    player2_hand = game.player2.hand[:]
    game.player1.give("SCH_159").play()
    assert game.player1.hand == player2_hand
    assert game.player2.hand == player1_hand
    game.skip_turn()
    assert game.player1.hand[:len(player1_hand)] == player1_hand
    assert game.player2.hand[:len(player2_hand)] == player2_hand


def test_speaker_gidra():
    game = prepare_game()
    gidra = game.player1.give("SCH_182").play()
    old_atk = gidra.atk
    old_health = gidra.max_health
    assert gidra.has_spellburst
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert gidra.atk == old_atk + 4
    assert gidra.max_health == old_health + 4
    assert not gidra.has_spellburst


def test_gibberling():
    game = prepare_game()
    gibberling = game.player1.give("SCH_242").play()
    assert gibberling.has_spellburst
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert not gibberling.has_spellburst
    assert len(game.player1.field) == 2
    assert game.player1.field[1].id == "SCH_242"
    assert game.player1.field[1].has_spellburst
