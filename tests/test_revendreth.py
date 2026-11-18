from unittest.mock import patch

import pytest

from fireplace.dsl.selector import IMPS
from fireplace.dsl.copy import Copy
from utils import *


def test_suspicious_alchemist():
    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    coin = game.player1.card(THE_COIN)
    fireball = game.player1.card(FIREBALL)
    pyroblast = game.player1.card(PYROBLAST)
    with mock(RandomSpell, [coin, fireball, pyroblast]):
        game.player1.give("REV_000").play()
    game.player1.choice.choose(coin)
    game.end_turn()
    game.player2.choice.choose(coin)
    assert game.player1.hand == [THE_COIN]
    assert game.player2.hand == [THE_COIN]


def test_suspicious_alchemist_2():
    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    coin = game.player1.card(THE_COIN)
    fireball = game.player1.card(FIREBALL)
    pyroblast = game.player1.card(PYROBLAST)
    with mock(RandomSpell, [coin, fireball, pyroblast]):
        game.player1.give("REV_000").play()
    game.player1.choice.choose(coin)
    game.end_turn()
    game.player2.choice.choose(fireball)
    assert game.player1.hand == [THE_COIN]
    assert game.player2.hand == []


def kill_friendly(game, card_id=WISP, count=1):
    for _ in range(count):
        game.player1.summon(card_id).destroy()


@pytest.mark.parametrize(
    "base,infused,count",
    [
        ("REV_956", "REV_956t", 3),
        ("REV_957", "REV_957t", 4),
        ("REV_336", "REV_336t4", 5),
        ("REV_350", "REV_350t2", 3),
        ("REV_938", "REV_938t", 2),
        ("REV_933", "REV_933t", 2),
        ("REV_019", "REV_019t", 4),
        ("REV_601", "REV_601t", 3),
    ],
)
def test_infuse_all_card_types(base, infused, count):
    game = prepare_empty_game()
    card = game.player1.give(base)
    game.player2.summon(WISP).destroy()
    assert card.infuse == 0
    kill_friendly(game, count=count - 1)
    assert card.zone == Zone.HAND
    assert card.infuse == count - 1
    kill_friendly(game)
    upgraded = game.player1.hand[-1]
    assert upgraded.id == infused
    assert card.morphed is upgraded


def test_infuse_reborn_counts_death_once():
    game = prepare_empty_game()
    card = game.player1.give("REV_956")
    reborn = game.player1.summon("ULD_208")
    reborn.destroy()
    assert card.infuse == 1


def test_infuse_race_and_afterlife_attendant():
    game = prepare_empty_game()
    card = game.player1.card("MAW_003", zone=Zone.DECK)
    kill_friendly(game)
    assert card.infuse == 0
    attendant = game.player1.summon("MAW_031")
    kill_friendly(game)
    assert card.infuse == 0
    kill_friendly(game, "CS2_050", 3)
    assert game.player1.deck[-1].id == "MAW_003t"
    card = game.player1.card("REV_019", zone=Zone.DECK)
    attendant.destroy()
    kill_friendly(game)
    assert card.infuse == 0


def test_altimor_two_infusion_stages():
    game = prepare_empty_game()
    game.player1.give("REV_353")
    kill_friendly(game, count=4)
    assert game.player1.hand[-1].id == "REV_353t"
    kill_friendly(game, count=3)
    assert game.player1.hand[-1].id == "REV_353t"
    kill_friendly(game)
    game.player1.hand[-1].play()
    assert {c.id for c in game.player1.field} == {
        "REV_353t2",
        "REV_353t3",
        "REV_353t4",
        "REV_353t5",
    }


def test_denathrius_endless_infuse_and_lifesteal():
    game = prepare_empty_game()
    game.player1.give("REV_906")
    kill_friendly(game, count=3)
    sire = game.player1.hand[-1]
    assert sire.id == "REV_906t"
    assert sire.data_num_2 == 8
    game.player1.hero.damage = 15
    sire.play()
    assert game.player2.hero.health == 22
    assert game.player1.hero.health == 23


def test_sinfueled_golem_gains_stats_after_infusing():
    game = prepare_empty_game()
    card = game.player1.give("REV_843")
    kill_friendly(game, "CS2_182", 2)  # 4-Attack Chillwind Yetis
    assert (card.atk, card.health) == (2, 2)
    kill_friendly(game, "CS2_182")
    infused = game.player1.hand[-1]
    assert infused.id == "REV_843t"
    assert (infused.atk, infused.health) == (14, 14)


def test_insatiable_devourer_neighbors():
    game = prepare_empty_game()
    targets = [game.player2.summon("CS2_182") for _ in range(3)]
    devourer = game.player1.give("REV_017t")
    devourer.play(target=targets[1])
    assert not game.player2.field
    assert (devourer.atk, devourer.health) == (16, 19)


def test_stewart_deathrattle_passes_to_next_recruit():
    game = prepare_empty_game()
    game.player1.summon("REV_955").destroy()
    recruit = game.player1.summon("CS2_101t")
    assert (recruit.atk, recruit.health) == (4, 4)
    assert recruit.has_deathrattle
    plain = game.player1.summon("CS2_101t")
    assert (plain.atk, plain.health) == (1, 1)
    recruit.destroy()
    heir = game.player1.summon("CS2_101t")
    assert (heir.atk, heir.health) == (4, 4)
    assert heir.has_deathrattle


def test_service_bell_draws_every_copy():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
    first = game.player1.card("REV_842", zone=Zone.DECK)
    second = game.player1.card("REV_842", zone=Zone.DECK)
    neutral = game.player1.card(WISP, zone=Zone.DECK)
    game.player1.give("REV_948").play()
    assert len(game.player1.choice.cards) == 1
    game.player1.choice.choose(first)
    assert first in game.player1.hand and second in game.player1.hand
    assert game.player1.deck == [neutral]


def test_countess_invitation_and_free_legendary():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
    game.player1.give("REV_951").play()
    assert game.player1.hand == ["REV_951t"] * 3
    game.player1.give(THE_COIN).play()
    game.player1.give(THE_COIN).play()
    game.player1.hand[0].play()
    options = game.player1.choice.cards
    assert all(
        CardClass.PALADIN not in card.classes and CardClass.NEUTRAL not in card.classes
        for card in options
    )
    game.player1.choice.choose(options[0])
    assert options[0] in game.player1.hand
    assert options[0].cost == 0


def test_order_in_the_court_and_great_hall():
    game = prepare_empty_game()
    game.player1.card(WISP, zone=Zone.DECK)
    game.player1.card(PYROBLAST, zone=Zone.DECK)
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player1.give("MAW_016").play()
    assert game.player1.hand[-1].id == PYROBLAST
    assert [c.cost for c in game.player1.deck] == [0, 4]
    target = game.player1.summon("CS2_182")
    target.hit(2)
    hall = game.player1.give("REV_983")
    hall.play()
    hall.activate(target=target)
    assert (target.atk, target.health, target.max_health) == (3, 3, 3)


def test_pelagos_uses_current_health():
    game = prepare_empty_game()
    game.player1.summon("REV_250")
    target = game.player1.summon("CS2_182")
    target.hit(2)
    game.player1.give(HAND_OF_PROTECTION).play(target=target)
    assert (target.atk, target.health, target.max_health) == (4, 4, 4)


def test_identity_theft_visitor_and_harvester():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.player2.discard_hand()
    original = game.player2.give(WISP)
    game.player2.card(FIREBALL, zone=Zone.DECK)
    game.player1.give("REV_253").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert game.player1.choice
    game.player1.choice.choose(game.player1.choice.cards[0])
    copied_spell = game.player1.hand[-1]
    assert copied_spell.copied_from is game.player2.deck[0]
    game.player1.give("REV_246").play()
    assert copied_spell.cost == 2
    game.player1.give("REV_011").play()
    copied_minion = game.player1.hand.filter(id=WISP)[0]
    copied_minion.play()
    assert original.controller is game.player1
    assert original in game.player1.hand


def test_partner_in_crime_only_copies_once():
    game = prepare_empty_game()
    minion = game.player1.give("REV_247")
    minion.play()
    game.end_turn()
    assert len(game.player1.field) == 2
    game.end_turn()
    game.end_turn()
    assert len(game.player1.field) == 2


def test_kidnap_returns_original_when_sack_dies():
    game = prepare_empty_game()
    game.player1.give("REV_828").play()
    game.end_turn()
    minion = game.player2.give("CS2_182")
    minion.play()
    assert minion.zone == Zone.REMOVEDFROMGAME
    sack = game.player1.field[0]
    assert sack.id == "REV_828t"
    sack.destroy()
    assert minion in game.player2.hand
    assert minion not in game.player1.hand


def test_halkias_resurrects_from_secret():
    game = prepare_empty_game()
    game.player1.give("REV_827").play()
    game.player1.summon("REV_829").destroy()
    game.end_turn()
    game.player2.give(THE_COIN).play()
    assert sorted(c.id for c in game.player1.field) == ["REV_827t", "REV_829"]


def test_tight_lipped_witness_prevents_secret_effects():
    game = prepare_empty_game()
    witness = game.player1.summon("MAW_032")
    secret = game.player1.give("MAW_006")
    secret.play()
    game.end_turn()
    minion = game.player2.give(WISP)
    minion.play()
    assert minion in game.player2.field
    assert secret in game.player1.secrets
    witness.destroy()
    countered = game.player2.give(WISP)
    countered.play()
    assert countered.cant_play
    assert secret.zone == Zone.GRAVEYARD


def test_serrated_bone_spike_discount_once_and_expires():
    game = prepare_empty_game()
    target = game.player2.summon(WISP)
    spell = game.player1.give(FIREBALL)
    game.player1.give("REV_939").play(target=target)
    assert spell.cost == 2
    game.player1.give(WISP).play()
    assert spell.cost == 4
    target = game.player2.summon(WISP)
    game.player1.give("REV_939").play(target=target)
    assert spell.cost == 2
    game.end_turn()
    assert spell.cost == 4


def test_barones_vashj_summons_instead_of_transforming():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    vashj = game.player1.summon("REV_925")
    game.player1.give("REV_920").play(target=vashj)
    assert vashj in game.player1.field
    assert len(game.player1.field) == 2
    assert game.player1.field[-1].cost == 6


def test_framester_overloads_on_draw():
    game = prepare_empty_game()
    game.player1.give("MAW_005").play()
    assert game.player2.deck == ["MAW_005t"] * 3
    game.player2.draw()
    assert not game.player2.deck
    assert game.player2.overloaded == 6


def test_stonewright_persists_and_totems_get_discount():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    stonewright = game.player1.give("REV_921")
    stonewright.play()
    stonewright.destroy()
    totem = game.player1.summon("CS2_050")
    assert totem.atk == 3
    assert game.player1.give("REV_838").cost == 9


def test_tome_tampering_preserves_originals_and_sets_cost():
    game = prepare_empty_game()
    game.player1.discard_hand()
    first = game.player1.give(FIREBALL)
    second = game.player1.give("CS2_182")
    game.player1.give("REV_240").play()
    assert not game.player1.hand
    assert first.zone == Zone.REMOVEDFROMGAME and second.zone == Zone.REMOVEDFROMGAME
    assert sorted(c.id for c in game.player1.deck) == sorted([FIREBALL, "CS2_182"])
    game.player1.draw()
    game.player1.draw()
    assert [c.cost for c in game.player1.hand] == [1, 1]


def test_imp_synergies():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    librarian = game.player1.summon("REV_242")
    game.player1.summon(IMP)
    game.player1.summon("REV_244")
    assert len(IMPS.eval(game, librarian)) == 2
    assert librarian.atk == 3
    game.player1.card(WISP, zone=Zone.DECK)
    game.player1.card(WISP, zone=Zone.DECK)
    game.player1.card(WISP, zone=Zone.DECK)
    before = len(game.player1.hand)
    game.player1.give("REV_245").play()
    assert len(game.player1.hand) == before + 3


def test_lady_darkvein_stores_shadow_spell():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    target = game.player2.summon("CS2_182")
    game.player1.give("CS2_057").play(target=target)  # Shadow Bolt
    game.player1.give("REV_373").play()
    shades = game.player1.field.filter(id="REV_373t")
    assert len(shades) == 2
    target = game.player2.summon("CS2_182")
    # Force the stored spell to hit the sole enemy minion rather than a Shade.
    with patch("fireplace.actions.CastSpell.choose_target", return_value=target):
        shades[0].destroy()
    assert target.health == 1


@pytest.mark.parametrize("buffed", [False, True])
def test_remornia_keeps_remaining_health_between_forms(buffed):
    game = prepare_empty_game()
    remornia = game.player1.give("REV_316")
    remornia.play()
    bonus = 2 if buffed else 0
    if buffed:
        remornia.buff(remornia, "REV_835e")
    target = game.player2.summon("CS2_182")
    remornia.attack(target)
    weapon = game.player1.weapon
    assert weapon.id == "REV_316t"
    assert (weapon.atk, weapon.durability) == (4 + bonus, 6 + bonus)
    game.player1.hero.attack(game.player2.hero)
    returned = game.player1.field[0]
    assert returned.id == "REV_316"
    assert (returned.atk, returned.health) == (4 + bonus, 5 + bonus)
    assert game.player1.weapon is None


def test_jailer_aura_persists_and_does_not_prevent_destroy():
    game = prepare_empty_game()
    game.player1.card(FIREBALL, zone=Zone.DECK)
    jailer = game.player1.give("MAW_034")
    jailer.play()
    assert not game.player1.deck
    assert jailer.immune
    jailer.hit(10)
    assert jailer.health == 10
    jailer.destroy()
    minion = game.player1.summon(WISP)
    assert minion.immune
    minion.destroy()
    assert minion.zone == Zone.GRAVEYARD


def test_kaelthas_every_third_minion_resets_each_turn():
    game = prepare_empty_game()
    game.player1.summon("REV_021")
    minion = game.player1.give("CS2_182")
    game.player1.give(WISP).play()
    assert minion.cost == 4
    game.player1.give(WISP).play()
    assert minion.cost == 0
    minion.play()
    assert game.player1.give("CS2_182").cost == 4
    game.end_turn()
    game.end_turn()
    assert game.player1.hand[-1].cost == 4


def test_theotar_swaps_chosen_cards():
    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    own = game.player1.give(FIREBALL)
    enemy = game.player2.give(WISP)
    game.player1.give("REV_238").play()
    game.player1.choice.choose(own)
    game.player1.choice.choose(enemy)
    assert game.player1.hand == [enemy]
    assert game.player2.hand == [own]


def prepare_holmes_game():
    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    game.player2.starting_hand = [game.player2.card(FIREBALL)]
    game.player2.give(WISP)
    game.player2.card(PYROBLAST, zone=Zone.DECK)
    return game


def test_murloc_holmes_three_correct_clues_award_all_copies_together():
    game = prepare_holmes_game()
    game.player1.give("REV_022").play()
    for answer in (FIREBALL, WISP, PYROBLAST):
        assert not game.player1.hand
        choice = game.player1.choice
        assert {card.id for card in choice.cards} == {FIREBALL, WISP, PYROBLAST}
        selected = next(card for card in choice.cards if card.id == answer)
        assert selected.copied_from.controller is game.player2
        assert selected is not selected.copied_from
        choice.choose(selected)
    assert game.player1.choice is None
    assert [card.id for card in game.player1.hand] == [FIREBALL, WISP, PYROBLAST]


def test_kelthuzad_only_explodes_skeletons_that_do_not_fit():
    game = prepare_empty_game()
    kill_friendly(game, "REV_845", 3)
    for _ in range(4):
        game.player1.summon(WISP)
    before = game.player2.hero.health
    game.player1.give("REV_514").play()
    assert len(game.player1.field) == 7
    assert len(game.player1.field.filter(id="REV_845")) == 2
    assert game.player2.hero.health == before - 2


def test_relic_extinction_twice_and_vault_expiry():
    game = prepare_empty_game()
    target = game.player2.summon("CS2_182")
    game.player1.give("REV_834").play()
    assert target.health == 3
    assert game.player1.relic_level == 2
    vault = game.player1.give("REV_942")
    vault.play()
    vault.activate()
    game.end_turn()
    game.end_turn()
    game.player1.give("REV_834").play()
    assert game.player1.relic_level == 3


def test_invitation_courier_only_copies_given_cards():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.player1.summon("REV_377")
    game.player1.give(FIREBALL)
    assert len(game.player1.hand.filter(id=FIREBALL)) == 2
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player1.draw()
    assert len(game.player1.hand.filter(id=FIREBALL)) == 3
    game.player1.give(WISP)
    assert len(game.player1.hand.filter(id=WISP)) == 1


@pytest.mark.parametrize(
    "card_id,picker,options",
    [
        ("REV_002", RandomMinion, ["EX1_563", "EX1_561", "EX1_572"]),
        ("REV_006", RandomWeapon, ["CS2_091", "CS2_112", "CS2_097"]),
    ],
)
@pytest.mark.parametrize("guess_index", [0, 1])
def test_suspicious_minion_opponent_guesses(card_id, picker, options, guess_index):
    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    offered = [game.player1.card(id) for id in options]
    with mock(picker, offered):
        game.player1.give(card_id).play()
    game.player1.choice.choose(offered[0])
    game.end_turn()
    game.player2.choice.choose(offered[guess_index])
    assert game.player1.hand == [options[0]]
    assert game.player2.hand == ([options[0]] if guess_index == 0 else [])


def test_accusations_use_the_accusers_side():
    game = prepare_empty_game()
    enemy = game.player2.summon("CS2_182")
    game.player1.give("MAW_001").play(target=enemy)
    game.player2.hero.hit(1)
    assert enemy in game.player2.field
    game.player1.hero.hit(1)
    assert enemy.zone == Zone.GRAVEYARD
    accused = game.player2.summon("CS2_182")
    game.player1.give("MAW_019").play(target=accused)
    game.player1.summon(WISP).destroy()
    assert accused in game.player2.field
    game.player2.summon(WISP).destroy()
    assert accused.zone == Zone.GRAVEYARD


def test_theft_accusation_requires_a_card_copied_from_opponent():
    game = prepare_empty_game()
    accused = game.player2.summon("CS2_182")
    original = game.player2.give(WISP)
    copied = Copy(original).evaluate(game.player1.hero)[0]
    game.player1.give("MAW_023").play(target=accused)
    game.player1.give(WISP).play()
    assert accused in game.player2.field
    game.player1.give(copied).play()
    assert accused.zone == Zone.GRAVEYARD


def test_habeas_corpses_gives_rush_and_dies_at_end_of_turn():
    game = prepare_empty_game()
    game.player1.summon("REV_952").destroy()
    game.player1.discard_hand()
    game.player1.give("MAW_002").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    revived = game.player1.field[0]
    assert revived.rush
    game.end_turn()
    assert revived.zone == Zone.GRAVEYARD
    assert game.player1.hand == ["CS2_101t", "CS2_101t"]


def test_party_crasher_throws_minion_from_hand_without_battlecry():
    game = prepare_empty_game()
    game.player1.discard_hand()
    thrown = game.player1.give("REV_952")
    target = game.player2.summon("CS2_182")
    game.player1.give("REV_370").play(target=target)
    assert thrown.zone == Zone.GRAVEYARD
    assert target.health == 3
    assert game.player1.hand == ["CS2_101t", "CS2_101t"]


def test_riot_protects_minions_for_one_turn():
    game = prepare_empty_game()
    friendly = game.player1.summon("CS2_182")
    game.player2.summon("EX1_563")  # Malygos, 4/12
    game.player1.give("REV_337").play()
    assert friendly.health == 1
    friendly.hit(10)
    assert friendly.health == 1
    game.end_turn()
    friendly.hit(1)
    assert friendly.zone == Zone.GRAVEYARD


def test_olgra_buffs_then_attacks_all_enemies():
    game = prepare_empty_game()
    friendly = game.player1.summon("CS2_182")
    friendly.hit(1)
    enemy = game.player2.summon(WISP)
    olgra = game.player1.give("REV_934")
    olgra.play()
    assert olgra.atk == 4
    assert enemy.zone == Zone.GRAVEYARD
    assert game.player2.hero.health == 26


def test_steamcleaner_only_preserves_original_deck_entities():
    game = prepare_empty_game()
    original = game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player1.starting_deck = [original]
    generated = game.player1.card(FIREBALL, zone=Zone.DECK)
    foreign = game.player2.card(WISP, zone=Zone.DECK)
    game.player1.give("REV_946").play()
    assert game.player1.deck == [original]
    assert generated.zone == Zone.GRAVEYARD
    assert foreign.zone == Zone.GRAVEYARD


def test_clear_conscience_allows_opposing_battlecries():
    game = prepare_empty_game()
    target = game.player1.summon(WISP)
    game.player1.give("MAW_021").play(target=target)
    assert target in game.player1.give(FIREBALL).targets
    assert target not in game.player2.give(FIREBALL).targets
    assert target in game.player2.give("REV_013t").targets


def test_door_of_shadows_temporary_copy_expires():
    game = prepare_empty_game()
    spell = game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player1.give("REV_938t").play()
    assert len(game.player1.hand.filter(id=FIREBALL)) == 2
    game.end_turn()
    assert game.player1.hand == [spell]


def test_location_durability_cooldown_and_destroy_targeting():
    game = prepare_empty_game()
    location = game.player1.give("REV_990")
    location.play()
    target = game.player2.summon("CS2_182")
    location.use(target=target)
    assert (target.atk, target.health) == (6, 4)
    assert location.durability == 2
    assert not location.is_usable()
    game.end_turn()
    enemy = game.player2.give("REV_023")
    assert location in enemy.targets
    enemy.play(target=location)
    assert location.zone == Zone.GRAVEYARD


def test_private_eye_combo_and_double_cross():
    game = prepare_empty_game()
    game.player1.card("REV_825", zone=Zone.DECK)
    game.player1.card("REV_827", zone=Zone.DECK)
    game.player1.give(WISP).play()
    game.player1.give("REV_826").play()
    assert len(game.player1.secrets) == 2
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.end_turn()
    game.player2.give(PYROBLAST).play(target=game.player1.hero)
    assert len(game.player1.hand.filter(id=FIREBALL)) == 2
    assert len(game.player1.field.filter(id="REV_827t")) == 1


def test_clean_scene_and_sylvanas_infused_effects():
    game = prepare_empty_game()
    target = game.player2.summon("CS2_182")
    game.player1.give("REV_252").play()
    assert target in game.player2.field
    game.player1.give("REV_252t").play()
    assert target.zone == Zone.GRAVEYARD
    game.player1.used_mana = 0
    target = game.player2.summon("CS2_182")
    game.player1.give("MAW_033t").play(target=target)
    assert target in game.player1.field


def test_nathanos_triggers_and_gains_deathrattle_without_drawing_it():
    game = prepare_empty_game()
    corpse = game.player1.summon("REV_952")
    corpse.destroy()
    game.player1.discard_hand()
    nathanos = game.player1.give("MAW_011")
    nathanos.play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert corpse.zone == Zone.GRAVEYARD
    assert game.player1.hand == ["CS2_101t", "CS2_101t"]
    nathanos.destroy()
    assert game.player1.hand == ["CS2_101t"] * 4


def test_deathborne_counts_only_minions_killed_by_its_damage():
    game = prepare_empty_game()
    game.player1.summon(WISP)
    game.player2.summon(WISP)
    survivor = game.player2.summon("CS2_182")
    game.player1.give("REV_840").play()
    assert len(game.player1.field.filter(id="REV_845")) == 2
    assert survivor.health == 3


def test_wild_spirits_only_accelerates_friendly_wildseeds():
    game = prepare_empty_game()
    enemy = game.player2.summon("REV_360t2")
    fox = game.player1.card("REV_360t")
    bear = game.player1.card("REV_360t1")
    with mock(RandomID, [fox, bear]):
        game.player1.give("REV_361").play()
    assert not fox.dormant
    assert bear.dormant_turns == 1
    assert enemy.dormant_turns == 3
    assert len(game.player1.field) == 2
    assert len({card.id for card in game.player1.field}) == 2
    assert all(card.type == CardType.MINION for card in game.player1.field)


def test_conquerors_banner_only_draws_strictly_higher_cards():
    game = prepare_empty_game()
    for _ in range(3):
        game.player1.card(PYROBLAST, zone=Zone.DECK)
        game.player2.card(WISP, zone=Zone.DECK)
    game.player1.give("REV_931").play()
    assert len(game.player1.hand.filter(id=PYROBLAST)) == 3
    assert len(game.player2.deck) == 3


@pytest.mark.parametrize("wrong_stage", [0, 1, 2])
def test_murloc_holmes_wrong_guess_awards_nothing(wrong_stage):
    game = prepare_holmes_game()
    game.player1.give("REV_022").play()
    answers = (FIREBALL, WISP, PYROBLAST)
    for answer in answers[:wrong_stage]:
        choice = game.player1.choice
        choice.choose(next(card for card in choice.cards if card.id == answer))
    choice = game.player1.choice
    choice.choose(
        next(card for card in choice.cards if card.id != answers[wrong_stage])
    )
    assert game.player1.choice is None
    assert not game.player1.hand


def test_location_refreshes_after_two_controller_turns_and_spends_last_charge():
    game = prepare_empty_game()
    location = game.player1.give("REV_602")
    location.play()
    target = game.player2.summon("CS2_182")
    location.use(target=target)
    game.skip_turn()
    assert not location.is_usable()
    game.skip_turn()
    assert location.is_usable()
    location.use(target=target)
    assert location.zone == Zone.GRAVEYARD


def test_collateral_damage_counts_spellpower_once_and_respects_shield():
    game = prepare_empty_game()
    game.player1.summon(KOBOLD_GEOMANCER)
    game.player2.summon("CS2_182")
    shield = game.player2.summon("EX1_008")  # Argent Squire
    game.player1.give("REV_369").play()
    assert shield.health == 1
    assert not shield.divine_shield
    assert game.player2.hero.health == 28


def test_crooked_cook_requires_damage_dealt_by_its_controller():
    game = prepare_empty_game()
    game.player1.summon("REV_016")
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player2.hero.hit(3)  # The enemy damages itself.
    game.end_turn()
    assert not game.player1.hand
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.card(FIREBALL, zone=Zone.DECK)
    before = len(game.player1.hand)
    game.end_turn()
    assert len(game.player1.hand) == before + 1


def test_creepy_painting_copies_buffs_and_restores_health():
    game = prepare_empty_game()
    painting = game.player1.summon("REV_916")
    victim = game.player2.summon("CS2_182")
    victim.buff(victim, "REV_350e")
    victim.destroy()
    copy = painting.morphed
    assert copy in game.player1.field
    assert copy.id == "CS2_182"
    assert (copy.atk, copy.health) == (5, 7)


def test_nightshade_bud_summons_original_without_battlecry():
    game = prepare_empty_game()
    minion = game.player1.card("REV_952", zone=Zone.DECK)
    game.player1.give("REV_311").play(choose="REV_311t2")
    game.player1.choice.choose(minion)
    assert minion in game.player1.field
    assert not game.player1.deck
    assert not game.player1.hand


def test_planted_evidence_discount_expires():
    game = prepare_empty_game()
    spell = game.player1.card(FIREBALL)
    with mock(RandomSpell, [spell]):
        game.player1.give("REV_313").play()
    game.player1.choice.choose(spell)
    assert spell in game.player1.hand
    assert spell.cost == 2
    game.end_turn()
    assert spell.cost == 4


def test_relic_vault_recasts_at_the_improved_level():
    game = prepare_empty_game()
    target = game.player2.summon("EX1_563")
    vault = game.player1.give("REV_942")
    vault.play()
    vault.use()
    game.player1.give("REV_834").play()
    assert target.health == 6  # Two hits for 1, then two hits for 2.
    assert game.player1.relic_level == 3
    game.player1.give("REV_834").play()
    assert game.player1.relic_level == 4


def test_shadow_waltz_and_imp_oster():
    game = prepare_empty_game()
    game.player1.summon(WISP).destroy()
    game.player1.give("REV_372").play()
    assert len(game.player1.field.filter(id="REV_372t")) == 2
    imp = game.player1.summon("REV_244")
    imp.buff(imp, "REV_835e")
    impostor = game.player1.give("MAW_000")
    assert imp in impostor.targets
    assert not any(card.id == "REV_372t" for card in impostor.targets)
    impostor.play(target=imp)
    assert impostor.morphed.id == "REV_244"
    assert (impostor.morphed.atk, impostor.morphed.health) == (5, 5)


def test_all_fel_breaks_loose_only_infuses_from_demons():
    game = prepare_empty_game()
    game.player1.give("MAW_012")
    kill_friendly(game, count=3)
    assert game.player1.hand[-1].id == "MAW_012"
    kill_friendly(game, IMP, 3)
    spell = game.player1.hand[-1]
    assert spell.id == "MAW_012t"
    spell.play()
    assert game.player1.field == [IMP] * 3


def test_life_sentence_removes_without_deathrattle():
    game = prepare_empty_game()
    minion = game.player2.summon("REV_952")
    game.player2.discard_hand()
    game.player1.give("MAW_013").play(target=minion)
    assert minion.zone == Zone.REMOVEDFROMGAME
    assert not game.player2.hand


def test_motion_denied_triggers_on_exactly_third_card():
    game = prepare_empty_game()
    secret = game.player1.give("MAW_010")
    secret.play()
    game.end_turn()
    for _ in range(2):
        game.player2.give(WISP).play()
        assert secret in game.player1.secrets
    game.player2.give(WISP).play()
    assert secret.zone == Zone.GRAVEYARD
    assert game.player2.hero.health == 24


def test_sinful_brand_damages_its_targets_hero():
    game = prepare_empty_game()
    target = game.player2.summon("CS2_182")
    game.player1.give("REV_506").play(target=target)
    target.hit(1)
    assert game.player1.hero.health == 30
    assert game.player2.hero.health == 28


def test_suspicious_guess_resumes_inside_copied_game():
    from copy import deepcopy

    game = prepare_empty_game()
    game.player1.discard_hand()
    game.player2.discard_hand()
    options = [game.player1.card(id) for id in (THE_COIN, FIREBALL, PYROBLAST)]
    with mock(RandomSpell, options):
        game.player1.give("REV_000").play()
    game.player1.choice.choose(options[0])
    game.end_turn()
    copied = deepcopy(game)
    copied.player2.choice.choose(copied.player2.choice.cards[0])
    assert copied.player2.hand == [THE_COIN]
    assert not game.player2.hand
    assert game.player2.choice is not None


@pytest.mark.parametrize(
    "remaining,spent,triggers", [(0, 0, False), (2, 1, False), (2, 2, True)]
)
def test_double_cross_only_triggers_when_positive_spending_exhausts_mana(
    remaining, spent, triggers
):
    game = prepare_empty_game()
    secret = game.player1.give("REV_825")
    secret.play()
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.end_turn()
    game.player2.used_mana = game.player2.max_mana - remaining
    game.cheat_action(game.player2, [SpendMana(game.player2, spent)])
    assert (secret.zone == Zone.GRAVEYARD) == triggers
    assert len(game.player1.hand) == (2 if triggers else 0)


def test_double_cross_triggers_when_hero_power_spends_last_mana():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    secret = game.player1.give("REV_825")
    secret.play()
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.player1.card(FIREBALL, zone=Zone.DECK)
    game.end_turn()
    game.player2.used_mana = game.player2.max_mana - 2
    game.player2.hero.power.use(target=game.player1.hero)
    assert secret.zone == Zone.GRAVEYARD
    assert game.player1.hand == [FIREBALL, FIREBALL]


def test_double_cross_does_not_trigger_for_free_or_health_paid_cards():
    game = prepare_empty_game()
    secret = game.player1.give("REV_825")
    secret.play()
    game.end_turn()
    game.player2.used_mana = game.player2.max_mana
    game.player2.give(WISP).play()
    assert secret in game.player1.secrets
    fireball = game.player2.give(FIREBALL)
    fireball.card_costs_health = True
    fireball.play(target=game.player1.hero)
    assert secret in game.player1.secrets
    assert game.player2.hero.health == 26


def test_draka_dagger_fixed_stats_include_previously_played_cards():
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give(WISP).play()
    game.player1.give("REV_940").play()
    weapon = game.player1.weapon
    assert weapon.id == "REV_940t"
    assert (weapon.atk, weapon.durability) == (3, 3)


def test_sinstone_graveyard_ghost_fixed_stats_include_previously_played_cards():
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    location = game.player1.give("REV_750")
    location.play()
    location.use()
    ghost = game.player1.field.filter(id="REV_750t2")[0]
    assert (ghost.atk, ghost.health) == (3, 3)
    assert ghost.stealthed


def test_meltranix_restricts_opponent_until_their_turn_ends():
    game = prepare_empty_game()
    game.player2.discard_hand()
    own = [game.player1.give(WISP) for _ in range(3)]
    other = [game.player2.give(WISP) for _ in range(3)]
    game.player1.give("MAW_014").play()
    assert not any(card.cant_play for card in own)
    game.end_turn()
    assert not other[0].cant_play
    assert other[1].cant_play
    assert not other[1].is_playable()
    assert not other[2].cant_play
    other[0].play()
    assert not other[1].cant_play  # The next card is now leftmost.
    game.player2.give(WISP)
    assert other[2].cant_play
    game.end_turn()
    assert not any(card.cant_play for card in other)


def test_forensic_duster_only_taxes_opponents_minions_for_one_turn():
    game = prepare_empty_game()
    own = game.player1.give("CS2_182")
    other = game.player2.give("CS2_182")
    spell = game.player2.give(FIREBALL)
    game.player1.give("REV_378").play()
    assert own.cost == 4
    game.end_turn()
    assert other.cost == 5
    assert spell.cost == 4
    assert game.player2.give("CS2_182").cost == 5
    game.end_turn()
    assert other.cost == 4


def test_ashen_elemental_only_damages_opponents_draws_next_turn():
    game = prepare_empty_game()
    for _ in range(5):
        game.player2.card(WISP, zone=Zone.DECK)
    game.player1.give("REV_960").play()
    game.player2.draw()
    assert game.player2.hero.health == 30
    game.end_turn()
    assert game.player2.hero.health == 28
    game.player2.draw()
    assert game.player2.hero.health == 26
    assert game.player1.hero.health == 30
    game.end_turn()
    game.end_turn()
    assert game.player2.hero.health == 26


@pytest.mark.parametrize("copies", [1, 2])
def test_dew_process_draws_extra_cards_for_each_player(copies):
    game = prepare_empty_game()
    for player in game.players:
        player.discard_hand()
        for _ in range(10):
            player.card(WISP, zone=Zone.DECK)
    for _ in range(copies):
        game.player1.give("MAW_024").play()
    game.end_turn()
    assert len(game.player2.hand) == 1 + copies
    game.end_turn()
    assert len(game.player1.hand) == 1 + copies
    game.end_turn()
    assert len(game.player2.hand) == 2 * (1 + copies)


def test_vengeful_visage_preserves_attackers_buffs_and_damage():
    game = prepare_empty_game()
    game.player1.give("REV_516").play()
    game.end_turn()
    attacker = game.player2.summon("CS2_182")
    attacker.buff(attacker, "REV_835e")
    attacker.hit(1)
    attacker.turns_in_play = 1
    attacker.attack(game.player1.hero)
    copy = game.player1.field[0]
    assert (copy.atk, copy.health, copy.max_health) == (6, 6, 7)
    assert game.player2.hero.health == 24


def test_identity_theft_preserves_and_continues_denathrius_infuse():
    game = prepare_empty_game()
    game.player2.discard_hand()
    game.player2.give("REV_906")
    for _ in range(3):
        game.player2.summon(WISP).destroy()
    original = game.player2.hand[0]
    assert original.data_num_2 == 8
    game.player1.give("REV_253").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    copy = game.player1.hand[-1]
    assert copy.data_num_2 == 8
    kill_friendly(game)
    copy = game.player1.hand[-1]
    assert copy.data_num_2 == 9
    assert original.data_num_2 == 8
    game.player1.used_mana = 0
    copy.play()
    assert game.player2.hero.health == 21


def test_identity_theft_preserves_partial_infuse_and_copy_source_after_morph():
    game = prepare_empty_game()
    game.player2.discard_hand()
    original = game.player2.give("REV_956")
    for _ in range(2):
        game.player2.summon(WISP).destroy()
    game.player1.give("REV_253").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    copy = game.player1.hand[-1]
    assert copy.infuse == 2
    kill_friendly(game)
    upgraded = game.player1.hand[-1]
    assert upgraded.id == "REV_956t"
    assert upgraded.copied_from is original
    game.player1.give("REV_246").play()
    assert upgraded.cost == 0


def test_copying_opponents_copy_keeps_the_direct_source_for_visitor_and_harvester():
    game = prepare_empty_game()
    game.player2.discard_hand()
    original = game.player1.give("CS2_182")
    enemy_copy = Copy(original).evaluate(game.player2.hero)[0]
    game.player2.give(enemy_copy)
    game.player1.give("REV_253").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    copy = game.player1.hand[-1]
    assert copy.copied_from is enemy_copy
    game.player1.give("REV_246").play()
    assert copy.cost == 2
    game.player1.give("REV_011").play()
    copy.play()
    assert enemy_copy.controller is game.player1
    assert enemy_copy in game.player1.hand
    assert original in game.player1.hand


def test_visitor_recognizes_copy_after_original_changes_controller():
    game = prepare_empty_game()
    original = game.player2.give("CS2_182")
    copy = Copy(original).evaluate(game.player1.hero)[0]
    game.player1.give(copy)
    game.player1.steal(original)
    game.player1.give("REV_246").play()
    assert copy.cost == 2


@pytest.mark.parametrize("combo", [False, True])
def test_private_eye_only_casts_secrets_that_can_be_added(combo):
    game = prepare_empty_game()
    game.player1.give("REV_827").play()
    duplicates = [game.player1.card("REV_827", zone=Zone.DECK) for _ in range(2)]
    for card_id in ("REV_825", "MAW_018"):
        game.player1.card(card_id, zone=Zone.DECK)
    if not combo:
        # Start a fresh turn so the already active secret does not enable Combo.
        game.end_turn()
        game.end_turn()
    game.player1.give("REV_826").play()
    ids = [card.id for card in game.player1.secrets]
    assert len(ids) == (3 if combo else 2)
    assert len(set(ids)) == len(ids)
    assert all(card.zone == Zone.DECK for card in duplicates)


def test_cast_spell_cannot_add_duplicate_or_sixth_secret():
    game = prepare_empty_game()
    game.player1.give("REV_827").play()
    duplicate = game.player1.card("REV_827", zone=Zone.DECK)
    game.cheat_action(game.player1.hero, [CastSpell(duplicate)])
    assert len(game.player1.secrets) == 1
    assert duplicate.zone == Zone.DECK
    for card_id in ("REV_825", "REV_828", "EX1_287", "EX1_289"):
        game.player1.summon(card_id)
    extra = game.player1.card("MAW_018", zone=Zone.DECK)
    game.cheat_action(game.player1.hero, [CastSpell(extra)])
    assert len(game.player1.secrets) == 5
    assert extra.zone == Zone.DECK


@pytest.mark.parametrize("level", [1, 3, 5])
def test_phantasms_spirits_scale_stats_without_changing_cost(level):
    game = prepare_empty_game()
    game.player1.relic_level = level
    game.player1.give("REV_943").play()
    spirits = game.player1.field.filter(id="REV_943t")
    assert len(spirits) == 2
    assert all(
        (card.atk, card.health, card.cost) == (level, level, 1) for card in spirits
    )
    assert game.player1.relic_level == level + 1


def test_nathanos_discovers_distinct_minions_without_weapons():
    game = prepare_empty_game()
    for _ in range(3):
        game.player1.summon("REV_952").destroy()
    game.player1.summon("REV_012").destroy()
    game.player1.summon("FP1_021").destroy()
    game.player1.give("MAW_011").play()
    options = game.player1.choice.cards
    assert len(options) == 2
    assert {card.id for card in options} == {"REV_952", "REV_012"}


def test_nathanos_does_not_offer_a_dead_weapon_without_dead_minions():
    game = prepare_empty_game()
    game.player1.summon("FP1_021").destroy()
    game.player1.give("MAW_011").play()
    assert game.player1.choice is None


def test_steamcleaner_keeps_a_starting_card_that_infused_in_deck():
    game = prepare_empty_game()
    original = game.player1.card("REV_956", zone=Zone.DECK)
    game.player1.starting_deck = [original]
    game.player1.summon("MAW_031")
    for _ in range(3):
        game.player1.summon(WISP).destroy()
    infused = game.player1.deck[0]
    assert infused.id == "REV_956t"
    game.player1.give("REV_946").play()
    assert infused in game.player1.deck


def test_harvester_steals_original_after_it_infuses():
    game = prepare_empty_game()
    game.player2.discard_hand()
    original = game.player2.give("REV_956")
    game.player1.give("REV_253").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    copy = game.player1.hand[-1]
    for _ in range(3):
        game.player2.summon(WISP).destroy()
    infused = game.player2.hand[0]
    assert infused.id == "REV_956t"
    game.player1.summon("REV_011")
    copy.play()
    assert infused.controller is game.player1


def test_remornia_keeps_its_maximum_health_between_forms():
    game = prepare_empty_game()
    target = game.player2.summon("CS2_182")
    minion = game.player1.give("REV_316")
    minion.play()
    minion.attack(target)
    assert game.player1.weapon.durability == 6
    game.player1.hero.attack(game.player2.hero)
    returned = game.player1.field[0]
    assert returned.health == 5
    assert returned.max_health == 10
    returned.heal(returned, 6)
    assert returned.health == 10


def test_remornia_keeps_charge_enchantment_when_returning():
    game = prepare_empty_game()
    target = game.player2.summon("CS2_182")
    minion = game.player1.give("REV_316")
    minion.play()
    game.cheat_action(minion, [GiveCharge(minion)])
    minion.attack(target)
    game.player1.hero.attack(game.player2.hero)
    returned = game.player1.field[0]
    assert returned.charge


def test_identity_theft_keeps_hand_buffs():
    game = prepare_empty_game()
    game.player2.discard_hand()
    original = game.player2.give("CS2_182")
    original.buff(original, "REV_835e")
    game.player1.give("REV_253").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    copy = game.player1.hand[-1]
    assert (copy.atk, copy.health) == (6, 7)


def test_kelthuzad_does_not_resurrect_skeletons_destroyed_in_deck():
    game = prepare_empty_game()
    skeleton = game.player1.card("REV_845", zone=Zone.DECK)
    game.player1.give("REV_946").play()
    assert skeleton.zone == Zone.GRAVEYARD
    game.player1.used_mana = 0
    game.player1.give("REV_514").play()
    assert not game.player1.field.filter(id="REV_845")


def test_habeas_corpses_does_not_resurrect_destroyed_deck_cards():
    game = prepare_empty_game()
    game.player1.card("CS2_182", zone=Zone.DECK)
    game.player1.give("REV_946").play()
    game.player1.give("MAW_002").play()
    assert game.player1.choice is None


def test_courier_copy_can_be_copied_again_when_given_again():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.player1.discard_hand()
    game.player1.summon("REV_377")
    game.player1.give(FIREBALL)
    copy = game.player1.hand.filter(id=FIREBALL)[-1]
    game.cheat_action(game.player1.hero, [Shuffle(game.player1, copy)])
    game.player1.discard_hand()
    game.player1.draw()
    assert len(game.player1.hand.filter(id=FIREBALL)) == 1
    copy.zone = Zone.SETASIDE
    game.cheat_action(game.player1.hero, [Give(game.player1, copy)])
    assert len(game.player1.hand.filter(id=FIREBALL)) == 2


def test_lady_darkvein_summons_four_shades_with_brann():
    game = prepare_empty_game()
    game.player1.summon("LOE_077")
    game.player1.give("REV_373").play()
    assert len(game.player1.field.filter(id="REV_373t")) == 4


def test_kelthuzad_resurrects_twice_with_brann():
    game = prepare_empty_game()
    game.player1.summon("REV_845").destroy()
    game.player1.summon("LOE_077")
    game.player1.give("REV_514").play()
    assert len(game.player1.field.filter(id="REV_845")) == 2


def test_rafaam_does_not_resurrect_imps_destroyed_in_deck():
    game = prepare_empty_game()
    game.player1.card("EX1_598", zone=Zone.DECK)
    game.player1.give("REV_946").play()
    game.player1.used_mana = 0
    game.player1.give("REV_835").play()
    assert not game.player1.field.filter(id="EX1_598")


@pytest.mark.parametrize("spell", ["MAW_012", "MAW_012t", "REV_835t"])
def test_other_resurrection_effects_ignore_minions_destroyed_in_deck(spell):
    game = prepare_empty_game()
    game.player1.card("EX1_598", zone=Zone.DECK)
    game.player1.give("REV_946").play()
    game.player1.used_mana = 0
    game.player1.give(spell).play()
    assert not game.player1.field.filter(id="EX1_598")


def test_nathanos_does_not_offer_minions_destroyed_in_deck():
    game = prepare_empty_game()
    game.player1.card("EX1_029", zone=Zone.DECK)
    game.player1.give("REV_946").play()
    game.player1.used_mana = 0
    game.player1.give("MAW_011").play()
    assert game.player1.choice is None


def test_two_couriers_each_copy_a_given_foreign_card_once():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.player1.discard_hand()
    game.player1.summon("REV_377")
    game.player1.summon("REV_377")
    game.player1.give(FIREBALL)
    copies = game.player1.hand.filter(id=FIREBALL)
    assert len(copies) == 3


def test_kelthuzad_second_battlecry_rechecks_available_slots():
    game = prepare_empty_game()
    kill_friendly(game, "REV_845", 4)
    game.player1.summon("LOE_077")
    health = game.player2.hero.health
    game.player1.give("REV_514").play()
    assert len(game.player1.field.filter(id="REV_845")) == 5
    assert game.player2.hero.health == health - 6


def test_invitation_courier_ignores_its_own_give():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.player1.discard_hand()
    courier = game.player1.summon("REV_377")
    game.cheat_action(courier, [Give(game.player1, FIREBALL)])
    assert len(game.player1.hand.filter(id=FIREBALL)) == 1


def test_invitation_courier_ignores_cards_given_to_the_opponent():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.player1.discard_hand()
    game.player2.discard_hand()
    game.player1.summon("REV_377")
    game.cheat_action(game.player1.hero, [Give(game.player2, FIREBALL)])
    assert not game.player1.hand
    assert len(game.player2.hand.filter(id=FIREBALL)) == 1


def test_murloc_holmes_shuffles_each_clue_and_tracks_the_copied_answer():
    game = prepare_holmes_game()
    with patch.object(
        game.random, "shuffle", side_effect=lambda cards: cards.reverse()
    ) as shuffle:
        game.player1.give("REV_022").play()
        for answer in (FIREBALL, WISP, PYROBLAST):
            choice = game.player1.choice
            assert choice.cards[-1].id == answer
            choice.choose(choice.cards[-1])
        assert shuffle.call_count == 3
    assert [card.id for card in game.player1.hand] == [FIREBALL, WISP, PYROBLAST]


def test_murloc_holmes_deduplicates_correct_and_wrong_pools_by_id():
    game = prepare_holmes_game()
    game.player2.starting_hand += [game.player2.card(FIREBALL)] * 2
    game.player2.starting_hand.append(game.player2.card("CS2_182"))
    game.player2.give(WISP)
    game.player2.give(FIREBALL)
    game.player2.card(PYROBLAST, zone=Zone.DECK)
    game.player2.card(WISP, zone=Zone.DECK)
    original_choice = game.random.choice
    original_sample = game.random.sample
    with patch.object(game.random, "choice", wraps=original_choice) as choose:
        with patch.object(game.random, "sample", wraps=original_sample) as sample:
            game.player1.give("REV_022").play()
    correct = choose.call_args.args[0]
    wrong = sample.call_args.args[0]
    assert len(correct) == 2
    assert {card.id for card in correct} == {FIREBALL, "CS2_182"}
    assert len(wrong) == 2
    assert {card.id for card in wrong} == {WISP, PYROBLAST}
    assert len({card.id for card in game.player1.choice.cards}) == 3
