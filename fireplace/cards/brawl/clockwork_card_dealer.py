"""
Clockwork Card Dealer
"""

from ..utils import *


class DealOnCurve(TargetedAction):
    """
    The card that the draw at the start of the turn of player targets gives:
    one whose cost is the number of that player's turn, when the deck has
    one (drawn at random among them); else the draw is left as it is.
    """

    TARGET = ActionArg()

    def do(self, source, target):
        turn = len(target.turns)
        on_curve = [card for card in target.deck if card.cost == turn]
        if not on_curve:
            return
        card = source.game.random.choice(on_curve)
        # The draw takes the end of the deck.
        target.deck.remove(card)
        target.deck.append(card)


class TB_GreatCurves_01:
    """TB_ClockworkCardDealer"""

    # The rule of the brawl, on each player. The wiki (Clockwork Card
    # Dealer): "the card draw at the start of each turn will always try to
    # draw a card whose mana cost matches the turn number, with a 1-mana card
    # drawn on turn 1, a 2-mana card drawn on turn 2, and so on. If the deck
    # lacks an appropriate on-curve draw on a given turn, a random card will
    # be drawn instead"; "The on-curve rule only applies to the cards drawn at
    # the start of each turn"; "The card drawn is based on the turn number
    # rather than the amount of mana available to the player." The turn of
    # the player (its mana curve): the second player draws a 1 on its first
    # turn.
    events = OWN_TURN_BEGIN.on(DealOnCurve(CONTROLLER))
