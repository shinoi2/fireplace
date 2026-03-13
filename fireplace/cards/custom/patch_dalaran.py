from ..utils import *


class VAN_EX1_145:
    play = Buff(CONTROLLER, "VAN_EX1_145o")


class VAN_EX1_145o:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -3})
    events = OWN_SPELL_PLAY.on(Destroy(SELF))
