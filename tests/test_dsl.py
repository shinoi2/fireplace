#!/usr/bin/env python
from types import SimpleNamespace

import pytest
from utils import *

from fireplace.card import Card
from fireplace.dsl import *
from fireplace.exceptions import *


@pytest.mark.parametrize(
    "condition, expected",
    [
        (Find(SELF), True),
        (Find(SELF - SELF), False),
        (Count(SELF) == 1, True),
        (Count(SELF) == 0, False),
    ],
)
def test_evaluator_negation(condition, expected):
    source = prepare_empty_game().player1
    negated = -condition

    assert condition.check(source) is expected
    assert negated.check(source) is not expected
    assert (-negated).check(source) is expected
    # Negating a copy must leave the original condition unchanged.
    assert condition.check(source) is expected

    assert (condition & "yes" | "no").evaluate(source) == ("yes" if expected else "no")
    assert (negated & "yes" | "no").evaluate(source) == ("no" if expected else "yes")


def test_evaluator_automatically_wraps_subclass_checks():
    class Condition(Evaluator):
        def check(self, source):
            return True

    class InheritedCondition(Condition):
        pass

    class OverriddenCondition(Condition):
        def check(self, source):
            return False

    assert InheritedCondition.check is Condition.check
    for cls, expected in (
        (Condition, True),
        (InheritedCondition, True),
        (OverriddenCondition, False),
    ):
        condition = cls()
        assert condition.check(None) is expected
        assert (-condition).check(None) is not expected
        assert (-(-condition)).check(None) is expected


def test_selector():
    game = prepare_game()
    game.player1.discard_hand()
    alex = game.player1.give("EX1_561")
    selector = PIRATE | DRAGON + MINION
    assert len(selector.eval(game.player1.hand, game.player1)) >= 1

    selector = IN_HAND + DRAGON + FRIENDLY
    targets = selector.eval(game, game.player1)
    assert len(targets) == 1
    assert targets[0] == alex


@pytest.mark.parametrize(
    "selector",
    [
        Selector(),
        FilterSelector(lambda entity, source: True),
        FuncSelector(lambda entities, source: entities),
    ],
)
def test_selectors_resolve_morph_chains_without_changing_order_or_duplicates(selector):
    latest = SimpleNamespace(morphed=None)
    intermediate = SimpleNamespace(morphed=latest)
    original = SimpleNamespace(morphed=intermediate)
    unchanged = object()
    entities = [original, unchanged, original]

    result = selector.eval(entities, None)

    assert len(result) == 3
    assert result[0] is latest
    assert result[1] is unchanged
    assert result[2] is latest
    assert entities[0] is original
    assert selector.eval([], None) == []


def test_selector_subclasses_resolve_morphs_when_inheriting_or_overriding_eval():
    class ParentSelector(Selector):
        def eval(self, entities, source):
            return entities

    class InheritedSelector(ParentSelector):
        pass

    class OverriddenSelector(ParentSelector):
        def eval(self, entities, source):
            return entities[::-1]

    latest = SimpleNamespace(morphed=None)
    original = SimpleNamespace(morphed=latest)
    unchanged = object()
    assert InheritedSelector.eval is ParentSelector.eval
    result = InheritedSelector().eval([original, unchanged], None)
    assert result[0] is latest
    assert result[1] is unchanged
    result = OverriddenSelector().eval([original, unchanged], None)
    assert result[0] is unchanged
    assert result[1] is latest


def test_self_selector_follows_repeated_infuse_transformations():
    game = prepare_empty_game()
    original = game.player1.give("REV_906")
    for _ in range(6):
        game.player1.summon(WISP).destroy()
    latest = game.player1.hand[-1]

    result = SELF.eval(game, original)

    assert len(result) == 1
    assert result[0] is latest
    assert latest.data_num_2 == 8


def test_target_selector_and_set_operations_follow_transformed_target():
    game = prepare_empty_game()
    original = game.player2.summon(WISP)
    spell = game.player1.give(MOONFIRE)
    spell.target = original
    game.cheat_action(spell, [Morph(original, "CS2_182")])
    game.cheat_action(spell, [Morph(original.morphed, "EX1_tk28")])
    latest = original.morphed.morphed

    result = TARGET.eval(game, spell)
    assert len(result) == 1
    assert result[0] is latest
    result = (TARGET + MINION + IN_PLAY).eval(game, spell)
    assert len(result) == 1
    assert result[0] is latest


def test_game_selectors_do_not_match_a_morphed_entity_by_its_former_type():
    game = prepare_empty_game()
    original = game.player1.give("VAN_EX1_323")
    original.play()
    assert original.morphed is game.player1.hero
    assert all(card.type == CardType.MINION for card in MINION.eval(game, game.player1))
    assert ALL_MINIONS.eval(game, game.player1) == []
    assert FRIENDLY_MINIONS.eval(game, game.player1) == []
    assert SELF.eval(game, original) == [game.player1.hero]


def test_empty_selector():
    game = prepare_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    selector = IN_HAND

    targets = selector.eval(game.player1.hand, game.player1)
    assert not targets


def test_random_card_picker():
    game = prepare_empty_game()
    picker = RandomCardPicker()
    ids = picker.find_cards(game)
    for id in ids:
        card = Card(id)
        assert card.is_standard
        assert card.type is not CardType.HERO
        assert card.type is not CardType.ENCHANTMENT
        assert card.type is not CardType.HERO_POWER

    game.player1.is_standard = False
    ids = picker.find_cards(game)
    has_wild = False
    for id in ids:
        card = Card(id)
        if not card.is_standard:
            has_wild = True
        assert card.type is not CardType.HERO
        assert card.type is not CardType.ENCHANTMENT
        assert card.type is not CardType.HERO_POWER
    assert has_wild


def test_controller():
    game = prepare_game()
    game.player1.discard_hand()
    wisp = game.player1.give(WISP)
    wisp.play()
    assert Controller().evaluate(wisp) is game.player1


def test_self_selector():
    game = prepare_empty_game()
    game.player1.summon(WISP)
    game.player2.give(FIREBALL)
    selector = SELF
    for source in game:
        targets = selector.eval(game, source)
        assert len(targets) == 1
        assert targets[0] is source


def test_owner_selector():
    game = prepare_game()
    wisp = game.player1.give(WISP)
    wisp.play()
    blessing_wisdom = game.player1.give("EX1_363")
    blessing_wisdom.play(target=wisp)
    targets = OWNER.eval(game, wisp.buffs[0])
    assert len(targets) == 1
    assert targets[0] is wisp


def test_id_selector():
    game = prepare_game()
    for entity in game.entities:
        id = getattr(entity, "id", None)
        if id:
            targets = ID(id).eval(game, game.player1)
            assert len(targets) >= 1
            assert targets[0].id == id


def test_target_selector():
    game = prepare_game()
    moonfire = game.player1.give(MOONFIRE)
    target = game.player1.hero
    # Set this manually for the selector
    moonfire.target = target

    targets = TARGET.eval(game, moonfire)
    assert len(targets) == 1
    assert targets[0] == target


def test_high_low_atk_selectors():
    game = prepare_game()
    game.player1.discard_hand()
    game.player2.discard_hand()

    # Give two wisps and make sure we only get back one
    wisp = game.player1.give(WISP)
    game.player1.give(WISP)

    IN_HAND = EnumSelector(Zone.HAND)
    high_selector = HIGHEST_ATK(IN_HAND)
    low_selector = LOWEST_ATK(IN_HAND)

    targets = high_selector.eval(game, game.player1)
    assert len(targets) == 1
    assert targets[0] == wisp.id

    targets = low_selector.eval(game, game.player1)
    assert len(targets) == 1
    assert targets[0] == wisp.id

    alex = game.player1.give("EX1_561")
    mountain = game.player1.give("EX1_105")

    targets = high_selector.eval(game, game.player1)
    assert len(targets) == 1
    assert targets[0] in [alex, mountain]

    targets = low_selector.eval(game, game.player1)
    assert len(targets) == 1
    assert targets[0] == wisp.id


def test_controlled_by_selector():
    game = prepare_game()
    game.player1.discard_hand()
    game.player2.discard_hand()

    wisp = game.player1.give(WISP)
    goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)

    wisp.play()
    goldshire.play()

    MINION = EnumSelector(CardType.MINION)
    IN_PLAY = EnumSelector(Zone.PLAY)
    selector = MINION + IN_PLAY + FRIENDLY

    for source in [wisp, goldshire, game.player1]:
        targets = selector.eval(game, source)
        assert len(targets) == 2
        assert set(targets) == set([wisp, goldshire])

    selector = MINION + IN_PLAY + ENEMY
    targets = selector.eval(game, game.player2)
    assert len(targets) == 2
    assert set(targets) == set([wisp, goldshire])

    moonfire = game.player1.give(MOONFIRE)
    moonfire.target = game.player1.hero
    selector = (
        MINION + IN_PLAY + CONTROLLED_BY(TARGET) + (AttrValue(GameTag.HEALTH) == 1)
    )
    targets = selector.eval(game, moonfire)
    assert len(targets) == 1
    assert targets[0] == wisp


def test_random_selector():
    game = prepare_game()
    selector = RANDOM(EnumSelector(CardType.MINION))
    targets = selector.eval(game, game.player1)
    assert len(targets) == 1

    targets = (selector * 3).eval(game, game.player1)
    assert len(targets) == 3


def test_positional_selectors():
    game = prepare_game()
    wisp1 = game.player1.give(WISP)
    wisp1.play()
    wisp2 = game.player1.give(WISP)
    wisp2.play()
    wisp3 = game.player1.give(WISP)
    wisp3.play()
    wisp4 = game.player1.give(WISP)
    wisp4.play()
    defender = game.player1.give("EX1_093")
    defender.play(index=2)
    assert game.player1.field == [wisp1, wisp2, defender, wisp3, wisp4]

    left = LEFT_OF(SELF).eval(game, defender)
    assert len(left) == 1
    assert left[0] is wisp2

    right = RIGHT_OF(SELF).eval(game, defender)
    assert len(right) == 1
    assert right[0] is wisp3

    adjacent = ADJACENT(SELF).eval(game, defender)
    assert len(adjacent) == 2
    assert adjacent[0] is wisp2
    assert adjacent[1] is wisp3


# 暂停测试：依赖冒险模式专用卡牌，按要求保留原内容为注释。
# def test_hijack():
#     game = prepare_game()
#     vial = game.player1.give("LOEA16_8")
#     with hijacked(RANDOM_ENEMY_MINION, FRIENDLY_HERO):
#         with pytest.raises(GameOver):
#             vial.play()


def test_lazynum():
    game = prepare_game()
    [game.player1.give(WISP).play() for _ in range(4)]
    game.end_turn()
    [game.player2.give(WISP).play() for _ in range(5)]
    game.end_turn()
    assert Count(FRIENDLY_MINIONS).evaluate(game.player1) == 4
    assert Count(ENEMY_MINIONS).evaluate(game.player1) == 5
    maxnum = Max(Count(FRIENDLY_MINIONS), Count(ENEMY_MINIONS)).evaluate(game.player1)
    assert maxnum == 5

    total = (Count(FRIENDLY_MINIONS) + Count(ENEMY_MINIONS)).evaluate(game.player1)
    assert total == 9
    diff = (Count(FRIENDLY_MINIONS) - Count(ENEMY_MINIONS)).evaluate(game.player1)
    assert diff == -1


def test_spell_damage_and_heal_are_lazy_numbers_and_support_arithmetic():
    game = prepare_empty_game()
    spell = game.player1.give(HOLY_LIGHT)
    damage = SPELL_DAMAGE(3)
    healing = SPELL_HEAL(3)
    for value in (damage, healing):
        assert isinstance(value, LazyNum)
        assert not isinstance(value, Selector)
        assert value.evaluate(spell) == 3

    game.player1.summon(KOBOLD_GEOMANCER)
    assert damage.evaluate(spell) == 4
    assert healing.evaluate(spell) == 3
    game.player1.summon("EX1_350")  # Prophet Velen
    for value, expected in ((damage, 8), (healing, 6)):
        assert value.evaluate(spell) == expected
        assert (value * 2).evaluate(spell) == expected * 2
        assert (value + 1).evaluate(spell) == expected + 1
        assert (-value).evaluate(spell) == -expected
        assert (value == expected).check(spell)


def test_spell_damage_and_heal_accept_lazy_amounts():
    game = prepare_empty_game()
    spell = game.player1.give(HOLY_LIGHT)
    minion = game.player1.summon(KOBOLD_GEOMANCER)
    assert SPELL_DAMAGE(Count(FRIENDLY_MINIONS)).evaluate(spell) == 2
    assert SPELL_HEAL(Count(FRIENDLY_MINIONS)).evaluate(spell) == 1
    minion.destroy()
    assert SPELL_DAMAGE(Count(FRIENDLY_MINIONS)).evaluate(spell) == 0
    assert SPELL_HEAL(Count(FRIENDLY_MINIONS)).evaluate(spell) == 0


def test_starting_hero_selector_returns_a_list():
    game = prepare_empty_game()
    result = STARTING_HERO.eval(game, game.player1.hero)
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0] is game.player1.starting_hero


def test_enchantments_initialize_independent_stored_card_lists():
    game = prepare_empty_game()
    first = game.player1.card("REV_373e")
    second = game.player1.card("REV_373e")
    assert first.store_card == []
    assert second.store_card == []
    assert first.store_card is not second.store_card
    first.store_card.append(game.player1.card(MOONFIRE))
    assert second.store_card == []
    assert STORE_CARD.eval(game, second) == []


@pytest.mark.parametrize("multiple", [False, True])
def test_storing_buff_always_stores_a_list(multiple):
    game = prepare_empty_game()
    owner = game.player1.summon(WISP)
    cards = [game.player1.card(MOONFIRE), game.player1.card(FIREBALL)]
    stored = cards if multiple else cards[0]
    buff = game.player1.card("REV_373e")
    StoringBuff(owner, buff, stored).do(owner, owner, buff, stored)
    assert isinstance(buff.store_card, list)
    assert buff.store_card == (cards if multiple else [cards[0]])
    assert STORE_CARD.eval(game, buff) == buff.store_card


def test_stored_card_selector_follows_a_transformed_card():
    game = prepare_empty_game()
    owner = game.player1.summon(WISP)
    stored = game.player1.summon(WISP)
    game.cheat_action(owner, [StoringBuff(owner, "REV_373e", stored)])
    buff = owner.buffs[-1]
    game.cheat_action(owner, [Morph(stored, "CS2_182")])
    result = STORE_CARD.eval(game, buff)
    assert len(result) == 1
    assert result[0] is stored.morphed
