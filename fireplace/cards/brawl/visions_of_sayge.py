"""
Visions of Sayge
"""

from ..utils import *


class SaygeChoice(GenericChoice):
    """
    The choice of Visions of Sayge: the card chosen goes to the hand of the
    player who chooses, the other one to the hand of the opponent (a full
    hand loses it, as a draw would).
    """

    def choose(self, card):
        others = [c for c in self.cards if c is not card]
        opponent = self.player.opponent
        for other in others:
            # GenericChoice discards what is not chosen: this one goes over.
            self.cards.remove(other)
        super().choose(card)
        for other in others:
            other.controller = opponent
            if len(opponent.hand) < opponent.max_hand_size:
                other.zone = Zone.HAND
            else:
                other.discard()
        self.cards.extend(others)


@custom_card
class TB_VisionsOfSayge_Rule:
    """Visions of Sayge"""

    # Not in CardDefs.xml: the rule of the brawl, on each player. The wiki
    # (Visions of Sayge): "At the start of each turn, the player is offered a
    # choice between two cards to add to their hand. The card they don't
    # choose is given to the opponent." and "Cards are still drawn from the
    # deck at the start of the turn." The two cards are collectible cards
    # drawn at random (the page names no pool); the draw of the turn waits
    # for the choice.
    tags = {
        GameTag.CARDNAME: "Visions of Sayge",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    events = OWN_TURN_BEGIN.on(SaygeChoice(CONTROLLER, RandomCollectible() * 2))
