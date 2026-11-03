from utils import *


def test_griftah():
    game = prepare_empty_game()
    game.player1.give("TRL_096").play()
    card1 = game.player1.choice.cards[0]
    game.player1.choice.choose(card1)
    card2 = game.player1.choice.cards[0]
    game.player1.choice.choose(card2)
    if card1.id != card2.id:
        assert (
            game.player1.hand[0].id == card1.id and game.player2.hand[1].id == card2.id
        ) ^ (
            game.player1.hand[0].id == card2.id and game.player2.hand[1].id == card1.id
        )
    else:
        assert game.player1.hand[0].id == card1.id
        assert game.player2.hand[1].id == card1.id
    assert not game.player1.choice


def test_hakkar():
    game = prepare_empty_game()
    hakkar = game.player1.give("TRL_541").play()
    hakkar.destroy()
    assert len(game.player1.deck) == 1
    assert game.player1.deck[0].id == "TRL_541t"
    assert len(game.player2.deck) == 1
    assert game.player2.deck[0].id == "TRL_541t"
    game.end_turn()
    assert len(game.player2.deck) == 2
    assert game.player2.deck[0].id == "TRL_541t"
    assert game.player2.deck[1].id == "TRL_541t"
    assert game.player2.hero.health == 27
    game.skip_turn()
    assert game.player2.hero.health == 21
    assert len(game.player2.deck) == 4


def test_hakkar_full():
    game = prepare_empty_game()
    game.player1.give("KAR_712").play()
    for _ in range(60):
        blood = game.player1.give("TRL_541t")
        blood.shuffle_into_deck()
    assert len(game.player1.deck) == 60
    game.skip_turn()
    assert len(game.player1.deck) == 60


def test_overkill():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    game.end_turn()
    direhorn = game.player2.give("TRL_232").play()
    game.skip_turn()
    direhorn.attack(wisp)
    assert len(game.player2.field) == 2


def test_overkill_spell():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    arrow = game.player1.give("TRL_347")
    arrow.play(target=wisp)
    assert len(game.player1.field) == 1


def test_snapjaw_shellfighter():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    shellfighter = game.player1.give("TRL_535").play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert wisp.damage == 0
    assert shellfighter.damage == 1


def test_two_snapjaw_shellfighters():
    game = prepare_game()
    shellfighter1 = game.player1.give("TRL_535").play()
    shellfighter2 = game.player1.give("TRL_535").play()
    game.player1.give(MOONFIRE).play(target=shellfighter1)
    assert shellfighter1.damage == 0
    assert shellfighter2.damage == 1


def test_treespeaker():
    game = prepare_game()
    game.player1.give("EX1_571").play()
    game.player1.give(WISP).play()
    game.player1.give("TRL_341").play()
    assert len(game.player1.field) == 5
    for i in range(3):
        assert game.player1.field[i].id == "TRL_341t"
    assert game.player1.field[3].id == WISP
    assert game.player1.field[4].id == "TRL_341"


def test_mass_hysteria():
    game = prepare_game()
    for _ in range(7):
        game.player1.give(WISP).play()
    game.player1.give("TRL_258").play()
    assert len(game.player1.field) == 1


def test_high_priest_thekal():
    game = prepare_game()
    game.player1.give("TRL_308").play()
    assert game.player1.hero.health == 1
    assert game.player1.hero.armor == 29


def test_spectral_cutlass():
    game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
    weapon = game.player1.give("GIL_672").play()
    durability = weapon.durability
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert weapon.durability == durability + 1


def test_stolen_steel():
    game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("TRL_156").play()
    assert game.player1.choice
    cards = game.player1.choice.cards
    for card in cards:
        assert card.card_class != CardClass.ROGUE
    game.player1.choice.choose(cards[0])


def test_masters_call():
    game = prepare_empty_game()
    beasts = ["NEW1_032", "NEW1_033", "NEW1_034"]
    for beast in beasts:
        game.player1.give(beast).shuffle_into_deck()
    game.player1.give("TRL_339").play()
    assert not game.player1.choice
    assert len(game.player1.hand) == 3

    game = prepare_empty_game()
    minions = [WISP, "NEW1_033", "NEW1_034"]
    for minion in minions:
        game.player1.give(minion).shuffle_into_deck()
    game.player1.give("TRL_339").play()
    assert game.player1.choice
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert len(game.player1.hand) == 1


def test_pyromaniac():
    game = prepare_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("TRL_315").play()
    wisp = game.player1.give(WISP).play()
    hand = len(game.player1.hand)
    game.player1.hero.power.use(target=wisp)
    assert len(game.player1.hand) == hand + 1


def test_janalai_the_dragonhawk():
    game = prepare_game(CardClass.HUNTER, CardClass.HUNTER)
    janalai = game.player1.give("TRL_316")
    assert not janalai.powered_up
    for _ in range(4):
        game.player1.hero.power.use()
        game.skip_turn()
    assert janalai.powered_up
    janalai.play()
    assert len(game.player1.field) == 2


def test_spirit_of_the_dragonhawk():
    game = prepare_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("TRL_319").play()
    game.end_turn()
    for _ in range(3):
        game.player2.give(WISP).play()
    game.end_turn()
    assert len(game.player2.field) == 3
    game.player1.hero.power.use(target=game.player2.field[1])
    assert len(game.player2.field) == 0


def test_daring_fire_eater():
    game = prepare_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("TRL_319").play()
    game.end_turn()
    for _ in range(3):
        game.player2.give(MECH).play()
    game.end_turn()
    game.player1.give("TRL_390").play()
    game.player1.hero.power.use(target=game.player2.field[1])
    for i in range(3):
        assert game.player2.field[i].damage == 3
    game.skip_turn()
    game.player1.hero.power.use(target=game.player2.field[1])
    for i in range(3):
        assert game.player2.field[i].damage == 4


def test_zuljin():
    game = prepare_game()
    game.player1.give(THE_COIN).play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player1.temp_mana == 0
    game.player1.give("TRL_065").play()
    assert game.player1.temp_mana == 1


def test_sulthraze():
    game = prepare_game()
    wisps = [game.player1.give(WISP).play() for _ in range(4)]
    game.end_turn()
    game.player2.give("TRL_325").play()
    for wisp in wisps:
        assert game.player2.hero.can_attack()
        game.player2.hero.attack(wisp)
    assert not game.player2.hero.can_attack()


def test_summon_tiger():
    game = prepare_game()
    game.player1.give("TRL_309").play()
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    tiger = game.player1.field[1]
    assert tiger.cost == 4
    assert tiger.atk == 4
    assert tiger.health == 4
    game.player1.give(SILENCE).play(target=tiger)
    assert tiger.cost == 4
    assert tiger.atk == 4
    assert tiger.health == 4
    game.end_turn()

    game.player2.give("EX1_564").play(target=tiger)
    copy_tiger = game.player2.field[0]
    assert copy_tiger.cost == 4
    assert copy_tiger.atk == 4
    assert copy_tiger.health == 4


def test_mojomaster_zihi():
    game = prepare_game()
    zihi = game.player1.give("TRL_564").play()
    assert game.player1.max_mana == 5
    assert game.player2.max_mana == 5
    assert game.player1.mana == 10 - zihi.cost
    assert game.player2.mana == 5

    game2 = prepare_game(game_class=Game)
    for _ in range(5):
        game2.player1.give(THE_COIN).play()
    game2.player1.give("TRL_564").play()
    assert game2.player1.max_mana == 5
    assert game2.player2.max_mana == 5
    assert game2.player1.mana == 0
    assert game2.player2.mana == 0

    game3 = prepare_game(game_class=Game)
    for _ in range(10):
        game3.player1.give(THE_COIN).play()
    game3.player1.give("TRL_564").play()
    assert game3.player1.max_mana == 5
    assert game3.player2.max_mana == 5
    assert game3.player1.mana == 10 - zihi.cost
    assert game3.player2.mana == 0


def test_heavy_metal():
    game = prepare_game()
    game.player1.give("TRL_324").play()
    assert game.player1.field[0].cost == 0
    game.skip_turn()
    game.player1.give("LOOT_285t").play()
    game.skip_turn()
    assert game.player1.hero.armor == 15
    game.player1.give("TRL_324").play()
    assert game.player1.field[1].cost == 10


def test_wartbringer():
    game = prepare_game()
    wartbringer = game.player1.give("TRL_522")
    assert not wartbringer.powered_up
    assert not wartbringer.requires_target()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert not wartbringer.powered_up
    assert not wartbringer.requires_target()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert wartbringer.powered_up
    assert wartbringer.requires_target()


def test_kragwa_the_frog():
    game = prepare_empty_game()
    frog = game.player1.give("TRL_345")
    for _ in range(4):
        game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.skip_turn()
    assert game.player1.hand == [frog]
    frog.play()
    assert game.player1.hand == [MOONFIRE] * 4


# WP-188 : les cartes de Rastakhan's Rumble qui jouaient autrement que leur texte.


def test_drakkari_trickster_gives_from_the_opponent_deck():
    # "Give each player a copy of a random card from their opponent's deck."
    game = prepare_empty_game()
    game.player1.give(WISP).shuffle_into_deck()
    game.player2.give(FIREBALL).shuffle_into_deck()
    game.player1.give("TRL_527").play()
    assert game.player1.hand[-1].id == FIREBALL
    assert game.player2.hand[-1].id == WISP
    assert len(game.player1.deck) == 1
    assert len(game.player2.deck) == 1


def test_scorch_costs_one_after_an_elemental():
    # "Costs (1) if you played an Elemental last turn" : 1, pas 4 - 1.
    game = prepare_game()
    scorch = game.player1.give("TRL_313")
    assert scorch.cost == 4
    game.player1.give(ELEMENTAL).play()
    game.end_turn()
    game.end_turn()
    assert scorch.cost == 1
    game.end_turn()
    game.end_turn()
    assert scorch.cost == 4


def test_zandalari_templar_gains_taunt():
    game = prepare_game()
    game.player1.hero.set_current_health(15)
    for _ in range(4):
        game.player1.give("TRL_128").play(target=game.player1.hero)
    templar = game.player1.give("TRL_545").play()
    assert templar.atk == 8
    assert templar.health == 8
    assert templar.taunt


def test_threshold_card_text_says_what_is_left():
    # ThresholdUtils: the "({0} left!)" of Zandalari Templar and Jan'alai.
    game = prepare_game()
    game.player1.hero.set_current_health(20)
    templar = game.player1.give("TRL_545")
    assert "(10 left!)" in templar.description
    game.player1.give("TRL_128").play(target=game.player1.hero)
    assert "(7 left!)" in templar.description
    for _ in range(3):
        game.player1.give("TRL_128").play(target=game.player1.hero)
    assert "(Ready!)" in templar.description


def test_zandalari_templar_not_ready():
    game = prepare_game()
    game.player1.hero.set_current_health(25)
    game.player1.give("TRL_128").play(target=game.player1.hero)
    templar = game.player1.give("TRL_545").play()
    assert templar.atk == 4
    assert not templar.taunt


def test_time_out_makes_the_hero_immune():
    game = prepare_game()
    game.player1.give("TRL_302").play()
    assert game.player1.hero.immune
    game.end_turn()
    game.player2.give("CS2_062").play()  # Hellfire
    assert game.player1.hero.health == 30
    game.end_turn()
    assert not game.player1.hero.immune
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert game.player1.hero.health == 29


def test_farraki_battleaxe_buffs_one_minion_in_hand():
    game = prepare_empty_game()
    wisp1 = game.player1.give(WISP)
    wisp2 = game.player1.give(WISP)
    game.player1.give("TRL_304").play()
    wisp = game.player2.summon(WISP)
    game.player1.hero.attack(wisp)
    assert sorted([wisp1.atk, wisp2.atk]) == [1, 3]
    assert sorted([wisp1.health, wisp2.health]) == [1, 3]


def test_spirit_of_the_dead_shuffles_a_one_cost_copy():
    game = prepare_empty_game()
    game.player1.give("TRL_502").play()
    raptor = game.player1.give("CS2_172").play()
    game.player1.give(FIREBALL).play(target=raptor)
    assert raptor.dead
    assert len(game.player1.deck) == 1
    copy = game.player1.deck[0]
    assert copy.id == "CS2_172"
    assert copy.cost == 1
    # Un serviteur adverse mort ne compte pas.
    wisp = game.player2.summon(WISP)
    game.player1.give(MOONFIRE).play(target=wisp)
    assert len(game.player1.deck) == 1


def test_spirit_of_the_bat_buffs_a_minion_in_hand():
    game = prepare_empty_game()
    game.player1.give("TRL_251").play()
    wisp = game.player1.give(WISP).play()
    in_hand = game.player1.give(WISP)
    game.player1.give(MOONFIRE).play(target=wisp)
    assert in_hand.atk == 2
    assert in_hand.health == 2


def test_blood_troll_sapper_hits_the_enemy_hero():
    game = prepare_empty_game()
    game.player1.give("TRL_257").play()
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert game.player2.hero.health == 28
    assert game.player1.hero.health == 30
    enemy = game.player2.summon(WISP)
    game.player1.give(MOONFIRE).play(target=enemy)
    assert game.player2.hero.health == 28


def test_bloodsail_howler_counts_other_pirates():
    game = prepare_empty_game()
    howler = game.player1.give("TRL_071").play()
    assert howler.atk == 1
    assert howler.health == 1
    game.player1.give("CS2_146").play()
    howler2 = game.player1.give("TRL_071").play()
    assert howler2.atk == 3
    assert howler2.health == 3


def test_gonk_lets_the_hero_attack_again():
    game = prepare_empty_game()
    game.player1.give("TRL_241").play()
    game.player1.give("TRL_243").play()
    wisp = game.player2.summon(WISP)
    yeti = game.player2.summon("CS2_182")
    game.player1.hero.attack(wisp)
    assert game.player1.hero.can_attack()
    game.player1.hero.attack(yeti)
    assert not game.player1.hero.can_attack()


def test_grave_horror_ignores_countered_spells():
    game = prepare_empty_game()
    horror = game.player1.give("TRL_408")
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert horror.cost == 11
    game.end_turn()
    game.player2.give("EX1_287").play()
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert horror.cost == 11


def test_masters_call_leaves_the_others_in_the_deck():
    game = prepare_empty_game()
    for minion in [WISP, "NEW1_033", "NEW1_034"]:
        game.player1.give(minion).shuffle_into_deck()
    game.player1.give("TRL_339").play()
    assert game.player1.choice
    chosen = game.player1.choice.cards[0]
    game.player1.choice.choose(chosen)
    assert [c.id for c in game.player1.hand] == [chosen.id]
    assert len(game.player1.deck) == 2
    assert chosen.id not in [c.id for c in game.player1.deck]


def test_void_contract_destroys_half_rounded_up():
    game = prepare_empty_game()
    for _ in range(5):
        game.player1.give(WISP).shuffle_into_deck()
    for _ in range(4):
        game.player2.give(WISP).shuffle_into_deck()
    game.player1.give("TRL_246").play()
    assert len(game.player1.deck) == 2
    assert len(game.player2.deck) == 2


def test_spirit_of_the_tiger_reads_the_cost_paid():
    game = prepare_empty_game()
    game.player1.give("TRL_309").play()
    game.end_turn()
    game.end_turn()
    game.player1.give("EX1_608").play()  # Sorcerer's Apprentice
    fireball = game.player1.give(FIREBALL)
    assert fireball.cost == 3
    fireball.play(target=game.player2.hero)
    tigers = [m for m in game.player1.field if m.id == "TRL_309t"]
    assert len(tigers) == 1
    tiger = tigers[0]
    assert tiger.atk == 3
    assert tiger.health == 3


def test_spirit_of_the_tiger_ignores_zero_cost_spells():
    game = prepare_empty_game()
    game.player1.give("TRL_309").play()
    game.player1.give(THE_COIN).play()
    assert len(game.player1.field) == 1
    assert not [c for c in game.player1.graveyard if c.id == "TRL_309t"]


def test_zentimo_casts_on_the_neighbours():
    game = prepare_empty_game()
    game.player1.give("TRL_085").play()
    left = game.player2.summon("CS2_182")
    middle = game.player2.summon("CS2_182")
    right = game.player2.summon("CS2_182")
    game.player1.give(MOONFIRE).play(target=middle)
    assert left.damage == 1
    assert middle.damage == 1
    assert right.damage == 1
    assert game.player2.hero.health == 30


def test_likkim_while_overload_is_owed_or_locked():
    game = prepare_empty_game(CardClass.SHAMAN, CardClass.SHAMAN)
    likkim = game.player1.give("TRL_352").play()
    assert likkim.atk == 1
    game.player1.give("EX1_238").play(target=game.player2.hero)
    assert likkim.atk == 3
    assert game.player1.hero.atk == 3
    game.end_turn()
    game.end_turn()
    assert likkim.atk == 3
    game.end_turn()
    game.end_turn()
    assert likkim.atk == 1


def test_spirit_of_the_shark_battlecries_and_combos_twice():
    game = prepare_empty_game()
    game.player1.give("TRL_092").play()
    game.player1.give("CS2_189").play(target=game.player2.hero)  # Elven Archer
    assert game.player2.hero.health == 28
    game.player1.give("EX1_134").play(target=game.player2.hero)  # SI:7 Agent, combo
    assert game.player2.hero.health == 24


def test_masked_contender_skips_an_active_secret():
    for _ in range(12):
        game = prepare_empty_game()
        game.player1.give("EX1_289").play()  # Ice Barrier
        game.player1.give("EX1_289").shuffle_into_deck()
        game.player1.give("EX1_295").shuffle_into_deck()  # Ice Block
        game.player1.give("TRL_530").play()
        assert sorted(s.id for s in game.player1.secrets) == ["EX1_289", "EX1_295"]
        assert [c.id for c in game.player1.deck] == ["EX1_289"]


def test_masked_contender_without_secret():
    game = prepare_empty_game()
    game.player1.give("EX1_295").shuffle_into_deck()
    game.player1.give("TRL_530").play()
    assert not game.player1.secrets
    assert len(game.player1.deck) == 1


def test_spellzerker_spell_damage_while_damaged():
    game = prepare_empty_game()
    spellzerker = game.player1.give("TRL_312").play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 29
    game.player1.give(MOONFIRE).play(target=spellzerker)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 26


def test_untamed_beastmaster_buffs_a_drawn_beast():
    game = prepare_empty_game()
    game.player1.give("TRL_405").play()
    game.player1.give("CS2_172").shuffle_into_deck()  # Bloodfen Raptor, 3/2
    game.player1.draw()
    raptor = game.player1.hand[-1]
    assert raptor.atk == 5
    assert raptor.health == 4
    game.player1.give(WISP).shuffle_into_deck()
    game.player1.draw()
    assert game.player1.hand[-1].atk == 1


def test_auchenai_phantasm_heals_deal_damage_this_turn():
    game = prepare_empty_game()
    game.player1.give("TRL_501").play()
    game.player1.give("TRL_128").play(target=game.player2.hero)
    assert game.player2.hero.health == 27
    game.end_turn()
    game.end_turn()
    # The next turn, healing heals again.
    game.player1.give("TRL_128").play(target=game.player2.hero)
    assert game.player2.hero.health == 30


def test_two_shellfighters_only_the_first_takes_it():
    game = prepare_empty_game()
    first = game.player1.give("TRL_535").play()
    wisp = game.player1.give(WISP).play()
    second = game.player1.give("TRL_535").play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert wisp.damage == 0
    assert first.damage == 1
    assert second.damage == 0


def test_stolen_steel_never_offers_a_neutral_weapon():
    # Sphere of Sapience (SCH_259) is the one neutral collectible weapon.
    for _ in range(60):
        game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
        game.player1.give("TRL_156").play()
        cards = game.player1.choice.cards
        assert len(cards) == 3
        for card in cards:
            assert card.type == CardType.WEAPON
            assert card.card_class not in (CardClass.ROGUE, CardClass.NEUTRAL)
        game.player1.choice.choose(cards[0])


def test_zuljin_casts_a_choose_one_spell():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    yeti = game.player2.summon("CS2_182")
    game.player1.give("EX1_154").play(choose="EX1_154a", target=yeti)  # Wrath, 3
    assert yeti.health == 2
    game.end_turn()
    game.end_turn()
    game.player1.give("TRL_065").play()
    # Either option: 3 damage, or 1 damage and a card; the only target is the
    # Yeti for 3 (heroes can not be its target), so it is dead or at 1.
    assert yeti.dead or yeti.health == 1


def test_zuljin_does_not_cast_an_active_secret_again():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    game.player1.give("EX1_554").play()  # Snake Trap
    game.player1.give("EX1_610").play()  # Explosive Trap
    game.end_turn()
    game.end_turn()
    game.player1.give("TRL_065").play()
    assert sorted(s.id for s in game.player1.secrets) == ["EX1_554", "EX1_610"]
    assert game.player1.hero.armor == 5


def test_pyromaniac_draws_for_each_minion_the_hero_power_kills():
    # Spirit of the Dragonhawk: the neighbours of the target die too, and each
    # of their deaths counts for Pyromaniac (A125).
    game = prepare_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("TRL_315").play()
    game.player1.give("TRL_319").play()
    game.end_turn()
    game.player2.give(WISP).play()
    yeti = game.player2.give("CS2_182").play()
    game.player2.give(WISP).play()
    game.end_turn()
    assert game.player2.field.index(yeti) == 1
    hand = len(game.player1.hand)
    game.player1.hero.power.use(target=yeti)
    assert len(game.player2.field) == 1
    assert yeti.damage == 1
    assert len(game.player1.hand) == hand + 2


def test_zuljin_does_not_cast_a_countered_spell():
    game = prepare_empty_game(CardClass.HUNTER, CardClass.MAGE)
    yeti = game.player2.summon("CS2_182")
    game.end_turn()
    game.player2.give("EX1_287").play()  # Counterspell
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=yeti)
    assert yeti.damage == 0
    assert not game.player2.secrets
    game.end_turn()
    game.end_turn()
    game.player1.give("TRL_065").play()
    # The countered Moonfire is not cast again, on whatever target it picks.
    assert yeti.damage == 0
    assert game.player1.hero.damage == 0
    assert game.player2.hero.damage == 0
