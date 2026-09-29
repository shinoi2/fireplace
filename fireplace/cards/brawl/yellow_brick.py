"""
Yellow-Brick Brawl
"""

from ..utils import *


def _side(left):
    def select(entities, source):
        field = source.controller.field
        if source not in field:
            return []
        i = field.index(source)
        side = field[:i] if left else field[i + 1 :]
        return [m for m in side if not m.dormant]

    return FuncSelector(select)


MINIONS_TO_THE_LEFT = _side(True)
MINIONS_TO_THE_RIGHT = _side(False)


class TB_Dorothee_001:
    """Dorothee"""

    # Minions to the left have Charge. Minions to the right have Taunt.
    # The wiki (Yellow-Brick Brawl): "a permanent minion card": she "cannot be
    # targeted or attacked", "will not be affected by auras", "is not affected
    # by AoE effects", "does not count as a minion for effects that require a
    # certain number of minions", but "still take[s] up a minion space";
    # "Silence does not remove the Charge or Taunt effects granted by
    # Dorothee". A permanent is dormant for good (as Nether Portal is): what
    # fireplace does for a dormant minion does all of that; her aura acts
    # while she is dormant.
    tags = {GameTag.DORMANT: True}
    dormant_update = (
        Refresh(MINIONS_TO_THE_LEFT, {GameTag.CHARGE: True}),
        Refresh(MINIONS_TO_THE_RIGHT, {GameTag.TAUNT: True}),
    )
