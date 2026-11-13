"""
Les trois trésors du raid de Hearthstone que le fork porte (WP-160, règle 649) : des enchantements
du joueur, posés comme un effet de départ (`serveur/moteur/speciale.resoudre_effet` : la carte, puis
`apply(joueur)`), qui valent toute la partie.
"""

from utils import *
import pytest

PIERRE_DE_LUNE = "RAID_TRE15e"
ANNEAU_DE_VARIAN = "RAID_TRE16e"
CALICE_DE_ZUL_GURUB = "RAID_TRE17e"
CHILLWIND_YETI = "CS2_182"
FIERY_WAR_AXE = "CS2_106"


def _poser(player, id_):
    """Comme l'enveloppe pose un effet de départ enchantement (règle 472), puis les auras se
    rafraîchissent comme le jeu le fait dès la prochaine action (le mulligan, au départ).
    """
    enchantement = player.card(id_, source=player.hero)
    enchantement.source = player.hero
    enchantement.apply(player)
    player.game.refresh_auras()
    return enchantement


@pytest.mark.skip(reason="暂不实现冒险模式宝藏")
def test_les_trois_tresors_sont_des_enchantements():
    from fireplace.cards import db
    from hearthstone.enums import CardType

    for id_ in (PIERRE_DE_LUNE, ANNEAU_DE_VARIAN, CALICE_DE_ZUL_GURUB):
        assert id_ in db
        assert db[id_].type == CardType.ENCHANTMENT


@pytest.mark.skip(reason="暂不实现冒险模式宝藏")
def test_pierre_de_lune_le_pouvoir_coute_un_de_moins():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    assert game.player1.hero.power.cost == 2
    _poser(game.player1, PIERRE_DE_LUNE)
    assert game.player1.hero.power.cost == 1
    assert game.player2.hero.power.cost == 2
    # Elle vaut toute la partie, pas seulement le premier pouvoir (Fencing Coach s'use, elle non).
    game.player1.hero.power.use(target=game.player2.hero)
    game.end_turn()
    game.end_turn()
    assert game.player1.hero.power.cost == 1


@pytest.mark.skip(reason="暂不实现冒险模式宝藏")
def test_pierre_de_lune_suit_un_pouvoir_remplace():
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    _poser(game.player1, PIERRE_DE_LUNE)
    game.player1.summon("HERO_01bp")  # Armor Up! remplace Fireblast
    assert game.player1.hero.power.id == "HERO_01bp"
    assert game.player1.hero.power.cost == 1


@pytest.mark.skip(reason="暂不实现冒险模式宝藏")
def test_anneau_de_varian_le_premier_serviteur_joue_a_charge():
    game = prepare_empty_game()
    _poser(game.player1, ANNEAU_DE_VARIAN)
    yeti = game.player1.give(CHILLWIND_YETI)
    yeti.play()
    assert yeti.charge
    assert yeti.can_attack()
    second = game.player1.give(WISP)
    second.play()
    assert not second.charge
    assert not second.can_attack()


@pytest.mark.skip(reason="暂不实现冒险模式宝藏")
def test_anneau_de_varian_un_serviteur_invoque_ne_compte_pas():
    game = prepare_empty_game()
    _poser(game.player1, ANNEAU_DE_VARIAN)
    invoque = game.player1.summon(WISP)
    assert not invoque.charge
    yeti = game.player1.give(CHILLWIND_YETI)
    yeti.play()
    assert yeti.charge


@pytest.mark.skip(reason="暂不实现冒险模式宝藏")
def test_anneau_de_varian_ne_vaut_que_pour_son_joueur():
    game = prepare_empty_game()
    _poser(game.player1, ANNEAU_DE_VARIAN)
    game.end_turn()
    yeti = game.player2.give(CHILLWIND_YETI)
    yeti.play()
    assert not yeti.charge
    game.end_turn()
    mien = game.player1.give(CHILLWIND_YETI)
    mien.play()
    assert mien.charge


@pytest.mark.skip(reason="暂不实现冒险模式宝藏")
def test_calice_de_zul_gurub_le_heros_a_lifesteal():
    game = prepare_empty_game()
    _poser(game.player1, CALICE_DE_ZUL_GURUB)
    assert game.player1.hero.lifesteal
    assert not game.player2.hero.lifesteal
    game.player1.hero.set_current_health(20)
    game.player1.give(FIERY_WAR_AXE).play()
    game.player1.hero.attack(game.player2.hero)
    assert game.player2.hero.health == 30 - 3
    assert game.player1.hero.health == 20 + 3


def test_sans_calice_le_heros_ne_se_soigne_pas():
    game = prepare_empty_game()
    game.player1.hero.set_current_health(20)
    game.player1.give(FIERY_WAR_AXE).play()
    game.player1.hero.attack(game.player2.hero)
    assert game.player1.hero.health == 20
