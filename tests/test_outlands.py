from utils import *


def test_kaelthas_sunstrider():
    game = prepare_empty_game()
    fireball = game.player1.give(FIREBALL)
    game.player1.give(THE_COIN).play()
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give("BT_255").play()
    assert fireball.cost == 0
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 0


def test_metamorphosis():
    game = prepare_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    game.player1.hero_power.use()
    old_hero_power = game.player1.hero_power
    game.player1.give("BT_429").play()
    assert game.player1.hero_power == "BT_429p"
    game.player1.hero_power.use(target=game.player2.hero)
    assert game.player1.hero_power == "BT_429p2"
    assert game.player1.hero_power.exhausted
    game.skip_turn()
    game.player1.hero_power.use(target=game.player2.hero)
    assert game.player1.hero_power == old_hero_power
    assert not game.player1.hero_power.exhausted


def test_imprisoned_antaen():
    game = prepare_game()
    antaen = game.player1.give("BT_934").play()
    assert antaen.dormant
    assert antaen.dormant_turns == 2
    game.skip_turn()
    assert antaen.dormant
    assert antaen.dormant_turns == 1
    game.skip_turn()
    assert not antaen.dormant
    assert antaen.dormant_turns == 0
    assert game.player2.hero.health == 20
    game.end_turn()
    sap = game.player2.give("EX1_581")
    sap.play(target=antaen)
    game.end_turn()
    antaen.play()
    assert antaen.dormant
    assert antaen.dormant_turns == 2
    game.skip_turn()
    assert antaen.dormant
    assert antaen.dormant_turns == 1
    game.skip_turn()
    assert not antaen.dormant
    assert antaen.dormant_turns == 0
    assert game.player2.hero.health == 10


def test_darkglare():
    game = prepare_game()
    game.player1.give("BT_307").play()
    assert game.player1.mana == 8
    game.player1.give(FIREBALL).play(target=game.player1.hero)
    assert game.player1.mana == 8 - 4 + 2


def test_maiev_shadowsong():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    assert not wisp.dormant
    assert wisp.dormant_turns == 0
    game.player1.give("BT_737").play(target=wisp)
    assert wisp.dormant
    assert wisp.dormant_turns == 2
    game.skip_turn()
    assert wisp.dormant
    assert wisp.dormant_turns == 1
    game.skip_turn()
    assert not wisp.dormant
    assert wisp.dormant_turns == 0
