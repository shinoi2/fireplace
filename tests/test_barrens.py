from utils import *


def test_frenzy():
    game = prepare_game()
    raider = game.player1.give("BAR_020").play()
    game.player1.give(MOONFIRE).play(target=raider)
    assert game.player2.hero.damage == raider.atk


def test_frenzy_2():
    game = prepare_game()
    grunt = game.player1.give("BAR_021").play()
    game.player1.give(MOONFIRE).play(target=grunt)
    assert game.player1.hero.armor == 1


def test_blood_shard_bristleback():
    game = prepare_empty_game()
    bristleback = game.player1.give("BAR_916")
    wisp = game.player1.give(WISP).play()

    assert len(game.player1.deck) == 0
    assert bristleback.requires_target()

    for _ in range(10):
        game.player1.give(WISP).shuffle_into_deck()
    assert len(game.player1.deck) == 10
    assert bristleback.requires_target()

    game.player1.give(WISP).shuffle_into_deck()
    assert len(game.player1.deck) == 11
    assert not bristleback.requires_target()
