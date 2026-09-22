from ..utils import *

##
# Minions


class AV_101:
    """Herald of Lokholar"""

    # <b>Battlecry:</b> Draw a Frost spell.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + FROST))


class AV_215:
    """Frantic Hippogryph"""

    # <b>Rush</b>. <b>Honorable Kill</b>: _Gain <b>Windfury</b>._
    honorable_kill = GiveWindfury(SELF)


class AV_219:
    """Ram Commander"""

    # [x]<b>Battlecry:</b> Add two 1/1 Rams with <b>Rush</b> to your hand.
    play = Give(CONTROLLER, "AV_219t") * 2


class AV_238:
    """Gankster"""

    # [x]<b>Stealth</b> After your opponent plays a minion, attack it.
    events = Play(OPPONENT, MINION).after(
        Find(Play.CARD + IN_PLAY - DEAD)
        & (Find(SELF - FROZEN) & Attack(SELF, Play.CARD))
    )


class AV_309:
    """Piggyback Imp"""

    # <b>Deathrattle:</b> Summon a 4/1 Imp.
    deathrattle = Summon(CONTROLLER, "AV_309t")


class AV_704:
    """Humongous Owl"""

    # <b>Deathrattle:</b> Deal 8 damage to a random enemy.
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 8)


class AV_121:
    """Gnome Private"""

    # [x]<b>Honorable Kill:</b> Gain +2 Attack.
    honorable_kill = Buff(SELF, "AV_121e")


AV_121e = buff(atk=2)


class AV_122:
    """Corporal"""

    # <b>Honorable Kill:</b> Give your other minions <b>Divine Shield</b>.
    honorable_kill = GiveDivineShield(FRIENDLY_MINIONS - SELF)


class AV_123:
    """Sneaky Scout"""

    # [x]<b>Stealth</b> <b>Honorable Kill:</b> Your next Hero Power costs (0).
    honorable_kill = Buff(CONTROLLER, "AV_123e")


class AV_123e:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})
    events = Activate(FRIENDLY_HERO_POWER).after(Destroy(SELF))


class AV_124:
    """Direwolf Commander"""

    # <b>Honorable Kill:</b> Summon a 2/2 Wolf with <b>Stealth</b>.
    honorable_kill = Summon(CONTROLLER, "AV_211t")


class AV_125:
    """Tower Sergeant"""

    # <b>Battlecry:</b> If you control at_least 2 other minions, gain +2/+2.
    powered_up = Count(FRIENDLY_MINIONS - SELF) >= 2
    play = powered_up & Buff(SELF, "AV_125e")


AV_125e = buff(+2, +2)


class AV_126:
    """Bunker Sergeant"""

    # [x]<b>Battlecry:</b> If your opponent has 2 or more minions, deal 1
    # damage to all enemy minions.
    powered_up = Count(ENEMY_MINIONS) >= 2
    play = powered_up & Hit(ENEMY_MINIONS, 1)


class AV_127:
    """Ice Revenant"""

    # Whenever you cast a Frost spell, gain +2/+2.
    events = Play(CONTROLLER, FROST).after(Buff(SELF, "AV_127e"))


AV_127e = buff(+2, +2)


class AV_129:
    """Blood Guard"""

    # Whenever this minion takes damage, give your minions +1 Attack.
    events = Damage(SELF).on(Buff(FRIENDLY_MINIONS, "AV_129e"))


AV_129e = buff(atk=1)


class AV_130:
    """Legionnaire"""

    # <b>Deathrattle:</b> Give all minions in your hand +2/+2.
    deathrattle = Buff(FRIENDLY_HAND + MINION, "AV_130e")


AV_130e = buff(+2, +2)


class AV_131:
    """Knight-Captain"""

    # [x]<b>Battlecry:</b> Deal 3 damage. <b>Honorable Kill:</b> Gain +3/+3.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 3)
    honorable_kill = Buff(SELF, "AV_131e")


AV_131e = buff(+3, +3)


class AV_132:
    """Troll Centurion"""

    # [x]<b>Rush</b>. <b>Honorable Kill:</b> Deal 8 damage to the enemy hero.
    honorable_kill = Hit(ENEMY_HERO, 8)


class AV_133:
    """Icehoof Protector"""

    # <b>Taunt</b> <b>Freeze</b> any character damaged by this minion.
    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class AV_401:
    """Stormpike Quartermaster"""

    # After you cast a spell, give a random minion in your hand +1/+1.
    events = OWN_SPELL_PLAY.after(Buff(RANDOM(FRIENDLY_HAND + MINION), "AV_401e"))


AV_401e = buff(+1, +1)


class ONY_001:
    """Onyxian Warder"""

    # [x]<b>Battlecry:</b> If you're holding a Dragon, summon two 2/1 Whelps
    # with <b>Rush</b>.
    powered_up = HOLDING_DRAGON
    play = powered_up & SummonBothSides(CONTROLLER, "ONY_001t") * 2


class AV_256:
    """Reflecto Engineer"""

    # <b>Battlecry:</b> Swap the Attack and Health of all minions in both
    # players' hands.
    play = Buff(IN_HAND + MINION, "AV_256e")


AV_256e = AttackHealthSwapBuff()
