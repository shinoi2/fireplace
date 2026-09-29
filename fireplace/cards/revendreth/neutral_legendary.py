from ..utils import *

##
# Minions


class REV_018:
    """Prince Renathal"""

    # [x]Your deck size and starting Health are 40.
    class Hand:
        events = GameStart().on(Buff(FRIENDLY_HERO, "REV_018e"))

    class Deck:
        events = GameStart().on(Buff(FRIENDLY_HERO, "REV_018e"))


@custom_card
class REV_018e:
    tags = {
        GameTag.CARDNAME: "Prince Renathal Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    max_health = SET(40)
