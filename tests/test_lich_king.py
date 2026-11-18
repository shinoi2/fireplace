import pytest

from utils import *


def test_sunwell_cost_tracks_other_cards_in_its_owners_hand():
    game = prepare_empty_game()
    game.player1.discard_hand()
    sunwell = game.player1.give("RLK_590")
    assert sunwell.cost == 9
    other = game.player1.give(WISP)
    assert sunwell.cost == 8
    game.player2.give(WISP)
    assert sunwell.cost == 8
    other.discard()
    assert sunwell.cost == 9
    second = game.player1.give("RLK_590")
    assert sunwell.cost == second.cost == 8


@pytest.mark.parametrize(
    "limit,other_cards", [(10, 0), (10, 4), (10, 9), (12, 0), (12, 11)]
)
def test_sunwell_fills_available_hand_slots_with_permanent_spells(limit, other_cards):
    game = prepare_empty_game()
    game.player1.discard_hand()
    if limit == 12:
        game.player1.give("DRG_208").play()
        game.player1.used_mana = 0
    original = [game.player1.give(WISP) for _ in range(other_cards)]
    sunwell = game.player1.give("RLK_590")
    assert sunwell.cost == max(0, 9 - other_cards)
    with mock(RandomSpell, lambda picker, source: [source.controller.card(FIREBALL)]):
        sunwell.play()
    assert len(game.player1.hand) == limit
    assert all(card in game.player1.hand for card in original)
    generated = game.player1.hand.filter(id=FIREBALL)
    assert len(generated) == limit - other_cards
    assert all(card.type == CardType.SPELL for card in generated)
    assert len({card.entity_id for card in generated}) == len(generated)
    assert sunwell.zone == Zone.GRAVEYARD
    game.end_turn()
    assert len(game.player1.hand) == limit
