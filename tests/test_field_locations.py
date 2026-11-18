from utils import *

LOCATION = "REV_942"  # Relic Vault
YETI = "CS2_182"


def test_field_filter_excludes_locations_and_dormant_minions():
    game = prepare_empty_game()
    location = game.player1.give(LOCATION).play()
    wisp = game.player1.summon(WISP)
    dormant = game.player1.summon("BT_121")
    assert dormant.dormant
    assert game.player1.field.filter(type=CardType.MINION, dormant=False) == [wisp]
    assert location in game.player1.field


def test_locations_keep_their_slots_and_actions_but_are_not_characters():
    game = prepare_empty_game()
    player = game.player1
    location = player.give(LOCATION).play()
    wisp = player.summon(WISP)
    assert player.characters == [player.hero, wisp]
    assert location not in list(player.live_entities)
    assert location in list(player.entities)
    assert location in list(player.actionable_entities)
    assert location in game.board
    assert player.minion_slots == 5
    game.skip_turn()
    assert location.zone == Zone.PLAY


def test_locations_are_not_attack_or_spell_targets():
    game = prepare_empty_game()
    enemy = game.player2
    location = enemy.summon(LOCATION)
    yeti = game.player1.summon(YETI)
    yeti.turns_in_play = 1
    assert location not in yeti.attack_targets
    assert enemy.hero in yeti.attack_targets
    assert location not in game.player1.give(FIREBALL).targets


def test_adjacent_minions_skip_locations_without_duplicates():
    game = prepare_empty_game()
    left = game.player1.summon(YETI)
    game.player1.summon(LOCATION)
    right = game.player1.summon(YETI)
    assert left.adjacent_minions == [right]
    assert right.adjacent_minions == [left]


def test_trueaim_crescent_ignores_friendly_locations():
    game = prepare_empty_game()
    game.player1.give("SCH_279").play()
    location = game.player1.give(LOCATION).play()
    first = game.player1.summon("CS2_120")
    second = game.player1.summon("CS2_120")
    enemy = game.player2.summon("CS2_186")
    game.player1.hero.attack(enemy)
    assert enemy.damage == 5
    assert first.dead and second.dead
    assert location.zone == Zone.PLAY


def test_lightbomb_ignores_locations_and_dormant_minions():
    game = prepare_empty_game()
    own_location = game.player1.summon(LOCATION)
    enemy_location = game.player2.summon(LOCATION)
    yeti = game.player2.summon(YETI)
    dormant = game.player2.summon("BT_121")
    game.player1.give("GVG_008").play()
    assert yeti.damage == 4
    assert dormant.damage == 0
    assert own_location.zone == enemy_location.zone == Zone.PLAY


def test_monster_smash_attacks_ignore_locations():
    from fireplace.cards.brawl.monster_smash import AttackRandomEnemyMinions

    game = prepare_empty_game()
    location = game.player1.summon(LOCATION)
    enemy_location = game.player2.summon(LOCATION)
    yeti = game.player1.summon(YETI)
    enemy = game.player2.summon(YETI)
    game.queue_actions(yeti, [AttackRandomEnemyMinions(CONTROLLER)])
    assert yeti.damage == enemy.damage == 8
    assert yeti.dead and enemy.dead
    assert location.zone == enemy_location.zone == Zone.PLAY


def test_monster_smash_amalgamate_preserves_locations():
    from fireplace.cards.brawl.monster_smash import Amalgamate

    game = prepare_empty_game()
    location = game.player1.summon(LOCATION)
    enemy_location = game.player2.summon(LOCATION)
    yeti = game.player1.summon(YETI)
    game.queue_actions(yeti, [Amalgamate(CONTROLLER)])
    assert yeti.dead
    amalgam = game.player1.field[-1]
    assert (amalgam.atk, amalgam.health) == (4, 5)
    assert location.zone == enemy_location.zone == Zone.PLAY
