from ..utils import *

##
# Minions


class AV_261:
    """Flag Runner"""

    # Whenever a friendly minion dies, gain +1 Attack.
    events = Death(FRIENDLY_MINIONS).on(Buff(SELF, "AV_261e"))


AV_261e = buff(atk=1)


class AV_262:
    """Warden of Chains"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If you're holding a Demon that costs
    # (5) or more, gain +1/+2.
    powered_up = Find(FRIENDLY_HAND + DEMON + (COST >= 5) - SELF)
    play = powered_up & Buff(SELF, "AV_262e2")


AV_262e2 = buff(atk=1, health=2)


class AV_265:
    """Ur'zul Giant"""

    # Costs (1) less for each friendly minion that died this game.
    cost_mod = -Count(FRIENDLY + KILLED + MINION)


class AV_267:
    """Caria Felsoul"""

    # <b>Battlecry:</b> Transform into a 6/6 copy of a Demon in your deck.
    play = Morph(SELF, RANDOM(FRIENDLY_DECK + DEMON)).then(Buff(SELF, "AV_267e2"))


class AV_267e2:
    atk = SET(6)
    max_health = SET(6)


class ONY_036:
    """Razorglaive Sentinel"""

    # After you play the left or right-most card in your hand, draw a card.
    events = Play(CONTROLLER, PLAY_OUTCAST).after(Draw(CONTROLLER))


class AV_118:
    """Battleworn Vanguard"""

    # [x]After your hero attacks, summon two 1/1 Felwings.
    events = Attack(FRIENDLY_HERO).after(SummonBothSides(CONTROLLER, "BT_922t") * 2)


##
# Spells


class AV_264:
    """Sigil of Reckoning"""

    # At the start of your next turn, summon a random Demon from your hand.
    events = OWN_TURN_BEGIN.on(Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON)))


class AV_269:
    """Flanking Maneuver"""

    # Summon a 4/2 Demon with <b>Rush</b>. If it dies this turn, summon
    # another.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "AV_269t").then(Buff(Summon.CARD, "AV_269e"))


class AV_269e:
    events = Death(OWNER).on(Summon(CONTROLLER, "AV_269t"))


class ONY_014:
    """Keen Reflex"""

    # [x]Deal $1 damage to all minions. <b>Honorable Kill:</b> Gain +1 Attack
    # this turn.
    play = Hit(ALL_MINIONS, 1)
    honorable_kill = Buff(FRIENDLY_HERO, "ONY_014e")


ONY_014e = buff(atk=1)


class ONY_016:
    """Wings of Hate (Rank 1)"""

    # Summon two 1/1 Felwings. <i>(Upgrades when you have 5 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "ONY_016t")

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "BT_922t") * 2


class ONY_016t:
    """Wings of Hate (Rank 2)"""

    # [x]Summon three 1/1 Felwings. <i>(Upgrades when you have 10 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "ONY_016t2")

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "BT_922t") * 3


class ONY_016t2:
    """Wings of Hate (Rank 3)"""

    # Summon four 1/1 Felwings.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "BT_922t") * 4


class AV_661:
    """Field of Strife"""

    # [x]Your minions have +1 Attack. Lasts 3 turns.
    update = Refresh(FRIENDLY_MINIONS, buff="AV_661e2")


AV_661e2 = buff(atk=1)


##
# Weapons


class AV_209:
    """Dreadprison Glaive"""

    # [x]<b>Honorable Kill:</b> Deal damage equal to your hero's Attack to the
    # enemy hero.
    honorable_kill = Hit(ENEMY_HERO, ATK(FRIENDLY_HERO))


##
# Heros


class AV_204:
    """Kurtrus, Demon-Render"""

    # [x]<b>Battlecry:</b> Summon two @/4 Demons with <b>Rush</b>. <i>(Improved
    # by your hero attacks this game.)</i>
    play = (
        SummonCustomMinion(
            CONTROLLER, "AV_204t2", 3, HERO_ATTACKS_THIS_GAME(CONTROLLER) + 1, 4
        )
        * 2
    )


class AV_204p:
    """Ashfallen's Fury"""

    # <b>Hero Power</b> +2 Attack this turn. After a friendly minion attacks,
    # refresh this.
    activate = Buff(FRIENDLY_HERO, "AV_204e")
    events = Death(FRIENDLY_MINIONS).on(RefreshHeroPower(SELF))


AV_204e = buff(atk=2)
