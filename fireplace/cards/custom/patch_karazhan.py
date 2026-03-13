from ..utils import *


class VAN_CS2_103:
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "VAN_CS2_103e2")


VAN_CS2_103e2 = buff(atk=2, charge=True)
