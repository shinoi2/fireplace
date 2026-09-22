from ..utils import *

##
# Minions


class AV_340:
    """Brasswing"""

    # [x]At the end of your turn, deal 2 damage to all enemies. <b>Honorable
    # Kill:</b> Restore 4 Health to your hero.
    events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 2))
    honorable_kill = Heal(FRIENDLY_HERO, 4)


class AV_339:
    """Templar Captain"""

    # [x]<b>Rush</b>. After this attacks a minion, summon a 5/5 Defender with
    # <b>Taunt</b>.
    events = events = Attack(SELF, ALL_MINIONS).after(Summon(CONTROLLER, "AV_342t"))


class AV_343:
    """Stonehearth Vindicator"""

    # [x]<b>Battlecry:</b> Draw a spell that costs (3) or less. It costs (0)
    # this turn.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST <= 3))).then(
        Buff(ForceDraw.TARGET, "AV_343e")
    )


class AV_343e:
    tags = {GameTag.COST: SET(0)}
    events = REMOVED_IN_PLAY


class ONY_020:
    """Stormwind Avenger"""

    # After you cast a spell on this minion, it gains +2 Attack.
    events = Play(CONTROLLER, SPELL, SELF).on(Buff(SELF, "ONY_020e"))


ONY_020e = buff(atk=2)


class ONY_022:
    """Battle Vicar"""

    # <b>Battlecry:</b> <b>Discover</b> a Holy spell.
    play = DISCOVER(RandomSpell(spell_school=SpellSchool.HOLY))


class AV_345:
    """Saidan the Scarlet"""

    # <b>Rush.</b> Whenever this minion gains Attack or Health, double that
    # amount <i>(wherever this is)</i>.
    def atk(self, value):
        origin_atk = self.data.tags[GameTag.ATK]
        buff_atk = max(0, value - origin_atk)
        return value + buff_atk

    def max_health(self, value):
        origin_max_health = self.data.tags[GameTag.HEALTH]
        buff_max_health = max(0, value - origin_max_health)
        return value + buff_max_health


##
# Spells


class AV_213:
    """Vitality Surge"""

    # Draw a minion. Restore Health to your hero equal to its Cost.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
        Heal(FRIENDLY_HERO, COST(ForceDraw.TARGET))
    )


class AV_338:
    """Hold the Bridge"""

    # [x]Give a minion +2/+1 and <b>Divine Shield</b>. It gains
    # <b>Lifesteal</b> until end of turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "AV_338e"), GiveDivineShield(TARGET), Buff(TARGET, "AV_338e2")


AV_338e = buff(+2, +1)
AV_338e2 = buff(lifesteal=True)


class AV_342:
    """Protect the Innocent"""

    # Summon a 5/5 Defender with <b>Taunt</b>. If your hero was healed this
    # turn, summon another.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    powered_up = HEALED_THIS_TURN(FRIENDLY_HERO) > 0
    play = (Summon(CONTROLLER, "AV_342t"), powered_up & Summon(CONTROLLER, "AV_342t"))


class ONY_027:
    """Ring of Courage"""

    # <b>Tradeable</b> Give a minion +1/+1. Repeat for each enemy minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ONY_027e") * (Count(ENEMY_MINIONS) + 1)


class AV_344:
    """Dun Baldar Bridge"""

    # [x]After you summon a minion, give it +2/+2. Lasts 3 turns.
    events = Summon(CONTROLLER, MINION).after(Buff(Summon.TARGET, "AV_344e"))


AV_344e = buff(+2, +2)


##
# Weapons


class AV_341:
    """Cavalry Horn"""

    # <b>Deathrattle:</b> Summon the lowest Cost minion in your hand.
    deathrattle = Summon(CONTROLLER, RANDOM(LOWEST_COST(FRIENDLY_HAND + MINION)))


##
# Heros


class AV_206:
    """Lightforged Cariel"""

    # [x]<b>Battlecry:</b> Deal 2 damage to all enemies. Equip a 2/5 Immovable
    # Object.
    play = Hit(ENEMY_MINIONS, 2), Summon(CONTROLLER, "AV_146")


class AV_206p:
    """Blessing of Queens"""

    # <b>Hero Power</b> Give a random minion in your hand +4/+4.
    activate = Buff(RANDOM(FRIENDLY_HAND + MINION), "AV_206pe")


AV_206pe = buff(+4, +4)


class AV_146:
    update = Refresh(SELF, {GameTag.IMMUNE: True})
    events = Predamage(FRIENDLY_HERO).on(
        Predamage(FRIENDLY_HERO, (Predamage.AMOUNT + 1) // 2)
    )
