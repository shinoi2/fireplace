"""
Wacky Waxy Winter's Veil
"""

from ..utils import *

GIFTS_PER_DROP = 4
# The wiki (Wacky Waxy Winter's Veil): "All gifts are summoned on turn 1. This
# allows player 2 to immediately attack with theirs if they're given a buff."
# and "At Turn 7, 4 more presents will drop on each side of the board. If
# there are not enough presents to fit the board, then it will only drop as
# much as it can fill the board." The turns of the game, not of a player.
DROP_TURNS = (1, 7)


class TB_KoboldGiftMinion:
    """Large Waxy Gift"""

    # Deathrattle: Add a random Legendary minion to your opponent's hand. It
    # costs (3) less.
    deathrattle = Give(OPPONENT, RandomLegendaryMinion()).then(
        Buff(Give.CARD, "TB_KoboldGiftMinione")
    )


@custom_card
class TB_KoboldGiftMinione:
    # Not in CardDefs.xml: "It costs (3) less." (as Cheap Gift does for Gift
    # Exchange); lost once played.
    tags = {
        GameTag.CARDNAME: "Large Waxy Gift",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -3,
    }
    events = REMOVED_IN_PLAY


DROP = Summon(CONTROLLER, "TB_KoboldGiftMinion") * GIFTS_PER_DROP


class TB_KoboldGiftSpell:
    """Great Father Kobold Spell"""

    # The presents dropping on its player's side: four Large Waxy Gifts, as
    # many as the board takes.
    play = DROP


def _drop(self, player, *args):
    if self.game.turn in DROP_TURNS:
        return [DROP]
    return []


class TB_KoboldGiftEnch:
    """Great Father Kobold Enchant"""

    # The rule of the brawl, on each player: the presents drop at the start
    # of turns 1 and 7 of the game, on each side.
    events = TURN_BEGIN.on(_drop)
