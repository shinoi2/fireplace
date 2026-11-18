"""
A minion returned to the hand or shuffled into the deck is its card again.

Wiki (Return to hand): a minion returned to its owner's hand is reset to its
card: it loses its enchantments, its damage and its silence, and played again
it is a new minion, with summoning sickness unless it has Charge or Rush.
The same goes for a minion shuffled into a deck, and for one that comes back
from the graveyard (Anub'arak, Malorne).
"""

from utils import *

YETI = "CS2_182"  # 4/5
ARCANE_DEVOURER = "EX1_187"  # 4/8
WOLFRIDER = "CS2_124"  # 3/1 Charge
RABID_WORGEN = "GIL_113"  # 3/3 Rush
SAP = "EX1_581"
SHADOWSTEP = "EX1_144"
FROSTBOLT = "CS2_024"
BLESSING_OF_KINGS = "CS2_092"
ANUBARAK = "AT_036"
MALORNE = "GVG_035"
UNEARTHED_RAPTOR = "LOE_019"
LOOT_HOARDER = "EX1_096"
HARVEST_GOLEM = "EX1_556"
FAERIE_DRAGON = "NEW1_023"
IMPRISONED_GANARG = "BT_121"


def _in_play_since_a_turn(game, player, card_id):
    """Summon a minion for `player` and pass turns until it is his turn again."""
    minion = player.summon(card_id)
    game.end_turn()
    game.end_turn()
    if game.current_player is not player:
        game.end_turn()
    assert minion.turns_in_play >= 1
    assert minion.can_attack()
    return minion


def test_sapped_minion_replayed_next_turn_is_asleep():
    # The user's game: the expert bot's Arcane Devourer, in play since a turn,
    # sapped, replayed on the next turn: it attacked at once.
    game = prepare_empty_game()
    game.end_turn()
    devourer = game.player2.summon(ARCANE_DEVOURER)
    game.end_turn()
    game.end_turn()
    assert devourer.can_attack()
    game.end_turn()

    game.player1.give(SAP).play(target=devourer)
    assert devourer.zone == Zone.HAND
    game.end_turn()

    devourer.play()
    assert devourer.zone == Zone.PLAY
    assert devourer.turns_in_play == 0
    assert devourer.asleep
    assert not devourer.can_attack()
    game.end_turn()
    game.end_turn()
    assert devourer.can_attack()


def test_shadowstep_replayed_same_turn_is_asleep():
    game = prepare_empty_game()
    yeti = _in_play_since_a_turn(game, game.player1, YETI)
    game.player1.give(SHADOWSTEP).play(target=yeti)
    assert yeti.zone == Zone.HAND
    yeti.play()
    assert yeti.asleep
    assert not yeti.can_attack()


def test_shuffled_minion_drawn_and_replayed_is_asleep():
    game = prepare_empty_game()
    yeti = _in_play_since_a_turn(game, game.player1, YETI)
    game.queue_actions(game.player1, [Shuffle(game.player1, yeti)])
    assert yeti.zone == Zone.DECK
    assert yeti.turns_in_play == 0
    game.player1.draw()
    yeti.play()
    assert not yeti.can_attack()


def test_charge_minion_returned_attacks_again_same_turn():
    # Shadowstep on a Charge minion that has attacked: played again, it is a
    # new minion and can attack again this turn.
    game = prepare_empty_game()
    wolfrider = _in_play_since_a_turn(game, game.player1, WOLFRIDER)
    wolfrider.attack(game.player2.hero)
    assert not wolfrider.can_attack()
    game.player1.give(SHADOWSTEP).play(target=wolfrider)
    assert wolfrider.num_attacks == 0
    wolfrider.play()
    assert wolfrider.can_attack()
    assert wolfrider.can_attack(game.player2.hero)


def test_rush_minion_returned_attacks_minions_only():
    game = prepare_empty_game()
    worgen = _in_play_since_a_turn(game, game.player1, RABID_WORGEN)
    enemy = game.player2.summon(YETI)
    assert worgen.can_attack(game.player2.hero)
    game.player1.give(SHADOWSTEP).play(target=worgen)
    worgen.play()
    assert worgen.can_attack(enemy)
    assert not worgen.can_attack(game.player2.hero)


def test_returned_minion_is_not_frozen():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.summon(YETI)
    game.end_turn()
    game.player1.give(FROSTBOLT).play(target=yeti)
    assert yeti.frozen
    game.player1.give(SAP).play(target=yeti)
    assert not yeti.frozen
    game.end_turn()
    yeti.play()
    game.end_turn()
    game.end_turn()
    assert not yeti.frozen
    assert yeti.can_attack()


def test_returned_minion_has_no_damage_nor_enchantment():
    game = prepare_empty_game()
    yeti = game.player1.summon(YETI)
    game.player1.give(BLESSING_OF_KINGS).play(target=yeti)
    game.player1.give(MOONFIRE).play(target=yeti)
    assert (yeti.atk, yeti.health) == (8, 8)
    game.player1.give(SHADOWSTEP).play(target=yeti)
    assert yeti.damage == 0
    assert (yeti.atk, yeti.health) == (4, 5)
    assert [buff.id for buff in yeti.buffs] == ["EX1_144e"]


def test_returned_minion_per_turn_counters_are_reset():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.summon(YETI)
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=yeti)
    assert yeti.damaged_this_turn
    assert yeti.damaged_on_opponent_turn
    game.player1.give(SAP).play(target=yeti)
    assert yeti.damaged_this_turn == 0
    assert yeti.damaged_on_opponent_turn == 0
    assert yeti.healed_this_turn == 0


def test_returned_minion_forgets_copied_deathrattles():
    # Unearthed Raptor copies Loot Hoarder's deathrattle; returned and played
    # again copying Harvest Golem's, it has only the golem's.
    game = prepare_empty_game()
    game.player1.summon(LOOT_HOARDER)
    golem = game.player1.summon(HARVEST_GOLEM)
    hoarder = game.player1.field[0]
    raptor = game.player1.give(UNEARTHED_RAPTOR)
    raptor.play(target=hoarder)
    assert raptor.has_deathrattle
    game.player1.give(SHADOWSTEP).play(target=raptor)
    assert raptor.additional_deathrattles == []
    raptor.play(target=golem)
    assert len(raptor.deathrattles) == 1
    hand = len(game.player1.hand)
    game.player1.give(FIREBALL).play(target=raptor)
    assert raptor.dead
    assert len(game.player1.hand) == hand
    assert game.player1.field[-1].id == "skele21"


def test_anubarak_returns_as_a_new_card():
    # Anub'arak dies and comes back from the graveyard: no enchantment, no
    # "killed this turn", and summoning sickness when played again.
    game = prepare_empty_game()
    anubarak = _in_play_since_a_turn(game, game.player1, ANUBARAK)
    game.player1.give(BLESSING_OF_KINGS).play(target=anubarak)
    anubarak.destroy()
    assert anubarak.zone == Zone.HAND
    assert not anubarak.buffs
    assert (anubarak.atk, anubarak.health) == (8, 4)
    assert anubarak.turns_in_play == 0
    assert not anubarak.killed_this_turn
    game.player1.used_mana = 0
    anubarak.play()
    assert not anubarak.can_attack()


def test_malorne_shuffled_back_as_a_new_card():
    game = prepare_empty_game()
    malorne = _in_play_since_a_turn(game, game.player1, MALORNE)
    game.player1.give(BLESSING_OF_KINGS).play(target=malorne)
    malorne.destroy()
    assert malorne.zone == Zone.DECK
    assert not malorne.buffs
    assert (malorne.atk, malorne.health) == (9, 7)
    assert malorne.turns_in_play == 0
    assert not malorne.killed_this_turn


def test_minion_shuffled_into_the_other_deck_is_a_new_card():
    # Played by one player, shuffled into the other's deck (through SETASIDE):
    # the same reset as a shuffle into its own deck.
    game = prepare_empty_game()
    yeti = _in_play_since_a_turn(game, game.player2, YETI)
    game.player2.give(BLESSING_OF_KINGS).play(target=yeti)
    game.player2.give(SILENCE).play(target=yeti)
    game.end_turn()
    game.queue_actions(game.player1, [Shuffle(game.player1, yeti)])
    assert yeti.zone == Zone.DECK
    assert yeti.controller is game.player1
    assert not yeti.buffs
    assert not yeti.silenced
    assert yeti.turns_in_play == 0
    game.player1.draw()
    yeti.play()
    assert (yeti.atk, yeti.health) == (4, 5)
    assert not yeti.can_attack()


def test_returned_elusive_minion_is_elusive_again():
    game = prepare_empty_game()
    dragon = game.player1.summon(FAERIE_DRAGON)
    # Elusive: no spell targets it; an untargeted silence (Mass Dispel) does
    game.queue_actions(game.player1, [Silence(dragon)])
    assert dragon.silenced
    assert not dragon.cant_be_targeted_by_abilities
    game.player1.give(SHADOWSTEP).play(target=dragon)
    assert dragon.cant_be_targeted_by_abilities


def test_returned_awakened_minion_is_dormant_again():
    game = prepare_empty_game()
    ganarg = game.player1.give(IMPRISONED_GANARG)
    ganarg.play()
    assert ganarg.dormant
    for _ in range(4):
        game.end_turn()
    assert not ganarg.dormant
    game.player1.give(SHADOWSTEP).play(target=ganarg)
    assert ganarg.dormant
    assert ganarg.dormant_turns == 2
    ganarg.play()
    assert ganarg.dormant
    assert not ganarg.can_attack()


def test_control_change_keeps_enchantments_until_returned_to_hand():
    game = prepare_empty_game()
    yeti = game.player1.summon(YETI)
    game.player1.give(BLESSING_OF_KINGS).play(target=yeti)
    game.end_turn()
    game.player2.give(MIND_CONTROL).play(target=yeti)
    assert yeti.controller is game.player2
    assert (yeti.atk, yeti.health) == (8, 9)
    game.end_turn()
    game.player1.give(SAP).play(target=yeti)
    assert yeti in game.player2.hand
    assert (yeti.atk, yeti.health) == (4, 5)
    assert yeti.turns_in_play == 0


def test_immortal_prelate_keeps_enchantments_when_shuffled_after_death():
    game = prepare_empty_game()
    prelate = game.player1.summon("TRL_306")
    game.player1.give(BLESSING_OF_KINGS).play(target=prelate)
    game.player1.give(MOONFIRE).play(target=prelate)
    prelate.destroy()
    assert prelate.zone == Zone.DECK
    assert (prelate.atk, prelate.health) == (5, 7)
    assert prelate.damage == 0
    assert prelate.buffs
    assert not prelate.killed_this_turn
