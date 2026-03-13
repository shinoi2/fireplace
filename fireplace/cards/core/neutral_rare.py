from ..utils import *

##
# Minions


class CS3_022:
    """Fogsail Freebooter"""

    # <b>Battlecry:</b> If you have a weapon equipped, deal_2_damage.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_WEAPON_EQUIPPED: 0}
    play = Hit(TARGET, 2)
