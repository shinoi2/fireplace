"""
Miniature Warfare
"""

from ..utils import *


class TB_Mini_1e:
    """Miniature"""

    atk = SET(1)
    max_health = SET(1)
    cost = SET(1)


@custom_card
class TB_Mini_Rule:
    """Miniature Warfare"""

    # Not in CardDefs.xml: the rule of the brawl, on each player. The wiki
    # (Miniature Warfare): Miniature "is granted to all minions while still in
    # the hand, and affects all minions whether played from the hand, or
    # summoned by spells, Hero Powers, or other minions' effects"; it is
    # "applied through a game-wide aura, and as a result cannot be removed
    # through Silences". Only minions: an aura on the player's minions, in the
    # deck, in the hand and in play.
    tags = {
        GameTag.CARDNAME: "Miniature Warfare",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    update = (
        Refresh(FRIENDLY_DECK + MINION, buff="TB_Mini_1e"),
        Refresh(FRIENDLY_HAND + MINION, buff="TB_Mini_1e"),
        Refresh(FRIENDLY_MINIONS, buff="TB_Mini_1e"),
    )
