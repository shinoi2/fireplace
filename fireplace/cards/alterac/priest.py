from ..utils import *

##
# Minions


class AV_325:
    """Undying Disciple"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Deal damage equal to this minion's
    # Attack to all enemy minions.
    deathrattle = Hit(ENEMY_MINIONS, ATK(SELF))


class AV_326:
    """Luminous Geode"""

    # After a friendly minion is healed, give it +2 Attack.
    events = Heal(FRIENDLY_MINIONS).after(Buff(Heal.TARGET, "AV_326e"))


AV_326e = buff(atk=2)


class AV_328:
    """Spirit Guide"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Draw a Holy spell and a Shadow spell.
    deathrattle = (
        ForceDraw(RANDOM(FRIENDLY_DECK + HOLY)),
        ForceDraw(RANDOM(FRIENDLY_DECK + SHADOW)),
    )


class AV_331:
    """Najak Hexxen"""

    # [x]<b>Battlecry:</b> Take control of an enemy minion. <b>Deathrattle:</b>
    # Give the minion back.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Steal(TARGET)
    deathrattle = HAS_TARGET & Steal(TARGET, OPPONENT)


class ONY_026:
    """Lightmaw Netherdrake"""

    # <b>Battlecry:</b> If you're holding a Holy and a Shadow spell, deal 3
    # damage to all other minions.
    powered_up = Find(FRIENDLY_HAND + HOLY) & Find(FRIENDLY_HAND + SHADOW)
    play = powered_up & Hit(ALL_MINIONS - SELF, 3)


class ONY_028:
    """Mi'da, Pure Light"""

    # [x]<b>Divine Shield</b>, <b>Lifesteal</b> <b>Deathrattle:</b> Shuffle a
    # Fragment into your deck that resummons Mi'da when drawn.
    deathrattle = Shuffle("ONY_028t")


class ONY_028t:
    play = Summon(CONTROLLER, "ONY_028")


##
# Spells


class AV_315:
    """Deliverance"""

    # Deal $3 damage to a minion. <b>Honorable Kill:</b> Summon a new 3/3 copy
    # of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)
    honorable_kill = Summon(CONTROLLER, Copy(TARGET)).then(
        Buff(Summon.TARGET, "AV_315e2")
    )


class AV_315e2:
    atk = SET(3)
    max_health = SET(3)


class AV_324:
    """Shadow Word: Devour"""

    # Choose a minion. It steals 1 Health from _ALL other minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(SELF, "AV_324e2") * Count(ALL_MINIONS - SELF),
        Buff(ALL_MINIONS - SELF, "AV_324eb"),
    )


AV_324e2 = buff(health=1)
AV_324eb = buff(health=-1)


class AV_329:
    """Bless"""

    # [x]Give a minion +2 Health, then set its Attack to be equal to its
    # Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "AV_329e").then(Buff(TARGET, "AV_329e2"))


AV_329e = buff(health=2)


class AV_329e2:
    atk = lambda self, i: self._xatk

    def apply(self, target):
        self._xatk = target.health


class AV_330:
    """Gift of the Naaru"""

    # [x]Restore #3 Health to all characters. If any are still damaged, draw a
    # card.
    play = (Heal(ALL_CHARACTERS, 3), Find(DAMAGED_CHARACTERS) & Draw(CONTROLLER))


class ONY_017:
    """Horn of Wrathion"""

    # Draw a minion. If it's a Dragon, summon two 2/1 Whelps with <b>Rush</b>.
    play = FORCE_DRAW(MINION).then(
        Find(ForceDraw.TARGET + DRAGON) & (Summon(CONTROLLER, "ONY_001t") * 2)
    )


class AV_664:
    """Stormpike Aid Station"""

    # [x]At the end of your turn, give your minions +2 Health. Lasts 3 turns.
    events = OWN_TURN_END.on(Buff(FRIENDLY_MINIONS, "AV_664e2"))


AV_664e2 = buff(health=2)


##
# Heros


class AV_207:
    """Xyrella, the Devout"""

    # [x]<b>Battlecry:</b> Trigger the <b>Deathrattle</b> of every friendly
    # minion that died this game.
    play = Deathrattle(SHUFFLE(FRIENDLY + KILLED + MINION + DEATHRATTLE))


class AV_207p:
    """Holy Touch"""

    # [x]<b>Hero Power</b> Restore #5 Health. Flip each turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    activate = Heal(TARGET, 5)
    events = OWN_TURN_END.on(Summon(CONTROLLER, "AV_207p2"))


class AV_207p2:
    """Void Spike"""

    # <b>Hero Power</b> Deal $5 damage. Flip each turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    activate = Hit(TARGET, 5)
    events = OWN_TURN_END.on(Summon(CONTROLLER, "AV_207p"))
