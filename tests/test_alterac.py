from utils import *


def test_honorable_kill():
    game = prepare_game()
    game.player2.summon(WISP)
    game.player2.summon(WISP)
    game.player1.give("ONY_014").play()
    assert game.player1.hero.atk == 2


def test_kurtrus_demon_render():
    game = prepare_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    game.player1.hero.power.use()
    game.player1.hero.attack(game.player2.hero)
    game.player1.give("AV_204").play()
    assert game.player1.field == ["AV_204t2", "AV_204t2"]
    assert game.player1.field[0].atk == 2
    assert game.player1.field[1].atk == 2


def test_field_of_strife():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    assert wisp.atk == 1
    field = game.player1.give("AV_661").play()
    assert field.zone == Zone.SECRET
    assert wisp.atk == 2
    game.skip_turn()
    assert wisp.atk == 2
    game.skip_turn()
    assert wisp.atk == 2
    game.end_turn()
    assert field.zone == Zone.GRAVEYARD
    assert wisp.atk == 1


def test_raid_negotiator():
    game = prepare_game()
    card = game.player1.card("EX1_165")
    assert not card.choose_both
    with mock(RandomCollectible, [card]):
        game.player1.give("ONY_019").play()
    game.player1.choice.choose(card)
    assert card is game.player1.hand[-1]
    assert card.choose_both
    card.play()
    assert game.player1.field[-1] == "OG_044a"


def test_saidan_the_scarlet():
    game = prepare_game()
    saidan = game.player1.give("AV_345").play()
    assert saidan.atk == 2
    assert saidan.health == 2
    game.player1.give("CS2_092").play(target=saidan)
    assert saidan.atk == 10
    assert saidan.health == 10


def test_magister_dawngrasp():
    game = prepare_game()
    game.player1.give("AV_200").play()
    game.player2.summon("GVG_093")
    assert game.player1.hero.power.data_num_1 == 2
    game.player1.hero.power.use(target=game.player2.field[0])
    assert game.player2.field == []
    assert game.player1.hero.power.data_num_1 == 4
    game.skip_turn()
    game.player2.summon("GVG_044")
    game.player1.hero.power.use(target=game.player2.field[0])
    assert game.player2.field == []
    assert game.player1.hero.power.data_num_1 == 6
