from utils import *


def test_duskhaven_hunter():
    game = prepare_empty_game()
    game.player1.give("GIL_200")
    game.player1.give("GIL_128").play()
    assert game.player1.hand[0].atk == 4
    assert game.player1.hand[0].health == 10
    game.skip_turn()
    assert game.player1.hand[0].atk == 10
    assert game.player1.hand[0].health == 4


def test_echo():
    game = prepare_empty_game()
    game.player1.give("GIL_680")
    for _ in range(3):
        game.player1.hand[0].play()
        assert game.player1.hand[0].id == "GIL_680"
    game.end_turn()
    assert len(game.player1.hand) == 0
    assert len(game.player1.field) == 3


def test_wing_blast():
    game = prepare_game()
    wing_blast = game.player1.give("GIL_518")
    assert wing_blast.cost == 4
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert wing_blast.cost == 1


def test_tess_greymane():
    game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("CS2_065").play()
    game.player1.give("EX1_169").play()
    mana = game.player1.mana
    tess = game.player1.give("GIL_598")
    tess.play()
    assert len(game.player1.field) == 3
    assert game.player1.mana == mana - tess.cost + 1


def test_shudderwock():
    game = prepare_game()
    for _ in range(2):
        engineer = game.player1.give("EX1_015").play()
        engineer.destroy()
    game.skip_turn()
    hand = len(game.player1.hand)
    shudderwock = game.player1.give("GIL_820")
    shudderwock.play()
    assert len(game.player1.hand) == hand + 2


def test_lady_in_white():
    game = prepare_game()
    game.player1.give("GIL_840").play()
    for card in game.player1.deck:
        if card.type == CardType.MINION:
            assert card.atk == card.health


def test_murkspark_eel():
    game = prepare_game()
    eel = game.player1.give("GIL_530")
    assert not eel.requires_target()
    eel.play()

    game = prepare_empty_game()
    eel = game.player1.give("GIL_530")
    assert eel.requires_target()
    eel.play(target=game.player2.hero)


def test_baku_and_genn():
    player1 = Player("Player1", [CHICKEN] * 29 + ["GIL_826"], "HERO_01")
    player2 = Player("Player1", [WISP] * 29 + ["GIL_692"], "HERO_02")
    game = BaseTestGame(players=(player1, player2))
    game.start()
    assert player1.hero.power.id == "HERO_01bp2"
    assert player2.hero.power.cost == 1


# WP-186: the cards of The Witchwood that played otherwise than their text


def _refill(player):
    player.used_mana = 0
    player.max_mana = 10


def _play(player, card_id, **kwargs):
    _refill(player)
    card = player.give(card_id)
    card.play(**kwargs)
    return card


def _to_deck(player, *card_ids):
    for card_id in card_ids:
        player.give(card_id).zone = Zone.DECK


def test_witchwood_apple_adds_three_treants():
    game = prepare_empty_game()
    _play(game.player1, "GIL_663")
    assert [c.id for c in game.player1.hand] == ["GIL_663t"] * 3


def test_dire_frenzy_buffs_the_beast_and_its_copies():
    game = prepare_empty_game()
    raptor = _play(game.player1, "CS2_172")
    _play(game.player1, "GIL_828", target=raptor)
    assert (raptor.atk, raptor.health) == (6, 5)
    assert len(game.player1.deck) == 3
    for copy in game.player1.deck:
        assert (copy.atk, copy.health) == (6, 5)


def test_curio_collector_grows_when_its_controller_draws():
    game = prepare_empty_game()
    curio = _play(game.player1, "GIL_640")
    _to_deck(game.player1, WISP)
    game.player1.draw(1)
    assert (curio.atk, curio.health) == (5, 5)
    assert (game.player1.hand[0].atk, game.player1.hand[0].health) == (1, 1)


def test_rat_trap_springs_on_the_third_card_only():
    game = prepare_empty_game()
    _play(game.player1, "GIL_577")
    game.end_turn()
    _play(game.player2, WISP)
    _play(game.player2, WISP)
    assert len(game.player1.secrets) == 1
    assert not game.player1.field
    _play(game.player2, WISP)
    assert not game.player1.secrets
    assert [c.id for c in game.player1.field] == ["GIL_577t"]


def test_hidden_wisdom_counts_the_opponents_cards():
    game = prepare_empty_game()
    _to_deck(game.player1, WISP, WISP, WISP, WISP)
    _play(game.player1, "GIL_903")
    game.end_turn()
    hand = len(game.player1.hand)
    _play(game.player2, WISP)
    _play(game.player2, WISP)
    assert len(game.player1.secrets) == 1
    _play(game.player2, WISP)
    assert not game.player1.secrets
    assert len(game.player1.hand) == hand + 2


def test_duskbat_and_deathweb_spider_need_damage_to_the_hero():
    game = prepare_empty_game()
    _play(game.player1, "GIL_508")
    assert len(game.player1.field) == 1
    spider = _play(game.player1, "GIL_565")
    assert not spider.lifesteal
    _play(game.player1, MOONFIRE, target=game.player1.hero)
    _play(game.player1, "GIL_508")
    assert len(game.player1.field) == 5
    spider = _play(game.player1, "GIL_565")
    assert spider.lifesteal


def test_witchwood_grizzly_loses_health_for_the_opponents_hand():
    game = prepare_empty_game()
    for _ in range(4):
        game.player2.give(WISP)
    grizzly = _play(game.player1, "GIL_623")
    assert (grizzly.atk, grizzly.health) == (3, 7)


def test_woodcutters_axe_only_serves_rush_minions():
    game = prepare_empty_game()
    axe = _play(game.player1, "GIL_653")
    wisp = _play(game.player1, WISP)
    axe.destroy()
    assert (wisp.atk, wisp.health) == (1, 1)
    game = prepare_empty_game()
    axe = _play(game.player1, "GIL_653")
    wisp = _play(game.player1, WISP)
    worgen = _play(game.player1, "GIL_113")
    axe.destroy()
    assert (wisp.atk, wisp.health) == (1, 1)
    assert (worgen.atk, worgen.health) == (5, 4)


def test_bogshaper_draws_one_minion_per_spell():
    game = prepare_empty_game()
    _play(game.player1, "GIL_807")
    _to_deck(game.player1, WISP, "CS2_182", "CS2_168")
    hand = len(game.player1.hand)
    _play(game.player1, MOONFIRE, target=game.player2.hero)
    assert len(game.player1.hand) == hand + 1
    assert len(game.player1.deck) == 2


def test_duskfallen_aviana_serves_both_players_once_per_turn():
    game = prepare_empty_game()
    aviana = _play(game.player1, "GIL_800")
    mine = game.player1.give("CS2_182")
    assert mine.cost == 4  # Aviana was this turn's first card
    game.end_turn()
    first = game.player2.give("CS2_182")
    second = game.player2.give("CS2_182")
    assert (first.cost, second.cost) == (0, 0)
    assert mine.cost == 4
    _refill(game.player2)
    first.play()
    assert second.cost == 4
    game.end_turn()
    assert mine.cost == 0
    aviana.destroy()
    assert mine.cost == 4


def test_dollmaster_dorian_and_archmage_arugal_hear_the_draw():
    game = prepare_empty_game()
    _play(game.player1, "GIL_620")
    _to_deck(game.player1, "CS2_182")
    game.player1.draw(1)
    assert [(c.id, c.atk, c.health) for c in game.player1.field[1:]] == [
        ("CS2_182", 1, 1)
    ]
    game = prepare_empty_game()
    _play(game.player1, "GIL_691")
    _to_deck(game.player1, WISP, MOONFIRE)
    game.player1.draw(2)
    assert sorted(c.id for c in game.player1.hand) == sorted([MOONFIRE, WISP, WISP])


def test_witchs_cauldron_hears_a_friendly_minion_die():
    game = prepare_empty_game()
    cauldron = _play(game.player1, "GIL_819")
    wisp = _play(game.player1, WISP)
    wisp.destroy()
    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].card_class == CardClass.SHAMAN
    assert game.player1.hand[0].type == CardType.SPELL
    cauldron.destroy()
    assert len(game.player1.hand) == 1


def test_glitter_moth_adds_the_current_health_to_the_maximum():
    # A110 (D-108): +current Health to the maximum, the damage stays: a 4/5
    # Yeti with 4 Health left goes to 8 Health of 9.
    game = prepare_empty_game()
    yeti = game.player1.give("CS2_182").play()
    yeti.damage = 1
    assert (yeti.health, yeti.max_health) == (4, 5)
    game.player1.give("GIL_837").play()
    assert (yeti.health, yeti.max_health) == (8, 9)
    assert yeti.damage == 1
