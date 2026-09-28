"""
Blingtron's Beauteous Brawl
"""

from ..utils import *


class TP_Bling_HP2:
    """Cash In"""

    activate = Destroy(FRIENDLY_WEAPON)


class TB_BlingBrawl_Blade1e:
    """Blingtron's Blade"""

    # A Death event does not reach the enchantments of the weapon that dies:
    # the new weapon comes from a deathrattle of the enchantment.
    deathrattle = Summon(CONTROLLER, RandomWeapon())
    tags = {GameTag.DEATHRATTLE: True}


@custom_card
class TB_BlingBrawl_Blade2:
    """Blingtron's Blade HERO"""

    # Not in CardDefs.xml: the rule of the brawl, on each player.
    tags = {
        GameTag.CARDNAME: "Blingtron's Blade HERO",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    events = Summon(CONTROLLER, WEAPON).on(Buff(Summon.CARD, "TB_BlingBrawl_Blade1e"))


class TB_BlingBrawl_Hero1p:
    """Sharpen (Unused)"""

    activate = Buff(FRIENDLY_WEAPON, "TB_BlingBrawl_Hero1e")


TB_BlingBrawl_Hero1e = buff(atk=1)
