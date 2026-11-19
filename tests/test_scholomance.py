from utils import *


def test_sphere_of_sapience():
    game = prepare_game()
    weapon = game.player1.give("SCH_259").play()
    hand_len = len(game.player1.hand)
    game.skip_turn()
    first_card = game.player1.deck[-1]
    second_card = game.player1.deck[-2]
    assert game.player1.choice.cards == ["SCH_259t", first_card]
    assert len(game.player1.hand) == hand_len
    game.player1.choice.choose(first_card)
    hand_len += 1
    assert game.player1.hand[-1] == first_card
    assert len(game.player1.hand) == hand_len
    assert weapon.damage == 0

    game.skip_turn()
    first_card = game.player1.deck[-1]
    second_card = game.player1.deck[-2]
    assert game.player1.choice.cards == ["SCH_259t", first_card]
    assert len(game.player1.hand) == hand_len
    game.player1.choice.choose(game.player1.choice.cards[0])
    hand_len += 1
    assert game.player1.deck[0] == first_card
    assert game.player1.hand[-1] == second_card
    assert len(game.player1.hand) == hand_len
    assert weapon.damage == 1


def test_sphere_of_sapience_empty():
    game = prepare_empty_game()
    weapon = game.player1.give("SCH_259").play()
    game.skip_turn()
    assert game.player1.choice is None
    assert weapon.damage == 0


def test_potion_of_illusion():
    game = prepare_empty_game()
    game.player1.give("SCH_352").play()
    assert len(game.player1.hand) == 0
    for _ in range(7):
        game.player1.give(TARGET_DUMMY).play()
    assert len(game.player1.hand) == 0
    game.player1.give("SCH_352").play()
    assert len(game.player1.hand) == 7
    for card in game.player1.hand:
        assert card == TARGET_DUMMY
        assert card.cost == 1
        assert card.atk == 1
        assert card.health == 1


def test_speaker_gidra():
    game = prepare_game()
    gidra = game.player1.give("SCH_182").play()
    old_atk = gidra.atk
    old_health = gidra.max_health
    assert gidra.has_spellburst
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert gidra.atk == old_atk + 4
    assert gidra.max_health == old_health + 4
    assert not gidra.has_spellburst


def test_gibberling():
    game = prepare_game()
    gibberling = game.player1.give("SCH_242").play()
    assert gibberling.has_spellburst
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert not gibberling.has_spellburst
    assert len(game.player1.field) == 2
    assert game.player1.field[1].id == "SCH_242"
    assert game.player1.field[1].has_spellburst


# WP-194 : les cartes de Scholomance Academy relues contre leur texte (patch
# 21.8) et hearthstone.wiki.gg ; le test de chaque réparation a été vu rouge
# sur 91fc645d (test_spellburst_lost_to_silence décrit ce qui jouait déjà juste).

from fireplace.actions import Hit


def _game(card_class=CardClass.MAGE):
    """An empty game on player1's turn, ten mana each, both heroes of one
    class (the coin decides which of the two players is player1)."""
    game = prepare_empty_game(card_class, card_class)
    if game.current_player is not game.player1:
        game.end_turn()
    return game


def _refill(game):
    game.player1.used_mana = 0
    game.player2.used_mana = 0


def _ready(*minions):
    for minion in minions:
        minion.turns_in_play = 1


def test_spellburst_not_triggered_by_a_countered_spell():
    game = _game()
    game.end_turn()
    game.player2.give("EX1_287").play()  # Counterspell
    game.end_turn()
    initiate = game.player1.give("SCH_231").play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 30
    assert initiate.atk == 1
    assert initiate.has_spellburst
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert initiate.atk == 3


def test_spellburst_after_a_spell_that_discovers():
    game = _game(CardClass.DRUID)
    gidra = game.player1.give("SCH_182").play()
    initiate = game.player1.give("SCH_231").play()
    game.player1.give("SCH_333").play()  # Nature Studies, 1
    assert game.player1.choice is not None
    assert initiate.atk == 1
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert initiate.atk == 3
    assert gidra.atk == 2 and gidra.max_health == 5


def test_spellburst_lost_to_silence():
    game = _game()
    initiate = game.player1.give("SCH_231").play()
    game.player1.give(SILENCE).play(target=initiate)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert initiate.atk == 1


def test_ceremonial_maul_spellburst_summons_a_student_of_the_spells_cost():
    game = _game(CardClass.WARRIOR)
    game.player1.give("SCH_523").play()
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert len(game.player1.field) == 1
    student = game.player1.field[0]
    assert student.id == "SCH_523t"
    assert student.atk == student.health == 4
    assert student.taunt
    _refill(game)
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert len(game.player1.field) == 1


def test_reapers_scythe_spellburst_damages_adjacent_minions_this_turn():
    game = _game(CardClass.WARRIOR)
    game.player1.give("SCH_238").play()
    left = game.player2.summon("CS2_182")
    middle = game.player2.summon("CS2_182")
    right = game.player2.summon("CS2_182")
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.hero.attack(middle)
    assert middle.damage == 4
    assert left.damage == right.damage == 4
    game.end_turn()
    game.end_turn()
    game.player1.hero.attack(left)
    assert middle.damage == 4


def test_teachers_pet_summons_a_random_three_cost_beast():
    game = _game(CardClass.HUNTER)
    pet = game.player1.summon("SCH_244")
    game.player1.give(PYROBLAST).play(target=pet)
    assert len(game.player1.field) == 1
    beast = game.player1.field[0]
    assert beast.cost == 3
    assert Race.BEAST in beast.races


def test_pen_flinger_damages_a_minion():
    game = _game()
    yeti = game.player2.summon("CS2_182")
    pen_flinger = game.player1.give("SCH_248")
    assert pen_flinger.requires_target()
    assert game.player2.hero not in pen_flinger.targets
    pen_flinger.play(target=yeti)
    assert yeti.damage == 1
    assert pen_flinger.damage == 0
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert pen_flinger.zone == Zone.HAND


def test_onyx_magescribe_gives_its_spells_at_spellburst():
    game = _game()
    game.player1.give("SCH_230").play()
    assert len(game.player1.hand) == 0
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.hand) == 2
    for card in game.player1.hand:
        assert card.type == CardType.SPELL


def test_ras_frostwhisper_hits_the_enemy_hero():
    game = _game(CardClass.SHAMAN)
    game.player1.give("SCH_273").play()
    yeti = game.player2.summon("CS2_182")
    game.end_turn()
    assert yeti.damage == 1
    assert game.player2.hero.health == 29
    assert game.player1.hero.health == 30


def test_steeldancer_summons_a_minion_of_the_weapons_attack():
    game = _game(CardClass.WARRIOR)
    game.player1.give("CS2_106").play()  # Fiery War Axe, 3/2
    game.player1.give("SCH_522").play()
    assert len(game.player1.field) == 2
    assert game.player1.field[1].cost == 3


def test_steeldancer_without_a_weapon_summons_nothing():
    # A188 (D-108): "Rien sans arme"
    game = _game(CardClass.WARRIOR)
    steeldancer = game.player1.give("SCH_522").play()
    assert game.player1.field == [steeldancer]


def test_spellburst_of_a_minion_killed_by_an_earlier_spellburst_does_nothing():
    # A185 (D-108): "Mort = pas de Spellburst". Wretched Tutor (first on the
    # board) kills the Gibberling, whose Spellburst then summons nothing.
    game = _game()
    tutor = game.player1.give("SCH_313").play()
    gibberling = game.player1.give("SCH_242").play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert gibberling.dead
    assert game.player1.field == [tutor]


def test_diligent_notetaker_returns_the_spell():
    game = _game(CardClass.SHAMAN)
    game.player1.give("SCH_236").play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert [card.id for card in game.player1.hand] == [MOONFIRE]


def test_soulshard_lapidary_destroys_a_soul_fragment():
    game = _game(CardClass.DEMONHUNTER)
    game.player1.give("SCH_700").play()  # Spirit Jailer: two Soul Fragments
    assert len(game.player1.deck) == 2
    game.player1.give("SCH_704").play()
    assert len(game.player1.deck) == 1
    assert game.player1.hero.atk == 5
    game.end_turn()
    assert game.player1.hero.atk == 0


def test_void_drinker_destroys_a_soul_fragment():
    game = _game(CardClass.WARLOCK)
    game.player1.give("SCH_700").play()
    drinker = game.player1.give("SCH_343").play()
    assert len(game.player1.deck) == 1
    assert drinker.atk == 7 and drinker.health == 8


def test_blood_herald_grows_in_hand():
    game = _game(CardClass.HUNTER)
    herald = game.player1.give("SCH_618")
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert herald.atk == herald.health == 2
    enemy = game.player2.summon(WISP)
    game.player1.give(MOONFIRE).play(target=enemy)
    assert herald.atk == 2


def test_fel_guardians_counts_only_deaths_while_in_hand():
    game = _game(CardClass.DEMONHUNTER)
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=wisp)
    guardians = game.player1.give("SCH_357")
    assert guardians.cost == 7
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert guardians.cost == 6


def test_lorekeeper_polkelt_draws_the_highest_cost_first():
    game = _game()
    for card_id in (WISP, PYROBLAST, "CS2_182", MOONFIRE):
        game.player1.give(card_id).shuffle_into_deck()
    game.player1.give("SCH_428").play()
    assert [card.cost for card in game.player1.deck] == [0, 0, 4, 10]
    game.end_turn()
    game.end_turn()
    assert game.player1.hand[-1].id == PYROBLAST


def test_mindrender_illucia_copies_the_opponents_hand_until_end_of_turn():
    game = _game(CardClass.PRIEST)
    for card in game.player2.hand[:]:  # The Coin
        card.discard()
    mine = [game.player1.give(card_id) for card_id in (WISP, FIREBALL)]
    theirs = [
        game.player2.give(card_id) for card_id in ("CS2_182", MOONFIRE, PYROBLAST)
    ]
    game.player1.give(WISP).shuffle_into_deck()
    game.player2.give("CS2_120").shuffle_into_deck()
    my_deck = game.player1.deck[:]
    their_deck = game.player2.deck[:]
    game.player1.give("SCH_159").play()
    assert [card.id for card in game.player1.hand] == ["CS2_182", MOONFIRE, PYROBLAST]
    assert all(card not in theirs for card in game.player1.hand)
    assert game.player2.hand[:] == theirs
    assert game.player1.deck[:] == my_deck and game.player2.deck[:] == their_deck
    game.player1.hand[1].play(target=game.player2.hero)
    assert game.player2.hero.health == 29
    game.end_turn()
    assert game.player1.hand[:] == mine
    assert game.player2.hand[:3] == theirs


def test_headmaster_kelthuzad_summons_the_minions_the_spell_destroys():
    game = _game()
    game.player1.give("SCH_224").play()
    wisp = game.player2.summon(WISP)
    game.player2.summon("CS2_182")
    game.player1.give(MOONFIRE).play(target=wisp)
    assert [card.id for card in game.player1.field] == ["SCH_224", WISP]
    assert not game.player1.field[0].has_spellburst


def test_headmaster_kelthuzad_summons_nothing_when_no_minion_dies():
    game = _game()
    game.player1.give("SCH_224").play()
    game.player2.summon(WISP)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert [card.id for card in game.player1.field] == ["SCH_224"]
    assert not game.player1.field[0].has_spellburst


def test_headmaster_kelthuzad_summons_both_sides_dead():
    game = _game(CardClass.WARLOCK)
    game.player1.give("SCH_224").play()
    mine = game.player1.summon(WISP)
    game.player2.summon("CS2_120")  # River Crocolisk 2/3
    game.player2.summon("CS2_182")
    game.player1.give("CS2_062").play()  # Hellfire, 3 to all
    assert [card.id for card in game.player1.field] == ["SCH_224", WISP, "CS2_120"]
    assert mine.dead


def test_jandice_barov_marks_one_of_the_two_minions_summoned():
    game = _game(CardClass.ROGUE)
    picks = iter(("CS2_150", "CS2_187"))

    def pick_minion(picker, source):
        assert picker.filters["cost"] == 5
        return [source.controller.card(next(picks), source=source)]

    with mock(RandomMinion, pick_minion):
        game.player1.give("SCH_351").play()
    summoned = game.player1.field[1:]
    assert len(summoned) == 2
    for minion in summoned:
        assert minion.cost == 5
    assert game.player1.choice is not None
    assert sorted(game.player1.choice.cards, key=id) == sorted(summoned, key=id)
    illusion = game.player1.choice.cards[1]
    game.player1.choice.choose(illusion)
    marked = [m for m in summoned if any(b.id == "SCH_351e" for b in m.buffs)]
    assert marked == [illusion]
    illusion.divine_shield = False
    game.queue_actions(game.player2, [Hit(illusion, 1)])
    assert illusion.dead


def test_rattlegore_resummons_one_copy_with_minus_one():
    game = _game(CardClass.WARRIOR)
    rattlegore = game.player1.summon("SCH_621")
    game.player1.give(FIREBALL).play(target=rattlegore)
    game.player1.give(FIREBALL).play(target=rattlegore)
    assert len(game.player1.field) == 1
    second = game.player1.field[0]
    assert second.id == "SCH_621"
    assert second.atk == second.max_health == 8
    _refill(game)
    game.player1.give(FIREBALL).play(target=second)
    game.player1.give(FIREBALL).play(target=second)
    assert len(game.player1.field) == 1
    assert game.player1.field[0].atk == game.player1.field[0].max_health == 7


def test_blessing_of_authority_cant_attack_heroes_this_turn_only():
    game = _game(CardClass.PALADIN)
    wisp = game.player1.summon(WISP)
    _ready(wisp)
    game.player1.give("SCH_138").play(target=wisp)
    assert wisp.atk == 9 and wisp.health == 9
    assert game.player2.hero not in wisp.attack_targets
    game.end_turn()
    game.end_turn()
    assert wisp.atk == 9
    assert game.player2.hero in wisp.attack_targets


def test_power_word_feast_needs_a_minion():
    game = _game(CardClass.PRIEST)
    feast = game.player1.give("SCH_136")
    assert not feast.is_playable()
    yeti = game.player1.summon("CS2_182")
    assert feast.is_playable()
    assert feast.requires_target()
    feast.play(target=yeti)
    assert yeti.atk == 6 and yeti.max_health == 7
    game.player1.give(FIREBALL).play(target=yeti)
    assert yeti.damage == 6
    game.end_turn()
    assert yeti.damage == 0


def test_ancient_void_hound_drains_zero_attack_minions():
    game = _game(CardClass.DEMONHUNTER)
    hound = game.player1.give("SCH_354").play()
    totem = game.player2.summon("SCH_537")  # Trick Totem, 0/3
    yeti = game.player2.summon("CS2_182")
    game.end_turn()
    assert totem.atk == 0 and totem.health == 2
    assert yeti.atk == 3 and yeti.health == 4
    assert hound.atk == 12 and hound.health == 12


def test_nature_studies_next_spell_costs_one_less():
    game = _game(CardClass.DRUID)
    game.player1.give("SCH_333").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert game.player1.hand[0].type == CardType.SPELL
    fireball = game.player1.give(FIREBALL)
    frostbolt = game.player1.give("CS2_024")
    assert fireball.cost == 3 and frostbolt.cost == 1
    fireball.play(target=game.player2.hero)
    assert frostbolt.cost == 2
    assert game.player1.give(FIREBALL).cost == 4


def test_studies_reduce_the_discovered_card_and_the_next_one():
    studies = (
        ("SCH_300", CardClass.HUNTER, "EX1_096"),  # Carrion Studies, Loot Hoarder
        ("SCH_270", CardClass.SHAMAN, KOBOLD_GEOMANCER),  # Primordial Studies
        ("SCH_158", CardClass.WARLOCK, "CS2_065"),  # Demonic Studies, Voidwalker
        ("SCH_233", CardClass.PRIEST, "EX1_284"),  # Draconic Studies, Azure Drake
        ("SCH_237", CardClass.WARRIOR, "SCH_311"),  # Athletic Studies, Broomstick
    )
    for card_id, card_class, sample in studies:
        game = _game(card_class)
        with mock(RandomMinion, [sample]):
            game.player1.give(card_id).play()
        game.player1.choice.choose(game.player1.choice.cards[0])
        discovered = game.player1.hand[0]
        first = game.player1.give(sample)
        second = game.player1.give(sample)
        assert discovered.cost == max(0, discovered.data.cost - 1), card_id
        assert first.cost == second.cost == first.data.cost - 1, card_id
        first.play()
        assert second.cost == second.data.cost, card_id


def test_instructor_fireheart_repeats_when_the_spell_is_played_this_turn():
    game = _game(CardClass.SHAMAN)
    bolts = [game.player1.card("EX1_238") for _ in range(3)]  # Lightning Bolt, 1
    with mock(RandomSpell, bolts[:1]):
        game.player1.give("SCH_507").play()
    game.player1.choice.choose(bolts[0])
    assert game.player1.hand[:] == [bolts[0]]
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player1.choice is None
    with mock(RandomSpell, bolts[1:2]):
        bolts[0].play(target=game.player2.hero)
    assert game.player1.choice is not None
    game.player1.choice.choose(bolts[1])
    assert bolts[1] in game.player1.hand
    game.end_turn()
    game.end_turn()
    with mock(RandomSpell, bolts[2:]):
        bolts[1].play(target=game.player2.hero)
    assert game.player1.choice is None


def test_weighted_card_choice_offers_what_there_is_once():
    # A Discover in a pool bounded to a reservoir (Demonic Studies played by a
    # priest, Keymaster Alabaster's copy) can have fewer than three cards; a
    # dual-class card is both in the neutral pool and in its class's pool.
    from fireplace.utils import weighted_card_choice

    game = _game(CardClass.PRIEST)
    for _ in range(20):
        cards = weighted_card_choice(game.player1, [1, 1], [["SCH_145"], []], 3)
        assert [card.id for card in cards] == ["SCH_145"]
        cards = weighted_card_choice(
            game.player1, [1, 1], [["SCH_250", "SCH_145"], ["SCH_250"]], 3
        )
        assert sorted(card.id for card in cards) == ["SCH_145", "SCH_250"]


def test_enchanted_cauldron_casts_a_spell_of_the_same_cost():
    game = _game()
    cauldron = game.player1.give("SCH_157").play()
    assert cauldron.has_spellburst
    with mock(RandomSpell, [game.player1.card(MOONFIRE)]):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert not cauldron.has_spellburst
    # the Moonfire cast hits a character drawn at random
    lost = 60 - game.player1.hero.health - game.player2.hero.health
    assert lost + cauldron.damage == 2


def test_cabal_acolyte_on_a_full_board_destroys_the_minion():
    game = _game(CardClass.PRIEST)
    game.player1.give("SCH_120").play()
    for _ in range(6):
        game.player1.summon(WISP)
    enemy = game.player2.summon(WISP)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.field) == 7
    assert enemy.dead
    assert enemy.controller is game.player2


def test_robes_of_protection_stops_hero_powers():
    game = _game()
    game.player1.give("SCH_146").play()
    wisp = game.player1.summon(WISP)
    assert wisp not in game.player1.give(MOONFIRE).targets
    assert wisp not in game.player1.hero.power.targets
    game.end_turn()
    assert wisp not in game.player2.hero.power.targets


def test_flesh_giant_counts_every_change_during_your_turns():
    game = _game(CardClass.WARLOCK)
    giant = game.player1.give("SCH_140")
    game.player1.hero.power.use()  # Life Tap: 2 damage
    assert giant.cost == 9
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert giant.cost == 9
    game.end_turn()
    assert giant.cost == 9
    game.player1.give("CS2_007").play(target=game.player1.hero)  # Healing Touch
    assert giant.cost == 8


def test_argent_braggart_matches_the_highest():
    game = _game(CardClass.PALADIN)
    game.player2.summon("CS2_186")  # War Golem 7/7
    game.player1.summon("CS2_179")  # Sen'jin Shieldmasta 3/5
    braggart = game.player1.give("SCH_149").play()
    assert braggart.atk == 7 and braggart.health == 7


def test_argent_braggart_takes_attack_and_health_from_different_minions():
    game = _game(CardClass.PALADIN)
    game.player2.summon("CS2_213")  # Reckless Rocketeer 5/2
    game.player1.summon("CS2_179")  # Sen'jin Shieldmasta 3/5
    braggart = game.player1.give("SCH_149").play()
    assert braggart.atk == 5 and braggart.health == 5


def test_trueaim_crescent_makes_every_friendly_minion_attack():
    game = _game(CardClass.HUNTER)
    game.player1.give("SCH_279").play()
    first = game.player1.summon("CS2_120")  # 2/3
    second = game.player1.summon("CS2_120")
    golem = game.player2.summon("CS2_186")  # 7/7
    game.player1.hero.attack(golem)
    assert golem.damage == 1 + 2 + 2
    assert first.dead and second.dead
    assert game.player1.hero.health == 23


def test_trueaim_crescent_stops_when_the_target_dies():
    game = _game(CardClass.HUNTER)
    game.player1.give("SCH_279").play()
    first = game.player1.summon("CS2_182")  # 4/5
    second = game.player1.summon("CS2_182")
    target = game.player2.summon("CS2_179")  # Sen'jin 3/5
    game.player1.hero.attack(target)
    assert target.dead
    assert first.damage == 3
    assert second.damage == 0
    _ready(first, second)
    assert game.player2.hero in first.attack_targets


def test_combustion_excess_damages_both_neighbours():
    game = _game()
    left = game.player2.summon("CS2_182")
    middle = game.player2.summon("CS2_120")  # 2/3
    right = game.player2.summon("CS2_182")
    game.player1.give("SCH_348").play(target=middle)
    assert middle.dead
    assert left.damage == right.damage == 1


def test_combustion_spell_damage_counts_once():
    game = _game()
    game.player1.summon(KOBOLD_GEOMANCER)
    left = game.player2.summon("CS2_182")
    middle = game.player2.summon(WISP)
    right = game.player2.summon("CS2_182")
    game.player1.give("SCH_348").play(target=middle)
    assert left.damage == right.damage == 4


def test_professor_slate_makes_spells_poisonous():
    game = _game(CardClass.HUNTER)
    game.player1.give("SCH_539").play()
    golem = game.player2.summon("CS2_186")
    game.player1.give(MOONFIRE).play(target=golem)
    assert golem.dead
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 29


def test_rune_dagger_gives_spell_damage_this_turn():
    game = _game(CardClass.SHAMAN)
    game.player1.give("SCH_301").play()
    game.player1.hero.attack(game.player2.hero)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 1 - 2
    game.end_turn()
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 27 - 1


def test_totem_goliath_overloads():
    game = _game(CardClass.SHAMAN)
    game.player1.give("SCH_615").play()
    assert game.player1.overloaded == 1


def test_lake_thresher_damages_the_defenders_neighbours():
    game = _game()
    thresher = game.player1.summon("SCH_605")
    _ready(thresher)
    left = game.player2.summon(WISP)
    middle = game.player2.summon("CS2_182")
    right = game.player2.summon(WISP)
    thresher.attack(middle)
    assert left.dead and right.dead
    assert middle.damage == 4


def test_brittlebone_destroyer_after_your_heros_health_changed():
    game = _game(CardClass.WARLOCK)
    yeti = game.player2.summon("CS2_182")
    destroyer = game.player1.give("SCH_513")
    assert not destroyer.requires_target()
    game.player1.hero.power.use()
    assert destroyer.requires_target()
    assert yeti in destroyer.targets
    destroyer.play(target=yeti)
    assert yeti.dead


def test_shadowlight_scholar_needs_a_soul_fragment():
    game = _game(CardClass.WARLOCK)
    scholar = game.player1.give("SCH_517")
    assert not scholar.requires_target()
    game.player1.give("SCH_700").play()
    assert scholar.requires_target()
    scholar.play(target=game.player2.hero)
    assert game.player2.hero.health == 27
    assert len(game.player1.deck) == 1


def test_groundskeeper_needs_a_spell_of_five_or_more():
    game = _game(CardClass.DRUID)
    game.player1.hero.set_current_health(20)
    keeper = game.player1.give("SCH_613")
    game.player1.give("CS2_186")  # a minion that costs 7 is not a spell
    assert not keeper.requires_target()
    game.player1.give(PYROBLAST)
    assert keeper.requires_target()
    keeper.play(target=game.player1.hero)
    assert game.player1.hero.health == 25


def test_secret_passage_swaps_back_at_end_of_turn():
    game = _game(CardClass.ROGUE)
    for card_id in ("CS2_182", "CS2_120", "CS2_186", "CS2_179", "CS2_172"):
        game.player1.give(card_id).shuffle_into_deck()
    original = [game.player1.give(FIREBALL), game.player1.give(MOONFIRE)]
    game.player1.give("SCH_305").play()
    taken = game.player1.hand[:]
    assert len(taken) == 4 and all(card.zone == Zone.HAND for card in taken)
    assert len(game.player1.deck) == 1
    game.player1.give(WISP)  # a card gained after the Passage is kept
    game.end_turn()
    assert [card.id for card in game.player1.hand] == [WISP, FIREBALL, MOONFIRE]
    assert game.player1.hand[1:] == original
    assert len(game.player1.deck) == 5


def test_vectus_whelps_copy_a_deathrattle():
    game = _game(CardClass.WARLOCK)
    hoarder = game.player1.summon("EX1_096")  # Loot Hoarder
    game.player1.give(FIREBALL).play(target=hoarder)
    vectus = game.player1.give("SCH_162").play()
    whelps = game.player1.field[1:]
    assert [card.id for card in whelps] == ["SCH_162t", "SCH_162t"]
    assert not vectus.has_deathrattle
    for whelp in whelps:
        assert whelp.has_deathrattle
    game.player1.give(WISP).shuffle_into_deck()
    _refill(game)
    game.player1.give(MOONFIRE).play(target=whelps[0])
    assert len(game.player1.hand) == 1


def _transfer_student_on_board(board):
    class FixedBoardGame(BaseTestGame):
        def setup(self):
            super().setup()
            self.skin = board

    game = prepare_game(
        CardClass.MAGE,
        CardClass.MAGE,
        include=("SCH_199",),
        game_class=FixedBoardGame,
    )
    student = next(
        card
        for card in [*game.player1.hand, *game.player1.deck]
        if card.id.startswith("SCH_199")
    )
    if student.zone != Zone.HAND:
        student.zone = Zone.HAND
    return game, student


def test_transfer_student_uses_orgrimmar_battlecry():
    from fireplace.enums import BoardEnum

    game, student = _transfer_student_on_board(BoardEnum.ORGRIMMAR)
    assert student.id == "SCH_199t2"
    student.play(target=game.player2.hero)
    assert game.player2.hero.health == 28


def test_transfer_student_on_scholomance_adds_a_dual_class_card():
    from fireplace.enums import BoardEnum

    game, student = _transfer_student_on_board(BoardEnum.SCHOLOMANCE)
    assert student.id == "SCH_199t23"
    game.player1.discard_hand()
    student.zone = Zone.HAND
    student.play()
    assert len(game.player1.hand) == 1
    assert len(game.player1.hand[0].classes) >= 2


def test_transfer_student_on_stormwind_has_no_discover_battlecry():
    from fireplace.enums import BoardEnum

    game, student = _transfer_student_on_board(BoardEnum.STORMWIND)
    assert student.id == "SCH_199t"
    student.play()
    assert game.player1.choice is None


def test_troublemaker_summons_a_ruffian_on_each_side_of_itself():
    # D-108, A109 (rule 80a): two minions summoned at once by a minion in play
    # stand one on each side of it.
    game = _game(CardClass.WARRIOR)
    game.player1.give("SCH_337").play()
    game.end_turn()
    assert [m.id for m in game.player1.field] == ["SCH_337t", "SCH_337", "SCH_337t"]


def test_archwitch_willow_summons_its_two_demons_on_each_side_of_itself():
    # D-108, A109 (rule 80a): the Demon of the hand on its right, the Demon of
    # the deck on its left.
    game = _game(CardClass.WARLOCK)
    game.player1.give("CS2_065").zone = Zone.HAND  # Voidwalker, in hand
    game.player1.give("EX1_319").shuffle_into_deck()  # Flame Imp, in deck
    willow = game.player1.give("SCH_181").play()
    assert [m.id for m in game.player1.field] == ["EX1_319", "SCH_181", "CS2_065"]
    assert game.player1.field[1] is willow
