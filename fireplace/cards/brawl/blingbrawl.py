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


class TB_BlingBrawl_Blade2e:
    """Blingtron's Blade HERO"""

    # The rule of the brawl, on each player (CardDefs.xml names it with an
    # "e", like every enchantment).
    events = Summon(CONTROLLER, WEAPON).on(Buff(Summon.CARD, "TB_BlingBrawl_Blade1e"))


class TB_BlingBrawl_Hero1p:
    """Sharpen (Unused)"""

    activate = Buff(FRIENDLY_WEAPON, "TB_BlingBrawl_Hero1e")


TB_BlingBrawl_Hero1e = buff(atk=1)
