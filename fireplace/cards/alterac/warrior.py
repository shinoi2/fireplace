from ..utils import *

##
# Minions


class AV_321:
    """Glory Chaser"""

    # After you play a <b>Taunt</b> minion, draw a card.
    events = Play(CONTROLLER, TAUNT).after(Draw(CONTROLLER))


class AV_323:
    """Scrapsmith"""

    # <b>Taunt</b> <b>Battlecry:</b> Add two 2/4 Grunts with <b>Taunt</b> to
    # your hand.
    play = Give(CONTROLLER, "AV_323t") * 2


class AV_145(metaclass=ThresholdUtils):
    """Captain Galvangar"""

    # [x]<b>Battlecry:</b> If you have gained 15 or more Armor this game, gain
    # +3/+3 and <b>Charge</b>.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = Buff(SELF, "AV_145e")


AV_145e = buff(+3, +3, charge=True)


class ONY_024:
    """Onyxian Drake"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Deal damage equal to your Armor to an
    # enemy minion.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, ARMOR(FRIENDLY_HERO))


class AV_565:
    """Axe Berserker"""

    # <b>Rush</b>. <b>Honorable Kill:</b> Draw a weapon.
    honorable_kill = FORCE_DRAW(WEAPON)


##
# Spells


class AV_108:
    """Shield Shatter"""

    # [x]Deal $5 damage to all minions. Costs (1) less for each Armor you have.
    cost_mod = -ARMOR(FRIENDLY_HERO)
    play = Hit(ALL_MINIONS, 5)


class AV_109:
    """Frozen Buckler"""

    # Gain 10 Armor. At the start of your next turn, lose 5 Armor.
    play = GainArmor(FRIENDLY_HERO, 10), Buff(CONTROLLER, "AV_109e")


class AV_109e:
    events = OWN_TURN_BEGIN.on(GainArmor(FRIENDLY_HERO, -5), Destroy(SELF))


class AV_322:
    """Snowed In"""

    # Destroy a damaged minion. <b>Freeze</b> all other minions.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET), Freeze(ALL_MINIONS - TARGET)


class AV_119:
    """To the Front!"""

    # Your minions cost (2) less this turn <i>(but not less than 1)</i>.
    update = Refresh(
        FRIENDLY_HAND + MINION, {GameTag.COST: lambda self, i: max(i - 1, 1)}
    )


class ONY_023:
    """Hit It Very Hard"""

    # Gain +10 Attack and "Can't attack heroes" this turn.
    play = Buff(FRIENDLY_HERO, "ONY_023e")


ONY_023e = buff(+10, cannot_attack_heroes=True)


class ONY_025:
    """Shoulder Check"""

    # <b>Tradeable</b> Give a minion +2/+1 and <b>Rush</b>.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "ONY_025e")


ONY_025e = buff(+2, +1, rush=True)


class AV_660:
    """Iceblood Garrison"""

    # [x]At the end of your turn, deal $1 damage to all_ minions. Lasts 3
    # turns.
    events = OWN_TURN_END.on(Hit(ALL_MINIONS, 1))


##
# Heros


class AV_202:
    """Rokara, the Valorous"""

    # <b>Battlecry:</b> Equip a 5/2 Unstoppable Force.
    play = Summon(CONTROLLER, "AV_202t2")


class AV_202p:
    """Grand Slam"""

    # [x]<b>Hero Power</b> Deal $2 damage. <b>Honorable Kill:</b> Gain 4 Armor.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 2)
    honorable_kill = GainArmor(FRIENDLY_HERO, 4)


class AV_202t2:
    """The Unstoppable Force"""

    # After you attack a minion, smash it into the enemy hero!
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Attack(Attack.DEFENDER, ENEMY_HERO)
    )
