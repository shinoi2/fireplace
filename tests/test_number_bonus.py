"""
Le bonus de nombre d'un sort (`Spell.number_bonus`, Hearthstone WP-143, « +1 ») : chaque nombre
`$n` et `#n` du texte du sort vaut `number_bonus` de plus, avant le pouvoir des sorts et les autres
modificateurs, qui s'ajoutent ensuite comme d'ordinaire. Le coût et les nombres sans `$` ni `#` ne
changent pas ; une copie n'a pas le bonus.
"""

from utils import *

from fireplace.dsl.copy import ExactCopy
from fireplace.dsl.selector import SELF

ARCANE_MISSILES = "EX1_277"
AVENGING_WRATH = "EX1_384"
FLAMESTRIKE = "CS2_032"
ARCANE_BLAST = "AT_004"
ARCANE_INTELLECT = "CS2_023"
HOLY_NOVA = "CS1_112"
STARFALL = "NEW1_007"
PROPHET_VELEN = "EX1_350"
AUCHENAI_SOULPRIEST = "EX1_591"
BOULDERFIST_OGRE = "CS2_200"
SOUL_CLEAVE = "BT_740"
EXPLOSIVE_TRAP = "EX1_610"


def _avec_bonus(player, card_id, bonus=1):
    card = player.give(card_id)
    card.number_bonus = bonus
    return card


def test_fireball_plus_one():
    game = prepare_empty_game()
    fireball = _avec_bonus(game.player1, FIREBALL)
    assert fireball.cost == 4
    assert "7" in fireball.description
    fireball.play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 7


def test_fireball_plus_one_then_spell_damage():
    game = prepare_empty_game()
    game.player1.give(KOBOLD_GEOMANCER).play()
    fireball = _avec_bonus(game.player1, FIREBALL)
    assert "8" in fireball.description
    fireball.play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 8


def test_fireball_plus_two():
    game = prepare_empty_game()
    _avec_bonus(game.player1, FIREBALL, 2).play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 8


def test_no_bonus_is_unchanged():
    game = prepare_empty_game()
    fireball = game.player1.give(FIREBALL)
    assert fireball.number_bonus == 0
    fireball.play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 6


def test_holy_light_plus_one():
    game = prepare_empty_game()
    game.player1.hero.set_current_health(10)
    holy_light = _avec_bonus(game.player1, HOLY_LIGHT)
    assert "9" in holy_light.description
    holy_light.play()
    assert game.player1.hero.health == 10 + 9


def test_arcane_missiles_plus_one_is_one_more_missile():
    game = prepare_empty_game()
    missiles = _avec_bonus(game.player1, ARCANE_MISSILES)
    assert "4" in missiles.description
    missiles.play()
    # Quatre missiles de 1 : le bonus va au nombre de missiles, pas à chacun.
    assert game.player2.hero.health == 30 - 4


def test_arcane_missiles_plus_one_then_spell_damage():
    game = prepare_empty_game()
    game.player1.give(KOBOLD_GEOMANCER).play()
    _avec_bonus(game.player1, ARCANE_MISSILES).play()
    assert game.player2.hero.health == 30 - 5


def test_avenging_wrath_plus_one():
    game = prepare_empty_game()
    _avec_bonus(game.player1, AVENGING_WRATH).play()
    assert game.player2.hero.health == 30 - 9


def test_flamestrike_plus_one_hits_each_for_six():
    game = prepare_empty_game()
    ogres = [game.player2.summon(BOULDERFIST_OGRE) for _ in range(2)]
    _avec_bonus(game.player1, FLAMESTRIKE).play()
    assert [o.health for o in ogres] == [7 - 6, 7 - 6]
    assert game.player2.hero.health == 30


def test_holy_nova_plus_one_damage_and_heal():
    game = prepare_empty_game()
    game.player1.hero.set_current_health(20)
    ogre = game.player2.summon(BOULDERFIST_OGRE)
    _avec_bonus(game.player1, HOLY_NOVA).play()
    assert ogre.health == 7 - 3
    assert game.player1.hero.health == 20 + 3


def test_arcane_blast_double_spell_damage_counts_bonus_once():
    # « This spell gets double bonus from Spell Damage » : le +1 n'est pas du pouvoir des sorts.
    game = prepare_empty_game()
    game.player1.give(KOBOLD_GEOMANCER).play()
    ogre = game.player2.summon(BOULDERFIST_OGRE)
    _avec_bonus(game.player1, ARCANE_BLAST).play(target=ogre)
    assert ogre.health == 7 - (2 + 1 + 1 + 1)


def test_velen_doubles_after_the_bonus():
    game = prepare_empty_game()
    game.player1.summon(PROPHET_VELEN)
    _avec_bonus(game.player1, FIREBALL).play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - (6 + 1) * 2
    game.player1.hero.set_current_health(5)
    _avec_bonus(game.player1, HOLY_LIGHT).play()
    assert game.player1.hero.health == 5 + (8 + 1) * 2


def test_auchenai_turns_the_bonus_heal_into_damage():
    game = prepare_empty_game()
    game.player1.summon(AUCHENAI_SOULPRIEST)
    _avec_bonus(game.player1, HOLY_LIGHT).play()
    assert game.player1.hero.health == 30 - 9


def test_choose_one_uses_the_bonus_of_the_card():
    game = prepare_empty_game()
    ogre = game.player2.summon(BOULDERFIST_OGRE)
    starfall = _avec_bonus(game.player1, STARFALL)
    starfall.play(target=ogre, choose="NEW1_007b")
    assert ogre.health == 7 - 6


def test_numbers_without_dollar_are_unchanged():
    game = prepare_empty_game()
    for _ in range(5):
        game.player1.give(WISP).shuffle_into_deck()
    intellect = _avec_bonus(game.player1, ARCANE_INTELLECT)
    before = len(game.player1.hand)
    assert intellect.cost == 3
    intellect.play()
    assert len(game.player1.hand) == before - 1 + 2
    assert len(game.player1.deck) == 5 - 2


def test_lifesteal_heals_the_damage_dealt_not_one_more():
    game = prepare_empty_game()
    game.player1.hero.set_current_health(20)
    ogres = [game.player2.summon(BOULDERFIST_OGRE) for _ in range(2)]
    _avec_bonus(game.player1, SOUL_CLEAVE).play()
    assert [o.health for o in ogres] == [7 - 3, 7 - 3]
    assert game.player1.hero.health == 20 + 3 + 3


def test_a_secret_keeps_its_bonus_until_it_triggers():
    game = prepare_empty_game()
    _avec_bonus(game.player1, EXPLOSIVE_TRAP).play()
    game.end_turn()
    wisp = game.player2.give(WISP)
    wisp.play()
    game.end_turn()
    game.end_turn()
    wisp.attack(game.player1.hero)
    assert game.player2.hero.health == 30 - 3


def test_an_immune_target_takes_nothing():
    game = prepare_empty_game()
    game.player2.hero.set_current_health(20)
    game.player2.hero.buff(game.player2.hero, "EX1_295o")
    assert game.player2.hero.immune
    _avec_bonus(game.player1, FIREBALL).play(target=game.player2.hero)
    assert game.player2.hero.health == 20


def test_a_copy_has_no_bonus():
    game = prepare_empty_game()
    fireball = _avec_bonus(game.player1, FIREBALL)
    copy = ExactCopy(SELF).evaluate(fireball)[0]
    assert copy.number_bonus == 0
