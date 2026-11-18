from utils import *


def test_magnetic():
    game = prepare_game()
    mech = game.player1.give(MECH).play()
    atk = mech.atk
    health = mech.health
    assert not mech.rush
    magnetic1 = game.player1.give("BOT_020")
    magnetic1.play(index=0)
    assert len(game.player1.field) == 1
    assert mech.atk == atk + 1
    assert mech.health == health + 1
    assert mech.rush
    magnetic1 = game.player1.give("BOT_020")
    magnetic1.play()
    assert len(game.player1.field) == 2


def test_whizbang():
    player1 = Player("Player1", ["BOT_914"], "BOT_914h")
    player2 = Player("Player1", ["BOT_914"], "BOT_914h")
    game = BaseTestGame(players=(player1, player2))
    game.start()
    assert len(game.player1.starting_deck) == 30
    assert len(game.player2.starting_deck) == 30


def test_stargazer_luna():
    game = prepare_game()
    game.player1.discard_hand()
    game.player1.give("BOT_103").play()
    assert len(game.player1.hand) == 0
    for _ in range(3):
        game.player1.give(WISP)
    assert len(game.player1.hand) == 3
    game.player1.hand[-1].play()
    assert len(game.player1.hand) == 3
    game.player1.hand[1].play()
    assert len(game.player1.hand) == 2


def test_prismatic_lens():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP)
    wisp.shuffle_into_deck()
    fireball = game.player1.give(FIREBALL)
    fireball.shuffle_into_deck()
    game.player1.give("BOT_436").play()
    assert wisp in game.player1.hand
    assert fireball in game.player1.hand
    assert wisp.cost == 4
    assert fireball.cost == 0


def test_kangors_endless_army():
    game = prepare_game()
    mech = game.player1.give(MECH).play()
    atk = mech.atk
    health = mech.health
    magnetic = game.player1.give("BOT_020")
    magnetic.play(index=0)
    game.player1.give("CS2_092").play(target=mech)
    mech.destroy()
    game.skip_turn()
    game.player1.give("BOT_912").play()
    assert len(game.player1.field) == 1
    mech = game.player1.field[0]
    assert mech.atk == atk + 1
    assert mech.health == health + 1
    assert mech.rush


def test_myra_rotspring():
    game = prepare_game()
    myra = game.player1.give("BOT_243")
    myra.play()
    game.player1.choice.choose(game.player1.choice.cards[0])


def test_electra_stormsurge():
    game = prepare_game()
    game.player1.give("BOT_411").play()
    game.player1.give("EX1_238").play(target=game.player2.hero)
    assert game.player2.hero.health == 24
    assert game.player1.overloaded == 2

    game.player1.give("EX1_238").play(target=game.player2.hero)
    assert game.player2.hero.health == 21


def test_holomancer():
    game = prepare_game()
    game.player1.give("BOT_280").play()
    game.end_turn()
    game.player2.give(MECH).play()
    assert len(game.player1.field) == 2
    new_mech = game.player1.field[1]
    assert new_mech.id == MECH
    assert new_mech.atk == 1
    assert new_mech.max_health == 1


def test_flarks_boom_zooka():
    game = prepare_game()
    game.player1.give("BOT_429").play()


def test_zereks_cloning_gallery_when_empty():
    game = prepare_empty_game()
    game.player1.give("BOT_567").play()


def test_omega_mind():
    game = prepare_game()
    game.player1.give("BOT_543").play()
    game.player1.hero.set_current_health(1)
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert game.player1.hero.health == 1 + 6


def _fresh_mana(game):
    game.player1.max_mana = 10
    game.player1.used_mana = 0


def test_celestial_emissary_gives_the_next_spell_spell_damage():
    # Le bonus était retiré avant que le sort ne frappe : Fireball faisait 6.
    game = prepare_empty_game()
    game.player1.give("BOT_531").play()
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 8
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert game.player2.hero.health == 30 - 8 - 6


def test_meteorologist_can_hit_the_enemy_hero():
    # Il ne visait que les serviteurs : sans serviteur adverse, rien ne partait.
    game = prepare_empty_game()
    for _ in range(3):
        game.player1.give(WISP)
    game.player1.give("BOT_601").play()
    assert game.player2.hero.health == 27


def test_loose_specimen_never_hits_itself():
    game = prepare_empty_game()
    for _ in range(10):
        _fresh_mana(game)
        specimen = game.player1.give("BOT_544").play()
        assert specimen.health == 6
        specimen.destroy()
    _fresh_mana(game)
    yeti = game.player1.give("CS2_182").play()
    specimen = game.player1.give("BOT_544").play()
    assert specimen.health == 6
    assert yeti.dead


def test_dead_ringer_draws_a_deathrattle_minion_only():
    # « Deathrattle minion » : une arme à râle d'agonie (Necrium Blade) ne se pioche pas.
    game = prepare_empty_game()
    game.player1.give("BOT_286").shuffle_into_deck()
    ringer = game.player1.give("BOT_509").play()
    ringer.destroy()
    assert len(game.player1.hand) == 0
    game.player1.give("BOT_445").shuffle_into_deck()
    ringer = game.player1.give("BOT_509").play()
    ringer.destroy()
    assert [c.id for c in game.player1.hand] == ["BOT_445"]


def test_dr_morrigan_swaps_with_a_minion_of_the_deck():
    # Le serviteur du deck entre en jeu, Morrigan retourne au deck (le wiki).
    game = prepare_empty_game()
    game.player1.give("CS2_186").shuffle_into_deck()
    morrigan = game.player1.give("BOT_433").play()
    morrigan.destroy()
    assert [m.id for m in game.player1.field] == ["CS2_186"]
    assert [c.id for c in game.player1.deck] == ["BOT_433"]
    # Sans serviteur dans le deck, rien n'est échangé.
    game = prepare_empty_game()
    morrigan = game.player1.give("BOT_433").play()
    morrigan.destroy()
    assert len(game.player1.field) == 0
    assert len(game.player1.deck) == 0


def test_flobbidinous_floop_is_a_3_4_copy_of_the_last_minion_for_4():
    # Le wiki : une copie 3/4 du dernier serviteur joué, au coût de 4 ; un sort ne la change pas.
    game = prepare_empty_game()
    _fresh_mana(game)
    floop = game.player1.give("BOT_434")
    game.player1.give("CS2_186").play()
    card = game.player1.hand[0]
    assert card.id == "CS2_186"
    assert (card.atk, card.health, card.cost) == (3, 4, 4)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player1.hand[0].id == "CS2_186"
    game.player1.give(WISP).play()
    card = game.player1.hand[0]
    assert card.id == WISP
    assert (card.atk, card.health, card.cost) == (3, 4, 4)


def test_augmented_elekk_doubles_a_card_shuffled_into_the_opponents_deck():
    # La copie va au deck où la carte est mélangée (le wiki : Seaforium Bomber).
    game = prepare_empty_game()
    game.player1.give("BOT_559").play()
    game.player1.give("BOT_511").play()
    assert len(game.player2.deck) == 2
    assert len(game.player1.deck) == 0
    game.player1.give(WISP).shuffle_into_deck()
    assert len(game.player1.deck) == 2


def test_omega_assembly_keeps_three_different_mechs():
    # À 10 cristaux, les trois cartes de la découverte sont distinctes.
    for _ in range(8):
        game = prepare_empty_game()
        _fresh_mana(game)
        game.player1.give("BOT_299").play()
        assert game.player1.choice is None
        assert len(game.player1.hand) == 3
        assert len(set(c.id for c in game.player1.hand)) == 3
    game = prepare_empty_game()
    game.player1.max_mana = 9
    game.player1.used_mana = 0
    game.player1.give("BOT_299").play()
    assert game.player1.choice is not None
    assert len(game.player1.choice.cards) == 3


def test_gloop_sprayer_puts_one_copy_on_each_side_of_itself():
    # D-108 : deux serviteurs invoqués à la fois par un serviteur en jeu, un de chaque côté.
    game = prepare_empty_game()
    left = game.player1.give(WISP).play()
    right = game.player1.give(MECH).play()
    game.player1.give("BOT_507").play(index=1)
    assert [m.id for m in game.player1.field] == [
        WISP,
        WISP,
        "BOT_507",
        MECH,
        MECH,
    ]
    # Un seul voisin : sa copie se pose de son côté.
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give("BOT_507").play(index=1)
    assert [m.id for m in game.player1.field] == [WISP, WISP, "BOT_507"]


def test_violet_haze_adds_deathrattle_weapons_too():
    # A116 (D-108): "on ajoute les armes aussi" (5% of the pool: 300 cards
    # make a miss a one in five million).
    game = prepare_empty_game()
    seen = set()
    for _ in range(150):
        game.player1.used_mana = 0
        game.player1.give("BOT_084").play()
        for card in list(game.player1.hand):
            assert card.has_deathrattle
            seen.add(card.type)
            card.discard()
    assert CardType.WEAPON in seen
    assert CardType.MINION in seen


def test_power_word_replicate_puts_the_copy_right_of_the_original():
    # A120 (D-108): "à droite de l'original".
    game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)
    first = game.player1.give(WISP).play()
    game.player1.give(CHICKEN).play()
    game.player1.give(MURLOC).play()
    game.player1.give("BOT_529").play(target=first)
    assert [m.id for m in game.player1.field] == [WISP, WISP, CHICKEN, MURLOC]
    copy = game.player1.field[1]
    assert (copy.atk, copy.health) == (5, 5)
    assert copy is not first
    # the original, in the middle: the copy follows it
    game.player1.used_mana = 0
    game.player1.give("BOT_529").play(target=game.player1.field[2])
    assert [m.id for m in game.player1.field] == [WISP, WISP, CHICKEN, CHICKEN, MURLOC]
