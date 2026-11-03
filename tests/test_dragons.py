from utils import *


def test_embiggen():
    game = prepare_empty_game()
    cards = []
    for i in range(1, 11):
        id = f"CFM_712_t{i:02d}"
        card = game.player1.give(id)
        cards.append(card)
        card.shuffle_into_deck()
    game.player1.give("DRG_315").play()
    for i in range(1, 11):
        card = cards[i - 1]
        assert card.atk == i + 2
        assert card.health == i + 2
        assert card.cost == min(i + 1, 10)


def test_strength_in_numbers():
    game = prepare_game()
    sidequest = game.player1.give("DRG_051").play()
    assert sidequest.progress == 0
    assert sidequest.zone == Zone.SECRET
    game.player1.give(THE_COIN).play()
    for i in range(4):
        game.player1.give(MECH).play()
        assert sidequest.progress == (i + 1) * 2
    game.player1.give(MECH).play()
    assert sidequest.progress == 0
    assert sidequest.zone == Zone.GRAVEYARD


def test_dwarven_sharpshooter():
    game = prepare_game(CardClass.HUNTER, CardClass.HUNTER)
    heropower = game.player1.hero.power
    assert not heropower.requires_target()

    sharpshooter = game.player1.give("DRG_253").play()
    assert heropower.requires_target()
    play_targets = heropower.play_targets
    assert len(play_targets) == 2
    assert game.player1.hero not in play_targets
    assert game.player2.hero in play_targets
    assert sharpshooter in play_targets

    sharpshooter.destroy()
    assert not heropower.requires_target()


def test_rolling_fireball():
    game = prepare_game()

    wisps = [game.player1.give(WISP).play() for i in range(7)]
    assert len(game.player1.field) == 7
    game.player1.give("DRG_321").play(target=wisps[0])
    assert len(game.player1.field) == 0

    game.skip_turn()
    wisps = [game.player1.give(WISP).play() for i in range(7)]
    assert len(game.player1.field) == 7
    game.player1.give("DRG_321").play(target=wisps[3])
    assert len(game.player1.field) == 3
    for i in range(3):
        game.player1.field[0].destroy()

    game.skip_turn()
    wisps = [game.player1.give(WISP).play() for i in range(7)]
    assert len(game.player1.field) == 7
    game.player1.give("DRG_321").play(target=wisps[6])
    assert len(game.player1.field) == 0


def test_elemental_allies():
    game = prepare_empty_game()
    allies = game.player1.give("DRG_324").play()
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 1
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 1
    game.skip_turn()
    assert allies.progress == 1
    game.skip_turn()
    assert allies.progress == 0
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 1
    game.skip_turn()
    assert allies.progress == 1
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 0
    assert allies.zone == Zone.GRAVEYARD


def test_sanctuary():
    game = prepare_game()
    sanctuary = game.player1.give("DRG_258").play()
    assert sanctuary.progress == 0
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    game.end_turn()
    assert sanctuary.progress == 0
    game.skip_turn()
    assert sanctuary.progress == 0
    assert sanctuary.zone == Zone.GRAVEYARD
    assert game.player1.field[0] == "DRG_258t"


def test_envoy_of_lazul():
    for _ in range(10):
        game = prepare_game()
        game.player1.give("DRG_306").play()
        choice = game.player1.choice
        assert game.player2.hand.contains(choice.correct_card.id)
        assert game.player2.deck.contains(choice.card_1.id)
        assert game.player2.deck.contains(choice.card_2.id)
        card = choice.correct_card
        choice.choose(choice.correct_card)
        assert card in game.player1.hand

    game = prepare_empty_game()
    game.player1.give("DRG_306").play()
    assert not game.player1.choice


def test_murozond_the_infinite():
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give("DS1_233").play()
    game.player1.give("ICC_481").play()
    game.end_turn()

    game.player2.give("DRG_090").play()
    assert game.player2.field[1] == WISP
    assert game.player1.hero.damaged_this_turn == 5
    assert game.player2.hero == "ICC_481"


def test_grizzled_wizard():
    game = prepare_game(CardClass.DRUID, CardClass.HUNTER)
    power1 = game.player1.hero.power
    power2 = game.player2.hero.power
    game.player1.give("DRG_401").play()
    assert game.player1.hero.power == power2.id
    assert game.player2.hero.power == power1.id
    game.end_turn()
    assert game.player1.hero.power == power2.id
    assert game.player2.hero.power == power1.id
    game.end_turn()
    assert game.player1.hero.power == power1.id
    assert game.player2.hero.power == power2.id


def test_living_dragonbreath():
    game = prepare_game()
    dragonbreath = game.player1.give("DRG_068").play()
    wisps = [game.player1.give(WISP).play() for i in range(6)]
    game.end_turn()
    game.player2.give("CS2_026").play()
    assert not dragonbreath.frozen
    for wisp in wisps:
        assert not wisp.frozen
    dragonbreath.destroy()
    for wisp in wisps:
        assert not wisp.frozen
    game.player2.give("CS2_026").play()
    for wisp in wisps:
        assert wisp.frozen
    dragonbreath = game.player1.summon("DRG_068")
    for wisp in wisps:
        assert not wisp.frozen


def test_tentacled_manace():
    game = prepare_empty_game()
    game.player1.give("DRG_084").play()

    game = prepare_game()
    card1_cost = game.player1.deck[-1].cost
    card2_cost = game.player2.deck[-1].cost
    game.player1.give("DRG_084").play()
    assert game.player1.hand[-1].cost == card2_cost
    assert game.player2.hand[-1].cost == card1_cost


def test_kronx_dragonhoof_draw_galakrond():
    game = prepare_empty_game()
    galakrond = game.player1.give("DRG_650")
    galakrond.shuffle_into_deck()
    game.player1.give("DRG_099").play()
    assert galakrond.zone == Zone.HAND


def test_kronx_dragonhoof_draw_unleash_devastation():
    game = prepare_empty_game()
    game.player1.summon("DRG_650")
    wisp = game.player1.give(WISP).play()
    dragonhoof = game.player1.give("DRG_099").play()
    # A155 (D-108): the Devastation is drawn at random among the four, no choice
    assert game.player1.choice.cards == ["DRG_099t1", "DRG_099t2", "DRG_099t3", "DRG_099t4"]


def test_invoke():
    game = prepare_empty_game()
    galakrond = game.player1.give("DRG_650")
    galakrond.shuffle_into_deck()

    game.player1.give("DRG_303").play()
    assert game.player1.hero.atk == 3
    assert game.player1.invoke_counter == 1
    assert not INVOKED_TWICE.check(game.player1)

    game.player1.give("DRG_303").play()
    assert game.player1.hero.atk == 6
    assert game.player1.invoke_counter == 2
    assert INVOKED_TWICE.check(game.player1)

    assert game.player1.deck == ["DRG_650t2"]
    game.player1.give("DRG_303").play()
    game.player1.give("DRG_303").play()
    assert game.player1.deck == ["DRG_650t3"]


def test_chaos_gazer():
    game = prepare_empty_game()
    the_coin = game.player2.hand[0]
    game.player1.give("YOD_027").play()
    game.skip_turn()
    assert the_coin.zone == Zone.GRAVEYARD

    molten = game.player2.give("EX1_620")
    game.player1.give("YOD_027").play()
    game.skip_turn()
    assert molten.zone == Zone.HAND

    wisp = game.player2.give(WISP)
    game.player1.give("YOD_027").play()
    game.skip_turn()
    assert wisp.zone == Zone.GRAVEYARD


def test_the_fist_of_raden():
    game = prepare_game()
    coin = game.player1.give(THE_COIN)
    raden = game.player1.give("YOD_042").play()
    coin.play()
    assert raden.damage == 0
    assert len(game.player1.field) == 0

    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert raden.damage == 1
    assert len(game.player1.field) == 1
    assert game.player1.field[0].cost == 4


def test_zzeraku_the_warpe():
    game = prepare_game()
    game.player1.give(WISP).play()
    game.player1.give("CFM_900").play()
    game.skip_turn()
    game.player1.give("DRG_209").play()
    assert game.player1.hero.health == 5
    assert game.player1.field == [WISP, "CFM_900", "DRG_209"] + ["DRG_209t"] * 4


def test_cleric_of_scales():
    game = prepare_empty_game()
    scales = game.player1.give("YOD_013")
    dragon = game.player1.give("EX1_043")
    assert scales.powered_up
    scales.play()
    assert not game.player1.choice


def test_wyrmrest_purifier():
    game = prepare_game(CardClass.DRUID, CardClass.DRUID)
    game.player1.give("DRG_062").play()


# WP-191: the cards the fork played otherwise than their text.


def test_wing_commander_follows_the_dragons_in_hand():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("BRM_020")
    commander = game.player1.give("DRG_058").play()
    assert commander.atk == 4
    game.player1.give("BRM_020")
    assert commander.atk == 6
    game.player1.hand[0].discard()
    assert commander.atk == 4


def test_dread_raven_counts_the_other_ravens():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    ravens = [game.player1.give("DRG_088").play() for _ in range(3)]
    assert [r.atk for r in ravens] == [9, 9, 9]
    ravens[0].destroy()
    assert [r.atk for r in ravens[1:]] == [6, 6]


def test_troll_batrider_only_hits_a_minion():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("DRG_067").play()
    assert game.player2.hero.health == 30
    golem = game.player2.summon("CS2_186")
    game.player1.give("DRG_067").play()
    assert golem.damage == 3
    assert game.player2.hero.health == 30


def test_dragonbane_hits_a_random_enemy_not_only_the_hero():
    hit_minion = hit_hero = False
    for _ in range(30):
        game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
        golem = game.player2.summon("CS2_186")
        game.player1.give("DRG_256").play()
        game.player1.hero.power.use()  # Steady Shot: 2 to the enemy hero
        assert (golem.damage == 5) != (game.player2.hero.health == 23)
        hit_minion |= golem.damage == 5
        hit_hero |= game.player2.hero.health == 23
    assert hit_minion and hit_hero


def test_toxic_reinforcements_summons_three_leper_gnomes():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
    game.player1.give("DRG_255").play()
    for _ in range(3):
        game.player1.hero.power.use()
        game.skip_turn()
    assert game.player1.field == ["EX1_029"] * 3


def test_arcane_breath_discovers_a_spell():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    wisp = game.player2.summon(WISP)
    game.player1.give("BRM_020")
    game.player1.give("DRG_106").play(target=wisp)
    assert wisp.dead
    assert len(game.player1.choice.cards) == 3
    assert all(c.type == CardType.SPELL for c in game.player1.choice.cards)


def test_lightforged_crusader_adds_five_cards():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    game.player1.give("DRG_231").play()
    assert len(game.player1.hand) == 5
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    game.player1.give(WISP).shuffle_into_deck()
    game.player1.give("DRG_231").play()
    assert len(game.player1.hand) == 0


def test_dragons_hoard_never_offers_a_neutral_or_own_class_card():
    for _ in range(15):
        game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
        game.player1.give("DRG_028").play()
        for card in game.player1.choice.cards:
            assert card.data.rarity == Rarity.LEGENDARY
            assert len(set(card.data.classes) - {CardClass.ROGUE, CardClass.NEUTRAL}) > 0


def test_overloaded_cards_see_the_crystals_about_to_be_locked():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    tempest = game.player1.summon("DRG_216")
    assert tempest.atk == 1
    game.player1.give("EX1_238").play(target=game.player2.hero)  # Overload (1)
    assert tempest.atk == 2
    golem = game.player2.summon("CS2_186")
    game.player1.give("DRG_223").play(target=golem)
    assert golem.damage == 5


def test_cumulo_maximus_needs_overloaded_crystals():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    golem = game.player2.summon("CS2_186")
    game.player1.give("DRG_223").play()
    assert golem.damage == 0


def test_scion_of_ruin_summons_a_copy_on_each_side():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    game.player1.give(WISP).play()
    game.player1.give(WISP).play(index=1)
    game.player1.give("DRG_019").play(index=1)
    assert game.player1.field == [WISP, "DRG_019", WISP]
    game.player1.invoke_counter = 2
    game.player1.give("DRG_019").play(index=1)
    assert game.player1.field == [WISP] + ["DRG_019"] * 4 + [WISP]


def test_valdris_felgorge_raises_the_hand_limit():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    game.player1.give("DRG_208").play()
    assert game.player1.max_hand_size == 12
    for _ in range(12):
        game.player1.give(WISP)
    assert len(game.player1.hand) == 12


def test_blowtorch_saboteur_makes_the_next_hero_power_cost_three():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
    game.player1.give("DRG_403").play()
    assert game.player2.hero.power.cost == 3
    assert game.player1.hero.power.cost == 2
    game.end_turn()
    game.player2.hero.power.use()
    assert game.player2.hero.power.cost == 2


def test_bandersmosh_becomes_a_5_5_each_turn():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    game.player1.give("DRG_096")
    for _ in range(2):
        game.skip_turn()
        card = game.player1.hand[0]
        assert card.id != "DRG_096"
        assert (card.atk, card.health) == (5, 5)


def test_kronx_dragonhoof_draws_galakrond_and_unleashes_a_devastation():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.WARRIOR)
    game.player1.give("DRG_650").play()
    game.player1.used_mana = 0
    game.player1.give("DRG_660").shuffle_into_deck()
    game.player2.give("DRG_610").shuffle_into_deck()
    game.player1.give("DRG_099").play()
    assert game.player1.hand == ["DRG_660"]
    assert game.player2.deck == ["DRG_610"]
    # the Devastation is drawn at random (A155, D-108): no choice opens
    assert game.player1.choice.cards == ["DRG_099t1", "DRG_099t2", "DRG_099t3", "DRG_099t4"]


def test_murozond_replays_the_cards_in_reverse_order_without_battlecries():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.end_turn()
    game.player2.max_mana = 10
    game.player2.used_mana = 0
    game.player2.give(WISP).play()
    game.player2.give("CS2_120").play()
    game.player2.give("CS2_122").play()
    game.end_turn()
    game.player1.max_mana = 10
    game.player1.used_mana = 0
    game.player1.give("DRG_090").play()
    assert game.player1.field == ["DRG_090", "CS2_122", "CS2_120", WISP]


# WP-192: the cards of Galakrond's Awakening (YEAR_OF_THE_DRAGON) the fork played otherwise
# than their text.


def test_arcane_amplifier_adds_two_to_the_hero_power():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    amplifier = game.player1.give("YOD_008").play()
    game.player1.hero.power.use(target=game.player2.hero)
    assert game.player2.hero.damage == 3
    amplifier.destroy()
    game.end_turn()
    game.end_turn()
    game.player1.hero.power.use(target=game.player2.hero)
    assert game.player2.hero.damage == 4


def test_skyvateer_draws_a_card_when_it_dies():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give(WISP).shuffle_into_deck()
    skyvateer = game.player1.give("YOD_016").play()
    assert skyvateer.has_deathrattle
    skyvateer.destroy()
    assert game.player1.hand == [WISP]
    assert len(game.player1.deck) == 0


def test_aeon_reaver_deals_the_targets_attack():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    game.end_turn()
    golem = game.player2.give("CS2_186").play()  # War Golem 7/7
    game.end_turn()
    reaver = game.player1.give("YOD_014")
    reaver.play(target=golem)
    assert golem.dead
    assert reaver.damage == 0


def test_hailbringer_puts_an_ice_shard_on_each_side():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give(WISP).play()
    game.player1.give("YOD_029").play()
    assert game.player1.field == [WISP, "YOD_029t", "YOD_029", "YOD_029t"]


def test_chaos_gazer_card_is_destroyed_at_the_end_of_the_opponents_turn():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    for card in list(game.player2.hand):
        card.discard()
    wisp = game.player2.give(WISP)
    game.player1.give("YOD_027").play()
    assert len(wisp.buffs) == 1
    game.end_turn()  # the end of the Gazer's own turn: the card is still there
    assert wisp.zone == Zone.HAND
    assert game.current_player is game.player2
    game.end_turn()  # the end of the opponent's turn
    assert wisp.zone == Zone.GRAVEYARD


def test_rotnest_drake_needs_a_dragon_in_hand():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
    game.end_turn()
    target = game.player2.give(WISP).play()
    game.end_turn()
    game.player1.give("YOD_036").play()
    assert target.zone == Zone.PLAY
    game.player1.used_mana = 0
    game.player1.give("EX1_043")
    game.player1.give("YOD_036").play()
    assert target.zone == Zone.GRAVEYARD


def test_winged_guardian_cannot_be_targeted_by_spells_and_hero_powers_and_comes_back():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    guardian = game.player1.give("YOD_003").play()
    game.end_turn()
    fireball = game.player2.give(FIREBALL)
    assert guardian not in fireball.targets
    assert guardian not in game.player2.hero.power.targets
    game.end_turn()
    guardian.destroy()
    assert [c.id for c in game.player1.field] == ["YOD_003"]
    assert game.player1.field[0].health == 1


def test_chaos_gazer_card_can_be_played_in_the_opponents_turn():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    for card in list(game.player2.hand):
        card.discard()
    game.player2.max_mana = 3
    yeti = game.player2.give("CS2_182")  # costs 4, playable next turn at 4 crystals
    game.player1.give("YOD_027").play()
    game.end_turn()
    assert yeti.is_playable()
    yeti.play()
    assert yeti.zone == Zone.PLAY


def test_skyfin_summons_a_murloc_on_each_side_of_itself():
    # D-108, A109 (rule 80a): two minions summoned at once by a minion in play
    # stand one on each side of it.
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give(WHELP)  # a Dragon in hand
    skyfin = game.player1.give("DRG_072").play(index=1)
    field = game.player1.field
    assert field[2] is skyfin
    assert len(field) == 4
    assert Race.MURLOC in field[1].races and Race.MURLOC in field[3].races
