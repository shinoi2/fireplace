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


def test_wildheart_guff():
    # "Battlecry: Set your maximum Mana to 20. Gain a Mana Crystal. Draw a
    # card." Nurture: "Choose One - Draw a card; or Gain a Mana Crystal."
    game = prepare_game(CardClass.DRUID, CardClass.DRUID)
    game.player1.discard_hand()
    guff = game.player1.give("AV_205")
    guff.play()
    assert game.player1.hero.id == "AV_205"
    assert len(game.player1.hand) == 1
    power = game.player1.hero.power
    assert power.id == "AV_205p"
    game.end_turn()
    game.end_turn()
    hand = len(game.player1.hand)
    power.use(choose="AV_205pb")  # Valley Root: draw a card
    assert len(game.player1.hand) == hand + 1
    game.end_turn()
    game.end_turn()
    crystals = game.player1.max_mana
    game.player1.hero.power.use(choose="AV_205a")  # Ice Blossom
    assert game.player1.max_mana == crystals + 1


def test_protect_the_innocent_reads_the_heros_healing():
    # HEALED_THIS_TURN read on a hero was a KeyError (managers.py, WP-196)
    game = prepare_empty_game()
    game.player1.give("AV_342").play()
    assert [m.id for m in game.player1.field] == ["AV_342t"]
    game = prepare_empty_game()
    game.player1.hero.set_current_health(20)
    game.player1.give(HOLY_LIGHT).play(target=game.player1.hero)
    game.player1.give("AV_342").play()
    assert [m.id for m in game.player1.field] == ["AV_342t", "AV_342t"]


def _choose(game, player=None, index=0):
    player = player or game.player1
    card = player.choice.cards[index]
    player.choice.choose(card)
    return card


def test_honorable_kill_is_exact_lethal_on_the_turn_of_its_source():
    # Gnome Private (1/3): +2 Attack on an Honorable Kill; the kill must be exact
    # (a minion left alive or dead of an excess of damage is not one), and on
    # the turn of the source's controller.
    game = prepare_empty_game()
    private = game.player1.give("AV_121").play()
    game.skip_turn()
    private.attack(game.player2.summon("CS2_142"))  # 2/2 takes 1: alive
    assert private.atk == 1
    game.skip_turn()
    game.player2.field[0].destroy()
    private.attack(game.player2.summon("CS2_189"))  # 1/1 takes 1: exactly
    assert private.atk == 3
    # on the opponent's turn, the minion that kills by defending gains nothing
    game = prepare_empty_game()
    private = game.player1.give("AV_121").play()
    archer = game.player2.summon("CS2_189")
    game.end_turn()
    archer.attack(private)
    assert private.atk == 1 and private.health == 2
    # an excess of damage is not an Honorable Kill; an exact one is, with a
    # battlecry as well (Knight-Captain: 3 damage)
    game = prepare_empty_game()
    over = game.player1.give("AV_131").play(target=game.player2.summon("CS2_121"))
    assert over.atk == 3
    exact = game.player1.give("AV_131").play(target=game.player2.summon("CS2_120"))
    assert exact.atk == 6 and exact.health == 6


def test_korrak_the_bloodrager_comes_back_unless_honorably_killed():
    game = prepare_empty_game()
    korrak = game.player2.summon("AV_143")
    korrak.destroy()  # no damage: it was not Honorably Killed
    assert game.player2.field == ["AV_143"]
    korrak = game.player2.field[0]
    korrak.damage = 4
    game.player1.give(MOONFIRE).play(target=korrak)
    assert game.player2.field == []
    korrak = game.player2.summon("AV_143")
    korrak = game.player2.field[0]
    game.player1.give(FIREBALL).play(target=korrak)  # an excess of damage
    assert game.player2.field == ["AV_143"]
    korrak = game.player2.field[0]
    korrak.damage = 3
    game.player1.give("ONY_010").play(target=korrak)  # Dragonbane Shot: 2, exactly
    assert game.player2.field == []


def test_snowball_fight_repeats_on_other_minions_while_they_survive():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    big = game.player2.summon("CS2_186")
    other = game.player1.summon("CS2_182")
    game.player1.give("AV_250").play(target=big)
    # it survives: the same on another minion
    assert big.damage == 1 and big.frozen
    assert other.damage == 1 and other.frozen
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    wisp = game.player2.summon(WISP)
    other = game.player2.summon("CS2_186")
    game.player1.give("AV_250").play(target=wisp)  # dies: no repeat
    assert wisp.dead and other.damage == 0 and not other.frozen
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    only = game.player2.summon("CS2_186")
    game.player1.give("AV_250").play(target=only)  # alone: no other minion
    assert only.damage == 1 and only.frozen


def test_revive_pet_discovers_a_dead_friendly_beast_and_summons_it():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    game.player1.summon("CS2_172").destroy()
    game.player1.give("AV_333").play()
    assert game.player1.choice
    _choose(game)
    assert game.player1.field == ["CS2_172"]


def test_beaststalker_tavish_discovers_and_casts_two_improved_secrets():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    game.player1.give("AV_113").play()
    first = _choose(game)
    assert game.player1.choice
    second = _choose(game)
    assert len(game.player1.secrets) == 2
    assert game.player1.secrets[0].id != game.player1.secrets[1].id
    assert game.player1.hero.power.id == "AV_113p"


def test_siphon_mana_honorable_kill_reduces_the_spells_in_hand_by_one():
    game = prepare_empty_game()
    fireball = game.player1.give(FIREBALL)
    coin = game.player1.give(WISP)
    game.player1.give("AV_212").play(target=game.player2.summon("CS2_142"))
    assert fireball.cost == 3  # 4, reduced by 1, not set to 1
    assert coin.cost == 0
    game = prepare_empty_game()
    fireball = game.player1.give(FIREBALL)
    game.player1.give("AV_212").play(target=game.player2.summon("CS2_182"))
    assert fireball.cost == 4


def test_haleh_splits_its_damage_among_all_enemies_the_hero_included():
    game = prepare_empty_game()
    game.player1.summon("ONY_007")
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert game.player2.hero.health == 26


def test_lightforged_cariel_hits_all_enemies_and_equips_the_immovable_object():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    wisp = game.player2.summon(WISP)
    game.player1.give("AV_206").play()
    assert game.player2.hero.health == 28 and wisp.dead
    weapon = game.player1.weapon
    assert weapon == "AV_146" and weapon.atk == 2 and weapon.durability == 5
    game.end_turn()
    # half damage, rounded up (the hero card gives 5 Armor, which takes it first)
    assert game.player1.hero.armor == 5
    game.player2.give(FIREBALL).play(target=game.player1.hero)
    assert game.player1.hero.armor == 5 - 3
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert game.player1.hero.armor == 5 - 3 - 1
    game.player2.used_mana = 0
    game.player2.give(PYROBLAST).play(target=game.player1.hero)  # 10: 5
    assert game.player1.hero.health == 30 - (5 - (5 - 3 - 1))
    game.end_turn()
    game.player2.summon("CS2_182")
    game.player1.hero.attack(game.player2.field[0])
    assert game.player1.weapon.durability == 5


def test_shadow_word_devour_steals_one_health_from_every_other_minion():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.MAGE)
    mine = game.player1.summon("CS2_186")
    wisp = game.player2.summon(WISP)
    kobold = game.player2.summon("CS2_142")
    game.player1.give("AV_324").play(target=mine)
    assert wisp.dead
    assert kobold.health == 1
    assert mine.health == 9  # 7 and one for each of the other two minions


def test_snowfall_guardian_gains_one_stat_for_each_frozen_minion():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    game.player2.summon("CS2_186")
    game.player2.summon(WISP)
    guardian = game.player1.give("AV_255").play()
    assert all(m.frozen for m in game.player2.field)
    assert (guardian.atk, guardian.health) == (7, 7)
    assert game.player2.field[0].atk == 7


def test_grave_defiler_copies_a_fel_spell_and_keeps_the_original():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    game.player1.give("BT_035")  # Chaos Strike, a Fel spell
    game.player1.give(WISP)
    game.player1.give("AV_308").play()
    assert game.player1.hand == ["BT_035", WISP, "BT_035"]
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    game.player1.give(WISP)
    game.player1.give("AV_308").play()  # no Fel spell: nothing
    assert game.player1.hand == [WISP]


def test_felwalker_casts_the_highest_cost_fel_spell_of_the_hand():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    game.player1.give("BT_035")
    game.player1.give("BRM_005")  # Demonwrath, 3
    game.player2.summon("CS2_186")
    game.player1.give("AV_286").play()
    assert game.player1.hand == ["BT_035"]
    assert game.player2.field[0].damage == 2


def _to_deck(player, *ids):
    # the last one given is the top of the deck
    cards = []
    for id in ids:
        card = player.give(id)
        card.zone = Zone.DECK
        cards.append(card)
    return cards


def test_pathmaker_casts_the_other_choice_of_the_last_choose_one_spell():
    game = prepare_empty_game(CardClass.DRUID, CardClass.MAGE)
    game.player1.give("AV_210").play()  # no Choose One spell cast yet
    assert game.player1.field == ["AV_210"]
    game = prepare_empty_game(CardClass.DRUID, CardClass.MAGE)
    game.player1.give("EX1_160").play(choose="EX1_160a")  # a Panther
    assert game.player1.field == ["EX1_160t"]
    game.player1.give("AV_210").play()  # the other choice: +1/+1 to the minions
    assert (game.player1.field[0].atk, game.player1.field[0].health) == (4, 3)


def test_dire_frostwolf_summons_one_wolf():
    game = prepare_empty_game(CardClass.DRUID, CardClass.MAGE)
    game.player1.give("AV_211").play().destroy()
    assert game.player1.field == ["AV_211t"]
    assert game.player1.field[0].stealthed


def test_frostsaber_matriarch_counts_the_beasts_played_and_summoned():
    game = prepare_empty_game(CardClass.DRUID, CardClass.MAGE)
    matriarch = game.player1.give("AV_291")
    assert matriarch.cost == 7
    game.player1.give("CS2_172").play()
    assert matriarch.cost == 6
    game.player1.summon("CS2_172")
    assert matriarch.cost == 5
    game.player2.summon("CS2_172")
    game.player1.summon(WISP)
    assert matriarch.cost == 5


def test_ring_of_courage_buffs_once_more_for_each_enemy_minion():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    wisp = game.player1.summon(WISP)
    game.player2.summon(WISP)
    game.player2.summon(WISP)
    game.player1.give("ONY_027").play(target=wisp)
    assert (wisp.atk, wisp.health) == (4, 4)


def test_cheaty_snobold_hits_a_frozen_enemy_hero():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    game.player1.give("AV_251").play()
    game.player1.give("CS2_037").play(target=game.player2.hero)  # Frost Shock
    assert game.player2.hero.frozen
    assert game.player2.hero.health == 30 - 1 - 3
    wisp = game.player1.summon(WISP)
    game.player1.give("AV_266").play(target=wisp)  # a friendly one: no damage
    assert wisp.frozen and wisp.health == 1


def test_lokholar_costs_five_less_with_15_health_or_less():
    game = prepare_empty_game()
    lokholar = game.player1.give("AV_141t")
    assert lokholar.cost == 10
    game.player1.hero.set_current_health(15)
    assert lokholar.cost == 5


def test_to_the_front_minions_cost_two_less_but_not_less_than_one():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    golem = game.player1.give("CS2_186")  # 7
    kobold = game.player1.give("CS2_142")  # 2
    one = game.player1.give("CS2_168")  # 1
    wisp = game.player1.give(WISP)  # 0
    fireball = game.player1.give(FIREBALL)
    game.player1.give("AV_119").play()
    assert [c.cost for c in (golem, kobold, one, wisp, fireball)] == [5, 1, 1, 0, 4]
    game.end_turn()
    game.end_turn()
    assert [c.cost for c in (golem, kobold, one, wisp)] == [7, 2, 1, 0]


def test_double_agent_summons_a_copy_when_holding_a_card_of_another_class():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give(FIREBALL)
    game.player1.give("AV_711").play()
    assert game.player1.field == ["AV_711", "AV_711"]
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give(WISP)  # neutral
    game.player1.give("CS2_072")  # a rogue card
    game.player1.give("AV_711").play()
    assert game.player1.field == ["AV_711"]


def test_wildpaw_gnoll_costs_one_less_for_each_card_added_from_another_class():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    gnoll = game.player1.give("AV_298")
    assert gnoll.cost == 5
    game.player1.give(WISP)
    game.player1.give("CS2_072")
    assert gnoll.cost == 5
    game.player1.give(FIREBALL)
    assert gnoll.cost == 4
    game.player1.give(FIREBALL).play(target=game.player2.hero)  # played, not new
    assert gnoll.cost == 3


def test_contraband_stash_replays_cards_from_other_classes():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("CS2_072")  # a card of its own class, not played
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    game.player1.give("AV_405").play()  # a random target: either hero
    assert game.player1.hero.health + game.player2.hero.health == 60 - 12
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give(THE_COIN).play()  # neutral
    game.player1.give("AV_405").play()
    assert game.player1.mana == 10 - 5  # the Coin is not played again


def test_cerathine_fleetrunner_replaces_the_minions_with_ones_of_other_classes():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give(WISP)
    _to_deck(game.player1, WISP, WISP)
    game.player1.give("AV_403").play()
    cards = game.player1.hand + game.player1.deck
    assert len(cards) == 3
    for card in cards:
        assert card.id != WISP and card.type == CardType.MINION
        assert any(
            cls not in (CardClass.ROGUE, CardClass.NEUTRAL) for cls in card.classes
        )
        assert card.cost == max(0, card.data.cost - 2)


def test_reconnaissance_discovers_a_deathrattle_minion_of_another_class():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("AV_710").play()
    for card in game.player1.choice.cards:
        assert card.has_deathrattle
        assert any(
            cls not in (CardClass.ROGUE, CardClass.NEUTRAL) for cls in card.classes
        )
    card = _choose(game)
    assert game.player1.hand == [card.id]
    assert card.cost == max(0, card.data.cost - 2)


def test_tooth_of_nefarian_discovers_a_spell_of_another_class_on_an_honorable_kill():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("ONY_032").play(target=game.player2.summon("CS2_182"))
    assert not game.player1.choice  # 3 damage on a 4/5: no kill
    game.player1.give("ONY_032").play(target=game.player2.summon("CS2_120"))
    assert game.player1.choice
    for card in game.player1.choice.cards:
        assert card.type == CardType.SPELL
        assert any(
            cls not in (CardClass.ROGUE, CardClass.NEUTRAL) for cls in card.classes
        )


def test_forsaken_lieutenant_becomes_a_copy_with_rush_of_a_deathrattle_minion():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    lieutenant = game.player1.give("AV_601").play()
    game.player1.give(WISP).play()
    assert game.player1.field == ["AV_601", WISP]  # a Wisp is not a Deathrattle
    game.player1.give("FP1_007").play()  # Nerubian Egg 0/2, a Deathrattle
    assert game.player1.field == ["FP1_007", WISP, "FP1_007"]
    copy = game.player1.field[0]
    assert copy.rush and (copy.atk, copy.health) == (2, 2)
    assert not game.player1.field[2].rush


def test_flanking_maneuver_summons_another_demon_when_the_first_dies_this_turn():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    game.player1.give("AV_269").play()
    assert game.player1.field == ["AV_269t"]
    game.player1.field[0].destroy()
    assert game.player1.field == ["AV_269t"]
    game.player1.field[0].destroy()
    assert game.player1.field == []
    game.player1.give("AV_269").play()
    game.skip_turn()
    game.player1.field[0].destroy()  # not this turn
    assert game.player1.field == []


def test_wing_commander_ichman_repeats_when_the_beast_kills_a_minion():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    _to_deck(game.player1, "CS2_172", "CS2_172")
    kobold = game.player2.summon("CS2_142")
    game.player1.give("AV_336").play()
    assert game.player1.field == ["AV_336", "CS2_172"]
    raptor = game.player1.field[1]
    assert raptor.rush
    raptor.attack(game.player2.summon("EX1_405"))  # Shieldbearer 0/4: no kill
    assert game.player1.field == ["AV_336", "CS2_172"]
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    _to_deck(game.player1, "CS2_172", "CS2_172")
    kobold = game.player2.summon("CS2_142")
    game.player1.give("AV_336").play()
    raptor = game.player1.field[1]
    raptor.attack(kobold)  # 3 damage on a 2/2: the Beast kills it, and dies
    assert kobold.dead and raptor.dead
    assert game.player1.field == ["AV_336", "CS2_172"]  # the next one, with Rush
    assert game.player1.field[1] is not raptor and game.player1.field[1].rush
    assert len(game.player1.deck) == 0


def test_hollow_abomination_gains_the_attack_of_the_minion_it_honorably_kills():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    game.player2.summon("EX1_011")  # Voodoo Doctor 2/1
    game.player2.summon("CS2_182")
    abomination = game.player1.give("AV_313").play()
    assert abomination.atk == 4
    assert game.player2.field[0].damage == 1


def test_dun_baldar_bridge_buffs_the_minions_summoned_for_three_turns():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    bridge = game.player1.give("AV_344").play()
    wisp = game.player1.give(WISP).play()
    assert (wisp.atk, wisp.health) == (3, 3)
    token = game.player1.summon(WISP)
    assert (token.atk, token.health) == (3, 3)
    enemy = game.player2.summon(WISP)
    assert enemy.atk == 1
    game.skip_turn()
    game.skip_turn()
    assert game.player1.summon(WISP).atk == 3
    game.end_turn()
    assert bridge.zone == Zone.GRAVEYARD
    assert game.player1.summon(WISP).atk == 1


def test_axe_berserker_draws_a_weapon_not_the_top_card():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    _to_deck(game.player1, "CS2_106", WISP, WISP)
    axe = game.player1.give("AV_565").play()
    game.skip_turn()
    game.player1.discard_hand()
    axe.attack(game.player2.summon("CS2_120"))  # 3 damage on a 2/3
    assert game.player1.hand == ["CS2_106"]


def test_capture_coldtooth_mine_draws_the_lowest_or_the_highest_cost_card():
    game = prepare_empty_game(CardClass.DRUID, CardClass.MAGE)
    _to_deck(game.player1, "CS2_182", "CS2_186", WISP, "CS2_142")
    game.player1.give("AV_295").play(choose="AV_295b")
    assert game.player1.hand == ["CS2_186"]
    game.player1.give("AV_295").play(choose="AV_295a")
    assert game.player1.hand == ["CS2_186", WISP]


def test_drekthar_and_vanndar_compare_their_cost_with_the_minions_of_the_deck():
    game = prepare_empty_game()
    _to_deck(game.player1, WISP, "CS2_142", "CS2_168")
    game.player1.give("AV_100").play()
    assert len(game.player1.field) == 3 and len(game.player1.deck) == 1
    game = prepare_empty_game()
    _to_deck(game.player1, WISP, "CS2_182")  # a 4-Cost: not less
    game.player1.give("AV_100").play()
    assert len(game.player1.field) == 1
    game = prepare_empty_game()
    ogres = _to_deck(game.player1, "CS2_200", "CS2_200")
    game.player1.give("AV_223").play()
    assert [c.cost for c in ogres] == [3, 3]
    game = prepare_empty_game()
    ogre, wisp = _to_deck(game.player1, "CS2_200", WISP)
    game.player1.give("AV_223").play()
    assert ogre.cost == 6


def test_kurtrus_hero_power_is_refreshed_after_a_friendly_minion_attacks():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    wisp = game.player1.give(WISP).play()
    game.skip_turn()
    game.player1.give("AV_204").play()
    power = game.player1.hero.power
    assert power.id == "AV_204p"
    power.use()
    assert game.player1.hero.atk == 2 and power.exhausted
    wisp.attack(game.player2.hero)
    assert not power.exhausted


def test_smokescreen_draws_five_cards_and_triggers_the_deathrattles_drawn():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    _to_deck(game.player1, *([WISP] * 6), MOONFIRE, "EX1_096")  # Loot Hoarder on top
    game.player1.give("ONY_031").play()
    assert len(game.player1.hand) == 6  # five, and the Loot Hoarder's
    assert "EX1_096" in [card.id for card in game.player1.hand]


def test_stonehearth_vindicator_draws_a_cheap_spell_that_costs_nothing_this_turn():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    _to_deck(game.player1, "CS2_023", FIREBALL)
    game.player1.give("AV_343").play()
    assert game.player1.hand == ["CS2_023"]
    assert game.player1.hand[0].cost == 0
    game.end_turn()
    game.end_turn()
    assert game.player1.hand[0].cost == 3


def test_dun_baldar_bunker_draws_a_secret_for_one_mana_each_turn():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    _to_deck(game.player1, "EX1_610", WISP)
    game.player1.give("AV_147").play()
    game.end_turn()
    assert game.player1.hand == ["EX1_610"]
    assert game.player1.hand[0].cost == 1


def test_spring_the_trap_casts_two_secrets_on_an_honorable_kill():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    _to_deck(game.player1, "EX1_610", "EX1_611", "EX1_609")
    game.player1.give("AV_224").play(target=game.player2.summon("CS2_182"))
    assert len(game.player1.secrets) == 1  # 3 damage on a 4/5: one Secret
    game.player2.summon("CS2_182").damage = 2  # 3 left: exactly
    game.player1.give("AV_224").play(target=game.player2.field[-1])
    assert len(game.player1.secrets) == 3  # an Honorable Kill: two more


def test_mida_pure_light_shuffles_a_fragment_that_resummons_it_when_drawn():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.MAGE)
    mida = game.player1.give("ONY_028").play()
    mida.destroy()
    assert game.player1.deck == ["ONY_028t"]
    game.player1.draw()
    assert game.player1.field == ["ONY_028"]
    assert game.player1.hand == []


def test_deliverance_summons_a_new_3_3_copy_on_an_honorable_kill():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.MAGE)
    game.player1.give("AV_315").play(target=game.player2.summon("CS2_182"))
    assert game.player1.field == []
    game.player1.give("AV_315").play(target=game.player2.summon("CS2_120"))
    assert game.player1.field == ["CS2_120"]
    assert (game.player1.field[0].atk, game.player1.field[0].health) == (3, 3)
    assert game.player2.field == ["CS2_182"]


def test_tamsins_phylactery_gives_your_minions_the_deathrattle_of_a_dead_one():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    game.player1.summon("EX1_096").destroy()  # Loot Hoarder
    game.player1.discard_hand()
    wisp = game.player1.summon(WISP)
    game.player1.give("AV_317").play()
    _choose(game)
    assert game.player1.hand == []
    assert wisp.has_deathrattle
    _to_deck(game.player1, "CS2_142")
    wisp.destroy()
    assert game.player1.hand == ["CS2_142"]


def test_si7_smuggler_summons_a_minion_that_costs_more_for_each_other_si7_card():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("ONY_030").play()
    assert len(game.player1.field) == 2
    assert game.player1.field[1].data.cost == 1
    game.player1.give("ONY_030").play()  # one other SI:7 card played: a 2-Cost
    assert len(game.player1.field) == 4
    assert game.player1.field[-1].data.cost == 2


def _hk_attack(minion_id, victim_id):
    """The minion, played, attacks the next turn a minion that has `victim_id`."""
    game = prepare_empty_game()
    ally = game.player1.summon(WISP)
    minion = game.player1.give(minion_id).play()
    game.skip_turn()
    victim = game.player2.summon(victim_id)
    minion.attack(victim)
    return game, ally, minion, victim


def test_honorable_kill_minions_effects():
    # Corporal 2/3: Divine Shield to its other minions (2 on a 2/2: exact)
    game, ally, corporal, _ = _hk_attack("AV_122", "CS2_142")
    assert ally.divine_shield and not corporal.divine_shield
    game, ally, corporal, _ = _hk_attack("AV_122", "CS2_189")  # 1/1: an excess
    assert not ally.divine_shield
    # Direwolf Commander 2/5: a 2/2 Wolf with Stealth
    game, _, _, _ = _hk_attack("AV_124", "CS2_142")
    assert game.player1.field == [WISP, "AV_124", "AV_211t"] or "AV_211t" in [
        m.id for m in game.player1.field
    ]
    # Frantic Hippogryph 3/7 Rush: Windfury (3 on a 2/3: exact)
    game, _, hippo, _ = _hk_attack("AV_215", "CS2_120")
    assert hippo.windfury
    game, _, hippo, _ = _hk_attack("AV_215", "CS2_142")  # an excess
    assert not hippo.windfury
    # Sneaky Scout 3/2: the next Hero Power costs 0 (3 on a 2/3: exact)
    game, _, scout, _ = _hk_attack("AV_123", "CS2_120")
    assert game.player1.hero.power.cost == 0


def test_battleworn_vanguard_summons_two_felwings_after_the_hero_attacks():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    game.player1.give("AV_118").play()
    game.skip_turn()
    game.player1.hero.power.use()
    game.player1.hero.attack(game.player2.hero)
    assert game.player1.field.count("BT_922t") == 2
    assert game.player1.field[0] == "BT_922t" and game.player1.field[-1] == "BT_922t"


def test_arcane_brilliance_adds_a_copy_of_a_7_8_9_and_10_cost_spell_of_the_deck():
    game = prepare_empty_game()
    for id in ("EX1_279", "CS2_029", "BRM_002"):  # 10, 4, 5: only the 10
        game.player1.give(id).zone = Zone.DECK
    game.player1.give("AV_116").play()
    assert game.player1.hand == ["EX1_279"]
    assert len(game.player1.deck) == 3


def test_caria_felsoul_becomes_a_6_6_copy_of_a_demon_of_the_deck():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    caria = game.player1.give("AV_267").play()  # no Demon in the deck: stays
    assert game.player1.field == ["AV_267"] and caria.atk == 7
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    _to_deck(game.player1, "BT_307")
    game.player1.give("AV_267").play()
    assert game.player1.field == ["BT_307"]
    assert (game.player1.field[0].atk, game.player1.field[0].health) == (7, 7)


def test_kazakusan_treasures_need_a_target_and_destroy_it():
    # the treasures were written with a set of requirements (a plantage in a game)
    game = prepare_empty_game()
    target = game.player2.summon("CS2_182")
    treasure = game.player1.give("ONY_005ta1")  # Necrotic Poison
    assert treasure.requires_target()
    treasure.play(target=target)
    assert target.dead


def test_frozen_mammoth_is_frozen_until_a_fire_spell_is_cast():
    game = prepare_empty_game()
    mammoth = game.player1.give("AV_128").play()
    assert mammoth.frozen
    game.skip_turn()
    assert mammoth.frozen and not mammoth.can_attack()
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert not mammoth.frozen and mammoth.can_attack()


def test_abominable_lieutenant_eats_an_enemy_minion_at_the_end_of_your_turn():
    game = prepare_empty_game()
    lieutenant = game.player1.give("AV_139").play()
    game.player2.summon("CS2_182")
    game.end_turn()
    assert game.player2.field == []
    assert (lieutenant.atk, lieutenant.health) == (3 + 4, 5 + 5)


def test_grimtotem_bounty_hunter_destroys_an_enemy_legendary_only():
    game = prepare_empty_game()
    mine = game.player1.summon("EX1_116")  # Leeroy Jenkins
    theirs = game.player2.summon("EX1_116")
    game.player2.summon("CS2_182")
    hunter = game.player1.give("AV_138")
    assert hunter.targets == [theirs]
    hunter.play(target=theirs)
    assert theirs.dead and not mine.dead


def test_frozen_buckler_loses_five_armor_at_the_start_of_the_next_turn_at_most():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    game.player1.give("AV_109").play()
    assert game.player1.hero.armor == 10
    game.end_turn()
    game.player2.give(FIREBALL).play(target=game.player1.hero)
    assert game.player1.hero.armor == 4
    gained = game.player1.armor_gained_this_game
    game.end_turn()
    assert game.player1.hero.armor == 0  # never below 0
    assert game.player1.armor_gained_this_game == gained


def test_improved_open_the_cages_needs_two_minions_and_summons_two_companions():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    game.player1.give("AV_113t8").play()
    game.player1.summon(WISP)
    game.skip_turn()
    assert len(game.player1.field) == 1 and len(game.player1.secrets) == 1
    game.player1.summon(WISP)
    game.skip_turn()
    assert len(game.player1.field) == 4 and not game.player1.secrets


def test_beaststalker_tavish_and_the_hero_card_armor():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    game.player1.give("AV_113").play()
    assert game.player1.hero.armor == 5
    _choose(game)
    _choose(game)
    assert game.player1.hero.armor == 5


def test_brukan_of_the_elements_calls_two_elements_then_changes_each_turn():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    game.player2.summon("CS2_186")
    game.player1.give("AV_258").play()
    assert game.player1.hero.armor == 5
    assert game.player1.hero.power.id in (
        "AV_258pt",
        "AV_258p2",
        "AV_258pt3",
        "AV_258pt4",
    )
    first = game.player1.hero.power.id
    offered = [c.id for c in game.player1.choice.cards]
    assert offered == ["AV_258t", "AV_258t2", "AV_258t3", "AV_258t4"]
    game.player1.choice.choose(game.player1.choice.cards[2])  # Fire
    assert [c.id for c in game.player1.choice.cards] == [
        "AV_258t",
        "AV_258t2",
        "AV_258t4",
    ]
    game.player1.choice.choose(game.player1.choice.cards[0])  # Earth
    assert game.player2.hero.health == 24  # Fire: 6 damage to the enemy hero
    assert game.player1.field == ["AV_258t6", "AV_258t6"]
    game.skip_turn()
    assert game.player1.hero.power.id != first


def test_dreadprison_glaive_and_bloodseeker_honorable_kills():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    game.player1.give("AV_209").play()
    game.skip_turn()
    game.player1.hero.attack(game.player2.summon(WISP))  # exactly 1
    assert game.player2.hero.health == 29
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    bloodseeker = game.player1.give("AV_244").play()
    game.skip_turn()
    game.player1.hero.attack(game.player2.summon("CS2_142"))  # 2 on a 2/2
    assert (bloodseeker.atk, bloodseeker.durability) == (3, 2)


def test_grand_slam_gains_armor_on_an_honorable_kill():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    game.player1.give("AV_202").play()
    assert game.player1.hero.armor == 10
    game.skip_turn()
    power = game.player1.hero.power
    assert power.id == "AV_202p"
    power.use(target=game.player2.summon("CS2_182"))
    assert game.player1.hero.armor == 10
    game.skip_turn()
    game.player1.hero.power.use(target=game.player2.summon("CS2_121"))  # 2 on a 2/2
    assert game.player1.hero.armor == 14


def test_the_unstoppable_force_smashes_the_minion_into_its_own_hero():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    game.player1.give("AV_202").play()
    game.skip_turn()
    ogre = game.player2.summon("CS2_200")  # 6/7: survives 5
    game.player1.hero.attack(ogre)
    assert ogre.damage == 5
    assert game.player2.hero.health == 30 - 5 or game.player2.hero.health < 30


def test_whelp_bonker_draws_on_frenzy_and_on_an_honorable_kill():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    bonker = game.player1.give("ONY_003").play()
    _to_deck(game.player1, WISP, WISP, WISP)
    game.player1.give(MOONFIRE).play(target=bonker)  # Frenzy: draws
    assert game.player1.hand == [WISP]
    game.skip_turn()
    game.player1.discard_hand()
    bonker.attack(game.player2.summon(WISP))  # exactly lethal
    assert game.player1.hand == [WISP]


def test_najak_hexxen_takes_an_enemy_minion_and_gives_it_back():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.MAGE)
    yeti = game.player2.summon("CS2_182")
    najak = game.player1.give("AV_331").play(target=yeti)
    assert game.player1.field == ["AV_331", "CS2_182"]
    najak.destroy()
    assert game.player2.field == ["CS2_182"]


def test_xyrella_flips_between_healing_and_damage_each_turn():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.MAGE)
    game.player1.give("AV_207").play()
    power = game.player1.hero.power
    assert power.id == "AV_207p"
    game.player1.hero.set_current_health(20)
    power.use(target=game.player1.hero)
    assert game.player1.hero.health == 25
    game.skip_turn()
    assert game.player1.hero.power.id == "AV_207p2"
    game.player1.hero.power.use(target=game.player2.hero)
    assert game.player2.hero.health == 25


# def test_zephrys_lamp_offers_three_cards():
#     # A146 (D-108), as Zephrys the Great: three cards of the list.
#     game = prepare_empty_game()
#     game.player1.give("ONY_005tb610").play()
#     choice = game.player1.choice
#     assert len(choice.cards) == 3
#     assert len({c.id for c in choice.cards}) == 3


def test_the_three_tradeable_cards_of_alterac_trade():
    # A233 (WP-189c): the three Tradeable cards of Alterac (Drakefire Amulet,
    # Ring of Replenishment, Dragonbane's Strike...) trade since WP-197 repaired
    # `Card.is_tradeable`.
    for card_id in ("ONY_025", "ONY_027", "ONY_029"):
        game = prepare_game()
        player = game.current_player
        card = player.give(card_id)
        assert card.tradeable, card_id
        assert card.is_tradeable(), card_id
        deck, mana = len(player.deck), player.used_mana
        card.trade()
        assert card.zone == Zone.DECK, card_id
        assert len(player.deck) == deck, card_id
        assert player.used_mana == mana + 1, card_id
