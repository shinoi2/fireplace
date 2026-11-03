import pytest
from utils import *

from fireplace.exceptions import GameOver, InvalidAction


def test_happy_ghoul():
    game = prepare_game()
    ghoul = game.player1.give("ICC_700")
    assert ghoul.cost == 3
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    game.player1.give("AT_055").play(target=game.player1.hero)
    assert ghoul.cost == 0
    game.end_turn()
    assert ghoul.cost == 3


def test_mindbreaker():
    game = prepare_game()
    breaker = game.player1.give("ICC_902").play()
    assert game.player1.hero.power.exhausted
    assert game.player2.hero.power.exhausted
    breaker.destroy()
    assert not game.player1.hero.power.exhausted
    assert not game.player2.hero.power.exhausted


def test_drakkari_enchanter():
    game = prepare_game()
    game.player1.give("EX1_298").play()
    game.player1.give(THE_COIN).play()
    game.player1.give("ICC_901").play()
    game.end_turn()
    assert game.player2.hero.health == 30 - 8 - 8


def test_fatespinner():
    game = prepare_game()
    game.player1.give("ICC_047").play(choose="ICC_047a")
    game.player1.give("ICC_047").play(choose="ICC_047b")
    assert game.player1.field[0].deathrattles
    assert game.player1.field[1].deathrattles


def test_spreading_plague():
    game = prepare_game()
    for _ in range(4):
        game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give("ICC_054").play()
    assert len(game.player2.field) == 4


def test_malfurion_the_pestilent():
    game = prepare_game()
    game.player1.give("ICC_832").play(choose="ICC_832a")
    game.player1.hero.power.use(choose="ICC_832pa")
    assert game.player1.hero.armor == 5 + 3


def test_deathstalker_rexxar():
    game = prepare_empty_game()
    game.player1.give("ICC_828").play()
    game.player1.hero.power.use()
    assert game.player1.choice
    choice = game.player1.choice
    card1 = choice.cards[0]
    choice.choose(card1)
    choice = game.player1.choice
    card2 = choice.cards[0]
    choice.choose(card2)
    assert not game.player1.choice
    assert game.player1.hand[0].atk == card1.atk + card2.atk
    assert game.player1.hand[0].health == card1.health + card2.health
    assert game.player1.hand[0].cost == card1.cost + card2.cost


def test_deathstalker_rexxar_zombeast_is_its_own_card():
    # A Zombeast takes the text of the first beast it is built from; the
    # card ICC_828t of the database, shared by every game, keeps its own.
    scripts = fireplace.cards.db["ICC_828t"].scripts
    zombeasts = []
    for _ in range(2):
        game = prepare_empty_game()
        game.player1.give("ICC_828").play()
        game.player1.hero.power.use()
        first = game.player1.choice.cards[0]
        game.player1.choice.choose(first)
        game.player1.choice.choose(game.player1.choice.cards[0])
        zombeast = game.player1.hand[0]
        assert zombeast.id == "ICC_828t"
        assert zombeast.data.scripts is first.data.scripts
        zombeasts.append((zombeast, first))
    assert fireplace.cards.db["ICC_828t"].scripts is scripts
    for zombeast, first in zombeasts:
        assert zombeast.data.scripts is first.data.scripts


def test_bolvar_fireblood():
    game = prepare_game()
    fireblood = game.player1.give("ICC_858").play()
    atk = fireblood.atk
    game.player1.give(MOONFIRE).play(target=fireblood)
    assert fireblood.atk == atk + 2


def test_uther_of_the_ebon_blade():
    game = prepare_game()
    game.player1.give("ICC_829").play()
    game.end_turn()
    game.end_turn()
    for _ in range(3):
        game.player1.hero.power.use()
        game.end_turn()
        game.end_turn()
    with pytest.raises(GameOver):
        game.player1.hero.power.use()


def test_embrace_darkness():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give("ICC_849").play(target=wisp)
    game.end_turn()
    game.end_turn()
    assert len(game.player1.field) == 0
    assert len(game.player2.field) == 1


def test_moorabi():
    game = prepare_empty_game()
    game.player1.give("ICC_289").play()
    wisp = game.player1.give(WISP).play()
    game.player1.give("CS2_031").play(target=wisp)
    assert game.player1.hand[0].id == WISP


def test_frost_lich_jaina():
    game = prepare_game()
    firefly = game.player1.give("UNG_809").play()
    assert not firefly.lifesteal
    game.player1.give("ICC_833").play()
    assert firefly.lifesteal
    game.end_turn()
    wisp = game.player2.give(WISP).play()
    game.end_turn()
    assert len(game.player1.field) == 2
    game.player1.hero.power.use(target=wisp)
    assert len(game.player1.field) == 3


def test_shadowreaper_anduin():
    game = prepare_game()
    game.player1.give("ICC_830").play()
    game.end_turn()
    game.end_turn()
    for _ in range(5):
        wisp = game.player1.give(WISP).play()
        game.player1.hero.power.use(target=wisp)
        assert game.player1.hero.power.exhausted


def test_valeera_the_hollow():
    game = prepare_empty_game()
    game.player1.give("ICC_827").play()
    assert game.player1.hero.stealthed
    game.end_turn()
    assert game.player1.hero.stealthed
    game.end_turn()
    assert not game.player1.hero.stealthed
    assert not game.player1.hero.power.is_usable()
    game.player1.give(WISP).play()
    assert game.player1.hand[0].id == WISP
    game.player1.give(CHICKEN).play()
    assert game.player1.hand[0].id == CHICKEN
    game.player1.hand[0].play()
    assert len(game.player1.hand) == 0
    game.skip_turn()
    assert len(game.player1.hand) == 1


def test_defile():
    game = prepare_empty_game()
    game.player1.give(WISP).play()  # 1/1
    game.player1.give(TARGET_DUMMY).play()  # 0/2
    game.player1.give("EX1_556").play()  # 2/3 deathrattle summon 2/1
    game.player1.give("CS2_033").play()  # 3/6
    game.player1.give("ICC_041").play()
    assert len(game.player1.field) == 1
    assert game.player1.field[0].health == 1


def test_defile_max_time():
    game = prepare_empty_game()
    grim1 = game.player1.give("BRM_019").play()
    game.player1.give(MOONFIRE).play(target=grim1)
    game.player1.give(WISP).play()
    game.player1.give("ICC_041").play()
    assert len(game.player1.field) > 0


def test_frostmourne():
    game = prepare_game()
    game.player1.give("ICC_314t1").play()
    game.end_turn()
    for _ in range(3):
        game.player2.give(WISP).play()
    game.end_turn()
    game.player1.hero.attack(game.player2.field[0])
    game.skip_turn()
    game.player1.hero.attack(game.player2.field[0])
    game.skip_turn()
    game.player1.hero.attack(game.player2.field[0])
    assert len(game.player1.field) == 3
    game.player1.field[0].id == WISP
    game.player1.field[1].id == WISP
    game.player1.field[2].id == WISP


def test_hero_armor():
    game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
    game.player1.hero.power.use()
    assert game.player1.hero.armor == 2
    game.player1.give("ICC_481").play()
    assert game.player1.hero.armor == 7


def test_hero_health():
    game = prepare_game()
    game.player1.give("UNG_940t8").play()
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert game.player1.hero.health == 39
    game.player1.give("ICC_481").play()
    assert game.player1.hero.health == 39


def test_death_grip():
    game = prepare_game()
    grip = game.player1.give("ICC_314t4")
    deck = len(game.player2.deck)
    hand = len(game.player1.hand)
    grip.play()
    assert len(game.player2.deck) == deck - 1
    assert len(game.player1.hand) == hand


def test_phantom_freebooter():
    game = prepare_game()
    weapon = game.player1.give("CS2_106").play()
    freebooter = game.player1.give("ICC_018")
    atk = freebooter.atk
    health = freebooter.health
    freebooter.play()
    assert freebooter.atk == atk + weapon.atk
    assert freebooter.health == health + weapon.durability


def test_plague_scientist():
    game = prepare_game()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    scientist = game.player1.give("ICC_809")
    assert not scientist.requires_target()
    assert not scientist.targets
    wisp = game.player1.give(WISP).play()
    assert scientist.requires_target()
    assert scientist.targets == [wisp]


# WP-184 : les cartes que le fork jouait autrement que leur texte (patch 21.8).


def _deck(player, *ids):
    cards = []
    for id in ids:
        card = player.card(id)
        card.zone = Zone.DECK
        cards.append(card)
    return cards


def test_crypt_lord_grows_after_any_summon():
    game = prepare_empty_game()
    lord = game.player1.give("ICC_808").play()
    assert lord.health == 6
    game.player1.give(WISP).play()
    assert lord.health == 7


def test_abominable_bowman_summons_one_beast():
    game = prepare_empty_game()
    for _ in range(3):
        game.player1.give("CS2_172").play().destroy()
        game.player1.used_mana = 0
    game.player1.give("ICC_825").play().destroy()
    assert [m.id for m in game.player1.field] == ["CS2_172"]


def test_simulacrum_copies_a_minion():
    game = prepare_empty_game()
    game.player1.give(MOONFIRE)
    game.player1.give(CHICKEN)
    game.player1.give("CS2_182")
    game.player1.give("ICC_823").play()
    assert sorted(c.id for c in game.player1.hand) == sorted(
        [MOONFIRE, CHICKEN, "CS2_182", CHICKEN]
    )


def test_avalanche_freezes_the_target_and_hits_its_neighbours():
    game = prepare_empty_game()
    game.end_turn()
    left = game.player2.give("CS2_182").play()
    middle = game.player2.give(WISP).play()
    right = game.player2.give("CS2_182").play()
    game.end_turn()
    game.player1.give("ICC_078").play(target=middle)
    assert middle.frozen and middle.health == 1
    assert left.health == 2 and not left.frozen
    assert right.health == 2 and not right.frozen


def test_drain_soul_deals_three():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.give("CS2_182").play()
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    game.player1.give("ICC_055").play(target=yeti)
    assert yeti.health == 2
    assert game.player1.hero.health == 30


def test_leeching_poison_lasts_this_turn():
    game = prepare_empty_game()
    game.player1.give("CS2_106").play()
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    game.player1.give("ICC_221").play()
    assert game.player1.weapon.lifesteal
    game.player1.hero.attack(game.player2.hero)
    assert game.player1.hero.health == 30
    game.end_turn()
    assert not game.player1.weapon.lifesteal
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    game.player1.hero.attack(game.player2.hero)
    assert game.player1.hero.health == 29


def test_prince_valanar_reads_four_cost_cards():
    game = prepare_empty_game()
    _deck(game.player1, "CS2_120")
    valanar = game.player1.give("ICC_853").play()
    assert valanar.taunt and valanar.lifesteal
    game.player1.used_mana = 0
    _deck(game.player1, "CS2_182")
    valanar = game.player1.give("ICC_853").play()
    assert not valanar.taunt and not valanar.lifesteal


def test_meat_wagon_summons_less_attack_only():
    game = prepare_empty_game()
    _deck(game.player1, WISP)
    game.player1.give("ICC_812").play().destroy()
    assert len(game.player1.field) == 0
    assert len(game.player1.deck) == 1
    game.player1.used_mana = 0
    _deck(game.player1, TARGET_DUMMY)
    game.player1.give("ICC_812").play().destroy()
    assert [m.id for m in game.player1.field] == [TARGET_DUMMY]


def test_obliterate_damages_the_hero_by_health():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.give("CS2_182").play()
    game.end_turn()
    game.player1.give("ICC_314t6").play(target=yeti)
    assert yeti.dead
    assert game.player1.hero.health == 30 - 5
    game.end_turn()
    yeti = game.player2.give("CS2_182").play()
    game.player2.give(MOONFIRE).play(target=yeti)
    game.player2.give(MOONFIRE).play(target=yeti)
    game.end_turn()
    game.player1.give("ICC_314t6").play(target=yeti)
    assert game.player1.hero.health == 30 - 5 - 3


def test_rotface_only_when_it_survives():
    game = prepare_empty_game()
    rotface = game.player1.give("ICC_405").play()
    game.player1.give(MOONFIRE).play(target=rotface)
    assert len(game.player1.field) == 2
    game.player1.used_mana = 0
    game.player1.give(FIREBALL).play(target=rotface)
    assert rotface.dead
    assert len(game.player1.field) == 1


def test_valkyr_soulclaimer_only_when_it_survives():
    game = prepare_empty_game()
    valkyr = game.player1.give("ICC_408").play()
    game.player1.give(MOONFIRE).play(target=valkyr)
    assert [m.id for m in game.player1.field] == ["ICC_408", "ICC_900t"]
    game.player1.give(FIREBALL).play(target=valkyr)
    assert [m.id for m in game.player1.field] == ["ICC_900t"]


def test_furnacefire_colossus_only_its_own_weapons():
    game = prepare_empty_game()
    game.player1.give("CS2_106")
    game.player1.give("CS2_112")
    axe = game.player2.give("CS2_106")
    colossus = game.player1.give("ICC_096").play()
    assert colossus.atk == 6 + 3 + 5
    assert colossus.health == 6 + 2 + 2
    assert axe.zone == Zone.HAND


def test_druid_of_the_swarm_under_fandral():
    game = prepare_empty_game()
    game.player1.give(FANDRAL_STAGHELM).play()
    game.player1.give("ICC_051").play()
    druid = game.player1.field[-1]
    assert druid.id == "ICC_051t3"
    assert druid.taunt and druid.poisonous
    assert (druid.atk, druid.health) == (1, 5)


def test_fatespinner_under_fandral_both_deathrattles():
    # Both at once (A86, D-108): the damage kills first, then the +2/+2 goes to
    # the survivors only. The 2/3 dies; the 4/5 ends 6/4.
    game = prepare_empty_game()
    game.player1.give(FANDRAL_STAGHELM).play()
    game.player1.give("ICC_047").play()
    fatespinner = game.player1.field[-1]
    assert fatespinner.id == "ICC_047t2"
    game.end_turn()
    croc = game.player2.give("CS2_120").play()
    yeti = game.player2.give("CS2_182").play()
    game.end_turn()
    fatespinner.destroy()
    assert croc.dead
    assert croc not in game.player2.field
    assert (yeti.atk, yeti.health) == (6, 4)


def test_shadow_essence_leaves_the_deck():
    game = prepare_empty_game()
    _deck(game.player1, WISP)
    game.player1.give("ICC_235").play()
    assert [(m.id, m.atk, m.health) for m in game.player1.field] == [(WISP, 5, 5)]
    assert [c.id for c in game.player1.deck] == [WISP]


def test_doomerang_the_weapon_deals_the_damage():
    game = prepare_empty_game()
    game.player1.give("CS2_106").play()
    game.end_turn()
    yeti = game.player2.give("CS2_182").play()
    other = game.player2.give("CS2_182").play()
    game.end_turn()
    game.player1.give(KOBOLD_GEOMANCER).play()
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    game.player1.give("ICC_221").play()
    game.player1.give("ICC_233").play(target=yeti)
    assert yeti.health == 2
    assert game.player1.hero.health == 30
    assert [c.id for c in game.player1.hand] == ["CS2_106"]
    assert game.player1.weapon is None
    game.player1.used_mana = 0
    game.player1.hand[0].play()
    game.player1.give("UNG_823").play()
    game.player1.give("ICC_233").play(target=other)
    assert other.dead


def test_valeera_the_hollow_cannot_be_attacked_while_stealthed():
    game = prepare_empty_game()
    game.player1.give("ICC_827").play()
    game.end_turn()
    boar = game.player2.give("CS2_171").play()
    assert game.player1.hero.stealthed
    assert game.player1.hero not in boar.attack_targets
    with pytest.raises(InvalidAction):
        boar.attack(game.player1.hero)
    game.end_turn()
    game.end_turn()
    assert game.player1.hero in boar.attack_targets


def test_valeera_the_hollow_stealthed_hero_is_not_targeted_by_enemy_spells_or_powers():
    # WP-214 (regle 805) : ni sort, ni pouvoir, ni attaque adverse ne le prend pour cible.
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("ICC_827").play()
    assert game.player1.hero.stealthed
    game.end_turn()
    fireball = game.player2.give(FIREBALL)
    assert game.player1.hero not in fireball.targets
    assert game.player2.hero in fireball.targets
    assert game.player1.hero not in game.player2.hero.power.targets
    with pytest.raises(InvalidAction):
        fireball.play(target=game.player1.hero)
    # its own side may still target it
    game.end_turn()
    heal = game.player1.give("CS2_007")
    assert game.player1.hero in heal.targets
    game.end_turn()
    game.end_turn()
    assert not game.player1.hero.stealthed
    game.end_turn()
    assert game.player1.hero in game.player2.give(FIREBALL).targets


def test_shadow_reflection_leaves_the_hand_at_end_of_turn():
    game = prepare_empty_game()
    game.player1.give("ICC_827").play()
    game.player1.give(WISP).play()
    assert [c.id for c in game.player1.hand] == [WISP]
    game.end_turn()
    assert len(game.player1.hand) == 0
    game.end_turn()
    assert [c.id for c in game.player1.hand] == ["ICC_827t"]


def test_valeera_the_hollow_reflection_stays_under_mindbreaker():
    # A87 (D-108): Valeera's battlecry is not a hero power; Mindbreaker does not
    # take the Shadow Reflection away from the hand.
    game = prepare_empty_game()
    game.player1.give("ICC_902").play()
    game.player1.used_mana = 0
    game.player1.give("ICC_827").play()
    assert [c.id for c in game.player1.hand] == ["ICC_827t"]
    game.player1.give(WISP).play()
    assert [c.id for c in game.player1.hand] == [WISP]


def test_snowfury_giant_counts_overloaded_crystals_not_cards():
    # WP-214 (regle 816) : "Costs (1) less for each Mana Crystal you've Overloaded this game".
    # Feral Spirit is Overload (1) in this patch; Lava Burst is Overload (2).
    game = prepare_empty_game()
    giant = game.player1.give("ICC_090")
    assert giant.cost == 11
    game.player1.give("EX1_248").play()
    assert giant.cost == 10
    game.player1.give("EX1_241").play(target=game.player2.hero)
    assert game.player1.overloaded_this_game == 3
    assert giant.cost == 8


def test_powered_up_icecrown_conditions():
    # WP-214 : Coldwraith and the three Princes glow in the hand.
    game = prepare_empty_game(CardClass.MAGE, CardClass.WARRIOR)
    cold = game.player1.give("ICC_252")
    keleseth = game.player1.give("ICC_851")
    taldaram = game.player1.give("ICC_852")
    valanar = game.player1.give("ICC_853")
    assert not cold.powered_up
    assert keleseth.powered_up and taldaram.powered_up and valanar.powered_up
    _deck(game.player1, "CS2_189")  # Elven Archer, 1 Cost
    assert keleseth.powered_up and taldaram.powered_up and valanar.powered_up
    _deck(game.player1, "CS2_179")  # Sen'jin Shieldmasta, 4 Cost
    assert not valanar.powered_up
    assert keleseth.powered_up and taldaram.powered_up
    _deck(game.player1, "CS2_172")  # Bloodfen Raptor, 2 Cost
    assert not keleseth.powered_up
    _deck(game.player1, "CS2_118")  # Magma Rager, 3 Cost
    assert not taldaram.powered_up
    game.player2.summon(WISP).frozen = True
    assert cold.powered_up


def test_necrotic_geist_summons_a_ghoul_when_another_friendly_minion_dies():
    # WP-214 (regle 812) : "Whenever another friendly minion dies, summon a 2/2 Ghoul".
    game = prepare_empty_game()
    game.player1.give("ICC_900").play()
    wisp = game.player1.give(WISP).play()
    assert [m.id for m in game.player1.field] == ["ICC_900", WISP]
    game.player1.give(MOONFIRE).play(target=wisp)
    assert [m.id for m in game.player1.field] == ["ICC_900", "ICC_900t"]
    # an enemy minion's death does not trigger it
    game.end_turn()
    enemy = game.player2.give(WISP).play()
    enemy.destroy()
    assert [m.id for m in game.player1.field] == ["ICC_900", "ICC_900t"]
