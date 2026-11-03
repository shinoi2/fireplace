from utils import *


def test_frenzy():
    game = prepare_game()
    raider = game.player1.give("BAR_020").play()
    game.player1.give(MOONFIRE).play(target=raider)
    assert game.player2.hero.damage == raider.atk


def test_frenzy_2():
    game = prepare_game()
    grunt = game.player1.give("BAR_021").play()
    game.player1.give(MOONFIRE).play(target=grunt)
    assert game.player1.hero.armor == 1


def test_blood_shard_bristleback():
    game = prepare_empty_game()
    bristleback = game.player1.give("BAR_916")
    wisp = game.player1.give(WISP).play()

    assert len(game.player1.deck) == 0
    assert bristleback.requires_target()

    for _ in range(10):
        game.player1.give(WISP).shuffle_into_deck()
    assert len(game.player1.deck) == 10
    assert bristleback.requires_target()

    game.player1.give(WISP).shuffle_into_deck()
    assert len(game.player1.deck) == 11
    assert not bristleback.requires_target()


# WP-196: the cards of Forged in the Barrens against their text and
# hearthstone.wiki.gg (jeux/hearthstone.md § 13.22).

YETI = "CS2_182"
SENJIN = "CS2_179"
RAPTOR = "CS2_172"  # Bloodfen Raptor, a 2-cost Beast
FROSTBOLT = "CS2_024"
LIGHTNING_BOLT = "EX1_238"  # Nature
WILD_GROWTH = "CS2_013"  # Nature
NOBLE_SACRIFICE = "EX1_130"
REDEMPTION = "EX1_136"
COUNTERSPELL = "EX1_287"
MURLOC_RAIDER = "CS2_168"
ELVEN_ARCHER = "CS2_189"
LOOT_HOARDER = "EX1_096"
FIERY_WAR_AXE = "CS2_106"


def _mana(game, amount, player=None):
    player = player or game.player1
    player.max_mana = amount
    player.used_mana = 0


# Frenzy


def test_frenzy_only_once_and_only_if_it_survives():
    game = prepare_empty_game()
    thrasher = game.player1.give("BAR_024").play()
    game.player1.give(FIREBALL).play(target=thrasher)
    assert thrasher.dead
    assert game.player2.hero.damage == 0

    game = prepare_empty_game()
    thrasher = game.player1.give("BAR_024").play()
    game.player1.give(MOONFIRE).play(target=thrasher)
    assert game.player2.hero.damage == 3
    game.player1.give(MOONFIRE).play(target=thrasher)
    assert game.player2.hero.damage == 3


def test_sunscale_raptor_frenzy_shuffles_a_bigger_raptor():
    # CardDefs.xml forgets its FRENZY tag: it never frenzied
    game = prepare_empty_game()
    raptor = game.player1.give("BAR_031").play()
    game.player1.give(MOONFIRE).play(target=raptor)
    assert len(game.player1.deck) == 1
    shuffled = game.player1.deck[0]
    assert shuffled.id == "BAR_031"
    assert shuffled.atk == 3
    assert shuffled.max_health == 4


# Rank spells


def test_rank_spells_upgrade_at_five_and_ten_mana_crystals():
    game = prepare_empty_game()
    _mana(game, 4)
    stab = game.player1.give("BAR_319")
    game.player1.give(WISP)
    assert game.player1.hand[0].id == "BAR_319"
    # Mana Crystals, not the mana left: 5 crystals, 3 spent
    _mana(game, 5)
    game.player1.used_mana = 3
    game.player1.give(WISP)
    assert game.player1.hand[0].id == "BAR_319t"
    _mana(game, 10)
    game.player1.give(WISP)
    assert game.player1.hand[0].id == "BAR_319t2"
    assert stab.zone != Zone.HAND


def test_conditioning_rank_two_upgrades_at_ten():
    game = prepare_empty_game()
    _mana(game, 5)
    game.player1.give("BAR_842")
    game.player1.give(WISP)
    assert game.player1.hand[0].id == "BAR_842t"
    _mana(game, 9)
    game.player1.give(WISP)
    assert game.player1.hand[0].id == "BAR_842t"
    _mana(game, 10)
    game.player1.give(WISP)
    assert game.player1.hand[0].id == "BAR_842t2"


# Sigils


def test_sigil_of_flame_at_the_start_of_the_next_turn():
    game = prepare_empty_game()
    wisp = game.player2.summon(WISP)
    yeti = game.player1.summon(YETI)
    game.player1.give("BAR_306").play()
    game.end_turn()
    assert wisp.zone == Zone.PLAY
    game.end_turn()
    assert wisp.dead
    assert yeti.damage == 3
    assert not game.player1.secrets


# Restoring Health this turn


def _heal_something(game):
    game.player1.hero.set_current_health(20)
    game.player1.give(HOLY_LIGHT).play(target=game.player1.hero)


def test_priest_of_anshe_after_restoring_health():
    # HEALED_THIS_TURN was read on the hero: a KeyError
    game = prepare_empty_game()
    priest = game.player1.give("BAR_313").play()
    assert (priest.atk, priest.health) == (5, 5)
    game = prepare_empty_game()
    _heal_something(game)
    priest = game.player1.give("BAR_313").play()
    assert (priest.atk, priest.health) == (8, 8)


def test_restoring_health_counts_for_the_healer_on_any_character():
    game = prepare_empty_game()
    yeti = game.player2.summon(YETI)
    game.player1.give(MOONFIRE).play(target=yeti)
    game.player1.give(CIRCLE_OF_HEALING).play()
    assert yeti.damage == 0
    priest = game.player1.give("BAR_313").play()
    assert priest.atk == 8
    # The opponent's healing does not count, and the count ends with the turn
    game.end_turn()
    game.player2.hero.set_current_health(20)
    game.player2.give(HOLY_LIGHT).play(target=game.player2.hero)
    game.end_turn()
    priest = game.player1.give("BAR_313").play()
    assert priest.atk == 5


def test_xyrella_deals_the_health_restored_this_turn():
    game = prepare_empty_game()
    yeti = game.player2.summon(YETI)
    game.player1.hero.set_current_health(27)
    game.player1.give(HOLY_LIGHT).play(target=game.player1.hero)
    game.player1.give("BAR_735").play()
    assert yeti.damage == 3


def test_cleric_of_anshe_discovers_a_spell_from_the_deck():
    game = prepare_empty_game()
    for card in (FIREBALL, MOONFIRE, FROSTBOLT, WISP):
        game.player1.give(card).shuffle_into_deck()
    game.player1.give("WC_803").play()
    assert not game.player1.choice
    _heal_something(game)
    game.player1.give("WC_803").play()
    choice = game.player1.choice
    assert sorted(c.id for c in choice.cards) == sorted([FIREBALL, MOONFIRE, FROSTBOLT])
    chosen = choice.cards[0]
    choice.choose(chosen)
    assert chosen.zone == Zone.HAND
    # The two others stay in the deck (GenericChoice discarded them)
    assert len(game.player1.deck) == 3


# Druid


def test_guff_runetotem_after_a_nature_spell():
    game = prepare_empty_game()
    guff = game.player1.give("BAR_720").play()
    wisp = game.player1.summon(WISP)
    game.player1.give(WILD_GROWTH).play()
    assert (wisp.atk, wisp.health) == (3, 3)
    assert (guff.atk, guff.health) == (2, 4)
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert wisp.atk == 3


def test_plaguemaw_the_rotting_resummons_a_taunt_minion_without_taunt():
    game = prepare_empty_game()
    game.player1.give("BAR_540").play()
    senjin = game.player1.summon(SENJIN)
    senjin.set_current_health(1)
    game.player1.give(MOONFIRE).play(target=senjin)
    copies = [m for m in game.player1.field if m.id == SENJIN]
    assert len(copies) == 1
    assert copies[0] is not senjin
    assert not copies[0].taunt
    assert copies[0].health == 5


# Hunter


def test_prospectors_caravan_gives_plus_one_plus_one():
    # The enchantment of CardDefs.xml has no stats: +0/+0
    game = prepare_empty_game()
    game.player1.give("BAR_033").play()
    yeti = game.player1.give(YETI)
    game.end_turn()
    game.end_turn()
    assert (yeti.atk, yeti.health) == (5, 6)


def test_pack_kodo_offers_a_beast_a_secret_and_a_weapon_of_its_class():
    # The three came from any class ("Hunter or Neutral", the wiki), whatever
    # the class of its player
    for _ in range(15):
        game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
        hero_class = CardClass.HUNTER
        game.player1.give("BAR_030").play()
        beast, secret, weapon = game.player1.choice.cards
        assert beast.type == CardType.MINION and Race.BEAST in beast.races
        assert secret.data.secret
        assert weapon.type == CardType.WEAPON
        for card in (beast, secret, weapon):
            assert hero_class in card.classes or CardClass.NEUTRAL in card.classes
        assert hero_class in secret.classes


def test_warsong_wrangler_draws_the_beast_and_buffs_every_copy():
    game = prepare_empty_game()
    for card in (RAPTOR, RAPTOR, "CS2_120", "CS2_119", WISP):
        game.player1.give(card).shuffle_into_deck()
    in_hand = game.player1.give(RAPTOR)
    enemy = game.player2.give(RAPTOR)
    game.player1.give("BAR_037").play()
    choice = game.player1.choice
    assert len(choice.cards) == 3
    raptor = [c for c in choice.cards if c.id == RAPTOR][0]
    choice.choose(raptor)
    assert raptor.zone == Zone.HAND
    # The two others stay in the deck
    assert len(game.player1.deck) == 4
    copies = [c for c in game.player1.hand if c.id == RAPTOR]
    copies += [c for c in game.player1.deck if c.id == RAPTOR]
    assert len(copies) == 3
    assert all((c.atk, c.health) == (5, 3) for c in copies)
    assert in_hand.atk == 5
    assert (enemy.atk, enemy.health) == (3, 2)


# Mage


def test_varden_dawngrasp_freezes_or_hits_the_frozen():
    game = prepare_empty_game()
    frozen = game.player2.summon(YETI)
    other = game.player2.summon(YETI)
    game.player1.give("CS2_031").play(target=frozen)  # Ice Lance
    assert frozen.frozen
    game.player1.give("BAR_748").play()
    assert frozen.damage == 4
    assert frozen.frozen
    assert other.frozen
    assert other.damage == 0


def test_floecaster_counts_a_frozen_hero():
    game = prepare_empty_game()
    floecaster = game.player1.give("WC_806")
    assert floecaster.cost == 6
    game.player1.give(FROSTBOLT).play(target=game.player2.hero)
    assert floecaster.cost == 4


def test_wildfire_hero_power_deals_one_more():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("BAR_546").play()
    game.player1.hero.power.use(target=game.player2.hero)
    assert game.player2.hero.damage == 2
    game.end_turn()
    game.end_turn()
    game.player1.give("BAR_546").play()
    game.player1.hero.power.use(target=game.player2.hero)
    assert game.player2.hero.damage == 2 + 3


# Neutral


def test_talented_arcanist_next_spell_this_turn():
    game = prepare_empty_game()
    game.player1.give("BAR_064").play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 3
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 4
    game = prepare_empty_game()
    game.player1.give("BAR_064").play()
    game.end_turn()
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.damage == 1


def test_kindling_elemental_next_elemental_costs_one_less():
    # With "after", the Kindling Elemental that gave it spent it
    game = prepare_empty_game()
    game.player1.give("BAR_854").play()
    kindling = game.player1.give("BAR_854")
    fireball = game.player1.give(FIREBALL)
    assert kindling.cost == 0
    assert fireball.cost == 4
    game.player1.give(WISP).play()
    assert kindling.cost == 0
    kindling.play()
    # Spent, and the second gives a new one
    assert game.player1.give("BAR_854").cost == 0
    assert len([b for b in game.player1.buffs if b.id == "BAR_854e"]) == 1


def test_far_watch_post_the_opponents_draw_costs_one_more():
    game = prepare_empty_game()
    post = game.player1.give("BAR_074").play()
    assert not post.can_attack()
    wisp = game.player2.give(WISP)
    wisp.shuffle_into_deck()
    game.end_turn()
    assert wisp.zone == Zone.HAND
    assert wisp.cost == 1


def test_crossroads_gossiper_after_a_friendly_secret_is_revealed():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    gossiper = game.player1.give("BAR_890").play()
    game.player1.give(COUNTERSPELL).play()
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert not game.player1.secrets
    assert (gossiper.atk, gossiper.health) == (6, 5)


def test_southsea_scoundrel_the_opponent_draws_the_chosen_card():
    # A48: ForceDraw(OPPONENT, …) made them draw the top card of their deck
    game = prepare_empty_game()
    for card in (YETI, WISP, FIREBALL):
        game.player2.give(card).shuffle_into_deck()
    top = game.player2.deck[-1]
    game.player1.give("BAR_081").play()
    choice = game.player1.choice
    chosen = [c for c in choice.cards if c is not top][0]
    choice.choose(chosen)
    assert chosen.zone == Zone.HAND
    assert chosen.controller == game.player2
    assert top.zone == Zone.DECK
    assert game.player1.hand[-1].id == chosen.id


def test_horde_operative_copies_only_secrets_not_already_active():
    game = prepare_empty_game()
    game.end_turn()
    game.player2.give(NOBLE_SACRIFICE).play()
    game.player2.give(REDEMPTION).play()
    game.end_turn()
    game.player1.give(NOBLE_SACRIFICE).play()
    game.player1.give("BAR_430").play()
    assert sorted(s.id for s in game.player1.secrets) == sorted(
        [NOBLE_SACRIFICE, REDEMPTION]
    )


def test_shadow_hunter_voljin_swaps_or_returns_alone():
    game = prepare_empty_game()
    yeti = game.player2.summon(YETI)
    wisp = game.player2.give(WISP)
    game.player1.give("BAR_080").play(target=yeti)
    assert wisp.zone == Zone.PLAY
    assert yeti.zone == Zone.HAND
    # No minion in its owner's hand: the target returns there alone
    game = prepare_empty_game()
    yeti = game.player2.summon(YETI)
    game.player1.give("BAR_080").play(target=yeti)
    assert yeti.zone == Zone.HAND
    assert yeti.controller == game.player2
    assert not game.player2.field


def test_archdruid_naralex_dormant_gives_dream_cards():
    game = prepare_empty_game()
    # The Dream cards are not Standard: a Standard game would give none
    game.player1.is_standard = False
    naralex = game.player1.give("WC_035").play()
    assert naralex.dormant
    game.end_turn()
    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].card_class == CardClass.DREAM
    game.end_turn()
    game.end_turn()
    assert len(game.player1.hand) == 2
    game.end_turn()
    assert not naralex.dormant
    game.end_turn()
    assert len(game.player1.hand) == 2


def _kazakus_golem(golem_index, effect_id):
    """A game whose player 1 holds a Golem of Kazakus with the effect asked
    (the three effects offered are drawn at random: try again until it is)."""
    for _ in range(100):
        game = prepare_empty_game()
        for _ in range(4):
            game.player1.give(WISP).shuffle_into_deck()
        game.player1.give("BAR_079").play()
        game.player1.choice.choose(game.player1.choice.cards[golem_index])
        game.player1.choice.choose(game.player1.choice.cards[0])
        wanted = [c for c in game.player1.choice.cards if c.id == effect_id]
        if wanted:
            game.player1.choice.choose(wanted[0])
            return game, game.player1.hand[-1]
    raise AssertionError("never offered: " + effect_id)


def test_kazakus_golem_casts_its_own_effect():
    game, golem = _kazakus_golem(1, "BAR_079t15b")  # 5 mana, draw 2 cards
    assert (golem.id, golem.cost, golem.atk, golem.health) == ("BAR_079_m2", 5, 5, 5)
    hand = len(game.player1.hand)
    golem.play()
    assert len(game.player1.hand) == hand - 1 + 2


def test_kazakus_golem_effect_is_not_shared_by_other_golems():
    # The effect was written into the card data that every Golem of a cost
    # shares: a later Golem, in any game, cast the last one's effect
    game, kingsblood = _kazakus_golem(0, "BAR_079t15")  # 1 mana, draw a card
    game2, mageroyal = _kazakus_golem(0, "BAR_079t14")  # 1 mana, Spell Damage +1
    assert (mageroyal.cost, mageroyal.atk, mageroyal.health) == (1, 1, 1)
    hand = len(game2.player1.hand)
    mageroyal.play()
    assert mageroyal.spellpower == 1
    assert len(game2.player1.hand) == hand - 1


# Paladin


def test_galloping_savior_after_three_cards_in_a_turn():
    # `secrets =` (a typo) was never read
    game = prepare_empty_game()
    game.player1.give("BAR_550").play()
    game.end_turn()
    game.player2.give(WISP).play()
    game.player2.give(WISP).play()
    assert game.player1.secrets
    game.player2.give(WISP).play()
    assert not game.player1.secrets
    assert [m.id for m in game.player1.field] == ["BAR_550t"]


def test_sword_of_the_fallen_casts_a_secret_not_already_active():
    # A duplicate drawn at random did nothing
    for _ in range(10):
        game = prepare_empty_game(CardClass.PALADIN, CardClass.MAGE)
        for card in (NOBLE_SACRIFICE, NOBLE_SACRIFICE, NOBLE_SACRIFICE, REDEMPTION):
            game.player1.give(card).shuffle_into_deck()
        game.player1.give(NOBLE_SACRIFICE).play()
        game.player1.give("BAR_875").play()
        game.player1.hero.attack(game.player2.hero)
        assert sorted(s.id for s in game.player1.secrets) == sorted(
            [NOBLE_SACRIFICE, REDEMPTION]
        )
        assert len(game.player1.deck) == 3


# Rogue


def test_oil_rig_ambusher_deals_two_or_four():
    # No requirement: it dealt nothing; "entered your hand", not only drawn
    game = prepare_empty_game()
    ambusher = game.player1.give("BAR_316")
    assert ambusher.requires_target()
    ambusher.play(target=game.player2.hero)
    assert game.player2.hero.damage == 4
    game = prepare_empty_game()
    ambusher = game.player1.give("BAR_316")
    game.end_turn()
    game.end_turn()
    ambusher.play(target=game.player2.hero)
    assert game.player2.hero.damage == 2


def test_scabbs_cutterbutter_next_two_cards_this_turn():
    game = prepare_empty_game()
    game.player1.give(THE_COIN).play()
    game.player1.give("BAR_552").play()
    fireball = game.player1.give(FIREBALL)
    yeti = game.player1.give(YETI)
    ogre = game.player1.give("CS2_200")
    assert (fireball.cost, yeti.cost, ogre.cost) == (1, 1, 3)
    fireball.play(target=game.player2.hero)
    assert (yeti.cost, ogre.cost) == (1, 3)
    yeti.play()
    assert ogre.cost == 6
    # Not on a later turn
    game = prepare_empty_game()
    game.player1.give(THE_COIN).play()
    game.player1.give("BAR_552").play()
    yeti = game.player1.give(YETI)
    game.end_turn()
    game.end_turn()
    assert yeti.cost == 4


def test_silverleaf_and_paralytic_poison_on_the_weapon():
    # The enchantments of a weapon heard no event and ran no aura
    game = prepare_empty_game(CardClass.ROGUE, CardClass.MAGE)
    game.player1.give(WISP).shuffle_into_deck()
    game.player1.give(FIERY_WAR_AXE).play()
    game.player1.give("BAR_318").play()
    hand = len(game.player1.hand)
    game.player1.hero.attack(game.player2.hero)
    assert len(game.player1.hand) == hand + 1
    game = prepare_empty_game(CardClass.ROGUE, CardClass.MAGE)
    game.player1.give(FIERY_WAR_AXE).play()
    game.player1.give("BAR_321").play()
    assert game.player1.weapon.atk == 4
    yeti = game.player2.summon(YETI)
    game.player1.hero.attack(yeti)
    assert yeti.damage == 4
    assert game.player1.hero.damage == 0


def test_shroud_of_concealment_draws_two_minions_stealthed_this_turn():
    game = prepare_empty_game()
    yeti = game.player1.give(YETI)
    yeti.shuffle_into_deck()
    wisp = game.player1.give(WISP)
    wisp.shuffle_into_deck()
    fireball = game.player1.give(FIREBALL)
    fireball.shuffle_into_deck()
    fireball.put_on_top()
    game.player1.give("WC_016").play()
    assert yeti.zone == Zone.HAND
    assert wisp.zone == Zone.HAND
    assert fireball.zone == Zone.DECK
    yeti.play()
    assert yeti.stealthed
    game.end_turn()
    assert yeti.stealthed
    game.end_turn()
    assert not yeti.stealthed


def test_yoink_swaps_back_after_two_uses():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.MAGE)
    original = game.player1.hero.power.id
    game.player1.give("BAR_323").play()
    choice = game.player1.choice
    choice.choose([c for c in choice.cards if c.id != original][0])
    stolen = game.player1.hero.power
    assert stolen.id != original
    assert stolen.cost == 0
    for use in range(2):
        power = game.player1.hero.power
        assert power.id == stolen.id
        if power.requires_target():
            power.use(target=game.player2.hero)
        else:
            power.use()
        game.end_turn()
        game.end_turn()
    assert game.player1.hero.power.id == original


# Priest


def test_devouring_plague_never_hits_a_dead_minion():
    # A missile on the dead Wisp was lost
    for _ in range(20):
        game = prepare_empty_game()
        wisp = game.player2.summon(WISP)
        yeti = game.player2.summon(YETI)
        game.player1.hero.set_current_health(20)
        game.player1.give("BAR_311").play()
        assert (1 if wisp.dead else 0) + yeti.damage == 4
        assert game.player1.hero.health == 24
    # Void Flayer the same: 1 damage per spell in hand
    for _ in range(20):
        game = prepare_empty_game()
        wisp = game.player2.summon(WISP)
        yeti = game.player2.summon(YETI)
        game.player1.give(MOONFIRE)
        game.player1.give(FIREBALL)
        game.player1.give("BAR_307").play()
        assert (1 if wisp.dead else 0) + yeti.damage == 2


# Shaman


def test_tinyfins_caravan_draws_a_murloc():
    # It drew any minion, the top card of the deck
    game = prepare_empty_game()
    murloc = game.player1.give(MURLOC_RAIDER)
    murloc.shuffle_into_deck()
    for _ in range(3):
        game.player1.give(YETI).put_on_top()
    game.player1.give("BAR_043").play()
    game.end_turn()
    game.end_turn()
    assert murloc.zone == Zone.HAND
    assert len(game.player1.hand) == 2


def test_primal_dungeoneer_draws_a_spell_then_an_elemental():
    game = prepare_empty_game()
    bolt = game.player1.give(LIGHTNING_BOLT)
    bolt.shuffle_into_deck()
    elemental = game.player1.give("BAR_888t")
    elemental.shuffle_into_deck()
    wisp = game.player1.give(WISP)
    wisp.shuffle_into_deck()
    wisp.put_on_top()
    game.player1.give("WC_005").play()
    assert bolt.zone == Zone.HAND
    assert elemental.zone == Zone.HAND
    assert wisp.zone == Zone.DECK


def test_brukan_nature_spell_damage_three():
    # CardDefs.xml says SPELLPOWER_NATURE 1
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.MAGE)
    game.player1.give("BAR_048").play()
    game.player1.give(LIGHTNING_BOLT).play(target=game.player2.hero)
    assert game.player2.hero.damage == 6
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert game.player2.hero.damage == 12


def test_perpetual_flame_overloads_at_each_recast():
    # "Perpetual Flame Overloads 1 each time it has been recast" (the wiki)
    game = prepare_empty_game()
    game.player2.summon(WISP)
    game.player2.summon(WISP)
    game.player1.give("WC_020").play()
    assert not game.player2.field
    assert game.player1.overloaded == 3


# Warlock


def test_altar_of_fire_destroys_three_of_each_deck():
    game = prepare_empty_game()
    for _ in range(5):
        game.player1.give(WISP).shuffle_into_deck()
        game.player2.give(WISP).shuffle_into_deck()
    game.player1.give("BAR_913").play()
    assert len(game.player1.deck) == 2
    assert len(game.player2.deck) == 2


def test_soul_rend_one_card_per_minion_killed():
    game = prepare_empty_game()
    for _ in range(5):
        game.player1.give(WISP).shuffle_into_deck()
    game.player1.summon(WISP)
    game.player2.summon(WISP)
    game.player2.summon(YETI)
    game.player2.summon("CS2_186")  # War Golem, survives
    game.player1.give("BAR_911").play()
    assert len(game.player1.deck) == 2


def test_rancor_two_armor_per_minion_destroyed():
    # 10 Armor for three minions
    game = prepare_empty_game()
    game.player1.summon(WISP)
    game.player2.summon(WISP)
    game.player2.summon(MURLOC_RAIDER)
    game.player2.summon(YETI)
    game.player1.give("BAR_845").play()
    assert game.player1.hero.armor == 6


def test_barrens_scavenger_costs_one():
    game = prepare_empty_game()
    scavenger = game.player1.give("BAR_917")
    assert scavenger.cost == 1
    for _ in range(11):
        game.player1.give(WISP).shuffle_into_deck()
    assert scavenger.cost == 6


def test_neeru_fireblade_portal_is_permanent():
    game = prepare_empty_game()
    game.player1.give("BAR_919").play()
    portal = game.player1.field[-1]
    assert portal.id == "BAR_919t"
    assert portal.dormant
    assert portal not in game.player1.give(MOONFIRE).play_targets
    game.end_turn()
    assert len(game.player1.field) == 7
    assert sum(1 for m in game.player1.field if m.id == "BAR_914t3") == 5


# Warrior


def test_keywords_the_data_forgot():
    # Battlecry tags absent from CardDefs.xml: Field Contact did not hear them
    game = prepare_empty_game()
    for _ in range(5):
        game.player1.give(WISP).shuffle_into_deck()
    game.player1.give("BAR_317").play()
    hand = len(game.player1.hand)
    game.player1.give("BAR_430").play()
    assert len(game.player1.hand) == hand + 1
    for card_id in ("BAR_040", "BAR_430", "BAR_916", "BAR_919", "BAR_031"):
        card = game.player1.card(card_id)
        if card_id == "BAR_031":
            assert card.has_frenzy
        else:
            assert card.has_battlecry


def test_overlord_saurfang_resurrects_one_minion_on_each_side_of_itself():
    # D-108, A109 (rule 80a): two minions summoned at once by a minion in play
    # stand one on each side of it.
    game = prepare_empty_game(CardClass.WARRIOR, CardClass.WARRIOR)
    game.player1.summon("BAR_022").destroy()  # Peon
    game.player1.summon("BAR_031").destroy()  # Sunscale Raptor
    game.player1.give("CS2_182").play()  # a Yeti
    game.player1.used_mana = 0
    saurfang = game.player1.give("BAR_334").play(index=1)
    field = game.player1.field
    assert [m.id for m in field][0] == "CS2_182"
    assert field[2] is saurfang
    assert sorted([field[1].id, field[3].id]) == ["BAR_022", "BAR_031"]
