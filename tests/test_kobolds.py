from utils import *


def test_kobold_apprentice_hits_all_enemies():
    # "Battlecry: Deal 3 damage randomly split among all enemies." The enemy hero
    # is one of them: with no enemy minion, the three missiles all hit it.
    game = prepare_empty_game()
    game.player1.give("LOOT_347").play()
    assert game.player2.hero.damage == 3
    # With a 1-Health minion, it takes at most one missile; nothing is lost.
    for _ in range(10):
        game = prepare_empty_game()
        wisp = game.player2.summon(WISP)
        game.player1.give("LOOT_347").play()
        assert game.player2.hero.damage + (1 if wisp.dead else 0) == 3


def test_lesser_jasper_spellstone():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    game.player1.give("LOOT_051")
    game.player1.give("CFM_308").play(choose="CFM_308a")
    assert game.player1.hand[0].id == "LOOT_051t1"
    game.skip_turn()
    game.player1.hero.power.use()
    assert game.player1.hand[0].id == "LOOT_051t1"
    assert game.player1.hand[0].progress == 1
    game.skip_turn()
    game.player1.hero.power.use()
    assert game.player1.hand[0].id == "LOOT_051t1"
    assert game.player1.hand[0].progress == 2
    game.skip_turn()
    game.player1.hero.power.use()
    assert game.player1.hand[0].id == "LOOT_051t2"


def test_branching_paths():
    game = prepare_game()
    game.player1.give("LOOT_054").play()
    choice = game.player1.choice
    assert choice
    choice.choose(choice.cards[1])
    assert game.player1.hero.armor == 6
    choice = game.player1.choice
    assert choice
    choice.choose(choice.cards[1])
    choice = game.player1.choice
    assert not choice
    assert game.player1.hero.armor == 12


def test_raven_familiar():
    game = prepare_empty_game()
    game.player1.give(FIREBALL).shuffle_into_deck()
    game.player2.give(MOONFIRE).shuffle_into_deck()
    game.player1.give("LOOT_170").play()
    assert game.player1.hand[0].id == FIREBALL


def test_explosive_runes():
    game = prepare_game()
    game.player1.give("LOOT_101").play()
    game.end_turn()
    game.player2.give(WISP).play()
    assert len(game.player2.field) == 0
    assert game.player2.hero.health == 25


def test_the_darkness():
    game = prepare_empty_game()
    darkness = game.player1.give("LOOT_526").play()
    assert darkness.dormant
    game.skip_turn()
    assert not darkness.dormant


def test_king_togwaggle():
    game = prepare_game()
    deck1 = [card.id for card in game.player1.deck]
    deck2 = [card.id for card in game.player2.deck]
    game.player1.give("LOOT_541").play()
    assert deck1 == [card.id for card in game.player2.deck]
    assert deck2 == [card.id for card in game.player1.deck]


def test_lynessa_sunsorrow():
    game = prepare_game()
    sunsorrow = game.player1.give("LOOT_216")
    atk = sunsorrow.atk
    for _ in range(3):
        wisp = game.player1.give(WISP).play()
        game.player1.give("CS2_087").play(target=wisp)
    sunsorrow.play()
    assert sunsorrow.atk == atk + 9


def test_sonya_shadowdancer():
    game = prepare_empty_game()
    game.player1.give("LOOT_165").play()
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert game.player1.hand[0].id == WISP
    assert game.player1.hand[0].buffs[0].id == "LOOT_165e"


def test_windshear_stormcaller():
    game = prepare_game()
    for totem in BASIC_TOTEMS:
        game.player1.give(totem).play()
    game.player1.give("LOOT_518").play()
    assert game.player1.field[5].id == "NEW1_010"


def test_crushing_walls():
    game = prepare_game()
    game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give("LOOT_522").play()
    assert len(game.player1.field) == 0
    game.end_turn()
    game.player1.give(WISP).play()
    game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give("LOOT_522").play()
    assert len(game.player1.field) == 0
    game.end_turn()
    game.player1.give(WISP).play()
    game.player1.give(CHICKEN).play()
    game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give("LOOT_522").play()
    assert len(game.player1.field) == 1
    assert game.player1.field[0].id == CHICKEN


def test_dragon_soul():
    game = prepare_game()
    game.player1.give("LOOT_209").play()
    for _ in range(3):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.field) == 1
    game.skip_turn()
    for _ in range(3):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.field) == 2


def test_reckless_flurry():
    game = prepare_game()
    game.player1.give("EX1_606").play()
    assert game.player1.hero.armor == 5
    game.player1.give(WISP).play()
    game.player1.give("LOOT_364").play()
    assert game.player1.hero.armor == 0
    assert len(game.player1.field) == 0


def test_the_runespear():
    game = prepare_game()
    game.player1.give("LOOT_506").play()
    game.player1.hero.attack(game.player2.hero)
    assert game.player1.choice
    game.player1.choice.choose(game.player1.choice.cards[0])


def test_dragons_fury():
    game = prepare_empty_game()
    game.player1.give(FIREBALL).shuffle_into_deck()
    wisp = game.player1.give(WISP).play()
    mech = game.player1.give(MECH).play()
    game.player1.give("LOOT_172").play()
    assert wisp.dead
    assert not mech.dead
    assert mech.health == 1


def test_unstable_evolution():
    game = prepare_game()
    game.player1.give(WISP).play()
    game.player1.give("LOOT_504")
    evolution = game.player1.hand[-1]
    evolution.play(target=game.player1.field[0])
    assert game.player1.field[0].cost == 1


# WP-185 (Kobolds & Catacombs, vague 23) : chaque carte relue contre son texte
# (patch 21.8) et le wiki ; un test rouge sur 4db06636, vert après la réparation.

YETI = "CS2_182"
FIERY_WAR_AXE = "CS2_106"
LOOT_HOARDER = "EX1_096"
ZOMBIE_CHOW = "FP1_001"


def test_unstable_evolution_leaves_the_hand_at_end_of_turn():
    # "Repeatable this turn": the copy it gives does not outlive the turn.
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give("LOOT_504").play(target=game.player1.field[0])
    assert game.player1.hand[-1].id == "LOOT_504t"
    game.end_turn()
    # (the evolved minion is random: only the copy is looked for)
    assert "LOOT_504t" not in [c.id for c in game.player1.hand]


def test_ebon_dragonsmith_reduces_a_weapon():
    # "Reduce the Cost of a random weapon in your hand by (2)."
    game = prepare_empty_game()
    axe = game.player1.give(FIERY_WAR_AXE)
    yeti = game.player1.give(YETI)
    game.player1.give("LOOT_118").play()
    assert axe.cost == 1
    assert yeti.cost == 4


def test_lone_champion_needs_an_empty_board():
    # "If you control no other minions, gain Taunt and Divine Shield."
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    champion = game.player1.give("LOOT_124").play()
    assert not champion.taunt
    assert not champion.divine_shield
    game = prepare_empty_game()
    champion = game.player1.give("LOOT_124").play()
    assert champion.taunt
    assert champion.divine_shield


def test_void_ripper_spares_itself():
    # "Swap the Attack and Health of all other minions."
    game = prepare_empty_game()
    yeti = game.player2.summon(YETI)
    ripper = game.player1.give("LOOT_529")
    ripper.buff(ripper, "LOOT_054be")  # +1 Attack in the hand: a 4/3
    ripper.play()
    assert (ripper.atk, ripper.health) == (4, 3)
    assert (yeti.atk, yeti.health) == (5, 4)


def test_master_oakheart_recruits_by_attack():
    # "Recruit a 1, 2, and 3-Attack minion" (Attack, not Cost).
    game = prepare_empty_game()
    for id in (YETI, "CS2_120", WISP, "CS2_172"):
        # 4/5 at 4, 2/3 at 2, 1/1 at 0, 3/2 at 2
        game.player1.give(id).shuffle_into_deck()
    game.player1.give("LOOT_521").play()
    recruited = sorted(m.atk for m in game.player1.field if m.id != "LOOT_521")
    assert recruited == [1, 2, 3]
    assert [c.id for c in game.player1.deck] == [YETI]


def test_the_darkness_shuffles_its_candles_into_the_enemy_deck():
    # "Shuffle 3 Candles into the enemy deck. When drawn, this awakens."
    game = prepare_empty_game()
    darkness = game.player1.give("LOOT_526").play()
    assert len(game.player1.deck) == 0
    assert [c.id for c in game.player2.deck] == ["LOOT_526t"] * 3
    assert darkness.dormant
    game.end_turn()
    assert not darkness.dormant


def test_arcane_tyrant_costs_zero_when_it_arrives_after_the_spell():
    # "Costs (0) if you've cast a spell that costs (5) or more this turn":
    # a condition, also for a Tyrant that comes to the hand afterwards.
    game = prepare_empty_game()
    game.player1.give(PYROBLAST).play(target=game.player2.hero)
    tyrant = game.player1.give("LOOT_130")
    assert tyrant.cost == 0
    game.end_turn()
    game.end_turn()
    assert tyrant.cost == 5
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert tyrant.cost == 5


def test_ironwood_and_gemstudded_golems_read_the_hero_armor():
    # "Can only attack if you have 3 (5) or more Armor."
    game = prepare_empty_game()
    ironwood = game.player1.give("LOOT_048").play()
    gemstudded = game.player1.give("LOOT_365").play()
    game.end_turn()
    game.end_turn()
    assert not ironwood.can_attack()
    assert not gemstudded.can_attack()
    game.player1.give("LOOT_047").play(target=ironwood)  # Barkskin: 3 Armor
    assert ironwood.can_attack()
    assert not gemstudded.can_attack()
    game.player1.give("LOOT_047").play(target=ironwood)
    assert gemstudded.can_attack()


def test_wandering_monster_answers_a_hero_attack():
    # "When an enemy attacks your hero": an enemy hero too.
    game = prepare_empty_game()
    game.player1.give("LOOT_079").play()
    game.end_turn()
    game.player2.give(LIGHTS_JUSTICE).play()
    game.player2.hero.attack(game.player1.hero)
    assert len(game.player1.field) == 1
    assert game.player1.field[0].cost == 3
    assert game.player1.hero.health == 30
    assert len(game.player1.secrets) == 0


def test_leyline_manipulator_reduces_cards_that_did_not_start_in_the_deck():
    game = prepare_game()
    started = game.player1.hand[0]
    started_cost = started.cost
    given = game.player1.give(FIREBALL)
    game.player1.give("LOOT_537").play()
    assert given.cost == 2
    assert started.cost == started_cost


def test_valanyr_buffs_a_minion_in_the_hand():
    # "Deathrattle: Give a minion in your hand +4/+2. When it dies, reequip this."
    game = prepare_empty_game()
    in_hand = game.player1.give(WISP)
    on_board = game.player1.give(WISP).play()
    game.player1.give("LOOT_500").play()
    game.player1.weapon.destroy()
    assert (in_hand.atk, in_hand.health) == (5, 3)
    assert on_board.atk == 1
    in_hand.play()
    in_hand.destroy()
    assert game.player1.weapon.id == "LOOT_500"


def test_elixir_of_hope_returns_the_minion_to_the_hand():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    game.player1.give("LOOT_278t4").play(target=wisp)
    wisp.destroy()
    assert len(game.player1.field) == 0
    assert game.player1.hand[-1].id == WISP
    assert game.player1.hand[-1].atk == 1


def test_elven_minstrel_draws_two_minions():
    game = prepare_empty_game()
    for _ in range(3):
        game.player1.give(WISP).shuffle_into_deck()
    game.player1.give(FIREBALL).shuffle_into_deck()
    game.player1.give(THE_COIN).play()
    game.player1.give("LOOT_211").play()
    assert [c.id for c in game.player1.hand] == [WISP, WISP]


def test_kobold_illusionist_summons_a_copy():
    # "Summon a 1/1 copy of a minion from your hand": the card stays there.
    game = prepare_empty_game()
    yeti = game.player1.give(YETI)
    illusionist = game.player1.give("LOOT_412").play()
    illusionist.destroy()
    assert yeti.zone == Zone.HAND
    assert len(game.player1.field) == 1
    copy = game.player1.field[0]
    assert copy.id == YETI
    assert (copy.atk, copy.health) == (1, 1)


def test_cheat_death_returns_the_minion_two_cheaper():
    game = prepare_empty_game()
    game.player1.give("LOOT_204").play()
    game.end_turn()
    yeti = game.player1.summon(YETI)
    game.player2.give(FIREBALL).play(target=yeti)
    returned = game.player1.hand[-1]
    assert returned.id == YETI
    assert returned.cost == 2


def test_evasion_is_spent_and_lasts_this_turn():
    # "After your hero takes damage, become Immune this turn."
    game = prepare_empty_game()
    game.player1.give("LOOT_214").play()
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert game.player1.hero.health == 29
    assert game.player1.hero.immune
    assert len(game.player1.secrets) == 0
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert game.player1.hero.health == 29
    game.end_turn()
    assert not game.player1.hero.immune


def test_onyx_spellstone_upgrades_to_greater():
    game = prepare_empty_game()
    game.player1.give("LOOT_503")
    for _ in range(3):
        game.player1.give(ZOMBIE_CHOW).play()
    assert game.player1.hand[0].id == "LOOT_503t"
    for _ in range(3):
        game.player1.give(ZOMBIE_CHOW).play()
    assert game.player1.hand[0].id == "LOOT_503t2"


def test_sapphire_spellstone_upgrades_on_overload():
    # "Overload 3 Mana Crystals to upgrade" (not "Play Deathrattle cards").
    game = prepare_empty_game()
    game.player1.give("LOOT_064")
    game.player1.give(ZOMBIE_CHOW).play()
    game.player1.give(ZOMBIE_CHOW).play()
    game.player1.give(ZOMBIE_CHOW).play()
    assert game.player1.hand[0].id == "LOOT_064"
    for _ in range(2):
        game.player1.give("EX1_238").play(target=game.player2.hero)  # Overload (1)
    assert game.player1.hand[0].id == "LOOT_064"
    game.player1.give("EX1_238").play(target=game.player2.hero)
    assert game.player1.hand[0].id == "LOOT_064t1"
    game.end_turn()
    game.end_turn()
    yeti = game.player2.summon(YETI)
    game.player1.give("LOOT_060").play(target=yeti)  # Crushing Hand, Overload (3)
    assert game.player1.hand[0].id == "LOOT_064t2"


def test_pearl_spellstone_counts_only_its_own_healing():
    # "Restore 3 Health to upgrade": the healing of its player, not of the
    # opponent; a heal that restores nothing does not count.
    game = prepare_empty_game()
    game.player1.give("LOOT_091")
    game.player1.give(HOLY_LIGHT).play()  # at full Health: nothing restored
    assert game.player1.hand[0].id == "LOOT_091"
    game.player1.hero.set_current_health(20)
    game.end_turn()
    game.player2.give("CS2_007").play(target=game.player1.hero)  # Healing Touch
    assert game.player1.hand[0].id == "LOOT_091"
    game.end_turn()
    game.player1.hero.set_current_health(20)
    game.player1.give("CS2_007").play(target=game.player1.hero)
    assert game.player1.hand[0].id == "LOOT_091t1"


def test_shifting_scroll_transforms_at_the_end_of_its_turn():
    # The wiki (D-38): "Shifting Scroll transforms at the end of your turn";
    # "While the actual Shifting Scroll is in your hand, it cannot be cast".
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("LOOT_104")
    assert not game.player1.hand[0].is_playable()
    game.end_turn()
    first = game.player1.hand[0]
    assert first.id != "LOOT_104"
    assert first.type == CardType.SPELL
    game.end_turn()
    assert game.player1.hand[0] is first
    game.end_turn()
    second = game.player1.hand[0]
    assert second is not first
    assert second.type == CardType.SPELL


def test_zarogs_crown_summons_two_copies():
    # Marin the Fox's treasure: "Discover a Legendary minion. Summon two
    # copies of it." Two on the board, none in the hand.
    game = prepare_empty_game()
    game.player1.give("LOOT_998j").play()
    choice = game.player1.choice
    assert len(choice.cards) == 3
    assert all(c.rarity == Rarity.LEGENDARY for c in choice.cards)
    chosen = choice.cards[0].id
    choice.choose(choice.cards[0])
    assert [m.id for m in game.player1.field] == [chosen, chosen]
    assert len(game.player1.hand) == 0


def test_leyline_manipulator_ignores_cards_that_transformed_themselves():
    # The wiki (Leyline Manipulator): not affected, "Cards transform themselves
    # into new cards while in the player's hand, such as Shifter Zerus, Molten
    # Blade, or Shifting Scroll"; a Spellstone upgrades itself in the same way.
    game = BaseTestGame(
        players=(
            Player("Player1", ["LOOT_104"] * 30, CardClass.MAGE.default_hero),
            Player("Player2", [WISP] * 30, CardClass.MAGE.default_hero),
        )
    )
    game.start()
    # The coin decides who starts: play the Shifting Scrolls' player.
    me = next(p for p in game.players if p.name == "Player1")
    if game.current_player is not me:
        game.end_turn()
    me.give("LOOT_051")  # given: did not start in the deck
    game.end_turn()
    game.end_turn()
    spells = [c for c in me.hand if c.type == CardType.SPELL and c.id != "LOOT_104"]
    spells = [c for c in spells if not c.id.startswith("LOOT_051")]
    assert spells
    costs = [c.cost for c in spells]
    me.give("LOOT_537").play()
    assert [c.cost for c in spells] == costs


def test_the_darkness_is_never_summoned_at_random():
    # The wiki: "The Darkness is exempt from random summon or transform effects."
    assert "LOOT_526" not in fireplace.cards.filter(
        collectible=True, type=CardType.MINION, cost=4
    )


def test_windshear_stormcaller_with_wrath_of_air():
    # The wiki: "Healing Totem, Searing Totem, Stoneclaw Totem, and one of Wrath
    # of Air Totem and Strength Totem."
    for fourth in ("CS2_052", "CS2_058"):
        game = prepare_empty_game()
        for totem in ("CS2_050", "CS2_051", "NEW1_009", fourth):
            game.player1.give(totem).play()
        game.player1.give("LOOT_518").play()
        assert game.player1.field[-1].id == "NEW1_010"


def test_recruit_summons_at_the_far_right():
    # The wiki (Recruit): "minions with this effect always summon other minions
    # on the rightmost side of the board, as opposed to the right of them."
    game = prepare_empty_game()
    game.player1.give(YETI).shuffle_into_deck()
    game.player1.give(WISP).play()
    game.player1.give("LOOT_375").play(index=0)  # Guild Recruiter, at the left
    assert [m.id for m in game.player1.field] == ["LOOT_375", WISP, YETI]
    game = prepare_empty_game()
    game.player1.give("CS2_120").shuffle_into_deck()  # River Crocolisk, a Beast
    kathrena = game.player1.summon("LOOT_511")
    game.player1.give(WISP).play()
    kathrena.destroy()
    assert [m.id for m in game.player1.field] == [WISP, "CS2_120"]


def test_lynessa_sunsorrow_casts_thirty_at_most():
    # The wiki: "Lynessa's Battlecry is limited to 30 cards and casts the buffs
    # in a random order."
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    for _ in range(31):
        game.player1.give("CS2_087").play(target=wisp)  # Blessing of Might, +3
        game.player1.used_mana = 0
    lynessa = game.player1.give("LOOT_216").play()
    assert lynessa.atk == 1 + 3 * 30


def test_primal_talismans_only_friendly_minions():
    game = prepare_empty_game()
    enemy = game.player2.summon(WISP)
    friend = game.player1.give(WISP).play()
    game.player1.give("LOOT_344").play()
    assert friend.has_deathrattle
    assert not enemy.has_deathrattle


def test_skull_of_the_manari_summons_a_demon_from_the_hand():
    game = prepare_empty_game()
    imp = game.player1.give("EX1_319")  # Flame Imp
    yeti = game.player1.give(YETI)
    game.player1.give("LOOT_420").play()
    game.end_turn()
    game.end_turn()
    assert imp.zone == Zone.PLAY
    assert yeti.zone == Zone.HAND
    assert [c.id for c in game.player1.hand] == [YETI]


def test_murmuring_elemental_doubles_the_next_battlecry():
    game = prepare_empty_game()
    game.player1.give("LOOT_517").play()
    game.player1.give("LOOT_413").play()  # Plated Beetle: no Battlecry
    game.player1.give("LOOT_069").play()  # Sewer Crawler, twice
    assert len([m for m in game.player1.field if m.id == "LOOT_069t"]) == 2
    game.player1.give("LOOT_069").play()  # only the next one
    assert len([m for m in game.player1.field if m.id == "LOOT_069t"]) == 3


def test_twilights_call_two_different_minions():
    for _ in range(10):
        game = prepare_empty_game()
        game.player1.give(LOOT_HOARDER).play().destroy()
        game.player1.give(WISP).play().destroy()
        game.player1.give(ZOMBIE_CHOW).play().destroy()
        game.player1.give("LOOT_187").play()
        ids = sorted(m.id for m in game.player1.field)
        assert ids == sorted([LOOT_HOARDER, ZOMBIE_CHOW])
        assert all((m.atk, m.health) == (1, 1) for m in game.player1.field)


def test_cave_hydra_hits_the_neighbours():
    game = prepare_empty_game()
    hydra = game.player1.give("LOOT_078").play()
    left = game.player2.summon(YETI)
    middle = game.player2.summon(YETI)
    right = game.player2.summon(YETI)
    game.end_turn()
    game.end_turn()
    hydra.attack(middle)
    assert (left.damage, middle.damage, right.damage) == (2, 2, 2)


def test_unidentified_cards_are_revealed_when_given():
    # A136, decision of the user (2026-10-02): an "Unidentified" card is
    # revealed as soon as it enters the hand, however it gets there.
    variants = {
        "LOOT_278": {"LOOT_278t1", "LOOT_278t2", "LOOT_278t3", "LOOT_278t4"},
        "LOOT_285": {"LOOT_285t", "LOOT_285t2", "LOOT_285t3", "LOOT_285t4"},
        "LOOT_286": {"LOOT_286t1", "LOOT_286t2", "LOOT_286t3", "LOOT_286t4"},
        "DAL_366": {"DAL_366t1", "DAL_366t2", "DAL_366t3", "DAL_366t4"},
    }
    for id, ids in variants.items():
        game = prepare_empty_game()
        card = game.player1.give(id)
        assert [c.id for c in game.player1.hand] == [card.id]
        assert card.id in ids
        assert card.zone == Zone.HAND


def test_unidentified_cards_are_revealed_when_drawn():
    game = prepare_empty_game()
    game.player1.card("LOOT_285", zone=Zone.DECK)
    assert game.player1.deck[0].id == "LOOT_285"
    game.player1.give(YETI)
    card = game.player1.draw()
    assert card.id.startswith("LOOT_285t")
    assert [c.id for c in game.player1.hand] == [YETI, card.id]
    assert card.drawn_this_turn


def test_unidentified_cards_are_revealed_in_the_starting_hand_and_mulligan():
    deck = ["LOOT_285"] * 30
    game = Game(
        players=(
            Player("Player1", deck, CardClass.WARRIOR.default_hero),
            Player("Player2", deck, CardClass.WARRIOR.default_hero),
        )
    )
    game.start()
    for player in game.players:
        mulligan = list(player.choice.cards)
        assert all(c.id.startswith("LOOT_285t") for c in mulligan)
        assert all(c.id != "LOOT_285" for c in player.hand)
        player.choice.choose(*mulligan)
        assert all(c.id != "LOOT_285" for c in player.hand)
        # Still cards that started in the deck (Leyline Manipulator).
        for card in player.hand:
            if card.id != THE_COIN:
                assert any(card is c for c in player.starting_deck)
        # In the deck, the cards never drawn stay unidentified; the ones sent
        # back by the mulligan (some may come back at once) stay what they became.
        unidentified = [c for c in player.deck if c.id == "LOOT_285"]
        assert len(unidentified) >= len(player.deck) - len(mulligan)
        assert len(unidentified) > 0


def test_twig_of_the_world_tree_refreshes_the_spent_mana():
    # D-108, A95 (rule 844): "Refresh your Mana Crystals" (patch 26.0.4).
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    player = game.player1
    twig = player.give("LOOT_392").play()
    player.max_mana = 6
    player.used_mana = 4
    assert player.mana == 2
    twig.destroy()
    assert player.mana == 6
    assert player.max_mana == 6  # no crystal is gained any more


def test_twig_of_the_world_tree_refreshes_at_ten_crystals():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    player = game.player1
    twig = player.give("LOOT_392").play()
    player.max_mana = 10
    player.used_mana = 7
    assert player.mana == 3
    twig.destroy()
    assert player.mana == 10
    assert player.max_mana == 10
