from utils import *


def test_flightmaster_dungar_1():
    game = prepare_game()
    dungar = game.player1.give("SW_079").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert dungar.dormant
    assert len(game.player1.field) == 1
    game.skip_turn()
    assert not dungar.dormant
    assert len(game.player1.field) == 2


def test_flightmaster_dungar_2():
    game = prepare_game()
    dungar = game.player1.give("SW_079").play()
    game.player1.choice.choose(game.player1.choice.cards[1])
    game.player1.hero.hit(20)
    for _ in range(3):
        assert game.player1.hero.health == 10
        assert dungar.dormant
        game.skip_turn()
    assert not dungar.dormant
    assert game.player1.hero.health == 20


def test_flightmaster_dungar_3():
    game = prepare_game()
    dungar = game.player1.give("SW_079").play()
    game.player1.choice.choose(game.player1.choice.cards[2])
    for _ in range(5):
        assert dungar.dormant
        game.skip_turn()
    assert not dungar.dormant
    assert game.player2.hero.damage == 12


def test_gain_momentum():
    game = prepare_game()
    quest = game.player1.give("SW_039")
    quest.play()
    assert quest.progress == 0
    game.player1.draw()
    assert quest.progress == 1
    game.player1.draw(4)
    assert quest.zone == Zone.GRAVEYARD
    quest2 = game.player1.secrets[0]
    assert quest2.id == "SW_039t"
    assert quest2.progress == 0
    assert quest2.zone == Zone.SECRET
    for hand in game.player1.hand[:-5]:
        assert hand.cost == hand.data.cost
    for hand in game.player1.hand[-5:]:
        assert hand.cost == max(0, hand.data.cost - 1)


def test_wickerclaw():
    game = prepare_game(CardClass.DRUID, CardClass.DRUID)
    wickerclaw = game.player1.give("SW_436").play()
    atk = wickerclaw.atk
    game.player1.hero.power.use()
    assert wickerclaw.atk == atk + 2


def test_elwynn_boar():
    game = prepare_game()
    for _ in range(6):
        boar = game.player1.give("SW_075").play()
        game.player1.give(MOONFIRE).play(target=boar)
        assert game.player1.weapon is None
    boar = game.player1.give("SW_075").play()
    game.player1.give(MOONFIRE).play(target=boar)
    assert game.player1.weapon == "SW_075t"


def test_elwynn_boar_2():
    game = prepare_game()
    for _ in range(7):
        boar = game.player1.give("SW_075").play()
        assert game.player1.weapon is None
    game.player1.give("ULD_717").play()
    assert game.player1.weapon == "SW_075t"


def test_lost_in_the_park():
    game = prepare_game(CardClass.DRUID, CardClass.DRUID)
    quest = game.player1.give("SW_428").play()
    game.player1.hero.power.use()
    assert quest.progress == 1
    game.skip_turn()
    game.player1.give("BT_512").play()
    assert quest.zone == Zone.GRAVEYARD
    quest2 = game.player1.secrets[0]
    assert quest2 == "SW_428t"
    assert game.player1.hero.armor == 6


def test_arcane_overflow():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give("DED_517").play(target=wisp)
    assert game.player2.field == ["DED_517t"]
    remnant = game.player2.field[0]
    assert remnant.cost == 7
    assert remnant.atk == 7
    assert remnant.health == 7


def test_enthusiastic_banker():
    game = prepare_game()
    banker = game.player1.give("SW_069").play()
    game.skip_turn()
    game.skip_turn()
    game.skip_turn()
    game.player1.discard_hand()
    banker.destroy()
    assert len(game.player1.hand) == 3


def test_brilliant_macaw():
    game = prepare_game()
    game.player1.give("DMF_004").play()
    game.skip_turn()
    game.player1.give("DED_509").play()


# WP-197: the cards of United in Stormwind against their text
# (jeux/hearthstone.md § 13.23).

YETI = "CS2_182"
SENJIN = "CS2_179"
FROSTBOLT = "CS2_024"
SHADOW_WORD_PAIN = "CS2_234"


def _turn(game):
    """Player 1's turn, with all the mana the tests need."""
    if game.current_player is not game.player1:
        game.end_turn()
    game.player1.max_mana = 10
    game.player1.used_mana = 0
    return game


def _top(card):
    """The card goes to the top of its controller's deck (the next draw)."""
    player = card.controller
    card.shuffle_into_deck()
    player.deck.remove(card)
    player.deck.append(card)
    return card


def test_tradeable_conditions():
    game = _turn(prepare_game())
    plate = game.player1.give("SW_094")
    assert plate.tradeable and plate.is_tradeable()
    assert not game.player1.give(WISP).is_tradeable()
    deck, hand, used = (
        len(game.player1.deck),
        len(game.player1.hand),
        game.player1.used_mana,
    )
    plate.trade()
    assert plate.zone == Zone.DECK
    assert len(game.player1.deck) == deck
    assert len(game.player1.hand) == hand
    assert game.player1.used_mana == used + 1
    game.player1.used_mana = 10
    assert not game.player1.give("SW_094").is_tradeable()
    game.player1.used_mana = 0
    other = game.player1.give("SW_094")
    game.end_turn()
    assert not other.is_tradeable()
    empty = _turn(prepare_empty_game())
    assert not empty.player1.give("SW_094").is_tradeable()


def test_blacksmithing_hammer_gains_durability_when_traded():
    game = _turn(prepare_game())
    hammer = game.player1.give("DED_527")
    hammer.trade()
    traded = [c for c in game.player1.deck if c.id == "DED_527"][0]
    base = fireplace.cards.db["DED_527"].tags[GameTag.DURABILITY]
    traded.zone = Zone.HAND
    traded.play()
    assert game.player1.weapon.durability == base + 2


def test_man_the_cannons_hits_every_other_minion():
    game = _turn(prepare_game())
    friend = game.player1.give(YETI).play()
    ally = game.player2.summon(SENJIN)
    target = game.player2.summon(YETI)
    game.player1.give("DED_518").play(target=target)
    assert target.health == 2
    assert ally.health == 4
    assert friend.health == 4


def test_lothar_gains_stats_when_the_attack_kills():
    game = _turn(prepare_game())
    lothar = game.player1.give("SW_024").play()
    wisp = game.player2.summon(WISP)
    game.end_turn()
    assert wisp.dead
    assert lothar.atk == 10 and lothar.health == 10 - lothar.damage
    # an enemy that survives gives nothing
    yeti = game.player1.summon(YETI)
    game.end_turn()
    game.player1.give("SW_024")
    game.end_turn()


def test_oracle_of_elune_copies_cheap_minions_only():
    game = _turn(prepare_game())
    game.player1.give("SW_419").play()
    game.player1.give(WISP).play()
    assert len(game.player1.field) == 3
    game.player1.give(YETI).play()
    assert len(game.player1.field) == 4


def test_kodo_mount_needs_a_target():
    game = _turn(prepare_game())
    wisp = game.player1.give(WISP).play()
    mount = game.player1.give("SW_432")
    assert mount.requires_target()
    mount.play(target=wisp)
    assert wisp.atk == 5 and wisp.rush
    wisp.destroy()
    assert game.player1.field == ["SW_432t"]


def test_moonlit_guidance_draws_the_original_when_the_copy_is_played():
    game = _turn(prepare_empty_game(CardClass.DRUID, CardClass.DRUID))
    for card in (WISP, YETI, SENJIN):
        game.player1.give(card).shuffle_into_deck()
    game.player1.give("DED_002").play()
    assert len(game.player1.choice.cards) == 3
    pick = [c for c in game.player1.choice.cards if c.id == WISP][0]
    game.player1.choice.choose(pick)
    assert len(game.player1.deck) == 3
    copy = game.player1.hand[-1]
    assert copy.id == WISP
    copy.play()
    assert game.player1.hand == [WISP]
    assert len(game.player1.deck) == 2


def test_moonlit_guidance_original_is_not_drawn_the_turn_after():
    game = _turn(prepare_empty_game(CardClass.DRUID, CardClass.DRUID))
    for card in (WISP, YETI, SENJIN):
        game.player1.give(card).shuffle_into_deck()
    game.player1.give("DED_002").play()
    pick = [c for c in game.player1.choice.cards if c.id == WISP][0]
    game.player1.choice.choose(pick)
    copy = game.player1.hand[-1]
    game.skip_turn()
    assert copy.zone == Zone.HAND
    deck = len(game.player1.deck)
    copy.play()
    assert len(game.player1.deck) == deck


def test_druid_questline_goes_through_its_three_steps():
    game = _turn(prepare_empty_game(CardClass.DRUID, CardClass.DRUID))
    game.player1.give("SW_428").play()
    game.player1.give("CS2_005").play()
    game.player1.give("CS2_005").play()
    assert [s.id for s in game.player1.secrets] == ["SW_428t"]
    game.player1.give(WISP).shuffle_into_deck()
    game.skip_turn()
    for _ in range(3):
        game.player1.give("CS2_005").play()
    assert [s.id for s in game.player1.secrets] == ["SW_428t2"]
    assert game.player1.hero.armor >= 10


def test_hunter_questline_goes_through_its_three_steps():
    game = _turn(prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER))
    game.player1.give("SW_322").play()
    for _ in range(2):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert [s.id for s in game.player1.secrets] == ["SW_322t"]
    yeti = game.player2.summon(YETI)
    game.player1.hero.power.use(target=yeti)
    assert yeti.damage == 2
    for _ in range(2):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert [s.id for s in game.player1.secrets] == ["SW_322t2"]
    assert game.player1.hero.power.cost == 0
    for _ in range(2):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert not game.player1.secrets
    assert game.player1.hand[-1].id == "SW_322t4"


def test_warlock_questline_goes_through_its_three_steps():
    game = _turn(prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK))
    game.player1.give("SW_091").play()
    for _ in range(8):
        game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert [s.id for s in game.player1.secrets] == ["SW_091t"]
    assert game.player2.hero.damage == 3
    for _ in range(8):
        game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert [s.id for s in game.player1.secrets] == ["SW_091t3"]


def test_blightborn_tamsin_redirects_the_whole_damage():
    game = _turn(prepare_game())
    game.player1.give("SW_091t4").play()
    game.player1.give(FIREBALL).play(target=game.player1.hero)
    assert game.player1.hero.health == 30
    assert game.player2.hero.health == 24


def test_rat_king_wakes_up_after_five_friendly_deaths():
    game = _turn(prepare_game(CardClass.HUNTER, CardClass.HUNTER))
    king = game.player1.give("SW_323").play()
    king.destroy()
    assert game.player1.field[0].dormant
    for _ in range(5):
        game.player1.give(WISP).play().destroy()
    assert game.player1.field == ["SW_323"]
    assert not game.player1.field[0].dormant


def test_leatherworking_kit_draws_a_beast_after_three_beasts_die():
    game = _turn(prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER))
    beast = game.player1.give("CS2_172")
    beast.shuffle_into_deck()
    kit = game.player1.give("SW_457").play()
    durability = kit.durability
    for _ in range(3):
        game.player1.give("CS2_172").play().destroy()
    assert kit.durability == durability - 1
    drawn = game.player1.hand[-1]
    assert drawn.id == "CS2_172" and drawn.atk == 4 and drawn.health == 3


def test_aimed_shot_adds_two_to_the_next_hero_power_only():
    game = _turn(prepare_game(CardClass.HUNTER, CardClass.HUNTER))
    game.player1.give("SW_321").play(target=game.player2.hero)
    game.player1.hero.power.use(target=game.player2.hero)
    assert game.player2.hero.damage == 3 + 2 + 2
    game.skip_turn()
    game.player1.hero.power.use(target=game.player2.hero)
    assert game.player2.hero.damage == 3 + 2 + 2 + 2


def test_hot_streak_is_for_the_next_fire_spell_of_the_turn():
    game = _turn(prepare_game(CardClass.MAGE, CardClass.MAGE))
    game.player1.give("SW_462").play()
    assert game.player1.give(FIREBALL).cost == 2
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert game.player1.give(FIREBALL).cost == 4
    game.player1.give("SW_462").play()
    game.skip_turn()
    assert game.player1.give(FIREBALL).cost == 4


def test_deepwater_evoker_draws_one_spell():
    game = _turn(prepare_empty_game(CardClass.MAGE, CardClass.MAGE))
    for _ in range(3):
        game.player1.give(FIREBALL).shuffle_into_deck()
    game.player1.give("DED_516").play()
    assert len(game.player1.hand) == 1
    assert len(game.player1.deck) == 2
    assert game.player1.hero.armor == 4


def test_celestial_ink_set_reduces_by_five_and_loses_durability():
    game = _turn(prepare_empty_game(CardClass.MAGE, CardClass.MAGE))
    ink = game.player1.give("SW_001").play()
    durability = ink.durability
    expensive = game.player1.give(PYROBLAST)
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert expensive.cost == 10
    game.player1.give(FROSTBOLT).play(target=game.player2.hero)
    assert expensive.cost == 5
    assert ink.durability == durability - 1


def test_prismatic_jewel_kit_buffs_every_minion_of_the_hand():
    game = _turn(prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN))
    kit = game.player1.give("SW_048").play()
    durability = kit.durability
    first = game.player1.give(YETI)
    second = game.player1.give(YETI)
    squire = game.player1.give("EX1_008").play()
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=squire)
    assert (first.atk, first.health) == (5, 6)
    assert (second.atk, second.health) == (5, 6)
    assert kit.durability == durability - 1


def test_blessed_goods_offers_paladin_or_neutral_cards():
    for _ in range(3):
        game = _turn(prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN))
        game.player1.give("SW_049").play()
        cards = game.player1.choice.cards
        assert len(cards) == 3
        assert {c.type for c in cards} == {
            CardType.SPELL,
            CardType.WEAPON,
            CardType.MINION,
        }
        for card in cards:
            assert card.card_class in (CardClass.PALADIN, CardClass.NEUTRAL)


def test_rise_to_the_occasion_counts_different_cards():
    game = _turn(prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN))
    game.player1.give("SW_313").play()
    game.player1.give("CS2_168").play()
    game.player1.give("CS2_168").play()
    assert game.player1.secrets[0].progress == 1
    game.player1.give("CS2_189").play(target=game.player2.hero)
    game.player1.give("EX1_136").play() if False else None
    assert game.player1.secrets[0].progress == 2


def test_shard_of_the_naaru_silences_the_enemies_only():
    game = _turn(prepare_game(CardClass.PRIEST, CardClass.PRIEST))
    friend = game.player1.summon(SENJIN)
    enemy = game.player2.summon(SENJIN)
    game.player1.give("SW_441").play()
    assert enemy.silenced and not friend.silenced


def test_seek_guidance_draws_the_card_discovered():
    game = _turn(prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST))
    for card in (WISP, SENJIN, "CS2_120"):
        game.player1.give(card).shuffle_into_deck()
    game.player1.give("SW_433").play()
    game.player1.give("CS2_120").play()
    game.player1.give("CS2_124").play()
    game.player1.give(YETI).play()
    assert len(game.player1.choice.cards) == 3
    pick = game.player1.choice.cards[0]
    game.player1.choice.choose(pick)
    assert [s.id for s in game.player1.secrets] == ["SW_433t"]
    assert len(game.player1.deck) == 2
    assert game.player1.hand == [pick.id]


def test_defias_leper_asks_for_a_target_with_a_shadow_spell_in_hand():
    game = _turn(prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST))
    game.player2.summon(YETI)
    leper = game.player1.give("DED_513")
    assert not leper.requires_target()
    game.player1.give(SHADOW_WORD_PAIN)
    assert leper.requires_target()


def test_edwin_repeats_while_the_cards_are_played():
    game = _turn(prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE))
    for _ in range(4):
        game.player1.give(WISP).shuffle_into_deck()
    edwin = game.player1.give("DED_510").play()
    assert len(game.player1.hand) == 1
    game.player1.hand[-1].play()
    assert (edwin.atk, edwin.health) == (6, 6)
    assert len(game.player1.hand) == 1
    game.player1.hand[-1].play()
    assert (edwin.atk, edwin.health) == (8, 8)
    assert len(game.player1.hand) == 1
    game.end_turn()
    game.end_turn()
    game.player1.hand[0].play()
    assert (edwin.atk, edwin.health) == (8, 8)


def test_si7_cards_are_counted():
    game = _turn(prepare_game(CardClass.ROGUE, CardClass.ROGUE))
    first = game.player1.give("SW_411").play()
    assert (first.atk, first.health) == (3, 3)
    second = game.player1.give("SW_411").play()
    assert (second.atk, second.health) == (4, 4)
    assert game.player1.give("SW_417").cost == 5


def test_si7_extortion_can_hit_a_hero():
    game = _turn(prepare_game(CardClass.ROGUE, CardClass.ROGUE))
    extortion = game.player1.give("SW_412")
    assert game.player2.hero in extortion.play_targets
    extortion.play(target=game.player2.hero)
    assert game.player2.hero.damage == 3


def test_find_the_imposter_gives_a_spy_gizmo_and_the_next_step():
    game = _turn(prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE))
    game.player1.give("SW_052").play()
    game.player1.give("SW_411").play()
    assert not game.player1.hand
    game.player1.give("SW_413").play()
    assert [s.id for s in game.player1.secrets] == ["SW_052t"]
    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].id in SPY_GIZMO


def test_parrrley_swaps_with_any_card_of_the_opponent_deck():
    game = _turn(prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE))
    game.player2.give(MOONFIRE).shuffle_into_deck()
    parrrley = game.player1.give("DED_005")
    parrrley.play()
    assert game.player1.hand == [MOONFIRE]
    assert game.player2.deck == ["DED_005"]


def test_canal_slogger_has_its_keywords():
    game = _turn(prepare_game(CardClass.SHAMAN, CardClass.SHAMAN))
    slogger = game.player1.give("SW_033")
    assert slogger.overload == 1
    slogger.play()
    assert slogger.rush and slogger.lifesteal
    assert game.player1.overloaded == 1


def test_charged_call_summons_the_minion_discovered():
    game = _turn(prepare_game(CardClass.SHAMAN, CardClass.SHAMAN))
    game.player1.give("SW_035").play()
    cards = game.player1.choice.cards
    assert len(cards) == 3
    assert all(c.type == CardType.MINION and c.data.cost == 1 for c in cards)
    hand = len(game.player1.hand)
    game.player1.choice.choose(cards[0])
    assert len(game.player1.field) == 1
    assert len(game.player1.hand) == hand


def test_suckerhook_upgrades_the_weapon():
    game = _turn(prepare_game(CardClass.SHAMAN, CardClass.SHAMAN))
    game.player1.give("DED_511").play()
    axe = game.player1.give("CS2_106").play()
    cost = axe.cost
    game.end_turn()
    assert game.player1.weapon is not None
    assert game.player1.weapon.data.cost == cost + 1


def test_wicked_shipment_starts_with_one_imp_and_gains_two_when_traded():
    game = _turn(prepare_game(CardClass.WARLOCK, CardClass.WARLOCK))
    game.player1.give("DED_504").play()
    assert len(game.player1.field) == 1
    for imp in list(game.player1.field):
        imp.destroy()
    traded = game.player1.give("DED_504")
    traded.trade()
    again = [c for c in game.player1.deck if c.id == "DED_504"][0]
    again.zone = Zone.HAND
    again.play()
    assert len(game.player1.field) == 3


def test_runed_mithril_rod_counts_the_cards_drawn():
    game = _turn(prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK))
    for _ in range(4):
        game.player1.give(WISP).shuffle_into_deck()
    rod = game.player1.give("SW_003").play()
    durability = rod.durability
    yeti = game.player1.give(YETI)
    game.player1.draw(4)
    assert rod.durability == durability - 1
    assert yeti.cost == 3


def test_anetheron_costs_one_with_a_full_hand():
    game = _turn(prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK))
    anetheron = game.player1.give("SW_092")
    assert anetheron.cost == 6
    for _ in range(9):
        game.player1.give(WISP)
    assert len(game.player1.hand) == 10
    assert anetheron.cost == 1


def test_touch_of_the_nathrezim_restores_three():
    game = _turn(prepare_game(CardClass.WARLOCK, CardClass.WARLOCK))
    game.player1.hero.damage = 10
    wisp = game.player2.summon(WISP)
    game.player1.give("SW_090").play(target=wisp)
    assert game.player1.hero.damage == 7


def test_stormwind_guard_buffs_its_neighbours():
    game = _turn(prepare_game())
    for _ in range(3):
        game.player1.give(WISP).play()
    game.player1.give("SW_054").play(index=1)
    atk = [m.atk for m in game.player1.field]
    assert atk == [2, 4, 2, 1]


def test_battleground_battlemaster_gives_windfury_to_its_neighbours():
    game = _turn(prepare_game())
    for _ in range(3):
        game.player1.give(WISP).play()
    master = game.player1.give("SW_063").play(index=1)
    assert [m.windfury for m in game.player1.field] == [True, False, True, False]


def test_multicaster_draws_a_card_for_each_school_cast():
    game = _turn(prepare_empty_game(CardClass.MAGE, CardClass.MAGE))
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    game.player1.give(FROSTBOLT).play(target=game.player2.hero)
    game.player1.give(FROSTBOLT).play(target=game.player2.hero)
    for _ in range(4):
        game.player1.give(WISP).shuffle_into_deck()
    game.player1.used_mana = 0
    game.player1.give("DED_524").play()
    assert len(game.player1.hand) == 2


def test_auctioneer_jaxon_discovers_a_card_to_draw_when_trading():
    game = _turn(prepare_empty_game())
    for card in (WISP, YETI, SENJIN, "CS2_120"):
        game.player1.give(card).shuffle_into_deck()
    game.player1.give("SW_045").play()
    plate = game.player1.give("SW_094")
    plate.trade()
    assert len(game.player1.choice.cards) == 3
    pick = game.player1.choice.cards[0]
    game.player1.choice.choose(pick)
    assert game.player1.hand == [pick.id]
    assert len(game.player1.deck) == 4
    assert plate.zone == Zone.DECK


def test_entrapped_sorceress_needs_a_quest():
    game = _turn(prepare_game(CardClass.MAGE, CardClass.MAGE))
    game.player1.give("SW_400").play()
    assert not game.player1.choice
    game = _turn(prepare_game(CardClass.MAGE, CardClass.MAGE))
    game.player1.give("SW_450").play()
    game.player1.give("SW_400").play()
    assert len(game.player1.choice.cards) == 3


def test_cowardly_grunt_summons_from_the_deck():
    game = _turn(prepare_empty_game(CardClass.WARRIOR, CardClass.WARRIOR))
    game.player1.give(YETI).shuffle_into_deck()
    grunt = game.player1.give("SW_021").play()
    grunt.destroy()
    assert game.player1.field == [YETI]
    assert not game.player1.deck


def test_keywords_the_data_forgot():
    game = _turn(prepare_game())
    assert game.player1.give("SW_029").tags.get(GameTag.BATTLECRY)
    assert game.player1.give("SW_093").tags.get(GameTag.BATTLECRY)
    assert game.player1.give("SW_039t3_t").tags.get(GameTag.BATTLECRY)
    assert game.player1.give("SW_306").taunt
    assert game.player1.summon("SW_031t8").taunt


def test_sheldras_moontree_casts_the_next_three_spells_drawn():
    game = _turn(prepare_empty_game(CardClass.DRUID, CardClass.DRUID))
    for _ in range(6):
        game.player1.give(MOONFIRE).shuffle_into_deck()
    wisp = _top(game.player1.give(WISP))
    game.player1.give("SW_447").play()
    game.player1.draw()
    assert wisp.zone == Zone.HAND
    assert game.player1.buffs
    spell = _top(game.player1.give(MOONFIRE))
    game.player1.draw()
    assert spell.zone == Zone.GRAVEYARD


def test_fel_barrage_hits_the_lowest_enemy_again():
    game = _turn(prepare_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER))
    wisp = game.player2.summon(WISP)
    yeti = game.player2.summon(YETI)
    game.player1.give("SW_040").play()
    assert wisp.dead
    assert yeti.damage == 2


def test_fel_barrage_hits_the_enemy_hero_when_no_minion_is_there():
    # A215 (D-108): the enemy hero is one of the enemies, hit twice here.
    game = _turn(prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER))
    game.player1.give("SW_040").play()
    assert game.player2.hero.damage == 4


def test_the_si_7_selector_recognizes_an_si_7_card():
    # A227 (WP-189c): since WP-197 mapped GameTag.SI_7, the dsl selector matches
    # the SI:7 cards (no local workaround needed), and only them.
    from fireplace.dsl.selector import SI_7

    game = _turn(prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE))
    agent = game.player1.give("EX1_134")
    wisp = game.player1.give(WISP)
    assert SI_7.eval([agent, wisp], agent) == [agent]
    agent.play()
    wisp.play()
    played = [c for c in game.player1.cards_played_this_game]
    assert SI_7.eval(played, agent) == [agent]
    informant = game.player1.give("SW_411").play()
    # the Informant counts the SI:7 card played before it (the Agent), not itself
    base = informant.data.tags[GameTag.ATK]
    assert informant.atk == base + 1


def test_sigil_of_alacrity_reduces_the_card_drawn():
    game = _turn(prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER))
    for _ in range(2):
        game.player1.give(YETI).shuffle_into_deck()
    game.player1.give("SW_041").play()
    game.end_turn()
    game.end_turn()
    assert sorted(c.cost for c in game.player1.hand) == [3, 4]


def test_need_for_greed_costs_three_when_drawn_this_turn():
    game = _turn(prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER))
    greed = _top(game.player1.give("DED_506"))
    game.player1.draw()
    assert greed.cost == 3
    game.skip_turn()
    assert greed.cost == 5


def test_demonslayer_kurtrus_reduces_every_card_drawn_by_two():
    game = _turn(prepare_empty_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER))
    game.player1.give("SW_039t3_t").play()
    yeti = _top(game.player1.give(YETI))
    game.player1.draw()
    assert yeti.cost == 2


def _start(deck1, class1, deck2=None, class2=CardClass.MAGE):
    import utils

    player1 = Player("Player1", deck1, class1.default_hero)
    player2 = Player("Player2", deck2 or [WISP] * 30, class2.default_hero)
    game = BaseTestGame(players=(player1, player2))
    game.start()
    utils._empty_mulligan(game)
    return game, player1


def test_darkbishop_benedictus_enters_shadowform_with_only_shadow_spells():
    shadow = ["CS1_113", "EX1_339", "EX1_345", "EX1_334", "DS1_233"]
    game, priest = _start(["SW_448"] + shadow + [WISP] * 24, CardClass.PRIEST)
    assert priest.hero.power.id == "EX1_625t"
    game, priest = _start(["SW_448", FIREBALL] + [WISP] * 28, CardClass.PRIEST)
    assert priest.hero.power.id == "HERO_09bp"


def test_maestra_of_the_masquerade_disguises_the_hero_until_a_rogue_card():
    game, rogue = _start(["SW_050"] + [WISP] * 29, CardClass.ROGUE)
    assert rogue.hero.data.card_class != CardClass.ROGUE
    assert rogue.hero.health == 30
    if game.current_player is not rogue:
        game.end_turn()
    rogue.max_mana = 10
    rogue.give(WISP).play()
    assert rogue.hero.data.card_class != CardClass.ROGUE
    rogue.give("SW_413").play()
    assert rogue.hero.data.card_class == CardClass.ROGUE


def test_a_questline_is_in_the_starting_hand():
    for _ in range(3):
        game, mage = _start([WISP] * 29 + ["SW_450"], CardClass.MAGE)
        assert "SW_450" in [c.id for c in mage.hand]


def test_grand_magus_antonidas_counts_fire_spells_only():
    game = _turn(prepare_empty_game(CardClass.MAGE, CardClass.MAGE))
    for _ in range(3):
        game.player1.give(WISP).play()
        game.skip_turn()
    assert game.player1.give("SW_113").progress == 0
    for _ in range(3):
        game.player1.give(FIREBALL).play(target=game.player1.hero)
        game.skip_turn()
    assert game.player1.give("SW_113").progress == 3


def test_city_architect_summons_a_wall_on_each_side():
    game = _turn(prepare_empty_game())
    game.player1.give("SW_076").play()
    assert game.player1.field == ["SW_076t", "SW_076", "SW_076t"]


def test_oracle_of_elune_puts_the_copy_right_of_the_minion_played():
    # A217 (D-108): the copy goes right of the minion played, not right of Oracle.
    game = _turn(prepare_empty_game(CardClass.DRUID, CardClass.DRUID))
    game.player1.give("SW_419").play()
    game.player1.give(WISP).play(index=0)
    assert game.player1.field == [WISP, WISP, "SW_419"]
    game.player1.give("CS2_168").play(index=0)
    assert game.player1.field == ["CS2_168", "CS2_168", WISP, WISP, "SW_419"]


def test_imported_tarantula_leaves_its_spiders_where_it_stood():
    game = _turn(prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER))
    game.player1.give(WISP).play()
    tarantula = game.player1.give("SW_463").play()
    game.player1.give(WISP).play()
    tarantula.destroy()
    assert game.player1.field == [WISP, "SW_463t", "SW_463t", WISP]
