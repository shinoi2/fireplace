from ..utils import *


##
# Minions


class SCH_142:
    """Voracious Reader"""

    # At the end of your turn, draw until you have 3 cards.
    events = OWN_TURN_END.on(DrawUntil(CONTROLLER, 3))


class SCH_146:
    """Robes of Protection"""

    # Your minions have "Can't be targeted by spells or Hero Powers."
    update = Refresh(FRIENDLY_MINIONS, {GameTag.CANT_BE_TARGETED_BY_SPELLS: True})


class SCH_713:
    """Cult Neophyte"""

    # <b>Battlecry:</b> Your opponent's spells cost (1) more next_turn.
    events = OWN_TURN_END.on(Buff(OPPONENT, "SCH_713e"))


class SCH_713e:
    update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +1})
    events = OWN_TURN_BEGIN.on(Destroy(SELF))
