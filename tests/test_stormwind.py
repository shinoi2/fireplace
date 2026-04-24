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


def test_gain_momentum():
    game = prepare_game()
    quest = game.player1.give("SW_039")
    quest.play()
    assert quest.progress == 0
    game.player1.draw()
    assert quest.progress == 1
    game.player1.draw(4)
    assert quest.zone == Zone.GRAVEYARD
    quest2 = game.player1.secrets[0]
    assert quest2.id == "SW_039t"
    assert quest2.progress == 0
    assert quest2.zone == Zone.SECRET
    for hand in game.player1.hand[:-5]:
        assert hand.cost == hand.data.cost
    for hand in game.player1.hand[-5:]:
        assert hand.cost == max(0, hand.data.cost - 1)


def test_wickerclaw():
    game = prepare_game(CardClass.DRUID, CardClass.DRUID)
    wickerclaw = game.player1.give("SW_436").play()
    atk = wickerclaw.atk
    game.player1.hero.power.use()
    assert wickerclaw.atk == atk + 2


def test_elwynn_boar():
    game = prepare_game()
    for _ in range(6):
        boar = game.player1.give("SW_075").play()
        game.player1.give(MOONFIRE).play(target=boar)
        assert game.player1.weapon is None
    boar = game.player1.give("SW_075").play()
    game.player1.give(MOONFIRE).play(target=boar)
    assert game.player1.weapon == "SW_075t"


def test_elwynn_boar_2():
    game = prepare_game()
    for _ in range(7):
        boar = game.player1.give("SW_075").play()
        assert game.player1.weapon is None
    game.player1.give("ULD_717").play()
    assert game.player1.weapon == "SW_075t"


def test_lost_in_the_park():
    game = prepare_game(CardClass.DRUID, CardClass.DRUID)
    quest = game.player1.give("SW_428").play()
    game.player1.hero.power.use()
    assert quest.progress == 1
    game.skip_turn()
    game.player1.give("BT_512").play()
    assert quest.zone == Zone.GRAVEYARD
    quest2 = game.player1.secrets[0]
    assert quest2 == "SW_428t"
    assert game.player1.hero.armor == 6


def test_arcane_overflow():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give("DED_517").play(target=wisp)
    assert game.player2.field == ["DED_517t"]
    remnant = game.player2.field[0]
    assert remnant.cost == 7
    assert remnant.atk == 7
    assert remnant.health == 7


def test_enthusiastic_banker():
    game = prepare_game()
    banker = game.player1.give("SW_069").play()
    game.skip_turn()
    game.skip_turn()
    game.skip_turn()
    game.player1.discard_hand()
    banker.destroy()
    assert len(game.player1.hand) == 3


def test_brilliant_macaw():
    game = prepare_game()
    game.player1.give("DMF_004").play()
    game.skip_turn()
    game.player1.give("DED_509").play()
