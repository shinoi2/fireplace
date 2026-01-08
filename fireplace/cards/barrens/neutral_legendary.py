from ..utils import *


class BAR_080:
    """Shadow Hunter Vol'jin"""

    # <b>Battlecry:</b> Choose a minion. Swap it with a random one in its
    # owners hand.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Find(TARGET + FRIENDLY) & Swap(
        TARGET, RANDOM(FRIENDLY_HAND + MINION)
    ) | Swap(TARGET, RANDOM(ENEMY_HAND + MINION))
