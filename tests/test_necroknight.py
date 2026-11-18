# 暂停测试：冒险专用随从 Necroknight（NAXM_001）；按要求保留原内容为注释。
# from utils import *
#
# from fireplace.dsl.selector import ADJACENT, LEFT_OF, RIGHT_OF, SELF
#
# NECROKNIGHT = "NAXM_001"
# DARKNESS = "LOOT_526"  # The Darkness: dormant when summoned
# WAR_GOLEM = "CS2_186"  # 7/7
# FLAMESTRIKE = "CS2_032"  # 4 damage to all enemy minions
#
#
# def test_necroknight_destroys_both_neighbours_when_killed_by_a_spell():
#     # Necroknight: "Deathrattle: Destroy the minions next to this one as well."
#     game = prepare_empty_game()
#     a = game.player1.summon(WISP)
#     necro = game.player1.summon(NECROKNIGHT)
#     b = game.player1.summon(WISP)
#     far = game.player1.summon(WISP)
#     assert list(game.player1.field) == [a, necro, b, far]
#     game.player1.give(PYROBLAST).play(target=necro)
#     assert necro.zone == Zone.GRAVEYARD
#     assert a.zone == Zone.GRAVEYARD
#     assert b.zone == Zone.GRAVEYARD
#     assert far.zone == Zone.PLAY
#     assert list(game.player1.field) == [far]
#
#
# def test_necroknight_destroys_both_neighbours_when_killed_in_combat():
#     game = prepare_empty_game()
#     a = game.player1.summon(WISP)
#     necro = game.player1.summon(NECROKNIGHT)
#     b = game.player1.summon(WISP)
#     game.end_turn()
#     attacker = game.player2.summon(WAR_GOLEM)
#     game.skip_turn()
#     attacker.attack(necro)
#     assert necro.zone == Zone.GRAVEYARD
#     assert a.zone == Zone.GRAVEYARD
#     assert b.zone == Zone.GRAVEYARD
#     assert list(game.player1.field) == []
#     assert attacker.zone == Zone.PLAY
#
#
# def test_necroknight_at_the_edge_has_one_neighbour():
#     game = prepare_empty_game()
#     necro = game.player1.summon(NECROKNIGHT)
#     b = game.player1.summon(WISP)
#     c = game.player1.summon(WISP)
#     game.player1.give(PYROBLAST).play(target=necro)
#     assert b.zone == Zone.GRAVEYARD
#     assert c.zone == Zone.PLAY
#
#     game = prepare_empty_game()
#     a = game.player1.summon(WISP)
#     b = game.player1.summon(WISP)
#     necro = game.player1.summon(NECROKNIGHT)
#     game.player1.give(PYROBLAST).play(target=necro)
#     assert b.zone == Zone.GRAVEYARD
#     assert a.zone == Zone.PLAY
#
#
# def test_necroknight_alone_destroys_nothing():
#     game = prepare_empty_game()
#     necro = game.player1.summon(NECROKNIGHT)
#     enemy = game.player2.summon(WISP)
#     game.player1.give(PYROBLAST).play(target=necro)
#     assert necro.zone == Zone.GRAVEYARD
#     assert enemy.zone == Zone.PLAY
#
#
# def test_necroknight_ignores_a_dormant_neighbour():
#     game = prepare_empty_game()
#     a = game.player1.summon(WISP)
#     darkness = game.player1.summon(DARKNESS)
#     necro = game.player1.summon(NECROKNIGHT)
#     b = game.player1.summon(WISP)
#     assert darkness.dormant
#     game.player1.give(PYROBLAST).play(target=necro)
#     assert necro.zone == Zone.GRAVEYARD
#     assert b.zone == Zone.GRAVEYARD
#     # The dormant Darkness is skipped: the wisp beyond it is the left neighbour.
#     assert a.zone == Zone.GRAVEYARD
#     assert darkness.zone == Zone.PLAY
#
#
# def test_necroknight_neighbour_dying_at_the_same_time_dies_once():
#     # A neighbour that dies with Necroknight (Flamestrike) is left to Death:
#     # it leaves its one Corpse and Necroknight does not destroy it a second time.
#     game = prepare_empty_game()
#     necro = game.player1.summon(NECROKNIGHT)
#     a = game.player1.summon(WISP)
#     b = game.player1.summon(WISP)
#     corpses = game.player1.corpses
#     necro.damage = 2  # Necroknight is 5/6: Flamestrike's 5 now kills it too
#     game.end_turn()
#     game.player2.give(FLAMESTRIKE).play()
#     assert necro.zone == Zone.GRAVEYARD
#     assert a.zone == Zone.GRAVEYARD
#     assert b.zone == Zone.GRAVEYARD
#     assert list(game.player1.field) == []
#     assert game.player1.corpses == corpses + 3
#
#
# def test_minion_never_in_play_has_no_neighbours():
#     game = prepare_empty_game()
#     game.player1.summon(WISP)
#     in_hand = game.player1.give(NECROKNIGHT)
#     assert not in_hand.has_board_place
#     assert LEFT_OF(SELF).eval([in_hand], in_hand) == []
#     assert RIGHT_OF(SELF).eval([in_hand], in_hand) == []
#     assert ADJACENT(SELF).eval([in_hand], in_hand) == []
