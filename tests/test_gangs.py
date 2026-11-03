import pytest
from utils import *


def test_aya_blackpaw():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    aya = game.current_player.give("CFM_902").play()
    assert game.current_player.field[1].id == "CFM_712_t01"
    assert game.current_player.jade_golem == 2
    aya.destroy()
    assert game.current_player.jade_golem == 3
    jade2 = game.current_player.field[0]
    assert jade2.id == "CFM_712_t02"
    assert jade2.health == jade2.atk == 2


def test_jade_behemoth():
    game = prepare_empty_game()
    card = game.current_player.give("CFM_343")
    description = card.data.description.replace("[x]", "").split("@")[0]
    assert card.description == description.format("1/1", "")
    card.play()
    assert card.taunt
    jade = game.current_player.field[-1]
    assert "CFM_712_t01" == jade.id
    assert jade.health == jade.atk == 1
    jade.destroy()
    card.destroy()

    game.end_turn()
    game.end_turn()
    card2 = game.current_player.give("CFM_343")
    assert card2.description == description.format("2/2", "")
    card2.play()
    jade2 = game.current_player.field[-1]
    assert jade2.id == "CFM_712_t02"
    assert jade2.health == jade2.atk == 2
    jade2.destroy()
    card2.destroy()

    for i in range(3, 8):
        game.end_turn()
        game.end_turn()
        card = game.current_player.give("CFM_343")
        assert card.description == description.format(f"{i}/{i}", "")
        card.play()
        assert card.taunt
        jade = game.current_player.field[-1]
        assert f"CFM_712_t0{i}" == jade.id
        assert jade.health == jade.atk == i
        jade.destroy()
        card.destroy()

    game.end_turn()
    game.end_turn()
    card = game.current_player.give("CFM_343")
    assert card.description == description.format("8/8", "n")
    card.play()
    assert card.taunt
    jade = game.current_player.field[-1]
    assert "CFM_712_t08" == jade.id
    assert jade.health == jade.atk == 8


def test_pilfered_power():
    game = prepare_game(game_class=Game)
    for _ in range(2):
        game.end_turn()
        game.end_turn()
    assert game.player1.max_mana == 3
    for _ in range(3):
        game.player1.give(WISP).play()
    pilfered_power_1 = game.player1.give("CFM_616")
    pilfered_power_1.play()
    assert game.player1.mana == 0
    assert game.player1.used_mana == 3 + 3
    assert game.player1.max_mana == 3 + 3

    for _ in range(3):
        game.end_turn()
        game.end_turn()
    game.player1.discard_hand()
    assert len(game.player1.hand) == 0
    assert game.player1.max_mana == 9
    pilfered_power_2 = game.player1.give("CFM_616")
    pilfered_power_2.play()
    assert len(game.player1.hand) == 0
    assert game.player1.mana == 6
    assert game.player1.max_mana == 10
    assert game.player1.used_mana == 4

    game.end_turn()
    game.end_turn()
    game.player1.discard_hand()
    assert len(game.player1.hand) == 0
    assert game.player1.max_mana == 10
    pilfered_power_3 = game.player1.give("CFM_616")
    pilfered_power_3.play()
    excess_mana = game.player1.hand[0]
    assert excess_mana.id == "CS2_013t"
    excess_mana.play()
    assert len(game.player1.hand) == 1


def test_jade_blossom():
    game = prepare_game(game_class=Game)
    assert game.current_player.mana == 1
    assert game.current_player.max_mana == 1
    for i in range(4):
        game.end_turn()
    assert game.current_player.mana == 3
    assert game.current_player.max_mana == 3
    assert game.current_player.jade_golem == 1
    blossom = game.current_player.give("CFM_713")
    blossom.play()
    assert len(game.current_player.field) == 1
    jade1 = game.current_player.field[-1]
    assert jade1.health == jade1.atk == 1
    assert game.current_player.jade_golem == 2
    assert game.current_player.mana == 0
    assert game.current_player.max_mana == 4
    assert game.current_player.opponent.max_mana == 2


def test_jade_chieftain():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    chieftain = game.current_player.give("CFM_312").play()
    assert game.current_player.jade_golem == 2
    assert game.current_player.field[1].id == "CFM_712_t01"
    assert game.current_player.field[1].taunt
    assert not chieftain.taunt


def test_jade_claws():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    game.current_player.give("CFM_717").play()
    assert game.current_player.field[0].id == "CFM_712_t01"
    assert game.current_player.jade_golem == 2
    game.current_player.hero.attack(game.current_player.opponent.hero)
    assert game.current_player.opponent.hero.health == 28

    game.current_player.summon("LOE_077")
    game.current_player.give("CFM_717").play()
    assert game.current_player.field[2].id == "CFM_712_t02"
    assert game.current_player.field[3].id == "CFM_712_t03"
    assert game.current_player.jade_golem == 4


def test_jade_idol():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    idol1 = game.current_player.give("CFM_602")
    idol1.play(choose="CFM_602a")
    jade1 = game.current_player.field[-1]
    assert jade1.health == jade1.atk == 1

    assert len(game.current_player.deck) == 26
    assert len(game.current_player.field) == 1
    idol2 = game.current_player.give("CFM_602")
    idol2.play(choose="CFM_602b")
    assert game.current_player.jade_golem == 2
    assert len(game.current_player.field) == 1
    assert len(game.current_player.deck) == 29

    game.current_player.summon(FANDRAL_STAGHELM)
    game.current_player.give("CFM_602").play()
    assert len(game.current_player.field) == 3
    jade3 = game.current_player.field[-1]
    assert jade3.health == jade3.atk == 2
    assert game.current_player.jade_golem == 3
    assert len(game.current_player.deck) == 29 + 3

    # reduce jade_idol's cost to 0
    game.current_player.summon("EX1_608")
    for i in range(26):
        game.current_player.give("CFM_602").play()
        assert game.current_player.jade_golem == 4 + i
        jade_i = game.current_player.field[-1]
        assert jade_i.health == jade_i.atk == 3 + i
        jade_i.destroy()
    # assert len(game.current_player.deck) == 60


def test_jade_lighting():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    lighting = game.current_player.give("CFM_707")
    lighting.play(target=game.current_player.hero)
    assert game.current_player.field[0].id == "CFM_712_t01"
    assert game.current_player.jade_golem == 2
    assert game.current_player.hero.health == 26


def test_jade_shuriken():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    shuriken1 = game.current_player.give("CFM_690")
    shuriken2 = game.current_player.give("CFM_690")
    shuriken3 = game.current_player.give("CFM_690")
    wisp = game.current_player.summon(WISP)
    hero2 = game.current_player.opponent.hero
    with pytest.raises(InvalidAction):
        shuriken1.play()
    shuriken1.play(target=hero2)
    assert hero2.health == 28
    assert game.current_player.jade_golem == 1
    assert len(game.current_player.field) == 1

    shuriken2.play(target=wisp)
    assert wisp.dead
    assert game.current_player.jade_golem == 2
    assert len(game.current_player.field) == 1

    game.current_player.summon("EX1_012")
    shuriken3.play(target=hero2)
    assert hero2.health == 25
    assert game.current_player.jade_golem == 3
    assert len(game.current_player.field) == 3

    blade = game.current_player.give("EX1_133")
    blade.play(target=hero2)
    assert hero2.health == 23
    assert game.current_player.jade_golem == 3


def test_jade_spirit():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    game.current_player.give("CFM_715").play()
    assert game.current_player.field[1].id == "CFM_712_t01"
    assert game.current_player.jade_golem == 2

    game.current_player.summon("LOE_077")
    game.current_player.give("CFM_715").play()
    assert game.current_player.jade_golem == 4
    jade2 = game.current_player.field[5]
    assert jade2.id == "CFM_712_t02"
    assert jade2.health == jade2.atk == 2
    # the extra battlecry comes next to its generator
    jade3 = game.current_player.field[4]
    assert jade3.id == "CFM_712_t03"
    assert jade3.health == jade3.atk == 3


def test_jade_swarmer():
    game = prepare_game()
    assert game.current_player.jade_golem == 1
    swarmer = game.current_player.give("CFM_691")
    swarmer.play()
    assert game.current_player.jade_golem == 1
    swarmer.destroy()
    assert game.current_player.jade_golem == 2
    assert game.current_player.field[0].id == "CFM_712_t01"


def test_weasel_tunneler():
    game = prepare_game()
    weasel = game.player1.give("CFM_095").play()
    assert weasel.zone == Zone.PLAY
    assert weasel.controller == game.player1
    game.player1.give("CS2_008").play(target=weasel)
    assert weasel.zone == Zone.DECK
    assert weasel.controller == game.player2


def test_finja():
    game = prepare_empty_game()
    finja = game.player1.give("CFM_344").play()
    game.end_turn()
    wisp = game.player2.give(WISP).play()
    game.end_turn()
    murloc1 = game.player1.give(MURLOC)
    murloc1.shuffle_into_deck()
    murloc2 = game.player1.give(MURLOC)
    murloc2.shuffle_into_deck()
    murloc3 = game.player1.give(MURLOC)
    murloc3.shuffle_into_deck()
    finja.attack(target=wisp)
    assert game.player1.field[0] == finja
    assert len(game.player1.field) == 3


def test_doppelgangster():
    game = prepare_game()
    doppel = game.player1.give("CFM_668")
    assert doppel.atk == 2
    game.player1.give("CFM_305").play()
    assert doppel.atk == 3
    doppel.play()
    assert len(game.player1.field) == 3
    assert game.player1.field[0].id == "CFM_668"
    assert game.player1.field[1].id == "CFM_668"
    assert game.player1.field[2].id == "CFM_668"


def test_seadevil_stinger():
    game = prepare_game()
    sea = game.player1.give("CFM_699")
    sea.play()
    assert game.player1.mana == 6
    assert game.player1.hero.health == 30
    murloc = game.player1.give("EX1_507")
    murloc.play()
    assert game.player1.mana == 6
    assert game.player1.hero.health == (30 - murloc.cost)


def test_kazakus():
    game = prepare_empty_game()
    assert len(game.player1.hand) == 0
    kazakus = game.player1.give("CFM_621")
    kazakus.play()
    chooses = []
    for _ in range(3):
        cards = game.player1.choice.cards
        chooses.append(cards[0])
        game.player1.choice.choose(cards[0])
    card = game.player1.hand[0]
    assert card.cost == 1
    assert (
        card.description == f"{chooses[1].description}\n{chooses[2].description}"
        or card.description == f"{chooses[2].description}\n{chooses[1].description}"
    )


def test_i_know_a_guy():
    game = prepare_game()
    guy = game.player1.give("CFM_940")
    guy.play()
    for card in game.player1.choice.cards:
        assert card.type == CardType.MINION
        assert card.taunt


def test_kabal_crystal_runner():
    game = prepare_game()
    runner = game.player1.give("CFM_760")
    runner_cost = runner.cost
    game.player1.give("EX1_295").play()
    assert runner.cost == runner_cost - 2
    runner2 = game.player1.give("CFM_760")
    assert runner2.cost == runner_cost - 2


def test_madam_goya():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    murloc = game.player1.give(MURLOC)
    murloc.shuffle_into_deck()
    assert wisp.zone == Zone.PLAY
    assert murloc.zone == Zone.DECK
    game.player1.give("CFM_672").play(target=wisp)
    assert wisp.zone == Zone.DECK
    assert murloc.zone == Zone.PLAY


def test_wrathion():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP)
    wisp.zone = Zone.DECK
    for _ in range(4):
        dragon = game.player1.give("NEW1_023")
        dragon.zone = Zone.DECK
    assert len(game.player1.hand) == 0
    game.player1.give("CFM_806").play()
    assert len(game.player1.hand) == 5


def test_wrathion_empty():
    game = prepare_empty_game()
    game.player1.cant_fatigue = False
    game.player1.give("NEW1_023").put_on_top()
    game.player1.give("CFM_806").play()
    assert game.player1.hero.health == 30 - 1


# WP-182 (Hearthstone, vague 23) : les cartes qui jouaient autrement que leur texte
# (patch 21.8) ou, le texte se taisant, que hearthstone.wiki.gg.


def _to_deck(player, card_id):
    card = player.card(card_id)
    card.zone = Zone.DECK
    return card


def test_rat_pack_summons_rats():
    """« Summon a number of 1/1 Rats equal to this minion's Attack » : des Rats, pas des Rat Packs."""
    game = prepare_empty_game()
    rat_pack = game.player1.give("CFM_316").play()
    game.player1.give("CS2_092").play(target=rat_pack)  # Blessing of Kings, 6/6
    rat_pack.destroy()
    assert [m.id for m in game.player1.field] == ["CFM_316t"] * 6
    assert all(m.atk == m.health == 1 for m in game.player1.field)


def test_sergeant_sally_hits_enemy_minions_only():
    game = prepare_empty_game()
    sally = game.player1.give("CFM_341").play()
    friendly = game.player1.summon("CS2_182")
    enemy = game.player2.summon("CS2_182")
    game.player1.give("CS2_092").play(target=sally)  # 5/5
    sally.destroy()
    assert not friendly.dead and friendly.zone == Zone.PLAY
    assert friendly.health == 5
    assert enemy.dead


def test_piranha_launcher_after_attacking_the_hero():
    game = prepare_empty_game()
    game.player1.give("CFM_337").play()
    game.player1.hero.attack(game.player2.hero)
    assert [m.id for m in game.player1.field] == ["CFM_337t"]
    game.end_turn()
    game.end_turn()
    wisp = game.player2.summon(WISP)
    game.player1.hero.attack(wisp)
    assert [m.id for m in game.player1.field] == ["CFM_337t", "CFM_337t"]


def test_cryomancer_gains_stats_if_an_enemy_is_frozen():
    game = prepare_empty_game()
    yeti = game.player2.summon("CS2_182")
    cryo1 = game.player1.give("CFM_671").play()
    assert (cryo1.atk, cryo1.health) == (5, 5)
    game.player1.give("CS2_024").play(target=yeti)  # Frostbolt
    game.player1.used_mana = 0
    cryo2 = game.player1.give("CFM_671").play()
    assert (cryo2.atk, cryo2.health) == (7, 7)


def test_raza_needs_a_deck_without_duplicates():
    game = prepare_empty_game()
    _to_deck(game.player1, WISP)
    _to_deck(game.player1, WISP)
    game.player1.give("CFM_020").play()
    assert game.player1.hero.power.cost == 2
    game.end_turn()
    _to_deck(game.player2, WISP)
    _to_deck(game.player2, "CS2_182")
    game.player2.give("CFM_020").play()
    assert game.player2.hero.power.cost == 0


def test_kazakus_superior_heart_of_fire_deals_eight():
    """Le texte de 21.8 : « Deal $8 damage » (CFM_621t25), pas 10."""
    game = prepare_empty_game()
    game.player1.give("CFM_621t25").play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 8


def test_gadgetzan_ferryman_combo_returns_a_friendly_minion():
    game = prepare_empty_game()
    swarmer = game.player1.summon("CFM_691")
    ferryman = game.player1.give("CFM_693")
    assert not ferryman.requires_target()
    ferryman.play()
    assert swarmer.zone == Zone.PLAY
    game.player1.give(THE_COIN).play()
    ferryman2 = game.player1.give("CFM_693")
    assert ferryman2.requires_target()
    ferryman2.play(target=swarmer)
    assert [c.id for c in game.player1.hand] == ["CFM_691"]


def test_blubber_baron_grows_on_summoned_battlecry_minions():
    """« Whenever you summon a Battlecry minion » : les deux copies de Doppelgangster comptent (wiki)."""
    game = prepare_empty_game()
    baron = game.player1.give("CFM_064")
    game.player1.give("CFM_668").play()
    assert (baron.atk, baron.health) == (1 + 3, 1 + 3)
    game.player1.summon("CS2_189")  # Elven Archer, invoquée
    assert (baron.atk, baron.health) == (5, 5)
    game.player1.summon(WISP)
    assert (baron.atk, baron.health) == (5, 5)


def test_hidden_cache_needs_a_minion_in_hand():
    """Le wiki : Hidden Cache ne se déclenche pas sans serviteur en main."""
    game = prepare_empty_game()
    game.player1.give("CFM_026").play()
    game.end_turn()
    game.player2.give(WISP).play()
    assert [s.id for s in game.player1.secrets] == ["CFM_026"]
    game.end_turn()
    yeti = game.player1.give("CS2_182")
    game.end_turn()
    game.player2.give(WISP).play()
    assert not game.player1.secrets
    assert (yeti.atk, yeti.health) == (6, 7)


def test_celestial_dreamer_counts_itself():
    """Le wiki : « If the Celestial Dreamer has 5 or more Attack when played, it will satisfy its own condition »."""
    game = prepare_empty_game()
    dreamer = game.player1.give("CFM_617")
    dreamer.buff(dreamer, "CFM_342e")  # +4/+4 en main, 7/7
    dreamer.play()
    assert (dreamer.atk, dreamer.health) == (9, 9)
    dreamer2 = game.player1.give("CFM_617").play()
    assert (dreamer2.atk, dreamer2.health) == (5, 5)


def test_wrathion_stops_on_overdraw_only():
    """Le wiki : Wrathion s'arrête quand une carte piochée brûle, dragon ou non ; une main
    qui vient de se remplir ne l'arrête pas."""
    game = prepare_empty_game()
    player = game.player1
    wisp = _to_deck(player, WISP)
    _to_deck(player, "NEW1_023")
    _to_deck(player, "NEW1_023")
    for _ in range(8):
        player.give("CS2_182")
    player.give("CFM_806").play()
    assert len(player.hand) == 10
    assert not player.deck
    assert wisp.zone not in (Zone.HAND, Zone.DECK)  # brûlée


def test_grimscale_chum_buffs_one_random_murloc():
    """« Give a random Murloc in your hand +1/+1 » : un seul."""
    game = prepare_empty_game()
    murlocs = [game.player1.give("CS2_168") for _ in range(3)]  # Murloc Raider 2/1
    game.player1.give("CFM_650").play()
    assert sorted((m.atk, m.health) for m in murlocs) == [(2, 1), (2, 1), (3, 2)]


def test_finders_keepers_never_offers_itself():
    # Environ 70 cartes de chaman à Surcharge : 150 découvertes la montreraient (p < 0,001).
    # Une partie Wild : sans cela, le vivier Standard n'a pas Mean Streets of Gadgetzan.
    game = prepare_empty_game()
    game.player1.is_standard = False
    for _ in range(150):
        game.player1.give("CFM_313").play()
        cards = game.player1.choice.cards
        assert "CFM_313" not in [c.id for c in cards]
        assert all(c.overload for c in cards)
        game.player1.choice.choose(cards[0])
        game.player1.discard_hand()
        game.player1.used_mana = 0
        game.player1.overloaded = 0


def test_getaway_kodo_after_the_deathrattle():
    """Le wiki : « When Getaway Kodo triggers on a Deathrattle minion, the Deathrattle effect
    occurs first » : Loot Hoarder pioche, puis revient en main ; main à 9, la pioche la remplit
    et Loot Hoarder ne revient pas."""
    game = prepare_empty_game()
    _to_deck(game.player1, WISP)
    game.player1.give("CFM_800").play()
    hoarder = game.player1.summon("EX1_096")
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=hoarder)
    assert [c.id for c in game.player1.hand] == [WISP, "EX1_096"]
    assert not game.player1.secrets

    game = prepare_empty_game()
    yeti = _to_deck(game.player1, "CS2_182")
    game.player1.give("CFM_800").play()
    hoarder = game.player1.summon("EX1_096")
    for _ in range(9):
        game.player1.give(WISP)
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=hoarder)
    assert yeti.zone == Zone.HAND
    assert "EX1_096" not in [c.id for c in game.player1.hand]


def test_doppelgangster_first_copy_on_the_left():
    """Le wiki : la première copie à gauche de l'original, la seconde à sa droite ; une seule
    place, la copie va à gauche."""
    game = prepare_empty_game()
    for _ in range(5):
        game.player1.summon(WISP)
    doppel = game.player1.give("CFM_668")
    doppel.play(index=0)
    assert len(game.player1.field) == 7
    assert game.player1.field[1] is doppel
    assert game.player1.field[0].id == "CFM_668"

    game2 = prepare_empty_game()
    left = game2.player1.summon(WISP)
    right = game2.player1.summon(WISP)
    doppel2 = game2.player1.give("CFM_668")
    doppel2.play(index=1)
    field = game2.player1.field
    assert [m.id for m in field] == [WISP, "CFM_668", "CFM_668", "CFM_668", WISP]
    assert field[2] is doppel2


def test_doppelgangster_copies_are_summons():
    """Le cœur : un SummonBothSides est une invocation ; « after you summon a minion »
    (Unlicensed Apothecary, Knife Juggler) l'entend, comme le wiki le dit d'Apothecary.
    """
    game = prepare_empty_game()
    game.player1.summon("NEW1_019")  # Knife Juggler, plateau adverse vide
    game.player1.summon("CFM_900")  # Unlicensed Apothecary : un couteau
    assert game.player2.hero.health == 30 - 1
    game.player1.give("CFM_668").play()
    assert game.player1.hero.health == 30 - 3 * 5
    assert game.player2.hero.health == 30 - 1 - 3


def test_devolve_zero_cost_minion_becomes_a_zero_cost_minion():
    """Le wiki : « 0-mana minions will transform into other 0-mana minions, which can include itself »."""
    game = prepare_empty_game()
    wisp = game.player2.summon(WISP)
    game.player1.give("CFM_696").play()
    assert wisp.zone != Zone.PLAY
    assert len(game.player2.field) == 1
    assert game.player2.field[0].cost == 0


def test_mayor_noggenfogger_redirects_the_hero_attack():
    """A66 (WP-182c, l'utilisateur) : le Mayor détourne aussi l'attaque du héros, à pile ou face."""
    game = prepare_empty_game()
    game.player1.summon("CFM_670")
    game.player1.summon("CS2_106")  # Fiery War Axe : le héros peut attaquer
    game.end_turn()
    wisp = game.player2.summon(WISP)
    game.end_turn()
    hero = game.player1.hero
    with mock(RandomNumber, 1):  # pile : l'attaque est détournée
        with mock(RANDOM, wisp):
            hero.attack(game.player2.hero)
    assert wisp.dead
    assert game.player2.hero.damage == 0
    game.end_turn()
    game.end_turn()
    wisp2 = game.player2.summon(WISP)
    with mock(RandomNumber, 0):  # face : l'attaque va où on l'a portée
        hero.attack(game.player2.hero)
    assert not wisp2.dead
    assert game.player2.hero.damage == 3


def test_lotus_assassin_has_stealth():
    # WP-189c, the sweep of Skyvateer's defect: CardDefs.xml only carries a
    # ReferencedTag STEALTH for Lotus Assassin, so the script gives the tag.
    game = prepare_empty_game()
    assassin = game.player1.give("CFM_634").play()
    assert assassin.stealthed
    game.end_turn()
    game.end_turn()
    wisp = game.player2.summon(WISP)
    assassin.attack(wisp)
    assert wisp.dead
    assert assassin.stealthed


def test_powered_up_reads_the_negation_of_its_condition():
    # WP-214 : "if your deck has no duplicates" glows when it has none (check() alone
    # answered the bare condition, so it glowed the wrong way round).
    game = prepare_empty_game()
    kazakus = game.player1.give("CFM_621")
    assert kazakus.powered_up
    _to_deck(game.player1, WISP)
    assert kazakus.powered_up
    _to_deck(game.player1, WISP)
    assert not kazakus.powered_up


def test_powered_up_gangs_conditions():
    # WP-214 : the Battlecry conditions that glow in the hand.
    game = prepare_empty_game(CardClass.MAGE, CardClass.WARRIOR)
    game.player2.discard_hand()
    cryo = game.player1.give("CFM_671")
    promoter = game.player1.give("CFM_328")
    chopper = game.player1.give("CFM_809")
    hogleader = game.player1.give("CFM_810")
    assert not cryo.powered_up
    assert not promoter.powered_up
    assert not hogleader.powered_up
    assert chopper.powered_up  # the opponent's hand is empty
    game.player2.give(WISP)
    assert not chopper.powered_up
    for _ in range(5):
        game.player2.give(WISP)
    assert hogleader.powered_up
    game.player1.summon("CS2_186")  # War Golem, 7 Health
    assert promoter.powered_up
    game.player2.summon(WISP).frozen = True
    assert cryo.powered_up
