from ..utils import *


##
# Minions


class SCH_162:
    """Vectus"""

    # [x]<b>Battlecry:</b> Summon two 1/1 Whelps. Each gains a
    # <b>Deathrattle</b> from your minions that died this game.
    play = (
        Summon(CONTROLLER, "SCH_162t").then(
            CopyDeathrattleBuff(
                RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE),
                "SCH_162e",
                source=Summon.CARD,
            )
        )
        * 2
    )


class SCH_224:
    """Headmaster Kel'Thuzad"""

    # <b>Spellburst:</b> If the spell destroys any minions, summon them.

    # TODO: need to be tested
    spellburst = Summon(CONTROLLER, Copy(ALL_MINIONS + DEAD))


class SCH_428:
    """Lorekeeper Polkelt"""

    # [x]<b>Battlecry:</b> Reorder your deck from the highest Cost card to the
    # lowest Cost card.
    def play(self):
        self.controller.deck.sort(key=lambda x: x.cost, reverse=True)


class SCH_717:
    """Keymaster Alabaster"""

    # [x]Whenever your opponent _draws a card, add a copy to_ _your hand that
    # costs (1).
    events = Draw(OPPONENT).on(
        Give(CONTROLLER, Copy(Draw.CARD)).then(Buff(Draw.CARD, "SCH_717e"))
    )


class SCH_717e:
    tags = {GameTag.COST: SET(1)}
    events = REMOVED_IN_PLAY


##
# Weapons


class SCH_259:
    """Sphere of Sapience"""

    # [x]At the start of your turn, look at your top card. You can put it on
    # the bottom _and lose 1 Durability.

    # TODO: need to be tested
    events = OWN_TURN_BEGIN.on(
        Choice(CONTROLLER, ["SCH_259t", FRIENDLY_DECK[-1]]).then(
            Switch(
                Choice.CARD,
                {
                    "SCH_259t": (
                        PutOnBottom(CONTROLLER, FRIENDLY_DECK[-1]),
                        Hit(SELF, 1),
                    ),
                },
            )
        )
    )
