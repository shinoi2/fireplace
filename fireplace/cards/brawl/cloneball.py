"""
Cloneball!
"""

from ..utils import *


def _other_copies(entities, source):
    # The copies of the legendary minion just played (Play.CARD), in the hand
    # and in the deck of the player who plays it.
    card = source.event_args[1]
    player = source.controller
    return [
        e for e in list(player.hand) + list(player.deck) if e.id == card.id and e is not card
    ]


OTHER_COPIES_OF_PLAYED = FuncSelector(_other_copies)


class TB_Superfriends001:
    """Offensive Play"""

    # The next Legendary minion you play and all your other copies cost (3)
    # less. The wiki (Cloneball!): "The effect from Offensive Play lasts until
    # the player plays a legendary minion card, and can stack multiple times."
    play = Buff(CONTROLLER, "TB_Superfriends001e")


class TB_Superfriends001e:
    """Facilitated"""

    # On the player: every Legendary minion in the hand costs (3) less, until
    # one is played; its other copies (hand and deck) then keep the (3) less.
    update = Refresh(FRIENDLY_HAND + LEGENDARY + MINION, {GameTag.COST: -3})
    events = Play(CONTROLLER, LEGENDARY + MINION).on(
        Buff(OTHER_COPIES_OF_PLAYED, "TB_Superfriends001e2"), Destroy(SELF)
    )


@custom_card
class TB_Superfriends001e2:
    # Not in CardDefs.xml: what the other copies keep, for good.
    tags = {
        GameTag.CARDNAME: "Offensive Play",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -3,
    }
