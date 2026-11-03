from utils import *


def test_kaelthas_sunstrider():
    game = prepare_empty_game()
    fireball = game.player1.give(FIREBALL)
    game.player1.give(THE_COIN).play()
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give("BT_255").play()
    # "Every third spell you cast each turn costs (1)" (the text of 21.8)
    assert fireball.cost == 1
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 1


def test_metamorphosis():
    game = prepare_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    game.player1.hero_power.use()
    old_hero_power = game.player1.hero_power
    game.player1.give("BT_429").play()
    assert game.player1.hero_power == "BT_429p"
    game.player1.hero_power.use(target=game.player2.hero)
    assert game.player1.hero_power == "BT_429p2"
    assert game.player1.hero_power.exhausted
    game.skip_turn()
    game.player1.hero_power.use(target=game.player2.hero)
    assert game.player1.hero_power == old_hero_power
    assert not game.player1.hero_power.exhausted


def test_imprisoned_antaen():
    game = prepare_game()
    antaen = game.player1.give("BT_934").play()
    assert antaen.dormant
    assert antaen.dormant_turns == 2
    game.skip_turn()
    assert antaen.dormant
    assert antaen.dormant_turns == 1
    game.skip_turn()
    assert not antaen.dormant
    assert antaen.dormant_turns == 0
    assert game.player2.hero.health == 20
    game.end_turn()
    sap = game.player2.give("EX1_581")
    sap.play(target=antaen)
    game.end_turn()
    antaen.play()
    assert antaen.dormant
    assert antaen.dormant_turns == 2
    game.skip_turn()
    assert antaen.dormant
    assert antaen.dormant_turns == 1
    game.skip_turn()
    assert not antaen.dormant
    assert antaen.dormant_turns == 0
    assert game.player2.hero.health == 10


def test_darkglare():
    game = prepare_game()
    game.player1.give("BT_307").play()
    assert game.player1.mana == 7
    game.player1.give(FIREBALL).play(target=game.player1.hero)
    # "refresh a Mana Crystal": one, not two
    assert game.player1.mana == 7 - 4 + 1


def test_maiev_shadowsong():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    assert not wisp.dormant
    assert wisp.dormant_turns == 0
    game.player1.give("BT_737").play(target=wisp)
    assert wisp.dormant
    assert wisp.dormant_turns == 2
    game.skip_turn()
    assert wisp.dormant
    assert wisp.dormant_turns == 1
    game.skip_turn()
    assert not wisp.dormant
    assert wisp.dormant_turns == 0


def test_eye_beam():
    # Lifesteal. Deal 3 damage to a minion: it needs its target, and only a minion (WP-146)
    game = prepare_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
    golem = game.player2.summon("CS2_186")
    game.player1.hero.set_current_health(20)
    eye_beam = game.player1.give("BT_801")
    assert eye_beam.requires_target()
    assert golem in eye_beam.targets
    assert game.player2.hero not in eye_beam.targets
    assert game.player1.hero not in eye_beam.targets
    eye_beam.play(target=golem)
    assert golem.damage == 3
    assert game.player1.hero.health == 20 + 3


def test_eye_beam_from_the_middle_of_the_hand():
    # Not an outcast play: the `play` script does the damage, at full cost
    game = prepare_empty_game()
    golem = game.player2.summon("CS2_186")
    game.player1.give(WISP)
    eye_beam = game.player1.give("BT_801")
    game.player1.give(WISP)
    assert not eye_beam.play_outcast
    assert eye_beam.cost == 3
    eye_beam.play(target=golem)
    assert golem.damage == 3
    assert game.player1.mana == 10 - 3


# WP-193 : cards played otherwise than their text


def test_kayn_sunfury_the_hero_ignores_taunt_too():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    taunt = game.player2.summon("CS2_179")
    assert game.player1.hero.attack_targets == [taunt]
    game.player1.summon("BT_187")
    assert taunt in game.player1.hero.attack_targets
    assert game.player2.hero in game.player1.hero.attack_targets


def test_furious_felfin_counts_the_extra_attack_of_the_warglaives():
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    game.player1.give("BT_430").play()
    golem = game.player2.summon("CS2_186")
    game.player1.hero.attack(golem)
    assert game.player1.hero.num_attacks == 1
    assert game.player1.hero.can_attack()
    felfin = game.player1.give("BT_496").play()
    assert felfin.atk == 4
    assert felfin.rush
    game.player1.hero.attack(golem)
    game.skip_turn()
    assert game.player1.hero.num_attacks == 0


def test_msshifn_prime_has_taunt_and_both_options():
    game = prepare_empty_game(CardClass.DRUID, CardClass.MAGE)
    prime = game.player1.give("BT_136t").play(choose="BT_136ta")
    assert prime.taunt
    guardian = game.player1.field[1]
    assert guardian == "BT_136tt" and guardian.taunt
    game = prepare_empty_game(CardClass.DRUID, CardClass.MAGE)
    game.player1.give("BT_136t").play(choose="BT_136tb")
    bruiser = game.player1.field[1]
    assert bruiser == "BT_136tt2" and bruiser.rush and not bruiser.taunt


def test_terrorguard_escapee_gives_three_huntresses():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    game.player1.give("BT_159").play()
    assert [m.id for m in game.player2.field] == ["BT_159t"] * 3


def test_bonechewer_vanguard_gains_two_attack():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    vanguard = game.player1.give("BT_716").play()
    game.player1.give(MOONFIRE).play(target=vanguard)
    assert vanguard.atk == 4 + 2
    brawler = game.player1.give("BT_715").play()
    game.player1.give(MOONFIRE).play(target=brawler)
    assert brawler.atk == 2 + 2


def test_waste_warden_without_a_target_and_without_a_type():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    warden = game.player1.give("BT_729")
    assert not warden.requires_target()
    warden.play()
    assert warden.zone == Zone.PLAY
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    wisp = game.player2.summon(WISP)
    yeti = game.player2.summon("CS2_182")
    felstalker = game.player2.summon("EX1_306")
    game.player1.give("BT_729").play(target=wisp)
    # a minion without a type shares no type with the others
    assert wisp.dead
    assert yeti.damage == 0 and felstalker.damage == 0
    friend = game.player1.summon("EX1_306")
    game.player1.give("BT_729").play(target=felstalker)
    # two Demons: the target and the one of the same type on the other side
    assert felstalker.dead and friend.dead


def test_maiev_shadowsong_can_be_played_alone():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    maiev = game.player1.give("BT_737")
    assert maiev.is_playable()
    maiev.play()
    assert maiev.zone == Zone.PLAY and not maiev.dormant


def test_magtheridon_awakens_when_the_three_warders_die():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    magtheridon = game.player1.give("BT_850").play()
    assert magtheridon.dormant
    yeti = game.player1.summon("CS2_182")
    warders = list(game.player2.field)
    assert len(warders) == 3
    warders[0].destroy()
    assert magtheridon.progress == 1 and magtheridon.dormant
    warders[1].destroy()
    warders[2].destroy()
    assert not magtheridon.dormant
    assert yeti.dead
    assert game.player1.field == [magtheridon]


def test_hand_of_adal_apotheosis_psyche_split_have_their_21_8_stats():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    wisp = game.player1.summon(WISP)
    game.player1.give("BT_292").play(target=wisp)
    assert (wisp.atk, wisp.health) == (3, 2)
    game = prepare_empty_game(CardClass.PRIEST, CardClass.MAGE)
    wisp = game.player1.summon(WISP)
    game.player1.give("BT_257").play(target=wisp)
    assert (wisp.atk, wisp.health, wisp.lifesteal) == (2, 3, True)
    game = prepare_empty_game(CardClass.PRIEST, CardClass.MAGE)
    yeti = game.player1.summon("CS2_182")
    game.player1.give("BT_253").play(target=yeti)
    assert [(m.atk, m.health) for m in game.player1.field] == [(5, 7), (5, 7)]


def test_corsair_cache_draws_a_weapon_from_the_deck():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    game.player1.card("CS2_106").zone = Zone.DECK
    game.player1.give("BT_124").play()
    assert [(c.id, c.durability) for c in game.player1.hand] == [("CS2_106", 3)]
    assert not game.player1.deck
    # a weapon in the hand is not drawn
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    axe = game.player1.give("CS2_106")
    game.player1.give("BT_124").play()
    assert axe.durability == 2


def test_vashj_prime_draws_three_spells_for_three_less():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    for _ in range(4):
        game.player1.card(FIREBALL).zone = Zone.DECK
    game.player1.card(WISP).zone = Zone.DECK
    game.player1.give("BT_109t").play()
    assert [(c.id, c.cost) for c in game.player1.hand] == [(FIREBALL, 1)] * 3
    assert len(game.player1.deck) == 2


def test_imprisoned_scrap_imp_buffs_minions_in_hand_only():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    game.player1.give("BT_305").play()
    wisp = game.player1.give(WISP)
    fireball = game.player1.give(FIREBALL)
    game.skip_turn()
    game.skip_turn()
    assert (wisp.atk, wisp.health) == (3, 2)
    assert fireball.cost == 4 and not fireball.buffs


def test_bloodboil_brute_counts_damaged_minions_only():
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.MAGE)
    brute = game.player1.give("BT_138")
    assert brute.cost == 7
    yeti = game.player2.summon("CS2_182")
    game.player1.give(MOONFIRE).play(target=yeti)
    assert brute.cost == 6
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.hero.set_current_health(20)
    assert brute.cost == 6


def test_keli_dan_drawn_this_turn_destroys_all_the_other_minions():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    golem = game.player2.summon("CS2_186")
    yeti = game.player1.summon("CS2_182")
    game.player1.card("BT_196").zone = Zone.DECK
    game.player1.draw()
    keli = game.player1.hand[-1]
    assert keli.drawn_this_turn and not keli.requires_target()
    keli.play()
    assert golem.dead and yeti.dead
    assert game.player1.field == [keli]
    # not drawn this turn: it destroys the minion it targets
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.MAGE)
    golem = game.player2.summon("CS2_186")
    yeti = game.player1.summon("CS2_182")
    game.player1.give("BT_196").play(target=golem)
    assert golem.dead and not yeti.dead


def test_ashtongue_slayer_lasts_one_turn():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.MAGE)
    spymistress = game.player1.summon("BT_701")
    game.player1.give("BT_702").play(target=spymistress)
    assert spymistress.atk == 6 and spymistress.immune
    game.end_turn()
    assert spymistress.atk == 3 and not spymistress.immune


def test_shadowjeweler_hanar_offers_secrets_of_other_classes_only():
    seen = set()
    for _ in range(8):
        game = prepare_empty_game(CardClass.ROGUE, CardClass.MAGE)
        game.player1.give("BT_188").play()
        game.player1.give("EX1_289").play()
        assert len(game.player1.choice.cards) == 3
        for card in game.player1.choice.cards:
            assert card.secret
            assert CardClass.ROGUE not in card.classes
            assert CardClass.NEUTRAL not in card.classes
            seen.add(card.id)
    assert len(seen) > 3


def _outcast_game(cid, position, deck_card=WISP):
    game = prepare_empty_game(CardClass.DEMONHUNTER, CardClass.MAGE)
    for _ in range(10):
        game.player1.card(deck_card).zone = Zone.DECK
    hand = [game.player1.give(WISP) for _ in range(3)]
    card = game.player1.give(cid)
    game.player1.hand.remove(card)
    game.player1.hand.insert(position, card)
    return game, card


def test_spectral_sight_draws_another_card_only_at_an_end_of_the_hand():
    for position, drawn in ((0, 2), (1, 1), (2, 1), (3, 2)):
        game, card = _outcast_game("BT_491", position)
        size = len(game.player1.hand)
        card.play()
        assert len(game.player1.hand) == size - 1 + drawn, position


def test_skull_of_guldan_reduces_the_cost_only_at_an_end_of_the_hand():
    game, card = _outcast_game("BT_601", 3, deck_card="CS2_186")
    card.play()
    assert [c.cost for c in game.player1.hand[-3:]] == [4, 4, 4]
    game, card = _outcast_game("BT_601", 2, deck_card="CS2_186")
    card.play()
    assert [c.cost for c in game.player1.hand[-3:]] == [7, 7, 7]
    game, card = _outcast_game("BT_480", 2)
    size = len(game.player1.hand)
    card.play()
    assert (
        len(game.player1.hand) == size - 1
    )  # Crimson Sigil Runner: nothing in the middle


def test_imprisoned_sungill_summons_a_murloc_on_each_side():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
    sungill = game.player1.give("BT_009").play()
    game.skip_turn()
    game.skip_turn()
    assert not sungill.dormant
    assert [m.id for m in game.player1.field] == ["BT_009t", "BT_009", "BT_009t"]


def test_evocation_discards_at_the_end_of_the_turn():
    game = prepare_empty_game(CardClass.MAGE, CardClass.HUNTER)
    wisp = game.player1.give(WISP)
    game.player1.give("BT_006").play()
    assert len(game.player1.hand) == 10
    game.end_turn()
    # every spell the enchantment is on is gone (a ranked spell that changed
    # card in the hand, Flurry (Rank 3), loses it: Forged in the Barrens)
    assert wisp in game.player1.hand
    assert len(game.player1.hand) <= 2


def test_overgrowth_gives_an_excess_mana_for_each_crystal_over_ten():
    # A176 (D-108): as two Wild Growth: none at 8 crystals, one at 9, two at 10.
    for crystals, gained, excess in ((8, 2, 0), (9, 1, 1), (10, 0, 2)):
        game = prepare_empty_game()
        game.player1.max_mana = crystals
        game.player1.used_mana = 0
        game.player1.give("BT_130").play()
        assert game.player1.max_mana == crystals + gained
        assert [c.id for c in game.player1.hand] == ["CS2_013t"] * excess
