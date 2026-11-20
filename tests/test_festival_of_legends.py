import pytest

from hearthstone.deckstrings import write_deckstring
from hearthstone.enums import CardClass, CardType, FormatType

from fireplace.cards import db
from fireplace.cards.utils import decode_deckstring
from utils import BaseTestGame, Player

ETC = "ETC_080"
BAND = ["CS2_029", "CS2_120", "SCH_259"]


def test_etc_discovers_each_member_once_from_the_controllers_band():
    sideboards = {ETC: BAND[:]}
    player = Player(
        "Player 1", [ETC], CardClass.MAGE.default_hero, sideboards=sideboards
    )
    opponent = Player("Player 2", [], CardClass.MAGE.default_hero, is_standard=False)
    game = BaseTestGame(players=(player, opponent))
    game.random.seed(14)
    for owner in game.players:
        owner.cant_fatigue = True
    game.start()

    assert game.current_player is player
    assert not player.is_standard
    assert [card.id for card in player.starting_deck] == [ETC]
    assert [card.id for card in player.hand] == [ETC]

    player.summon("LOE_077")  # Brann runs both choices through the same sideboard.
    player.hand[0].play()
    for count, expected in enumerate(BAND[:2]):
        assert [card.id for card in player.choice.cards] == BAND[count:]
        chosen = player.choice.cards[0]
        player.choice.choose(chosen)
        assert player.hand[-1].id == expected
    assert player.choice is None

    player.give(ETC).play()
    assert [card.id for card in player.choice.cards] == BAND[2:]
    player.choice.choose(player.choice.cards[0])
    assert player.choice is None and not player.sideboards[ETC]
    assert sideboards[ETC] == BAND
    assert not opponent.sideboards

    player.used_mana = 0
    player.give(ETC).play()
    assert player.choice is None

    game.end_turn()
    opponent.give(ETC).play()
    assert opponent.choice is None


def test_etc_sideboard_survives_deckstring_import():
    hero_id = CardClass.MAGE.default_hero
    manager_id = db[ETC].dbf_id
    deckstring = write_deckstring(
        [(manager_id, 1)],
        [db[hero_id].dbf_id],
        FormatType.FT_WILD,
        [(db[card_id].dbf_id, 1, manager_id) for card_id in BAND],
    )

    imported_hero, cards = decode_deckstring(deckstring)

    assert imported_hero == hero_id
    assert list(cards) == [ETC]
    assert sorted(cards.sideboards[ETC]) == sorted(BAND)
    assert Player("Imported", cards, imported_hero).sideboards == cards.sideboards
    assert Player("Empty band", cards, imported_hero, sideboards={}).sideboards == {}


def test_etc_band_counts_for_deck_limits_but_not_deck_size():
    hero = "HERO_08a"
    filler = db.filter(
        collectible=True,
        card_class=CardClass.NEUTRAL,
        type=CardType.MINION,
        exclude=BAND + [ETC],
    )[:29]
    deck = [ETC, *filler]
    assert Player("Mage", deck, hero, False, sideboards={ETC: BAND}).is_legal()

    duplicate_legendary = [*deck[:-1], "SCH_259"]
    assert not Player(
        "Mage", duplicate_legendary, hero, False, sideboards={ETC: BAND}
    ).is_legal()


@pytest.mark.parametrize(
    "owner_in_deck, sideboards",
    [
        (True, {}),
        (False, {ETC: BAND}),
        (True, {"CS2_120": BAND}),
        (True, {ETC: BAND[:2]}),
        (True, {ETC: [*BAND, "CS2_182"]}),
        (True, {ETC: [*BAND[:2], "MISSING_CARD"]}),
        (True, {ETC: [*BAND[:2], "GAME_005"]}),
        (True, {ETC: [*BAND[:2], "CS2_091"]}),
    ],
)
def test_player_rejects_invalid_sideboards(owner_in_deck, sideboards):
    filler = db.filter(
        collectible=True,
        card_class=CardClass.NEUTRAL,
        type=CardType.MINION,
        exclude=BAND + [ETC],
    )
    deck = [ETC, *filler[:29]] if owner_in_deck else filler[:30]
    player = Player("Mage", deck, "HERO_08a", False, sideboards=sideboards)

    assert not player.is_legal()
