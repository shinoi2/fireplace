from utils import *
from utils import _empty_mulligan


def test_lucentbark():
    game = prepare_game()
    lucentbark = game.player1.give("DAL_357").play()
    lucentbark.destroy()
    spirit = game.player1.field[0]
    assert spirit.id == "DAL_357t"
    game.player1.hero.set_current_health(25)
    game.player1.give("AT_055").play(target=game.player1.hero)
    new_lucentbark = game.player1.field[0]
    assert new_lucentbark.id == "DAL_357"


def test_keeper_stalladris():
    game = prepare_empty_game()
    game.player1.give("DAL_732").play()
    wild = game.player1.give("EX1_160")
    wild.play(choose="EX1_160a")
    assert game.player1.hand[0].id == "EX1_160a"
    assert game.player1.hand[1].id == "EX1_160b"


def test_lifeweaver():
    game = prepare_empty_game()
    game.player1.give("DAL_355").play()
    game.player1.hero.set_current_health(25)
    game.player1.give("AT_055").play(target=game.player1.hero)
    assert len(game.player1.hand) == 1
    game.end_turn()
    game.player2.hero.set_current_health(25)
    game.player2.give("AT_055").play(target=game.player2.hero)
    assert len(game.player1.hand) == 1


def test_nine_lives():
    game = prepare_game()
    nine_lives = game.player1.give("DAL_377")
    assert not nine_lives.is_playable()

    gnome = game.player1.give("EX1_029")
    gnome.destroy()

    nine_lives.play()
    assert game.player1.choice
    cards = game.player1.choice.cards
    assert len(cards) == 1
    assert cards[0].id == gnome.id

    count = len(game.player1.hand)
    health = game.player2.hero.health
    game.player1.choice.choose(cards[0])
    assert len(game.player1.hand) == count + 1
    assert game.player2.hero.health == health - 2


def test_khadgar():
    game = prepare_game()
    game.player1.give("DAL_575").play()
    game.player1.give("CFM_315").play()
    assert len(game.player1.field) == 4
    game.end_turn()
    game.player2.give("DAL_575").play()
    game.player2.give("DAL_575").play()
    game.player2.give("CFM_315").play()
    assert len(game.player2.field) == 6


def test_kalecgos():
    game = prepare_game()
    fireball = game.player1.give(FIREBALL)
    assert fireball.cost == 4
    game.player1.give("DAL_609").play()
    game.player1.choice.choose(game.player1.choice.cards[0])
    assert fireball.cost == 0
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4


def test_unseen_saboteur():
    game = prepare_empty_game()
    game.player2.discard_hand()
    blast = game.player2.give("DS1_233")
    game.player1.give("DAL_538").play()
    assert game.player1.hero.health == 25
    assert blast.zone == Zone.GRAVEYARD


def test_barista_lynchen():
    # "each of your other Battlecry minions": those on the board, from left to
    # right (hearthstone.wiki.gg); the hand is not read (WP-189).
    game = prepare_empty_game()
    for _ in range(3):
        game.player1.give("EX1_015")
    game.player1.summon("EX1_015")
    game.player1.summon(WISP)
    game.player1.summon("CS2_189")
    game.player1.give("DAL_546").play()
    assert game.player1.hand == ["EX1_015"] * 3 + ["EX1_015", "CS2_189"]


def test_archivist_elysiana():
    game = prepare_game()
    game.player1.give("DAL_736").play()
    cards = []
    for _ in range(5):
        choice = game.player1.choice
        cards.append(choice.cards[0].id)
        choice.choose(choice.cards[0])
    assert len(game.player1.deck) == 10
    assert sorted([card.id for card in game.player1.deck]) == sorted(cards * 2)


def test_jepetto_joybuzz():
    game = prepare_empty_game()
    for _ in range(2):
        game.player1.give("EX1_543").shuffle_into_deck()
    game.player1.give("DAL_752").play()
    assert game.player1.hand == ["EX1_543"] * 2
    for _ in range(2):
        card = game.player1.hand[0]
        assert card.cost == 1
        assert card.atk == 1
        assert card.health == 1
        card.play()
        assert card.cost == 9
        assert card.atk == 1
        assert card.health == 1


def test_commander_rhyssa():
    game = prepare_game(CardClass.WARLOCK, CardClass.WARLOCK)
    game.player1.give("LOE_021").play()
    game.player1.give("DAL_573").play()
    game.end_turn()

    assert game.player2.hero.health == 30
    game.player2.hero.power.use()
    assert game.player2.hero.health == 30 - 5 - 5 - 2


def test_madame_lazul():
    game = prepare_game()
    game.player2.discard_hand()
    game.player2.give(WISP)
    game.player2.give(MURLOC)
    game.player2.give(CHICKEN)
    game.player1.give("DAL_729").play()
    choice = game.player1.choice
    assert WISP in choice.cards
    assert MURLOC in choice.cards
    assert CHICKEN in choice.cards
    choice.choose(choice.cards[0])
    assert not game.player1.choice


def test_lazuls_scheme():
    game = prepare_game()
    # Turn 1
    scheme = game.player1.give("DAL_011")
    game.end_turn()
    dragon = game.player2.give("NEW1_030").play()
    assert dragon.atk == 12
    game.end_turn()
    # Turn 2
    game.skip_turn()
    # Turn 3
    game.skip_turn()
    # Turn 4
    scheme.play(target=dragon)
    assert dragon.atk == 12 - 4
    game.end_turn()
    assert dragon.atk == 12 - 4
    game.end_turn()
    assert dragon.atk == 12


def test_forbidden_words():
    game = prepare_game()
    words = game.player1.give("DAL_723")
    assert not words.is_playable()
    game.end_turn()

    minion_12 = game.player2.summon("CFM_712_t12")
    minion_10 = game.player2.summon("CFM_712_t10")
    minion_8 = game.player2.summon("CFM_712_t08")
    minion_6 = game.player2.summon("CFM_712_t06")
    minion_4 = game.player2.summon("CFM_712_t04")
    minion_2 = game.player2.summon("CFM_712_t02")

    game.end_turn()
    assert words.is_playable()
    assert minion_12 not in words.play_targets
    assert words.play_targets == [minion_10, minion_8, minion_6, minion_4, minion_2]
    game.player1.pay_cost(game.player1, 4)
    assert words.play_targets == [minion_6, minion_4, minion_2]
    words.play(target=minion_4)
    assert minion_4.dead
    assert game.player1.mana == 0


def test_tak_nozwhisker():
    game = prepare_empty_game()
    game.player1.give("DAL_719").play()
    game.player1.give("CFM_602").play(choose="CFM_602b")
    assert game.player1.hand == ["CFM_602"] * 3
    assert game.player1.deck == ["CFM_602"] * 3


def test_swampqueen_hagatha():
    game = prepare_empty_game()
    game.player1.give("DAL_431").play()
    choice = game.player1.choice
    assert choice
    card1 = choice.cards[0]
    choice.choose(card1)
    choice = game.player1.choice
    assert choice
    card2 = choice.cards[0]
    choice.choose(card2)

    horror = game.player1.hand[0]
    assert horror.id == "DAL_431t"
    assert horror.entity_1 == card1.id
    assert horror.entity_2 == card2.id
    assert horror.overload == card1.overload + card2.overload


def test_darkest_hour():
    game = prepare_empty_game()
    for _ in range(4):
        game.player1.give(WISP).play()
        game.player1.give(CHICKEN).shuffle_into_deck()
    game.player1.give("DAL_173").play()
    assert game.player1.field == [CHICKEN] * 4
    assert len(game.player1.deck) == 0


def test_plot_twist():
    game = prepare_game()
    count = len(game.player1.hand)
    game.player1.give("DAL_602").play()
    assert len(game.player1.hand) == count


def test_dimensional_ripper():
    game = prepare_empty_game()
    game.player1.give(WISP).shuffle_into_deck()
    game.player1.give(CHICKEN).shuffle_into_deck()
    game.player1.give("DAL_059").play()
    assert (game.player1.field == [WISP] * 2) ^ (game.player1.field == [CHICKEN] * 2)


def test_zayle():
    player1 = Player("Player1", ["DAL_800"], "DAL_800h")
    player2 = Player("Player1", ["DAL_800"], "DAL_800h")
    game = BaseTestGame(players=(player1, player2))
    game.start()
    assert len(game.player1.starting_deck) == 30
    assert len(game.player2.starting_deck) == 30


def test_twin_spell():
    game = prepare_game()
    twin_spell = game.player1.give("DAL_141")
    game.player1.give("EX1_095").play()
    while len(game.player1.hand) < game.player1.max_hand_size:
        game.player1.give(WISP)
    twin_spell.play()
    assert game.player1.hand[-1].id == "DAL_141ts"


def test_duel():
    game1 = prepare_empty_game()
    game1.player1.give("DAL_731").play()
    assert len(game1.player1.field) == 0
    assert len(game1.player1.field) == 0

    game2 = prepare_empty_game()
    game2.player1.give(MECH).shuffle_into_deck()
    game2.player2.give(MECH).shuffle_into_deck()
    game2.player1.give("DAL_731").play()
    assert game2.player1.field == [MECH]
    assert game2.player1.field == [MECH]
    assert len(game2.player1.deck) == 0
    assert len(game2.player1.deck) == 0
    assert game2.player1.field[0].damage == 1
    assert game2.player2.field[0].damage == 1

    game3 = prepare_empty_game()
    game3.player1.give(MECH).shuffle_into_deck()
    game3.player2.give(MECH).shuffle_into_deck()
    for _ in range(7):
        game3.player1.summon(WISP)
        game3.player2.summon(WISP)
    duel = game3.player1.give("DAL_731")
    assert not duel.is_playable()


def test_sweeping_strikes():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    sweeping_strikes = game.player1.give("DAL_062")
    sweeping_strikes.play(target=wisp)
    game.skip_turn()
    wisp.attack(game.player2.hero)
    assert game.player2.hero.health == 29

    game.end_turn()
    dummies = [game.player2.give(TARGET_DUMMY).play() for _ in range(3)]
    game.end_turn()
    wisp.attack(dummies[1])
    for i in range(3):
        assert dummies[i].health == 1


def test_nine_lives_triggers_the_deathrattle():
    # Was a second `test_nine_lives`, which hid the first (WP-189).
    game = prepare_game()
    highmane = game.player1.give("EX1_534").play()
    highmane.destroy()
    game.skip_turn()
    game.player1.discard_hand()
    assert len(game.player1.field) == 2
    game.player1.give("DAL_377").play()
    game.player1.choice.choose("EX1_534")
    assert len(game.player1.field) == 4


def test_unseen_saboteur_casts_nine_lives():
    # Was a second `test_unseen_saboteur`, which hid the first (WP-189).
    game = prepare_empty_game()
    highmane = game.player1.give("EX1_534").play()
    highmane.destroy()
    game.player1.give("DAL_377")
    game.end_turn()
    game.player2.give("DAL_538").play()
    assert len(game.player1.field) == 4


# WP-189: Rise of Shadows read against its text (patch 21.8) and hearthstone.wiki.gg.


def test_rapid_fire_deals_two():
    game = prepare_empty_game()
    game.player1.give("DAL_373").play(target=game.player2.hero)
    assert game.player2.hero.health == 28
    twin = game.player1.hand[0]
    assert twin.id == "DAL_373ts"
    twin.play(target=game.player2.hero)
    assert game.player2.hero.health == 26


def test_blastmaster_boom_counts_the_bombs_in_the_enemy_deck():
    game = prepare_empty_game()
    game.player1.give("DAL_060").play()
    game.player1.give("DAL_060").play()
    assert game.player2.deck == ["BOT_511t"] * 2
    # The same turn: the opponent's next draw would cast both Bombs.
    game.player1.used_mana = 0
    game.player1.give("DAL_064").play()
    assert game.player1.field.filter(id="GVG_110t") == ["GVG_110t"] * 4


def test_blastmaster_boom_ignores_its_own_deck():
    game = prepare_empty_game()
    for _ in range(2):
        game.player1.give("BOT_511t").shuffle_into_deck()
    game.player1.give("DAL_064").play()
    assert game.player1.field == ["DAL_064"]


def test_call_to_adventure_draws_the_lowest_cost_minion():
    game = prepare_empty_game()
    game.player1.give("NEW1_021").shuffle_into_deck()  # Doomsayer, 2 mana, 0 attack
    game.player1.give(WISP).shuffle_into_deck()  # 0 mana, 1 attack
    game.player1.give("DAL_727").play()
    assert game.player1.hand == [WISP]
    wisp = game.player1.hand[0]
    assert (wisp.atk, wisp.health) == (3, 3)


def test_conjurers_calling_replaces_for_the_owner():
    game = prepare_empty_game()
    yeti = game.player2.summon("CS2_182")
    game.player1.give("DAL_177").play(target=yeti)
    assert len(game.player1.field) == 0
    assert len(game.player2.field) == 2
    assert all(minion.cost == 4 for minion in game.player2.field)


def test_spellward_jeweler_hero_cant_be_targeted():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("DAL_081").play()
    moonfire = game.player1.give(MOONFIRE)
    assert game.player1.hero not in moonfire.play_targets
    assert game.player1.hero not in game.player1.hero.power.play_targets
    game.end_turn()
    enemy_moonfire = game.player2.give(MOONFIRE)
    assert game.player1.hero not in enemy_moonfire.play_targets
    assert game.player1.hero not in game.player2.hero.power.play_targets
    assert game.player2.hero in enemy_moonfire.play_targets
    game.end_turn()
    assert game.player1.hero in moonfire.play_targets


def test_sunreaver_warmage_with_a_big_spell():
    game = prepare_empty_game()
    warmage = game.player1.give("DAL_539")
    assert not warmage.requires_target()
    game.player1.give(PYROBLAST)
    assert warmage.requires_target()
    warmage.play(target=game.player2.hero)
    assert game.player2.hero.health == 26


def test_sunreaver_warmage_a_big_minion_is_not_a_spell():
    game = prepare_empty_game()
    game.player1.give("CS2_186")  # War Golem, 7 mana
    warmage = game.player1.give("DAL_539")
    assert not warmage.requires_target()


def test_thoridal_spell_damage_after_the_hero_attacks():
    game = prepare_empty_game()
    game.player1.give("DAL_379").play()
    assert game.player1.weapon.id == "DAL_379t"
    assert game.player1.spellpower == 0
    game.player1.hero.attack(game.player2.hero)
    assert game.player1.spellpower == 2
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 2 - 3
    game.end_turn()
    assert game.player1.spellpower == 0


def test_khadgar_doubles_an_enemy_summon_on_your_side():
    # hearthstone.wiki.gg: "Despite the card text, the effect also works from
    # opponent's cards that summon minions on your board, such as Dirty Rat and
    # Hecklebot."
    game = prepare_empty_game()
    game.player1.give("DAL_575").play()
    game.player1.give("CS2_182").shuffle_into_deck()
    game.end_turn()
    game.player2.give("DAL_058").play()
    assert game.player1.field == ["DAL_575", "CS2_182", "CS2_182"]


def test_khadgar_does_not_double_a_played_minion():
    game = prepare_empty_game()
    game.player1.give("DAL_575").play()
    game.player1.give(WISP).play()
    assert game.player1.field == ["DAL_575", WISP]


def test_lucentbark_awakens_on_your_healing_only():
    game = prepare_empty_game()
    lucentbark = game.player1.summon("DAL_357")
    lucentbark.destroy()
    assert game.player1.field == ["DAL_357t"]
    game.end_turn()
    game.player2.hero.set_current_health(20)
    game.player2.give(HOLY_LIGHT).play(target=game.player2.hero)
    assert game.player1.field == ["DAL_357t"]
    game.end_turn()
    game.player1.hero.set_current_health(20)
    game.player1.give(HOLY_LIGHT).play(target=game.player1.hero)
    assert game.player1.field == ["DAL_357"]


def test_underbelly_fence_with_a_card_from_another_class():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give(MOONFIRE)
    fence = game.player1.give("DAL_714").play()
    assert (fence.atk, fence.health, fence.rush) == (3, 4, True)


def test_underbelly_fence_neutral_and_rogue_cards_do_not_count():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give(WISP)
    game.player1.give("DAL_728")
    fence = game.player1.give("DAL_714").play()
    assert (fence.atk, fence.health) == (2, 3)
    assert not fence.rush


def test_vendetta_costs_zero_with_a_card_from_another_class():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.ROGUE)
    vendetta = game.player1.give("DAL_716")
    game.player1.give(WISP)
    assert vendetta.cost == 4
    game.player1.give(MOONFIRE)
    assert vendetta.cost == 0


def test_arch_villain_rafaam_replaces_hand_and_deck():
    game = prepare_empty_game()
    game.player1.give(WISP)
    game.player1.give("CS2_182").shuffle_into_deck()
    game.player1.give("DAL_422").play()
    assert len(game.player1.hand) == 1
    assert len(game.player1.deck) == 1
    for card in list(game.player1.hand) + list(game.player1.deck):
        assert card.type == CardType.MINION
        assert card.rarity == Rarity.LEGENDARY


def test_desperate_measures_never_casts_an_active_secret():
    for _ in range(20):
        game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
        secrets = ["EX1_130", "EX1_136", "EX1_132", "EX1_379"]
        for secret in secrets:
            game.player1.give(secret).play()
            game.end_turn()
            game.end_turn()
        game.player1.give("DAL_141").play()
        assert len(game.player1.secrets) == 5
        names = [secret.data.name for secret in game.player1.secrets]
        assert len(set(names)) == 5


def test_sweeping_strikes_damage_is_the_minions():
    # "Overkill can trigger against adjacent minions" (hearthstone.wiki.gg): the
    # minion deals that damage (Poisonous, Vicious Scraphound).
    game = prepare_empty_game()
    cobra = game.player1.summon("EX1_170")  # Emperor Cobra, Poisonous 2/3
    game.player1.give("DAL_062").play(target=cobra)
    left = game.player2.summon("CS2_182")
    wisp = game.player2.summon(WISP)
    right = game.player2.summon("CS2_182")
    game.end_turn()
    game.end_turn()
    cobra.attack(wisp)
    assert left.dead and right.dead

    game = prepare_empty_game()
    scraphound = game.player1.summon("DAL_759")
    game.player1.give("DAL_062").play(target=scraphound)
    game.player2.summon("CS2_182")
    wisp = game.player2.summon(WISP)
    game.player2.summon("CS2_182")
    game.end_turn()
    game.end_turn()
    scraphound.attack(wisp)
    assert game.player1.hero.armor == 2 + 2 + 2


def test_unseen_saboteur_twinspell_copy_goes_to_the_caster():
    game = prepare_empty_game()
    game.player2.discard_hand()
    game.player2.give("DAL_351")
    game.player1.give("DAL_538").play()
    assert game.player2.hand == ["DAL_351ts"]
    assert "DAL_351ts" not in game.player1.hand


def test_spellbook_binder_spell_damage_in_play_only():
    game = prepare_empty_game()
    game.player1.give(KOBOLD_GEOMANCER)
    game.player1.give(WISP).shuffle_into_deck()
    game.player1.give("DAL_089").play()
    assert game.player1.hand == [KOBOLD_GEOMANCER]
    game.player1.give(KOBOLD_GEOMANCER).play()
    game.player1.give("DAL_089").play()
    assert game.player1.hand == [KOBOLD_GEOMANCER, WISP]


def test_arcane_watcher_spell_damage_in_play_only():
    game = prepare_empty_game()
    watcher = game.player1.summon("DAL_434")
    game.player1.give(KOBOLD_GEOMANCER)
    game.player1.give(KOBOLD_GEOMANCER).shuffle_into_deck()
    game.end_turn()
    game.end_turn()
    assert not watcher.can_attack()
    game.player1.summon(KOBOLD_GEOMANCER)
    assert watcher.can_attack()


def test_duel_no_fight_when_the_enemy_board_is_full():
    game = prepare_empty_game()
    game.player1.give("CS2_182").shuffle_into_deck()
    game.player2.give("CS2_172").shuffle_into_deck()
    for _ in range(7):
        game.player2.summon(WISP)
    game.player1.give("DAL_731").play()
    yeti = game.player1.field[0]
    assert yeti.id == "CS2_182"
    assert yeti.damage == 0
    raptor = game.player2.deck[0]
    assert raptor.zone == Zone.DECK
    assert raptor.damage == 0


def test_duel_no_fight_when_your_board_is_full():
    game = prepare_empty_game()
    game.player1.give("CS2_182").shuffle_into_deck()
    game.player2.give("CS2_172").shuffle_into_deck()
    for _ in range(7):
        game.player1.summon(WISP)
    game.player1.give("DAL_731").play()
    assert game.player2.field == ["CS2_172"]
    assert game.player2.field[0].damage == 0
    assert game.player1.deck[0].damage == 0


def _swampqueen(game, first, second):
    game.player1.give("DAL_431").play()
    choice = game.player1.choice
    choice.cards[0] = game.player1.card(first)
    choice.choose(choice.cards[0])
    choice = game.player1.choice
    if second is not None:
        choice.cards[0] = game.player1.card(second)
    second_cards = list(choice.cards)
    choice.choose(choice.cards[0])
    return game.player1.hand[-1], second_cards


def test_swampqueen_hagatha_two_horrors_keep_their_spells():
    game = prepare_empty_game()
    first, _ = _swampqueen(game, "CS2_037", "EX1_244")  # Frost Shock, Totemic Might
    game.end_turn()
    game.end_turn()
    second, _ = _swampqueen(game, "EX1_259", "CS2_053")  # Lightning Storm, Far Sight
    yeti = game.player2.summon("CS2_182")
    game.end_turn()
    game.end_turn()
    first.play(target=yeti)
    assert yeti.frozen
    assert yeti.damage == 1


def test_swampqueen_hagatha_after_a_targeted_spell_offers_untargeted_ones():
    for _ in range(10):
        game = prepare_empty_game()
        game.player1.is_standard = False
        game.player1.give("DAL_431").play()
        choice = game.player1.choice
        choice.cards[0] = game.player1.card("CS2_037")  # Frost Shock, targeted
        choice.choose(choice.cards[0])
        for card in game.player1.choice.cards:
            assert PlayReq.REQ_TARGET_TO_PLAY not in card.requirements
            assert PlayReq.REQ_TARGET_IF_AVAILABLE not in card.requirements


def test_swampqueen_hagatha_horror_casts_both_spells():
    game = prepare_empty_game()
    horror, _ = _swampqueen(game, "EX1_259", "CS2_053")  # Lightning Storm, Far Sight
    yeti = game.player2.summon("CS2_182")
    game.end_turn()
    game.end_turn()
    game.player1.give(WISP).shuffle_into_deck()
    hand = len(game.player1.hand)
    horror.play()
    assert yeti.damage in (2, 3)
    assert len(game.player1.hand) == hand
    assert game.player1.overloaded == 2


def test_unidentified_contract_is_revealed_however_it_enters_the_hand():
    # A136, decision of the user (2026-10-02, WP-185): revealed as soon as it
    # enters the hand (given, discovered, starting hand), not only when drawn.
    contracts = {"DAL_366t1", "DAL_366t2", "DAL_366t3", "DAL_366t4"}
    game = prepare_empty_game()
    given = game.player1.give("DAL_366").morphed
    assert given.id in contracts
    assert [c.id for c in game.player1.hand] == [given.id]
    game.player1.card("DAL_366", zone=Zone.DECK)
    assert game.player1.deck[0].id == "DAL_366"
    drawn = game.player1.draw().morphed
    assert drawn.id in contracts
    deck = ["DAL_366"] * 30
    game = Game(
        players=(
            Player("Player1", deck, CardClass.ROGUE.default_hero),
            Player("Player2", deck, CardClass.ROGUE.default_hero),
        )
    )
    game.start()
    for player in game.players:
        player.choice.choose()
    for player in game.players:
        assert all(c.id in contracts or c.id == THE_COIN for c in player.hand)


def test_scheme_of_the_starting_hand_does_not_grow_on_its_first_turn():
    # A135 (D-108): "not on turn 1": a scheme of the starting hand is worth 1 on
    # its player's first turn (progress 0), and grows from the second turn on.
    deck = ["DAL_008"] * 30
    game = BaseTestGame(
        players=(
            Player("Player1", list(deck), CardClass.WARRIOR.default_hero),
            Player("Player2", list(deck), CardClass.WARRIOR.default_hero),
        )
    )
    game.start()
    _empty_mulligan(game)
    first = game.current_player
    second = first.opponent
    starting = [c for c in first.hand if c.id == "DAL_008"]
    # three cards of the starting hand, one drawn on the turn
    assert len(starting) == 4
    assert [c.progress for c in starting] == [0] * 4
    game.end_turn()
    assert [c.progress for c in second.hand if c.id == "DAL_008"] == [0] * 5
    game.end_turn()
    assert [c.progress for c in starting] == [1] * 4
