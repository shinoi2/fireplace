import pytest

from utils import *


def test_guess_the_weight():
    # Guess More! Right
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card2.put_on_top()
    card1.put_on_top()
    game.player1.give("DMF_075").play()
    assert card1.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert card2.zone == Zone.HAND
    # Guess More! Wrong
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card2.put_on_top()
    card1.put_on_top()
    game.player1.give("DMF_075").play()
    assert card1.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[1])
    assert card2.zone == Zone.DECK
    # Guess Less! Right
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card1.put_on_top()
    card2.put_on_top()
    game.player1.give("DMF_075").play()
    assert card2.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[1])
    assert card1.zone == Zone.HAND
    # Guess Less! Wrong
    game = prepare_empty_game()
    card1 = game.player1.give(WISP)
    card2 = game.player1.give(GOLDSHIRE_FOOTMAN)
    card1.put_on_top()
    card2.put_on_top()
    game.player1.give("DMF_075").play()
    assert card2.zone == Zone.HAND
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert card1.zone == Zone.DECK


def test_horrendous_growth():
    game = prepare_empty_game()
    growth = game.player1.give("DMF_124")
    assert growth.cost == 2
    assert growth.atk == 2
    assert growth.max_health == 2
    game.player1.give("CS2_127").play()
    corrputed = game.player1.hand[0]
    assert corrputed.id == "DMF_124t"
    assert corrputed.atk == 3
    assert corrputed.max_health == 3
    game.player1.give("CS2_127").play()
    corrputed = game.player1.hand[0]
    assert corrputed.atk == 4
    assert corrputed.max_health == 4
    game.player1.give("CS2_127").play()
    corrputed = game.player1.hand[0]
    assert corrputed.atk == 5
    assert corrputed.max_health == 5


def test_cthun_the_shattered():
    game = prepare_game(include=tuple(["DMF_254"] + [WISP] * 29))
    all_card = list(game.player1.deck + game.player1.hand)
    assert "DMF_254" not in all_card
    pieces = ["DMF_254t3", "DMF_254t4", "DMF_254t5", "DMF_254t7"]
    for piece in pieces:
        assert piece in all_card
        card = all_card[all_card.index(piece)]
        card.zone = Zone.HAND
        game.player1.used_mana = 0
        if card == "DMF_254t7":
            card.play(target=game.player1.field[0])
        else:
            card.play()
    assert "DMF_254" in list(game.player1.deck)


def test_illgynoth_lifesteal():
    game = prepare_game()
    game.player1.hero.damage = 15
    assert game.player1.hero.health == 15
    wisp = game.player1.give(WISP).play()
    # Drain Soul deals 3 at patch 21.8 (WP-184; 2 before).
    game.player1.give("ICC_055").play(target=wisp)
    assert game.player1.hero.health == 15 + 3
    assert game.player2.hero.damage == 0
    wisp2 = game.player1.give(WISP).play()
    game.player1.give("DMF_230").play()
    game.player1.give("ICC_055").play(target=wisp2)
    assert game.player1.hero.health == 15 + 3
    assert game.player2.hero.damage == 3


# WP-195 : les cartes de Madness at the Darkmoon Faire relues contre leur texte
# (patch 21.8) et hearthstone.wiki.gg ; le test de chaque réparation a été vu
# rouge sur 6b38f1cd avant de passer.

YETI = "CS2_182"
RIVER_CROCOLISK = "CS2_120"
BLOODFEN_RAPTOR = "CS2_172"
BOULDERFIST_OGRE = "CS2_200"
WAR_GOLEM = "CS2_186"
SENJIN = "CS2_179"
LOOT_HOARDER = "EX1_096"
ARCANE_INTELLECT = "CS2_023"
ICE_BARRIER = "EX1_289"
EXPLOSIVE_TRAP = "EX1_610"
LIGHTNING_BOLT = "EX1_238"
SPECTRAL_SIGHT = "BT_491"
SEARING_TOTEM = "CS2_050"


def _refill(game):
    game.player1.used_mana = 0
    game.player2.used_mana = 0


# Corrupt


def test_corrupt_when_a_card_of_higher_cost_is_played():
    game = prepare_empty_game()
    dirigible = game.player1.give("DMF_073")
    game.player1.give(YETI).play()
    corrupted = game.player1.hand[0]
    assert corrupted.id == "DMF_073t"
    assert corrupted.rush
    assert dirigible.zone != Zone.HAND


def test_corrupt_not_by_a_card_of_equal_cost_nor_by_the_opponent():
    game = prepare_empty_game()
    game.player1.give("DMF_073")
    game.player1.give("EX1_557").play()  # Nat Pagle, 2
    game.player1.give("CS2_122").play()  # Raid Leader, 3
    assert game.player1.hand[0].id == "DMF_073"
    game.end_turn()
    game.player2.give(BOULDERFIST_OGRE).play()
    assert game.player1.hand[0].id == "DMF_073"


def test_corrupt_compares_the_cost_paid():
    # "Corrupt triggers on the current cost of both cards" (the wiki): a
    # Fireball paid 2 under Lunar Eclipse does not corrupt a 2-cost card.
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give("DMF_517")  # Sweet Tooth, 2
    game.player1.give("DMF_057").play(target=game.player1.field[0])
    fireball = game.player1.give(FIREBALL)
    assert fireball.cost == 2
    fireball.play(target=game.player2.hero)
    assert game.player1.hand[0].id == "DMF_517"
    # A Corrupt card made cheaper is corrupted by a card that costs more.
    game.end_turn()
    game.end_turn()
    tooth = game.player1.hand[0]
    game.player1.give(RIVER_CROCOLISK).play()
    assert game.player1.hand[0].id == "DMF_517"
    tooth.buff(tooth, "DMF_054e")  # -2
    assert tooth.cost == 0
    game.player1.give("CS2_168").play()  # Murloc Raider, 1
    assert game.player1.hand[0].id == "DMF_517a"


def test_corrupt_a_reduced_spell_is_corrupted_by_its_own_reduction():
    # Lunar Eclipse makes a Corrupt spell in hand cheaper too: a Fireball paid
    # 2 then corrupts a Nitroboost Poison brought to 0.
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give("YOP_015")
    game.player1.give("DMF_057").play(target=game.player1.field[0])
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert game.player1.hand[0].id == "YOP_015t"


def test_corrupt_keeps_the_enchantments_in_hand():
    game = prepare_empty_game()
    pearltusk = game.player1.give("DMF_080")
    game.player1.give("DMF_531").play()  # Stage Hand: +1/+1
    assert pearltusk.atk == 5
    game.player1.give(BOULDERFIST_OGRE).play()
    corrupted = game.player1.hand[0]
    assert corrupted.id == "DMF_080t"
    assert corrupted.atk == 9
    assert corrupted.max_health == 9


def test_felsteel_executioner_becomes_a_weapon():
    game = prepare_empty_game()
    game.player1.give("DMF_248")
    game.player1.give(YETI).play()
    weapon = game.player1.hand[0]
    assert weapon.id == "DMF_248t"
    assert weapon.type == CardType.WEAPON


def test_ring_toss_corrupted_discovers_and_casts_two_secrets():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("DMF_105")
    game.player1.give(BOULDERFIST_OGRE).play()
    toss = game.player1.hand[0]
    assert toss.id == "DMF_105t"
    _refill(game)
    toss.play()
    assert game.player1.choice
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert game.player1.choice
    # An already active Secret cannot be cast a second time.
    active_ids = {card.id for card in game.player1.secrets}
    game.player1.choice.choose(
        next(card for card in game.player1.choice.cards if card.id not in active_ids)
    )
    assert len(game.player1.secrets) == 2


def test_cascading_disaster_corrupts_twice():
    game = prepare_empty_game()
    disaster = game.player1.give("DMF_117")
    game.player1.give(BOULDERFIST_OGRE).play()
    _refill(game)
    assert game.player1.hand[0].id == "DMF_117t"
    game.player1.give(BOULDERFIST_OGRE).play()
    assert game.player1.hand[0].id == "DMF_117t2"
    game.end_turn()
    for _ in range(4):
        game.player2.give(WISP).play()
    game.end_turn()
    game.player1.hand[0].play()
    assert len(game.player2.field) == 1


# Neutral


def test_darkmoon_statue_does_not_buff_itself():
    game = prepare_empty_game()
    statue = game.player1.give("DMF_082").play()
    wisp = game.player1.give(WISP).play()
    assert statue.atk == 0
    assert wisp.atk == 2


def test_derailed_coaster_counts_only_minions():
    game = prepare_empty_game()
    game.player1.give(WISP)
    game.player1.give(MOONFIRE)
    game.player1.give(FIREBALL)
    game.player1.give("DMF_202").play()
    assert len(game.player1.field) == 2


def test_banana_vendor_bananas_buff_a_minion():
    game = prepare_empty_game()
    game.player1.give("DMF_065").play()
    assert [c.id for c in game.player1.hand] == ["DMF_065t"] * 2
    assert [c.id for c in game.player2.hand if c.id == "DMF_065t"] == ["DMF_065t"] * 2
    banana = game.player1.hand[0]
    assert banana.requires_target()
    wisp = game.player1.give(WISP).play()
    banana.play(target=wisp)
    assert wisp.atk == 2
    assert wisp.max_health == 2


@pytest.mark.skip("crabrider has windfury keyword, not battlecry")
def test_crabrider_windfury_this_turn_only():
    game = prepare_empty_game()
    crab = game.player1.give("YOP_031").play()
    assert crab.windfury
    game.end_turn()
    assert not crab.windfury


def test_darkmoon_rabbit_damages_and_poisons_the_neighbours():
    game = prepare_empty_game()
    game.end_turn()
    left = game.player2.give(BOULDERFIST_OGRE).play()
    _refill(game)
    middle = game.player2.give(YETI).play()
    _refill(game)
    right = game.player2.give(WAR_GOLEM).play()
    game.end_turn()
    rabbit = game.player1.give("DMF_070").play()
    rabbit.attack(middle)
    assert middle.dead
    assert left.dead
    assert right.dead


def test_moonfang_takes_one_damage_at_a_time():
    game = prepare_empty_game()
    moonfang = game.player1.give("YOP_035").play()
    game.player1.give(FIREBALL).play(target=moonfang)
    assert moonfang.damage == 1


def test_deathwarden_stops_every_deathrattle():
    game = prepare_empty_game()
    game.player1.give("YOP_012").play()
    hoarder = game.player1.give(LOOT_HOARDER).play()
    game.end_turn()
    enemy_hoarder = game.player2.give(LOOT_HOARDER).play()
    game.end_turn()
    hand1 = len(game.player1.hand)
    hand2 = len(game.player2.hand)
    game.player1.give(MOONFIRE).play(target=hoarder)
    game.player1.give(MOONFIRE).play(target=enemy_hoarder)
    assert len(game.player1.hand) == hand1
    assert len(game.player2.hand) == hand2


def test_silas_darkmoon_this_way():
    # "This Way": your minions move left, the opponent's right (the board
    # turns clockwise as seen by the player).
    game = prepare_empty_game()
    game.end_turn()
    e1 = game.player2.give(WISP).play()
    e2 = game.player2.give(RIVER_CROCOLISK).play()
    game.end_turn()
    f1 = game.player1.give(WISP).play()
    silas = game.player1.give("DMF_074").play()
    choice = game.player1.choice
    assert [c.id for c in choice.cards] == ["DMF_074a", "DMF_074b"]
    choice.choose(choice.cards[0])
    # The left-most friendly goes to the far left of the opponent's board;
    # the right-most enemy to the far right of ours.
    assert list(game.player2.field) == [f1, e1]
    assert list(game.player1.field) == [silas, e2]
    assert e2.controller is game.player1
    assert not e2.can_attack()


def test_silas_darkmoon_on_full_boards():
    game = prepare_empty_game()
    game.end_turn()
    enemies = [game.player2.give(WISP).play() for _ in range(7)]
    game.end_turn()
    friends = [game.player1.give(WISP).play() for _ in range(6)]
    silas = game.player1.give("DMF_074").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert len(game.player1.field) == 7
    assert len(game.player2.field) == 7
    assert game.player2.field[0] is friends[0]
    assert game.player1.field[-1] is enemies[-1]
    assert not any(m.dead for m in friends + enemies + [silas])


def test_silas_darkmoon_that_way():
    game = prepare_empty_game()
    game.end_turn()
    e1 = game.player2.give(WISP).play()
    e2 = game.player2.give(RIVER_CROCOLISK).play()
    game.end_turn()
    f1 = game.player1.give(WISP).play()
    silas = game.player1.give("DMF_074").play()
    game.player1.choice.choose(game.player1.choice.cards[1])
    # Silas is the right-most friendly minion: he goes to the far right of
    # the opponent's board; their left-most comes to the far left of ours.
    assert list(game.player1.field) == [e1, f1]
    assert list(game.player2.field) == [e2, silas]


# def test_yogg_saron_master_of_fate_needs_ten_spells():
#     game = prepare_empty_game()
#     with mock(WheelOfYogg, "DMF_004t4"):
#         game.end_turn()
#         game.player2.give(WISP).play()
#         game.end_turn()
#         game.player1.give("DMF_004").play()
#         assert game.player1.field.contains("CS2_231") is False
#         for _ in range(10):
#             game.player1.give(MOONFIRE).play(target=game.player2.hero)
#         _refill(game)
#         game.player1.give("DMF_004").play()
#         assert len(game.player2.field) == 0


# def test_wheel_of_yogg_saron_odds():
#     # "Only Rod of Roasting has 5% chance to be cast, while all other spells
#     # have 19% chance" (the wiki).
#     game = prepare_empty_game()
#     counts = {}
#     for _ in range(4000):
#         card = WheelOfYogg().evaluate(game.player1)[0]
#         counts[card] = counts.get(card, 0) + 1
#     assert set(counts) == {"DMF_004t%d" % i for i in range(1, 7)}
#     assert 100 < counts["DMF_004t6"] < 300
#     for i in range(1, 6):
#         assert 600 < counts["DMF_004t%d" % i] < 920


# def test_yogg_saron_curse_of_flesh_fills_both_boards():
#     game = prepare_empty_game()
#     for _ in range(10):
#         game.player1.give(MOONFIRE).play(target=game.player2.hero)
#     with mock(WheelOfYogg, "DMF_004t3"), mock(RandomCardPicker, [WISP]):
#         game.player1.give("DMF_004").play()
#     assert len(game.player1.field) == 7
#     assert len(game.player2.field) == 7
#     for minion in game.player1.field[1:]:
#         assert minion.id == WISP
#         assert minion.rush
#     for minion in game.player2.field:
#         assert minion.id == WISP
#         assert not minion.rush


# def test_yogg_saron_devouring_hunger_feeds_yogg():
#     game = prepare_empty_game()
#     game.end_turn()
#     game.player2.give(YETI).play()
#     game.end_turn()
#     game.player1.give(WISP).play()
#     for _ in range(10):
#         game.player1.give(MOONFIRE).play(target=game.player2.hero)
#     with mock(WheelOfYogg, "DMF_004t5"):
#         yogg = game.player1.give("DMF_004").play()
#     assert len(game.player1.field) == 1
#     assert len(game.player2.field) == 0
#     assert yogg.atk == 7 + 4 + 1
#     assert yogg.health == 5 + 5 + 1


# def test_yogg_saron_hand_of_fate_spells_cost_zero_this_turn_only():
#     game = prepare_empty_game()
#     for _ in range(10):
#         game.player1.give(MOONFIRE).play(target=game.player2.hero)
#     with mock(WheelOfYogg, "DMF_004t2"), mock(RandomCardPicker, [FIREBALL]):
#         game.player1.give("DMF_004").play()
#     assert len(game.player1.hand) == 10
#     assert all(card.cost == 0 for card in game.player1.hand)
#     game.end_turn()
#     assert all(card.cost == 4 for card in game.player1.hand)


def test_yshaarj_corrupted_copies_cost_zero_this_turn_only():
    game = prepare_empty_game()
    game.player1.give("DMF_073")
    game.player1.give(YETI).play()
    game.player1.hand[0].play()
    _refill(game)
    game.player1.give("DMF_188").play()
    copy = game.player1.hand[0]
    assert copy.id == "DMF_073t"
    assert copy.cost == 0
    game.end_turn()
    assert copy.cost == 3


def test_carnival_clown_summons_two_copies():
    game = prepare_empty_game()
    game.player1.give("DMF_163").play()
    assert [m.id for m in game.player1.field] == ["DMF_163"] * 3


def test_carnival_clown_corrupted_fills_the_board():
    game = prepare_empty_game()
    clown = game.player1.give("DMF_163")
    clown.buff(clown, "DMF_054e")  # 9 -> 7
    game.player1.give("EX1_298").play()  # Ragnaros, 8
    clown = game.player1.hand[0]
    assert clown.id == "DMF_163t"
    _refill(game)
    clown.play()
    assert len(game.player1.field) == 7
    assert [m.id for m in game.player1.field].count("DMF_163t") == 6


def test_inconspicuous_rider_casts_a_secret_from_the_deck():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    barrier = game.player1.give(ICE_BARRIER)
    barrier.zone = Zone.DECK
    game.player1.give("DMF_079").play()
    assert barrier in game.player1.secrets
    assert len(game.player1.deck) == 0


# Demon Hunter


def test_felscream_blast_needs_a_minion_and_hits_its_neighbours():
    game = prepare_empty_game()
    game.end_turn()
    w1 = game.player2.give(WISP).play()
    w2 = game.player2.give(RIVER_CROCOLISK).play()
    w3 = game.player2.give(WISP).play()
    game.end_turn()
    game.player1.hero.set_current_health(20)
    blast = game.player1.give("DMF_221")
    assert blast.requires_target()
    assert game.player2.hero not in blast.targets
    blast.play(target=w2)
    assert w1.dead and w3.dead
    assert w2.damage == 1
    assert game.player1.hero.health == 23


def test_redeemed_pariah_grows_after_an_outcast_card():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    pariah = game.player1.give("DMF_222").play()
    game.player1.give(WISP)
    sight = game.player1.give(SPECTRAL_SIGHT)
    game.player1.give(WISP)
    sight.play()  # in the middle: still an Outcast card
    assert pariah.atk == 3
    assert pariah.max_health == 4
    game.end_turn()
    game.player2.give(SPECTRAL_SIGHT).play()
    assert pariah.atk == 3


def test_stiltstepper_only_this_turn():
    game = prepare_empty_game()
    card = game.player1.give(WISP)
    card.zone = Zone.DECK
    game.player1.give("DMF_229").play()
    assert card.zone == Zone.HAND
    card.play()
    assert game.player1.hero.atk == 4
    game.end_turn()
    game.end_turn()
    assert game.player1.hero.atk == 0
    # Drawn now, played next turn: nothing.
    card = game.player1.give(WISP)
    card.zone = Zone.DECK
    game.player1.give("DMF_229").play()
    game.end_turn()
    game.end_turn()
    _refill(game)
    card.play()
    assert game.player1.hero.atk == 0


def test_expendable_performers_summon_seven_more_when_they_all_die():
    game = prepare_empty_game()
    game.player1.give("DMF_224").play()
    assert len(game.player1.field) == 7
    _refill(game)
    game.player1.give("EX1_312").play()  # Twisting Nether
    assert len(game.player1.field) == 7
    for minion in game.player1.field:
        assert minion.id == "BT_036t"
    _refill(game)
    game.player1.give("EX1_312").play()
    assert len(game.player1.field) == 0


def test_expendable_performers_not_if_one_survives():
    game = prepare_empty_game()
    game.player1.give("DMF_224").play()
    for minion in game.player1.field[1:]:
        minion.destroy()
    assert len(game.player1.field) == 1
    # The last one dies later in the turn: all seven died this turn.
    game.player1.give(WISP).play()
    game.player1.field[0].destroy()
    assert [m.id for m in game.player1.field] == [WISP] + ["BT_036t"] * 6


def test_expendable_performers_this_turn_only():
    game = prepare_empty_game()
    game.player1.give("DMF_224").play()
    game.end_turn()
    game.player2.give("EX1_312").play()
    assert len(game.player1.field) == 0


def test_acrobatics_draws_two_more_if_both_are_played_this_turn():
    game = prepare_empty_game()
    for _ in range(4):
        card = game.player1.give(WISP)
        card.zone = Zone.DECK
    game.player1.give("DMF_249").play()
    assert len(game.player1.hand) == 2
    for card in game.player1.hand[:]:
        card.play()
    assert len(game.player1.hand) == 2


def test_acrobatics_not_on_a_later_turn():
    game = prepare_empty_game()
    for _ in range(4):
        card = game.player1.give(WISP)
        card.zone = Zone.DECK
    game.player1.give("DMF_249").play()
    game.end_turn()
    game.end_turn()
    for card in game.player1.hand[:]:
        card.play()
    assert len(game.player1.hand) == 0


def test_throw_glaive_returns_a_temporary_copy_when_it_kills():
    game = prepare_empty_game()
    game.end_turn()
    wisp = game.player2.give(WISP).play()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    game.player1.give("DMF_225").play(target=yeti)
    assert len(game.player1.hand) == 0
    game.player1.give("DMF_225").play(target=wisp)
    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].id == "DMF_225"
    game.end_turn()
    assert len(game.player1.hand) == 0


def test_illidari_studies_discovers_and_reduces():
    # A47: the reduction queued after the Discover in the same tuple was lost.
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    sight = game.player1.give(SPECTRAL_SIGHT)
    base = sight.cost
    game.player1.give("YOP_001").play()
    choice = game.player1.choice
    assert choice
    assert all(c.has_outcast for c in choice.cards)
    picked = choice.cards[0]
    choice.choose(picked)
    assert picked.zone == Zone.HAND
    assert sight.cost == base - 1
    assert len(game.player1.hand) == 2


def test_illidari_studies_reduction_spent_by_the_next_outcast_card():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    sight1 = game.player1.give(SPECTRAL_SIGHT)
    sight2 = game.player1.give(SPECTRAL_SIGHT)
    base = sight1.cost
    game.player1.give("YOP_001").play()
    picked = game.player1.choice.cards[0]
    game.player1.choice.choose(picked)
    game.end_turn()
    game.end_turn()
    assert sight1.cost == base - 1
    sight1.play()
    assert sight2.cost == base


def test_dreadlords_bite_outcast():
    game = prepare_empty_game()
    game.end_turn()
    wisp = game.player2.give(WISP).play()
    game.end_turn()
    game.player1.give(WISP)
    bite = game.player1.give("DMF_227")
    bite.play()
    assert wisp.dead
    assert game.player2.hero.damage == 1


# Druid


def test_lunar_eclipse_reduction_this_turn_only():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    game.player1.give("DMF_057").play(target=wisp)
    fireball = game.player1.give(FIREBALL)
    assert fireball.cost == 2
    game.end_turn()
    game.end_turn()
    assert fireball.cost == 4


def test_solar_eclipse_next_spell_casts_twice():
    game = prepare_empty_game()
    game.player1.give("DMF_058").play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 2
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 3


def test_solar_eclipse_this_turn_only():
    game = prepare_empty_game()
    game.player1.give("DMF_058").play()
    game.end_turn()
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 1


def test_cenarion_ward_summons_a_minion():
    for _ in range(10):
        game = prepare_empty_game()
        game.player1.give("DMF_732").play()
        assert game.player1.hero.armor == 8
        assert len(game.player1.field) >= 1
        assert game.player1.field[0].type == CardType.MINION
        assert game.player1.field[0].cost == 8


def test_faire_arborist_corrupted_does_both():
    game = prepare_empty_game()
    card = game.player1.give(WISP)
    card.zone = Zone.DECK
    game.player1.give("DMF_061")
    game.player1.give(YETI).play()
    arborist = game.player1.hand[0]
    assert arborist.id == "DMF_061t"
    arborist.play()
    assert card.zone == Zone.HAND
    assert len(game.player1.field) == 3


def test_resizing_pouch_discovers_at_the_remaining_mana():
    game = prepare_empty_game()
    game.player1.used_mana = 4
    game.player1.give("YOP_029").play()
    assert game.player1.mana == 5
    for card in game.player1.choice.cards:
        assert card.cost == 5


def test_guidance_both_spells_with_overload():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    game.player1.give("YOP_024").play()
    choice = game.player1.choice
    assert len(choice.cards) == 3
    assert choice.cards[0].id != choice.cards[1].id
    choice.choose(choice.cards[2])
    assert len(game.player1.hand) == 2
    assert game.player1.overloaded == 1


def test_guidance_one_spell_without_overload():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    game.player1.give("YOP_024").play()
    choice = game.player1.choice
    spell = choice.cards[0]
    choice.choose(spell)
    assert list(game.player1.hand) == [spell]


def test_guidance_spells_are_weighted_toward_the_hero_class():
    # D-108, A199 (rule 1236): like a discover, the two spells are of the
    # hero's class or neutral, never another class's.
    for hero in (CardClass.DRUID, CardClass.MAGE):
        for _ in range(40):
            game = prepare_empty_game(hero, hero)
            game.player1.give("YOP_024").play()
            choice = game.player1.choice
            spells = choice.cards[:2]
            assert spells[0].id != spells[1].id
            for spell in spells:
                # `classes` : une carte à deux classes (Adorable Infestation)
                # est des deux.
                assert {hero, CardClass.NEUTRAL} & set(spell.classes), spell.id
    assert game.player1.overloaded == 0


# Hunter


def test_trampling_rhino_excess_damage_hits_the_enemy_hero():
    game = prepare_empty_game()
    game.end_turn()
    wisp = game.player2.give(WISP).play()
    game.end_turn()
    rhino = game.player1.give("DMF_087").play()
    rhino.attack(wisp)
    assert game.player2.hero.damage == 4


def test_maxima_blastenheimer():
    game = prepare_empty_game()
    yeti = game.player1.give(YETI)
    yeti.zone = Zone.DECK
    game.player1.give("DMF_089").play()
    assert game.player2.hero.damage == 4
    assert yeti.dead
    assert len(game.player1.field) == 1


def test_jewel_of_nzoth_summons_deathrattle_minions():
    game = prepare_empty_game()
    hoarder = game.player1.give(LOOT_HOARDER).play()
    yeti = game.player1.give(YETI).play()
    game.player1.give(FIREBALL).play(target=yeti)
    game.player1.give(MOONFIRE).play(target=hoarder)
    _refill(game)
    game.player1.give("DMF_084").play()
    assert len(game.player1.field) >= 1
    for minion in game.player1.field:
        assert minion.id == LOOT_HOARDER


def test_open_the_cages_needs_two_minions():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
    game.player1.give("DMF_123").play()
    game.player1.give(WISP).play()
    game.end_turn()
    game.end_turn()
    assert len(game.player1.field) == 1
    assert len(game.player1.secrets) == 1
    game.player1.give(WISP).play()
    game.player1.give(WISP).play()
    game.end_turn()
    game.end_turn()
    assert len(game.player1.field) == 4
    assert len(game.player1.secrets) == 0


def test_bola_shot_needs_a_minion():
    game = prepare_empty_game()
    bola = game.player1.give("YOP_027")
    assert not bola.is_playable()
    game.end_turn()
    w1 = game.player2.give(WISP).play()
    croc = game.player2.give(RIVER_CROCOLISK).play()
    w3 = game.player2.give(BLOODFEN_RAPTOR).play()
    game.end_turn()
    assert bola.requires_target()
    bola.play(target=croc)
    assert croc.damage == 1
    assert w1.dead and w3.dead


# Mage


def test_firework_elemental_targets_if_possible():
    game = prepare_empty_game()
    elemental = game.player1.give("DMF_101")
    assert elemental.is_playable()
    elemental.play()
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    elemental = game.player1.give("DMF_101")
    assert elemental.requires_target()
    assert game.player2.hero not in elemental.targets
    elemental.play(target=yeti)
    assert yeti.damage == 3


def test_conjure_mana_biscuit_refreshes_two_crystals():
    game = prepare_empty_game()
    game.player1.give("YOP_019").play()
    biscuit = game.player1.hand[0]
    game.player1.used_mana = 10
    biscuit.play()
    assert game.player1.mana == 2
    game.player1.give("YOP_019t").play()
    assert game.player1.mana == 4
    game.player1.used_mana = 0
    game.player1.give("YOP_019t").play()
    assert game.player1.mana == 10


def test_rigged_faire_game_needs_no_damage_during_the_opponents_turn():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    for _ in range(6):
        card = game.player1.give(WISP)
        card.zone = Zone.DECK
    game.player1.give("DMF_107").play()
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    game.end_turn()
    assert len(game.player1.secrets) == 1
    assert len(game.player1.hand) == 1
    game.end_turn()
    game.end_turn()
    assert len(game.player1.secrets) == 0
    assert len(game.player1.hand) == 1 + 1 + 3


# Paladin


def test_carnival_barker_gives_plus_one_plus_two():
    game = prepare_empty_game()
    game.player1.give("DMF_237").play()
    wisp = game.player1.give(WISP).play()
    assert wisp.atk == 2
    assert wisp.max_health == 3


def test_oh_my_yogg_counters_and_casts_another():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    game.player1.give("DMF_236").play()
    game.end_turn()
    for player in game.players:
        for _ in range(3):
            card = player.give(WISP)
            card.zone = Zone.DECK
    hand1 = len(game.player1.hand)
    hand2 = len(game.player2.hand)
    fireball = game.player2.give(FIREBALL)
    with mock(RandomCardPicker, [ARCANE_INTELLECT]):
        fireball.play(target=game.player1.hero)
    assert len(game.player1.secrets) == 0
    assert fireball.cant_play
    assert game.player1.hero.damage == 0
    # The opponent casts it: the opponent draws.
    assert len(game.player2.hand) == hand2 + 2
    assert len(game.player1.hand) == hand1


# Priest


def test_dark_inquisitor_xanesh_reduces_corrupt_cards_in_hand_and_deck():
    game = prepare_empty_game()
    in_hand = game.player1.give("DMF_073")
    in_deck = game.player1.give("DMF_080")
    in_deck.zone = Zone.DECK
    game.player1.give("YOP_007").play()
    # Xanesh (5) corrupts the Dirigible first, then reduces the Corrupted one.
    corrupted = game.player1.hand[0]
    assert corrupted.id == "DMF_073t"
    assert corrupted.cost == 1
    assert in_deck.cost == 3


def test_lightsteed_heal_gives_two_health():
    game = prepare_empty_game()
    game.player1.give("YOP_008").play()
    yeti = game.player1.give(YETI).play()
    game.player1.give(MOONFIRE).play(target=yeti)
    game.player1.give(CIRCLE_OF_HEALING).play()
    assert yeti.max_health == 7
    assert yeti.health == 7


def test_palm_reading_reduces_the_discovered_spell():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    fireball = game.player1.give(FIREBALL)
    with mock(RandomCardPicker, [FIREBALL, "CS2_024", ARCANE_INTELLECT]):
        game.player1.give("DMF_187").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert fireball.cost == 3
    picked = game.player1.hand[1]
    assert picked is not fireball
    assert picked.cost == picked.data.cost - 1


# Rogue


def test_tenwu_costs_one_this_turn_only():
    game = prepare_empty_game()
    yeti = game.player1.give(YETI).play()
    game.player1.give("DMF_071").play(target=yeti)
    assert yeti.zone == Zone.HAND
    assert yeti.cost == 1
    game.end_turn()
    assert yeti.cost == 4


def test_prize_plunderer_counts_the_other_cards():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    game.player1.give(WISP).play()
    game.player1.give(WISP).play()
    game.player1.give("DMF_519").play(target=yeti)
    assert yeti.damage == 2


def test_grand_empress_shekzara_draws_all_copies():
    game = prepare_empty_game()
    for _ in range(2):
        card = game.player1.give(YETI)
        card.zone = Zone.DECK
    for _ in range(3):
        card = game.player1.give(WISP)
        card.zone = Zone.DECK
    game.player1.give("DMF_516").play()
    choice = game.player1.choice
    ids = [c.id for c in choice.cards]
    assert sorted(ids) == sorted(set(ids))
    yeti = next(c for c in choice.cards if c.id == YETI)
    choice.choose(yeti)
    assert [c.id for c in game.player1.hand] == [YETI, YETI]
    assert len(game.player1.deck) == 3


def test_sparkjoy_cheat_casts_the_secret_from_hand():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    card = game.player1.give(WISP)
    card.zone = Zone.DECK
    trap = game.player1.give(EXPLOSIVE_TRAP)
    game.player1.give("YOP_016").play()
    assert trap in game.player1.secrets
    assert card.zone == Zone.HAND
    assert trap not in game.player1.hand


# Shaman


def test_grand_totem_eysor_buffs_totems_on_the_battlefield():
    game = prepare_empty_game()
    eysor = game.player1.give("DMF_709").play()
    totem = game.player1.give(SEARING_TOTEM).play()
    in_hand = game.player1.give(SEARING_TOTEM)
    game.end_turn()
    assert totem.atk == 2
    assert in_hand.atk == 2
    assert eysor.atk == 0


def test_stormstrike_needs_a_minion():
    game = prepare_empty_game()
    strike = game.player1.give("DMF_702")
    assert not strike.is_playable()
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    assert strike.requires_target()
    strike.play(target=yeti)
    assert yeti.damage == 3
    assert game.player1.hero.atk == 3
    game.end_turn()
    assert game.player1.hero.atk == 0


def test_landslide_counts_the_overload_owed():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    game.player1.give(LIGHTNING_BOLT).play(target=game.player2.hero)
    assert game.player1.overloaded == 1
    game.player1.give("YOP_023").play()
    assert yeti.damage == 2


# Warlock


def test_deck_of_chaos_swaps_cost_and_attack():
    game = prepare_empty_game()
    ogre = game.player1.give(BOULDERFIST_OGRE)
    ogre.zone = Zone.DECK
    game.player1.give("DMF_534").play()
    assert ogre.cost == 6
    assert ogre.atk == 6
    croc = game.player1.give(WISP)
    croc.zone = Zone.DECK
    game.player1.give("DMF_534").play()
    assert croc.cost == 1
    assert croc.atk == 0


# Warrior


def test_sword_eater_equips_a_sword():
    game = prepare_empty_game()
    game.player1.give("DMF_521").play()
    assert game.player1.weapon.id == "DMF_521t"
    assert game.player1.hero.atk == 3


# Second pass: cards read as right, played once to be sure.


def test_gyreworm_after_an_elemental_last_turn():
    game = prepare_empty_game()
    worm = game.player1.give("DMF_062")
    assert not worm.requires_target()
    game.player1.give("DMF_100t").play()  # Sugar Elemental
    game.end_turn()
    game.end_turn()
    assert worm.requires_target()
    worm.play(target=game.player2.hero)
    assert game.player2.hero.damage == 3


def test_nzoth_god_of_the_deep_one_of_each_type():
    game = prepare_empty_game()
    beasts = [game.player1.give(BLOODFEN_RAPTOR).play() for _ in range(2)]
    murloc = game.player1.give("CS2_168").play()
    wisp = game.player1.give(WISP).play()
    for minion in beasts + [murloc, wisp]:
        minion.destroy()
    _refill(game)
    game.player1.give("DMF_002").play()
    ids = sorted(m.id for m in game.player1.field[1:])
    assert ids == sorted([BLOODFEN_RAPTOR, "CS2_168"])


def test_keywarden_ivory_spellburst_gives_another_copy():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("YOP_018").play()
    choice = game.player1.choice
    picked = choice.cards[0]
    assert len(choice.cards) == 3
    assert all(len(c.classes) == 2 for c in choice.cards)
    assert all(c.type == CardType.SPELL for c in choice.cards)
    choice.choose(picked)
    assert [c.id for c in game.player1.hand] == [picked.id]
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert [c.id for c in game.player1.hand] == [picked.id, picked.id]
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.hand) == 2


def test_imprisoned_phoenix_spell_damage_once_awake():
    game = prepare_empty_game()
    phoenix = game.player1.give("YOP_021").play()
    assert phoenix.dormant
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 1
    for _ in range(2):
        game.end_turn()
        game.end_turn()
    assert not phoenix.dormant
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 1 + 3


def test_imprisoned_celestial_spellburst_once_awake():
    game = prepare_empty_game()
    celestial = game.player1.give("YOP_010").play()
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert not wisp.divine_shield
    for _ in range(2):
        game.end_turn()
        game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert wisp.divine_shield
    assert celestial.divine_shield


def test_game_master_first_secret_each_turn_costs_one():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("DMF_102").play()
    barrier = game.player1.give(ICE_BARRIER)
    entity = game.player1.give("EX1_294")  # Mirror Entity
    assert barrier.cost == 1 and entity.cost == 1
    barrier.play()
    assert entity.cost == 3
    game.end_turn()
    game.end_turn()
    assert entity.cost == 1


def test_sayge_draws_one_more_per_triggered_secret():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    for _ in range(5):
        card = game.player1.give(WISP)
        card.zone = Zone.DECK
    game.player1.give(ICE_BARRIER).play()
    game.end_turn()
    game.player2.give(WISP).play()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    (
        game.player2.field[0].attack(game.player1.hero)
        if game.player2.field[0].can_attack()
        else None
    )
    game.end_turn()
    triggered = 0 if game.player1.secrets else 1
    hand = len(game.player1.hand)
    game.player1.give("DMF_109").play()
    assert len(game.player1.hand) == hand + 1 + triggered


def test_grand_finale_repeats_per_elemental_last_turn():
    game = prepare_empty_game()
    game.player1.give("DMF_100t").play()
    game.player1.give("DMF_100t").play()
    game.end_turn()
    game.end_turn()
    game.player1.give("DMF_104").play()
    assert [m.id for m in game.player1.field[2:]] == ["DMF_104t"] * 3


def test_deck_of_lunacy_keeps_the_cost():
    game = prepare_empty_game()
    bolt = game.player1.give(MOONFIRE)
    bolt.zone = Zone.DECK
    game.player1.give("DMF_108").play()
    spell = game.player1.deck[0]
    assert spell.type == CardType.SPELL
    assert spell.data.cost == 3
    assert spell.cost == 0


def test_petting_zoo_one_more_per_secret():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
    game.player1.give(EXPLOSIVE_TRAP).play()
    game.player1.give("EX1_609").play()  # Snipe
    game.player1.give("DMF_086").play()
    assert [m.id for m in game.player1.field] == ["DMF_086e"] * 3


def test_rinlings_rifle_discovers_and_casts_a_secret():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
    game.player1.give("DMF_088").play()
    game.player1.hero.attack(game.player2.hero)
    choice = game.player1.choice
    assert choice
    picked = choice.cards[0]
    choice.choose(picked)
    assert [s.id for s in game.player1.secrets] == [picked.id]


def test_shadow_clone_copies_the_attacker_with_stealth():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("DMF_513").play()
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    game.end_turn()
    yeti.attack(game.player1.hero)
    assert [m.id for m in game.player1.field] == [YETI]
    assert game.player1.field[0].stealthed


def test_ticket_master_tickets_summon_a_bear_when_drawn():
    game = prepare_empty_game()
    master = game.player1.give("DMF_514").play()
    master.destroy()
    assert [c.id for c in game.player1.deck] == ["DMF_514t"] * 3
    game.end_turn()
    game.end_turn()
    # A Ticket cast when drawn draws the next card: the three in a row.
    assert [m.id for m in game.player1.field] == ["DMF_514t2"] * 3
    assert len(game.player1.deck) == 0


def test_shenanigans_second_draw_becomes_a_banana():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("YOP_017").play()
    game.end_turn()
    for _ in range(3):
        card = game.player2.give(WISP)
        card.zone = Zone.DECK
    game.player2.give(ARCANE_INTELLECT).play()
    ids = [c.id for c in game.player2.hand]
    assert ids.count(WISP) == 1
    assert len(game.player1.secrets) == 0


def test_malevolent_strike_cheaper_per_card_that_did_not_start_in_the_deck():
    game = prepare_empty_game()
    strike = game.player1.give("DMF_518")
    assert strike.cost == 5
    game.player1.give("DMF_514").play().destroy()  # three Tickets
    assert strike.cost == 2


def test_ghuun_draws_cost_health():
    game = prepare_empty_game()
    for _ in range(2):
        card = game.player1.give(YETI)
        card.zone = Zone.DECK
    game.player1.give("DMF_056").play()
    game.player1.used_mana = 10
    yeti = game.player1.hand[0]
    assert yeti.is_playable()
    yeti.play()
    assert game.player1.hero.damage == 4


def test_the_nameless_one_becomes_a_four_four_copy_and_silences():
    game = prepare_empty_game()
    game.end_turn()
    golem = game.player2.give(WAR_GOLEM).play()
    game.end_turn()
    one = game.player1.give("DMF_116").play(target=golem)
    nameless = game.player1.field[0]
    assert nameless.id == WAR_GOLEM
    assert nameless.atk == 4 and nameless.max_health == 4
    assert golem.silenced


def test_hysteria_attacks_until_it_dies():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    w1 = game.player2.give(WISP).play()
    game.end_turn()
    croc = game.player1.give(RIVER_CROCOLISK).play()
    game.player1.give("YOP_006").play(target=yeti)
    assert w1.dead and croc.dead
    assert yeti.damage == 1 + 2
    assert not yeti.dead


def test_fortune_teller_grows_per_spell_in_hand():
    game = prepare_empty_game()
    game.player1.give(MOONFIRE)
    game.player1.give(FIREBALL)
    game.player1.give(WISP)
    teller = game.player1.give("DMF_121").play()
    assert teller.atk == 5 and teller.max_health == 5


def test_rally_resurrects_one_of_each_cost():
    game = prepare_empty_game()
    for card in (WISP, "CS2_168", RIVER_CROCOLISK, "CS2_122"):
        game.player1.give(card).play().destroy()
    _refill(game)
    game.player1.give("YOP_009").play()
    costs = sorted(m.cost for m in game.player1.field)
    assert costs == [1, 2, 3]


def test_barricade_two_guards_if_alone():
    game = prepare_empty_game()
    game.player1.give("YOP_005").play()
    assert [m.id for m in game.player1.field] == ["YOP_005t"] * 2
    game.player1.give("YOP_005").play()
    assert len(game.player1.field) == 3


def test_high_exarch_yrel_without_neutral_cards():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
    card = game.player1.give("CS2_087")  # Blessing of Might
    card.zone = Zone.DECK
    yrel = game.player1.give("DMF_241").play()
    assert yrel.rush and yrel.lifesteal and yrel.taunt and yrel.divine_shield
    # A dual-class card is not a Neutral card.
    card = game.player1.give("YOP_009")  # Rally!, paladin and priest
    card.zone = Zone.DECK
    _refill(game)
    yrel = game.player1.give("DMF_241").play()
    assert yrel.taunt
    card = game.player1.give(WISP)
    card.zone = Zone.DECK
    _refill(game)
    yrel = game.player1.give("DMF_241").play()
    assert not yrel.taunt


def test_lothraxion_and_balloon_merchant():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
    game.player1.give("DMF_240").play()
    game.player1.give("DMF_244").play()
    recruits = game.player1.field[1:]
    assert all(r.divine_shield for r in recruits)
    _refill(game)
    game.player1.give("DMF_235").play()
    assert all(r.atk == 2 for r in recruits)


def test_inara_stormcrash_on_your_turn():
    game = prepare_empty_game()
    game.player1.give("DMF_708").play()
    assert game.player1.hero.atk == 2
    assert game.player1.hero.windfury
    game.end_turn()
    assert game.player1.hero.atk == 0


def test_magicfin_after_a_friendly_murloc_dies():
    game = prepare_empty_game()
    game.player1.give("DMF_707").play()
    murloc = game.player1.give("CS2_168").play()
    murloc.destroy()
    assert len(game.player1.hand) == 1
    card = game.player1.hand[0]
    assert card.type == CardType.MINION
    assert card.rarity == Rarity.LEGENDARY


def test_revenant_rascal_destroys_a_crystal_for_each_player():
    game = prepare_empty_game()
    game.player1.max_mana = 5
    game.player2.max_mana = 5
    game.player1.give("DMF_115").play()
    assert game.player1.max_mana == 4
    assert game.player2.max_mana == 4
    # An empty crystal first: 5 - 3 paid = 2 left, still 2 (the wiki, Mana).
    assert game.player1.mana == 2
    assert game.player2.mana == 4


def test_free_admission_reduces_two_demons():
    game = prepare_empty_game()
    for _ in range(2):
        card = game.player1.give("CS2_065")  # Voidwalker
        card.zone = Zone.DECK
    game.player1.give("DMF_113").play()
    assert [c.cost for c in game.player1.hand] == [0, 0]


def test_tickatus_corrupted_removes_from_the_opponents_deck():
    game = prepare_empty_game()
    for _ in range(6):
        card = game.player2.give(WISP)
        card.zone = Zone.DECK
    game.player1.give("DMF_118")
    game.player1.give(WAR_GOLEM).play()
    _refill(game)
    game.player1.hand[0].play()
    assert len(game.player2.deck) == 1


def test_wicked_whispers_discards_the_lowest_cost():
    game = prepare_empty_game()
    game.player1.give(FIREBALL)
    game.player1.give(WISP)
    yeti = game.player1.give(YETI).play()
    game.player1.give("DMF_119").play()
    assert [c.id for c in game.player1.hand] == [FIREBALL]
    assert yeti.atk == 5


def test_tent_trasher_cheaper_per_minion_type():
    game = prepare_empty_game()
    trasher = game.player1.give("DMF_528")
    game.player1.give(BLOODFEN_RAPTOR).play()
    game.player1.give(BLOODFEN_RAPTOR).play()
    game.player1.give("CS2_168").play()
    game.player1.give(WISP).play()
    assert trasher.cost == 5 - 2


def test_etc_after_a_rush_minion_attacks():
    game = prepare_empty_game()
    game.player1.give("DMF_529").play()
    car = game.player1.give("DMF_523").play()
    game.end_turn()
    wisp = game.player2.give(WISP).play()
    game.end_turn()
    car.attack(wisp)
    assert game.player2.hero.damage == 2


def test_spiked_wheel_and_ironclad_with_armor():
    game = prepare_empty_game()
    wheel = game.player1.give("YOP_013").play()
    assert game.player1.hero.atk == 0
    game.player1.give("YOP_032").play()  # Armor Vendor: 4 Armor to each hero
    assert game.player1.hero.atk == 3
    clad = game.player1.give("YOP_014").play()
    assert clad.atk == 4


def test_ringmasters_baton_buffs_a_mech_dragon_and_pirate():
    game = prepare_empty_game()
    game.player1.give("DMF_524").play()
    mech = game.player1.give(MECH)
    pirate = game.player1.give("NEW1_018")
    wisp = game.player1.give(WISP)
    game.player1.hero.attack(game.player2.hero)
    assert mech.atk == mech.data.atk + 1
    assert pirate.atk == pirate.data.atk + 1
    assert wisp.atk == 1


def test_stage_dive_corrupted_buffs_the_rush_minion():
    game = prepare_empty_game()
    car = game.player1.give("DMF_523")
    car.zone = Zone.DECK
    game.player1.give("DMF_526")
    game.player1.give(RIVER_CROCOLISK).play()
    dive = game.player1.hand[0]
    assert dive.id == "DMF_526a"
    dive.play()
    assert car.zone == Zone.HAND
    assert car.atk == 3 and car.max_health == 4


def test_redscale_dragontamer_draws_a_dragon():
    game = prepare_empty_game()
    drake = game.player1.give("EX1_284")  # Azure Drake
    drake.zone = Zone.DECK
    game.player1.give("DMF_194").play().destroy()
    assert drake.zone == Zone.HAND


def test_snack_run_heals_by_the_cost():
    game = prepare_empty_game()
    game.player1.hero.set_current_health(10)
    game.player1.give("DMF_195").play()
    # A ranked spell (Barrens) changes on reaching the hand: pick another.
    choice = game.player1.choice
    picked = next(
        (c for c in choice.cards if "Rank" not in c.data.name), choice.cards[0]
    )
    cost = picked.cost
    choice.choose(picked)
    assert game.player1.hero.health == min(30, 10 + cost)


def test_keywords_the_data_forgot():
    game = prepare_empty_game()
    gryphon = game.player1.give("DMF_064").play()
    performer = game.player1.give("DMF_223").play()
    assert gryphon.divine_shield
    assert performer.rush
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    _refill(game)
    ilgynoth = game.player1.give("DMF_230").play()
    game.player1.hero.set_current_health(20)
    game.end_turn()
    game.end_turn()
    ilgynoth.attack(yeti)
    # Its own Lifesteal damages the enemy hero instead of healing.
    assert game.player1.hero.health == 20
    assert game.player2.hero.damage == ilgynoth.atk


def test_mistrunner_gives_three_three():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    game.player1.give("YOP_022").play(target=wisp)
    assert wisp.atk == 4 and wisp.max_health == 4
    assert game.player1.overloaded == 1


def test_deathmatch_pavilion_two_if_the_hero_attacked():
    game = prepare_empty_game()
    game.player1.give("DMF_706").play()
    assert len(game.player1.field) == 1
    game.player1.give("DMF_705").play()  # Whack-A-Gnoll Hammer
    game.player1.hero.attack(game.player2.hero)
    assert game.player1.field[0].atk == 4
    game.player1.give("DMF_706").play()
    assert len(game.player1.field) == 3


def test_foxy_fraud_next_combo_card_this_turn():
    game = prepare_empty_game()
    game.player1.give("DMF_511").play()
    agent = game.player1.give("EX1_134")  # SI:7 Agent
    assert agent.cost == agent.data.cost - 2
    game.end_turn()
    assert agent.cost == agent.data.cost


def test_cloak_of_shadows_for_one_turn():
    game = prepare_empty_game()
    game.player1.give("DMF_512").play()
    assert game.player1.hero.stealthed
    game.end_turn()
    assert game.player1.hero.stealthed
    game.end_turn()
    assert not game.player1.hero.stealthed


def test_mana_ri_mosher_this_turn():
    game = prepare_empty_game()
    void = game.player1.give("CS2_065").play()
    game.player1.give("DMF_111").play(target=void)
    assert void.atk == 4 and void.lifesteal
    game.end_turn()
    assert void.atk == 1 and not void.lifesteal


def test_luckysoul_hoarder_corrupted_draws():
    game = prepare_empty_game()
    game.player1.give("YOP_003")
    game.player1.give(YETI).play()
    hoarder = game.player1.hand[0]
    assert hoarder.id == "YOP_003t"
    game.player1.hero.set_current_health(20)
    hoarder.play()
    # It draws a Soul Fragment, which is cast and draws the other one.
    assert len(game.player1.hand) == 0
    assert len(game.player1.deck) == 0
    assert game.player1.hero.health == 24


def test_zai_copies_both_ends_of_the_hand():
    game = prepare_empty_game()
    game.player1.give(WISP)
    game.player1.give(MOONFIRE)
    game.player1.give(FIREBALL)
    game.player1.give("DMF_231").play()
    # Each copy to the left of the card it copies (the wiki).
    assert [c.id for c in game.player1.hand] == [
        WISP,
        WISP,
        MOONFIRE,
        FIREBALL,
        FIREBALL,
    ]
    assert game.player1.hand[0] is not game.player1.hand[1]


def test_bladed_lady_costs_one_with_six_attack():
    game = prepare_empty_game()
    lady = game.player1.give("DMF_226")
    assert lady.cost == 6
    game.player1.give("DMF_219").play()  # +4
    game.player1.give("DMF_730").play()  # +4
    assert lady.cost == 1


def test_felsaber_attacks_only_after_the_hero():
    game = prepare_empty_game()
    saber = game.player1.give("YOP_002").play()
    game.end_turn()
    game.end_turn()
    assert not saber.can_attack()
    game.player1.give("DMF_219").play()
    game.player1.hero.attack(game.player2.hero)
    assert saber.can_attack()


def test_line_hopper_outcast_cards_cost_less():
    game = prepare_empty_game()
    sight = game.player1.give(SPECTRAL_SIGHT)
    game.player1.give("DMF_217").play()
    assert sight.cost == sight.data.cost - 1


def test_umbral_owl_cheaper_per_spell_cast():
    game = prepare_empty_game()
    owl = game.player1.give("DMF_060")
    for _ in range(3):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert owl.cost == 4


def test_greybough_gives_its_deathrattle():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    grey = game.player1.give("DMF_734").play()
    grey.destroy()
    wisp.destroy()
    assert [m.id for m in game.player1.field] == ["DMF_734"]


def test_moontouched_amulet_corrupted_gains_armor():
    game = prepare_empty_game()
    game.player1.give("DMF_730")
    game.player1.give(YETI).play()
    amulet = game.player1.hand[0]
    assert amulet.id == "DMF_730t"
    amulet.play()
    assert game.player1.hero.atk == 4
    assert game.player1.hero.armor == 6
    game.end_turn()
    assert game.player1.hero.atk == 0


def test_cthun_the_shattered_battlecry_deals_thirty():
    game = prepare_empty_game()
    game.player2.hero.armor = 10
    game.player1.give("DMF_254").play()
    assert game.player2.hero.armor == 0
    assert game.player2.hero.damage == 20


def test_runaway_blackwing_at_the_end_of_your_turn():
    game = prepare_empty_game()
    game.end_turn()
    yeti = game.player2.give(YETI).play()
    game.end_turn()
    game.player1.give("YOP_034").play()
    game.end_turn()
    assert yeti.dead


def test_circus_medic_heals_or_corrupted_deals_four():
    game = prepare_empty_game()
    game.player1.give("DMF_174")
    game.player1.give(BOULDERFIST_OGRE).play()
    medic = game.player1.hand[0]
    assert medic.id == "DMF_174t"
    _refill(game)
    medic.play(target=game.player2.hero)
    assert game.player2.hero.damage == 4


def test_prize_vendor_and_knife_vendor():
    game = prepare_empty_game()
    for player in game.players:
        card = player.give(WISP)
        card.zone = Zone.DECK
    game.player1.give("DMF_067").play()
    assert len(game.player1.hand) == 1
    assert WISP in [c.id for c in game.player2.hand]
    game.player1.give("DMF_066").play()
    assert game.player1.hero.damage == 4
    assert game.player2.hero.damage == 4
