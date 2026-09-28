"""
Gift Exchange
"""

from ..utils import *


class TB_GiftExchange_Snowball:
    """Hardpacked Snowballs"""

    play = Bounce(RANDOM_ENEMY_MINION) * 3


class TB_GiftExchange_Treasure:
    """Winter Veil Gift"""

    deathrattle = Give(CURRENT_PLAYER, "TB_GiftExchange_Treasure_Spell")


class GiftClass(LazyValue):
    """
    The class of the player who controlled the Winter Veil Gift: the gift
    created the Stolen Gift (its deathrattle gave it), and is dead by then.
    """

    def evaluate(self, source):
        creator = getattr(source, "creator", None)
        player = creator.controller if creator is not None else source.controller
        return player.hero.card_class


class TB_GiftExchange_Treasure_Spell:
    """Stolen Winter Veil Gift"""

    # The wiki (Gift Exchange): "Discover a card belonging to the class of the
    # player who controlled the Winter Veil Gift minion, with its mana cost
    # reduced by 5"; spells and minions of 5 or more, no neutral card.
    RandomGift = RandomCollectible(
        cost=range(5, 100),
        type=[CardType.MINION, CardType.SPELL],
        card_class=GiftClass(),
    )
    play = Discover(CONTROLLER, RandomGift).then(
        Give(CONTROLLER, Discover.CARD),
        Buff(Discover.CARD, "TB_GiftExchange_Enchantment"),
    )


# Cheap Gift
class TB_GiftExchange_Enchantment:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -5}
