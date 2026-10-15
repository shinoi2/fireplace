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


class REV_906:
    """Sire Denathrius"""

    # <b><b>Lifesteal</b>.</b> <b>Battlecry:</b> Deal 5 damage amongst enemies.
    # <b>Endlessly Infuse (1):</b> Deal 1 more.
    pass


class REV_238:
    """Theotar, the Mad Duke"""

    # <b>Battlecry:</b> <b>Discover</b> a card in each player's hand and swap
    # them.
    pass


class MAW_033:
    """Sylvanas, the Accused"""

    # [x]<b>Battlecry:</b> Destroy an enemy minion. <b>Infuse (@):</b> Take
    # control of it instead.
    pass


class MAW_034:
    """The Jailer"""

    # <b>Battlecry:</b> Destroy your  deck. For the rest of the game, your
    # minions are <b>Immune</b>.
    pass


class REV_021:
    """Kael'thas Sinstrider"""

    # Every third minion you play each turn costs (0).
    pass


class REV_022:
    """Murloc Holmes"""

    # [x]<b>Battlecry:</b> Solve 3 Clues about your opponent's cards to get
    # copies of them.
    pass
