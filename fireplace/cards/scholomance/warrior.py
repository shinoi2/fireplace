from ..utils import *


##
# Minions


class SCH_317:
    """Playmaker"""

    # [x]After you play a <b>Rush</b> minion, summon a copy _with 1 Health
    # remaining.
    events = Play(CONTROLLER, RUSH + MINION).after(
        Summon(CONTROLLER, ExactCopy(Play.CARD)).then(SetCurrentHealth(Summon.CARD, 1))
    )


class SCH_337:
    """Troublemaker"""

    # At the end of your turn, summon two 3/3 Ruffians that attack random
    # enemies.
    events = OWN_TURN_END.on(
        Summon(CONTROLLER, "SCH_337t").then(
            Attack(Summon.CARD, RANDOM(ENEMY_CHARACTERS))
        )
        * 2
    )


class SCH_621:
    """Rattlegore"""

    # <b>Deathrattle:</b> Resummon this with -1/-1.
    deathrattle = Summon(CONTROLLER, ExactCopy(SELF)).then(
        SummonCustomMinion(
            CONTROLLER, "SCH_621", 9, ATK(SELF) - 1, MAX_HEALTH(SELF) - 1
        )
    )


##
# Spells


class SCH_237:
    """Athletic Studies"""

    # <b>Discover</b> a <b>Rush</b> minion. Your next one costs (1) less.
    play = DISCOVER(RandomMinion(rush=True)), Buff(CONTROLLER, "SCH_237e")


class SCH_237e:
    update = Refresh(FRIENDLY_HAND + RUSH + MINION, "SCH_237e2")
    events = Play(CONTROLLER, RUSH + MINION).after(Destroy(SELF))


class SCH_237e2:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class SCH_525:
    """In Formation!"""

    # Add 2 random <b>Taunt</b> minions to your hand.
    play = Give(CONTROLLER, RandomMinion(taunt=True)) * 2


##
# Weapons


class SCH_238:
    """Reaper's Scythe"""

    # [x]<b>Spellburst</b>: Also damages adjacent minions this turn.
    spellburst = Buff(SELF, "SCH_238e")


class SCH_238e:
    events = Attack(FRIENDLY_HERO).on(
        Hit(ADJACENT(Attack.DEFENDER), ATK(FRIENDLY_HERO))
    )
