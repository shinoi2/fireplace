from ..utils import *

##
# Minions


class TSC_032:
    """Blademaster Okani"""

    # [x]<b>Battlecry:</b> <b>Secretly</b> choose to <b>Counter</b> the next
    # minion or spell your opponent plays while this is alive.
    play = Choice(CONTROLLER, ["TSC_032t", "TSC_032t2"]).then(
        StoringBuff(SELF, "TSC_032e3", Choice.CARD)
    )


class TSC_032e3:
    """Blade Counter"""

    # This <b>Counters</b> the next <b>Secretly</b> chosen minion or spell your
    # opponent plays.@Okani will <b>Secretly</b> counter the next minion your
    # opponent plays.@Okani will <b>Secretly</b> counter the next spell your
    # opponent plays.
    events = (
        Play(OPPONENT, MINION).on(
            FindId(STORE_CARD, "TSC_032t") & (Counter(Play.CARD), Destroy(SELF))
        ),
        Play(OPPONENT, SPELL).on(
            FindId(STORE_CARD, "TSC_032t") & (Counter(Play.CARD), Destroy(SELF))
        ),
    )
