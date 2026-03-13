from ..utils import *

##
# Minions


class CS3_024:
    """Taelan Fordring"""

    # [x]<b><b>Taunt</b>, Divine Shield</b> <b>Deathrattle:</b> Draw your
    # highest Cost minion.
    deathrattle = ForceDraw(RANDOM(HIGHEST_COST(FRIENDLY_DECK + MINION)))


class CS3_025:
    """Overlord Runthak"""

    # [x]<b>Rush</b>. Whenever this attacks, give +1/+1 to all minions in your
    # hand.
    events = Attack(SELF).on(Buff(FRIENDLY_HAND + MINION, "CS3_025e"))


CS3_025e = buff(+1, +1)


class CS3_031:
    """Alexstrasza the Life-Binder"""

    # [x]<b>Battlecry</b>: Choose a character. If it's friendly, restore 8
    # Health. If it's an ___enemy, deal 8 damage.
    play = Find(TARGET + FRIENDLY) & Heal(TARGET, 8) | Hit(TARGET, 8)


class CS3_032:
    """Onyxia the Broodmother"""

    # At the end of each turn, fill_your board with 1/1_Whelps.
    events = OWN_TURN_END.on(SummonBothSides(CONTROLLER, "ds1_whelptoken") * 7)


class CS3_033:
    """Ysera the Dreamer"""

    # <b>Battlecry:</b> Add one of each Dream card to your hand.
    play = (
        Give(CONTROLLER, "DREAM_01"),
        Give(CONTROLLER, "DREAM_02"),
        Give(CONTROLLER, "DREAM_03"),
        Give(CONTROLLER, "DREAM_04"),
        Give(CONTROLLER, "DREAM_05"),
    )


class CS3_034:
    """Malygos the Spellweaver"""

    # <b>Battlecry:</b> Draw spells until your hand is full.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class CS3_035:
    """Nozdormu the Eternal"""

    # [x]<b>Start of Game:</b> If this is in BOTH players' decks, turns _are
    # only 15 seconds long.
    class Deck:
        events = GameStart().on(
            Find(ENEMY_STARTING_DECK + ID("CS3_035")) & Buff(CONTROLLER, "CS3_035e")
        )

    class Hand:
        events = GameStart().on(
            Find(ENEMY_STARTING_DECK + ID("CS3_035")) & Buff(CONTROLLER, "CS3_035e")
        )


class CS3_035e:
    tags = {GameTag.TIMEOUT: SET(15)}


class CS3_036:
    """Deathwing the Destroyer"""

    # <b>Battlecry:</b> Destroy all other minions. Discard a card for each
    # destroyed.
    def play(self):
        minion_count = Count(ALL_MINIONS - SELF).evaluate(self)
        yield Destroy(ALL_MINIONS - SELF)
        yield Discard(RANDOM(FRIENDLY_HAND) * minion_count)
