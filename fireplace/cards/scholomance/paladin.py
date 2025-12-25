from ..utils import *


##
# Minions


class SCH_135:
    """Turalyon, the Tenured"""

    # [x]<b>Rush</b>. Whenever this attacks a minion, set the defender's Attack
    # and Health to 3.
    events = Attack(SELF, MINION).on(Buff(Attack.DEFENDER, "SCH_135e"))


class SCH_135e:
    atk = SET(3)
    max_health = SET(3)


class SCH_139:
    """Devout Pupil"""

    # [x]<b>Divine Shield, Taunt</b> Costs (1) less for each spell you've cast
    # on friendly characters this game.
    cost_mod = -Count(CAST_ON_FRIENDLY_CHARACTERS)


class SCH_141:
    """High Abbess Alura"""

    # <b>Spellburst:</b> Cast a spell from your deck <i>(targets this if
    # possible)</i>.
    spellburst = CastSpellTargetsSelfIfPossible(RANDOM(FRIENDLY_DECK + SPELL))


class SCH_149:
    """Argent Braggart"""

    # <b>Battlecry:</b> Gain Attack and Health to match the highest in the
    # battlefield.
    play = Buff(SELF, "SCH_149e")


def SCH_149e():
    def apply(self, target):
        self._xatk = HIGHEST_ATK(ALL_MINIONS).eval(self.game)
        self._xhealth = HIGHEST_HEALTH(ALL_MINIONS).eval(self.game)
        target.damage = 0

    cls = buff()
    cls.atk = lambda self, i: self._xatk
    cls.max_health = lambda self, i: self._xhealth
    cls.apply = apply

    return cls


class SCH_526:
    """Lord Barov"""

    # [x]<b>Battlecry:</b> Set the Health of all other minions to 1.
    # <b>Deathrattle:</b> Deal 1 damage to all minions.
    play = Buff(ALL_MINIONS - SELF, "SCH_526e")
    deathrattle = Hit(ALL_MINIONS, 1)


class SCH_526e:
    max_health = SET(1)


class SCH_532:
    """Goody Two-Shields"""

    # <b>Divine Shield</b> <b>Spellburst:</b> Gain <b>Divine Shield</b>.
    spellburst = GiveDivineShield(SELF)


##
# Spells


class SCH_138:
    """Blessing of Authority"""

    # Give a minion +8/+8. It_can't attack heroes this turn.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "SCH_138e")


class SCH_138e:
    tags = {
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
        GameTag.CANNOT_ATTACK_HEROES: True,
    }


class SCH_247:
    """First Day of School"""

    # Add 2 random 1-Cost minions to your hand.
    play = Give(CONTROLLER, RandomMinion(cost=1)) * 2


class SCH_250:
    """Wave of Apathy"""

    # Set the Attack of all enemy minions to 1 until your next turn.
    play = Buff(ENEMY_MINIONS, "SCH_250e")


class SCH_250e:
    atk = SET(1)
    events = OWN_TURN_BEGIN.on(Destroy(SELF))


class SCH_302:
    """Gift of Luminance"""

    # Give a minion <b>Divine Shield</b>, then summon a_1/1 copy of it.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = GiveDivineShield(TARGET), Summon(CONTROLLER, ExactCopy(TARGET)).then(
        Buff(Summon.CARD, "SCH_302e")
    )


class SCH_302e:
    atk = SET(1)
    max_health = SET(1)


class SCH_524:
    """Shield of Honor"""

    # Give a damaged minion +3 Attack and <b>Divine Shield</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }
    play = Buff(TARGET, "SCH_524e"), GiveDivineShield(TARGET)


SCH_524e = buff(atk=3)


class SCH_533:
    """Commencement"""

    # Summon a minion from your deck. Give it <b>Taunt</b> and <b>Divine
    # Shield</b>.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(
        Taunt(Summon.CARD), GiveDivineShield(Summon.CARD)
    )


##
# Weapons


class SCH_523:
    """Ceremonial Maul"""

    # <b>Spellburst</b>: Summon a Student with <b>Taunt</b> and stats equal to
    # the spell's Cost.
    spellburst = SummonCustomMinion(
        CONTROLLER, "SCH_523t", Min(COST(SELF), 10), COST(SELF), COST(SELF)
    )
