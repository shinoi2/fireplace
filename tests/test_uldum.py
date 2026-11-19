from utils import *


def test_siamat():
    game = prepare_game()
    siamat = game.player1.give("ULD_178").play()
    choice = game.player1.choice
    choice.choose(choice.cards[0])
    choice = game.player1.choice
    choice.choose(choice.cards[0])
    assert siamat.windfury
    assert siamat.divine_shield


def test_vulpera_scoundrel():
    game = prepare_empty_game()
    game.player1.give("ULD_209").play()
    choice = game.player1.choice
    assert len(choice.cards) == 4
    assert choice.cards[3].id == "ULD_209t"
    choice.choose(choice.cards[3])
    assert game.player1.hand[0].type == CardType.SPELL
    assert not game.player1.choice


def test_dwarven_archaeologist():
    # Sinister Deal discovers a Lackey (1 mana, no cost of its own that moves):
    # Ethereal Lackey's spells of every set made this test fail at random (a
    # Rank spell turns into its rank when given, Bogbeam costs 0 at 7 mana).
    game = prepare_empty_game()
    game.player1.give("ULD_309").play()
    game.player1.give("ULD_160").play()
    choice = game.player1.choice
    card = choice.cards[0]
    assert card.cost == 1
    choice.choose(card)
    assert card.zone == Zone.HAND
    assert card.cost == 0


def test_dwarven_archaeologist_only_the_discovered_card():
    game = prepare_empty_game()
    game.player1.give("ULD_309").play()
    game.player1.give("ULD_439").play()  # Sandwasp Queen: given, not discovered
    assert [(c.id, c.cost) for c in game.player1.hand] == [("ULD_439t", 1)] * 2


def test_evil_recruiter():
    game = prepare_game()
    recruiter = game.player1.give("ULD_162")
    assert not recruiter.requires_target()
    wisp = game.player1.summon(WISP)
    assert not recruiter.requires_target()
    lackey = game.player1.summon("DAL_613")
    assert recruiter.requires_target()
    assert wisp not in recruiter.targets
    assert lackey in recruiter.targets


def test_BEEEES():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    mech = game.player1.give(MECH).play()
    game.end_turn()
    game.player2.give("ULD_134").play(target=mech)
    assert game.player2.field == []
    assert mech.damage == 4
    game.player2.give("ULD_134").play(target=wisp)
    assert wisp.dead
    assert game.player2.field == ["ULD_134t"] * 3


def test_questing_explorer():
    game = prepare_game()
    game.player1.discard_hand()
    assert len(game.player1.hand) == 0
    game.player1.give("ULD_157").play()
    assert len(game.player1.hand) == 0
    game.player1.give("ULD_433").play()
    game.player1.give("ULD_157").play()
    assert len(game.player1.hand) == 1


def test_mischief_maker():
    game = prepare_game()
    maker = game.player1.give("ULD_229")
    card1 = game.player1.deck[-1]
    card2 = game.player2.deck[-1]
    maker.play()
    assert game.player1.deck[-1] == card2
    assert game.player2.deck[-1] == card1


# WP-190 (Hearthstone, vague 23) : les cartes de Saviors of Uldum relues contre
# leur texte (patch 21.8), puis hearthstone.wiki.gg.

YETI = "CS2_182"
HARVEST_GOLEM = "EX1_556"
LIGHTNING_BOLT = "EX1_238"
ELVEN_ARCHER = "CS2_189"
UPGRADED = {
    "HERO_01bp2",
    "HERO_02bp2",
    "HERO_03bp2",
    "HERO_04bp2",
    "HERO_05bp2",
    "HERO_06bp2",
    "HERO_07bp2",
    "HERO_08bp2",
    "HERO_09bp2",
    "HERO_10bp2",
    "HERO_11bp2",
}


def _class_of(card):
    return {CardClass(c) for c in card.classes}


def test_blatant_decoy_summons_the_lowest_cost_minion():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    p1, p2 = game.player1, game.player2
    p1.give("EX1_045")  # Ancient Watcher, 2 mana, 4/5
    p1.give("CS2_179")  # Sen'jin Shieldmasta, 4 mana, 3/5
    p2.give("EX1_045")
    p2.give("CS2_200")  # Boulderfist Ogre, 6 mana, 6/7
    decoy = p1.give("ULD_706").play()
    decoy.destroy()
    assert p1.field == ["EX1_045"]
    assert p2.field == ["EX1_045"]
    assert "CS2_179" in [c.id for c in p1.hand]
    assert "CS2_200" in [c.id for c in p2.hand]


def test_reno_the_relicologist_hits_enemy_minions_only():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    p1, p2 = game.player1, game.player2
    a = p2.summon("NEW1_030")  # Deathwing 12/12: none dies, no damage forgotten
    b = p2.summon("NEW1_030")
    p1.give("ULD_238").play()
    assert p2.hero.health == 30
    assert a.damage + b.damage == 10


def test_reno_the_relicologist_without_enemy_minions():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    p1, p2 = game.player1, game.player2
    reno = p1.give("ULD_238").play()
    assert p2.hero.health == 30
    assert reno.damage == 0


def test_shadow_of_death_shuffles_three_shadows():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    p1 = game.player1
    yeti = game.player2.summon(YETI)
    p1.give("ULD_286").play(target=yeti)
    assert p1.deck == ["ULD_286t"] * 3
    p1.draw()
    # each Shadow casts itself when drawn and draws the next one
    assert p1.field == [YETI] * 3
    assert len(p1.deck) == 0
    assert len(p1.hand) == 0


def test_clever_disguise_adds_two_spells_from_another_class():
    for _ in range(20):
        game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
        p1 = game.player1
        p1.give("ULD_328").play()
        assert len(p1.hand) == 2
        for card in p1.hand:
            assert card.type == CardType.SPELL
            classes = _class_of(card)
            assert any(card_class != CardClass.ROGUE for card_class in classes)
            assert CardClass.NEUTRAL not in classes


def test_bazaar_mugger_minion_from_another_class():
    for hero_class in (CardClass.ROGUE, CardClass.MAGE) * 10:
        game = prepare_empty_game(hero_class, hero_class)
        p1 = game.player1
        p1.give("ULD_327").play()
        card = p1.hand[-1]
        assert card.type == CardType.MINION
        classes = _class_of(card)
        assert any(card_class != hero_class for card_class in classes)
        assert CardClass.NEUTRAL not in classes


def test_bazaar_burglary_counts_cards_from_another_class():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    p1 = game.player1
    quest = p1.give("ULD_326").play()
    p1.give("ULD_327").play()  # Bazaar Mugger
    assert quest.progress == 1
    p1.give(WISP)  # neutral: no
    p1.give(MOONFIRE)  # a druid card given: 2
    assert quest.progress == 2
    p1.give("ULD_328").play()  # Clever Disguise: two more
    assert quest.zone == Zone.GRAVEYARD
    assert p1.hero.power.id == "ULD_326p"


def test_mogu_cultist_summons_highkeeper_ra():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    p1 = game.player1
    for _ in range(6):
        p1.summon("ULD_705")
    p1.give("ULD_705").play()
    assert p1.field == ["ULD_705t"]


def test_evil_recruiter_with_a_full_board():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    p1 = game.player1
    for _ in range(5):
        p1.summon(WISP)
    lackey = p1.summon("DAL_613")
    p1.give("ULD_162").play(target=lackey)
    assert lackey.dead
    assert p1.field.count("ULD_162t") == 1
    assert len(p1.field) == 7


def test_evil_recruiter_without_a_lackey():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    p1 = game.player1
    p1.summon(WISP)
    p1.give("ULD_162").play()
    assert p1.field == [WISP, "ULD_162"]


def test_wretched_reclaimer_with_a_full_board():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    p1 = game.player1
    for _ in range(5):
        p1.summon(WISP)
    yeti = p1.summon(YETI)
    yeti.damage = 3
    p1.give("ULD_269").play(target=yeti)
    assert yeti.dead
    assert len(p1.field) == 7
    back = p1.field.filter(id=YETI)
    assert len(back) == 1 and back[0].health == 5


def test_wretched_reclaimer_deathrattle_first():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    p1 = game.player1
    for _ in range(5):
        p1.summon(WISP)
    golem = p1.summon(HARVEST_GOLEM)
    p1.give("ULD_269").play(target=golem)
    # The Damaged Golem fills the seventh space: the Harvest Golem does not come
    # back (hearthstone.wiki.gg, Reincarnate, which Wretched Reclaimer's notes cite)
    assert "skele21" in [m.id for m in p1.field]
    assert HARVEST_GOLEM not in [m.id for m in p1.field]
    assert len(p1.field) == 7


def test_earthquake_death_phase_between_the_two_hits():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    p1, p2 = game.player1, game.player2
    p2.summon(HARVEST_GOLEM)
    ironbark = p2.summon("CS2_232")  # Ironbark Protector 8/8
    p1.give("ULD_181").play()
    # hearthstone.wiki.gg: "All damage and death triggers caused by the initial
    # damage will resolve before the second round": the Damaged Golem takes 2
    assert p2.field == ["CS2_232"]
    assert ironbark.damage == 7


def test_vessina_with_overload_owed():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    p1, p2 = game.player1, game.player2
    wisp = p1.summon(WISP)
    vessina = p1.give("ULD_173").play()
    assert wisp.atk == 1
    p1.give(LIGHTNING_BOLT).play(target=p2.hero)
    assert p1.overloaded == 1
    assert wisp.atk == 3
    assert vessina.atk == 2
    game.end_turn()
    game.end_turn()
    assert p1.overload_locked == 1
    assert wisp.atk == 3
    game.end_turn()
    game.end_turn()
    assert wisp.atk == 1


def test_sir_finley_of_the_sands_discovers_an_upgraded_hero_power():
    for _ in range(10):
        game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
        p1 = game.player1
        p1.give("ULD_500").play()
        choice = p1.choice
        offered = [c.id for c in choice.cards]
        assert len(set(offered)) == 3
        assert set(offered) <= UPGRADED
        choice.choose(choice.cards[0])
        assert p1.hero.power.id == offered[0]


def test_anubisath_defender_costs_zero_this_turn_only():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    p1, p2 = game.player1, game.player2
    defender = p1.give("ULD_138")
    assert defender.cost == 5
    p1.give(PYROBLAST).play(target=p2.hero)
    assert defender.cost == 0
    later = p1.give("ULD_138")
    assert later.cost == 0
    game.end_turn()
    assert defender.cost == 5
    game.end_turn()
    assert defender.cost == 5
    assert later.cost == 5


def test_anubisath_defender_a_cheap_spell_does_not_count():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    p1, p2 = game.player1, game.player2
    defender = p1.give("ULD_138")
    p1.give(FIREBALL).play(target=p2.hero)
    assert defender.cost == 5


def test_activate_the_obelisk_counts_the_health_restored():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    p1 = game.player1
    quest = p1.give("ULD_724").play()
    p1.hero.set_current_health(20)
    p1.give(HOLY_LIGHT).play()  # restores 8 to its hero
    assert quest.progress == 8
    p1.hero.set_current_health(28)
    p1.give(HOLY_LIGHT).play()  # only 2 restored
    assert quest.progress == 10
    p1.hero.set_current_health(20)
    p1.give(HOLY_LIGHT).play()
    assert quest.zone == Zone.GRAVEYARD
    assert p1.hero.power.id == "ULD_724p"


def test_wild_bloodstinger_enemy_board_full():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.HUNTER)
    p1, p2 = game.player1, game.player2
    for _ in range(7):
        p2.summon(WISP)
    p2.give(YETI)
    stinger = p1.give("ULD_212").play()
    assert YETI in [c.id for c in p2.hand]
    assert stinger.damage == 0


def test_sunstruck_henchman_falls_asleep_half_the_time():
    asleep = 0
    for _ in range(40):
        game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
        p1 = game.player1
        henchman = p1.summon("ULD_180")
        game.end_turn()
        game.end_turn()
        if not henchman.can_attack():
            asleep += 1
            assert henchman.asleep
    assert 0 < asleep < 40


def test_heart_of_virnaal_battlecries_twice_this_turn():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    p1, p2 = game.player1, game.player2
    p1.summon("ULD_291p")
    p1.hero.power.use()
    p1.give(ELVEN_ARCHER).play(target=p2.hero)
    assert p2.hero.health == 28
    game.end_turn()
    game.end_turn()
    p1.give(ELVEN_ARCHER).play(target=p2.hero)
    assert p2.hero.health == 27


def test_diseased_vulture_on_your_turn_only():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    p1, p2 = game.player1, game.player2
    p1.give("ULD_167").play()

    def pick_minion(picker, source):
        assert picker.filters["cost"] == 3
        return ["CS2_127"]

    with mock(RandomMinion, pick_minion):
        p1.give(MOONFIRE).play(target=p1.hero)
    assert len(p1.field) == 2
    assert p1.field[1].cost == 3

    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    p1, p2 = game.player1, game.player2
    p1.give("ULD_167").play()
    game.end_turn()
    p2.give(MOONFIRE).play(target=p1.hero)
    assert len(p1.field) == 1


def test_oasis_surger_gains_two_two():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    p1 = game.player1
    surger = p1.give("ULD_292")
    surger.play(choose="ULD_292a")
    assert (surger.atk, surger.health) == (5, 5)


def test_oasis_surger_with_ossirian_tear():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    p1 = game.player1
    p1.summon("ULD_131p")
    p1.give("ULD_292").play()
    assert [(m.id, m.atk, m.health) for m in p1.field] == [("ULD_292", 5, 5)] * 2


def test_crystal_merchant_needs_unspent_mana():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    p1 = game.player1
    for _ in range(4):
        p1.give(WISP).zone = Zone.DECK
    p1.summon("ULD_133")
    p1.give("CS2_186").play()  # 7
    p1.give("CS2_124").play()  # Wolfrider, 3: no mana left
    assert p1.mana == 0
    game.end_turn()
    assert len(p1.hand) == 0
    game.end_turn()
    assert len(p1.hand) == 1  # the draw of the turn
    game.end_turn()
    assert len(p1.hand) == 2  # 10 unspent: one more


def test_untapped_potential_needs_unspent_mana():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    p1 = game.player1
    quest = p1.give("ULD_131").play()
    p1.give("CS2_186").play()
    p1.give("EX1_045").play()  # Ancient Watcher, 2: 10 - 1 - 7 - 2
    assert p1.mana == 0
    game.end_turn()
    assert quest.progress == 0
    game.end_turn()
    game.end_turn()
    assert quest.progress == 1


def test_pharaoh_cat_adds_a_reborn_minion():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    p1 = game.player1
    # Every Reborn minion is Wild: a Standard game (empty decks) has none to give
    for player in game.players:
        player.is_standard = False
    p1.give("ULD_186").play()
    assert len(p1.hand) == 1
    assert p1.hand[0].type == CardType.MINION
    assert p1.hand[0].reborn


def test_flame_ward_is_revealed():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    p1, p2 = game.player1, game.player2
    p1.give("ULD_239").play()
    game.end_turn()
    boar = p2.give("CS2_171").play()  # Stonetusk Boar, Charge
    yeti = p2.summon(YETI)
    boar.attack(p1.hero)
    assert boar.dead
    assert yeti.damage == 3
    assert not p1.secrets
    boar2 = p2.give("CS2_171").play()
    boar2.attack(p1.hero)
    assert not boar2.dead
    assert yeti.damage == 3


def test_reborn_comes_back_once_with_one_health():
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    p1 = game.player1
    p1.summon(WISP)
    murmy = p1.summon("ULD_723")
    p1.summon(WISP)
    p1.give("ULD_143").play(target=murmy)  # +4/+4, Divine Shield, Taunt
    murmy.destroy()
    game.process_deaths() if hasattr(game, "process_deaths") else None
    back = p1.field[1]
    assert back.id == "ULD_723"
    assert (back.atk, back.health) == (1, 1)
    assert not back.reborn and not back.taunt and not back.divine_shield
    back.destroy()
    assert p1.field == [WISP, WISP]


def test_corrupt_the_waters_reward_replaces_the_hero_power():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    p1, p2 = game.player1, game.player2
    quest = p1.give("ULD_291").play()
    for _ in range(5):
        p1.give(ELVEN_ARCHER).play(target=p2.hero)
    assert quest.progress == 5
    assert p1.hero.power.id != "ULD_291p"
    p1.give(ELVEN_ARCHER).play(target=p2.hero)
    assert quest.zone == Zone.GRAVEYARD
    assert p1.hero.power.id == "ULD_291p"
    assert p1.hero.power.is_usable()


def test_tortollan_pilgrim_casts_the_spell():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    p1, p2 = game.player1, game.player2
    for _ in range(2):
        p1.give(FIREBALL).zone = Zone.DECK
    pilgrim = p1.give("ULD_236").play()
    choice = p1.choice
    assert [c.id for c in choice.cards] == [FIREBALL]
    choice.choose(choice.cards[0])
    assert p1.deck == [FIREBALL] * 2
    # a random target among all the Fireball can hit, the Pilgrim comprised
    assert p1.hero.health + p2.hero.health == 54 or pilgrim.dead


def test_zephrys_the_great_offers_three_cards_of_its_list():
    # A146 (D-108): three cards drawn at random from the list, not the 155.
    from fireplace.cards.utils import ZEPHRYS_POOL

    game = prepare_empty_game()
    p1 = game.player1
    p1.give("ULD_003").play()
    choice = p1.choice
    assert choice is not None
    assert len(choice.cards) == 3
    assert len({c.id for c in choice.cards}) == 3
    assert all(c.id in ZEPHRYS_POOL for c in choice.cards)
    chosen = choice.cards[1]
    choice.choose(chosen)
    assert p1.choice is None
    assert chosen in p1.hand


def test_garden_gnome_summons_a_treant_on_each_side_of_itself():
    # D-108, A109 (rule 80a): two minions summoned at once by a minion in play
    # stand one on each side of it.
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    game.player1.give(WISP).play()
    game.player1.give(PYROBLAST)  # a spell that costs 5 or more in hand
    gnome = game.player1.give("ULD_137").play(index=1)
    assert [m.id for m in game.player1.field] == [
        WISP,
        "ULD_137t",
        "ULD_137",
        "ULD_137t",
    ]
    assert game.player1.field[2] is gnome


def test_supreme_archaeology_counts_a_card_burned_by_a_full_hand():
    # D-108, A147 (rule 1043): a card drawn into a full hand burns, and
    # still counts as drawn for the quest.
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    p1 = game.player1
    quest = p1.give("ULD_140").play()
    p1.card(WISP).zone = Zone.DECK
    p1.draw()
    assert quest.progress == 1
    assert len(p1.hand) == 1
    while len(p1.hand) < 10:
        p1.give(WISP)
    burned = p1.card(WISP)
    burned.zone = Zone.DECK
    p1.draw()
    assert len(p1.hand) == 10
    assert burned.zone == Zone.REMOVEDFROMGAME
    assert quest.progress == 2


def test_supreme_archaeology_ignores_an_empty_deck():
    game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
    p1 = game.player1
    quest = p1.give("ULD_140").play()
    p1.draw()  # nothing to draw: fatigue, not a card
    assert quest.progress == 0
