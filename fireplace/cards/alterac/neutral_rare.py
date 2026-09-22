from ..utils import *

##
# Minions


class AV_112:
    """Snowblind Harpy"""

    # <b>Battlecry:</b> If you're holding a Frost spell, gain 5 Armor.
    powered_up = Find(FRIENDLY_HAND + FROST)
    play = powered_up & GainArmor(FRIENDLY_HERO, 5)


class AV_134:
    """Frostwolf Warmaster"""

    # Costs (1) less for each card you've played this turn.
    cost_mod = -NUM_CARDS_PLAYED_THIS_TURN


class AV_135:
    """Stormpike Marshal"""

    # [x]<b>Taunt</b> If you took 5 or more damage on your opponent's turn,
    # this costs (1).
    class Hand:
        update = (DAMAGED_ON_OPPONENT_TURN(FRIENDLY_HERO) >= 5) & Refresh(
            SELF, {GameTag.COST: SET(1)}
        )


class AV_136:
    """Kobold Taskmaster"""

    # [x]<b>Battlecry:</b> Add 2 Armor Scraps to your hand that give +2 Health
    # to a minion.
    play = Give(CONTROLLER, "AV_136t") * 2


class AV_136t:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "AV_136e")


AV_136e = buff(health=2)


class AV_137:
    """Irondeep Trogg"""

    # [x]After your opponent casts a spell, summon _another Irondeep Trogg.
    events = Play(OPPONENT, SPELL).after(Summon(CONTROLLER, "AV_137"))


class ONY_002:
    """Gear Grubber"""

    # <b>Taunt</b>. If you end your turn with any unspent Mana, reduce this
    # card's Cost by (1).
    class Hand:
        events = OWN_TURN_END.on(
            (CURRENT_MANA(CONTROLLER) > 0) & Buff(SELF, "ONY_002e")
        )


class ONY_002e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY
