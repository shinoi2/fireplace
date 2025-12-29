from ..utils import *


##
# Minions


class SCH_236:
    """Diligent Notetaker"""

    # <b>Spellburst:</b> Return the spell to your hand.
    spellburst = Give(CONTROLLER, SELF)


class SCH_507:
    """Instructor Fireheart"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a spell that costs (1) or more. If
    # you play it this turn, repeat this effect.
    play = DISCOVER(RandomSpell(cost=range(1, 100))).then(
        Buff(Discover.CARD, "SCH_507e")
    )


class SCH_507e:
    events = Play(CONTROLLER, OWNER).after(
        DISCOVER(RandomSpell(cost=range(1, 100))).then(Buff(Discover.CARD, "SCH_507e"))
    )


class SCH_537:
    """Trick Totem"""

    # At the end of your turn, cast a random spell that costs (3) or less.
    events = OWN_TURN_END.on(CastSpell(RandomSpell(cost=range(0, 4))))


class SCH_615:
    """Totem Goliath"""

    # <b>Deathrattle:</b> Summon all four basic Totems. <b>Overload: (1)</b>
    deathrattle = Summon(CONTROLLER, BASIC_TOTEMS)


##
# Spells


class SCH_235:
    """Devolving Missiles"""

    # [x]Shoot three missiles at random enemy minions that transform them into
    # ones that cost (1) less.
    play = Evolve(RANDOM_ENEMY_MINION, -1) * 3


class SCH_270:
    """Primordial Studies"""

    # <b>Discover</b> a <b>Spell Damage</b> minion. Your next one costs (1)
    # less.
    play = DISCOVER(RandomMinion(spell_damage=True)), Buff(CONTROLLER, "SCH_270e")


class SCH_270e:
    update = Refresh(FRIENDLY_HAND + SPELLPOWER + MINION, "SCH_270e2")
    events = Play(CONTROLLER, SPELLPOWER + MINION).after(Destroy(SELF))


class SCH_270e2:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class SCH_271:
    """Molten Blast"""

    # Deal $2 damage. Summon that many 1/1 Elementals.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = (Hit(TARGET, 2), Summon(CONTROLLER, "CS2_050") * SPELL_DAMAGE(2))


class SCH_273:
    """Ras Frostwhisper"""

    # At the end of your turn, deal $1 damage to all enemies <i>(improved by
    # <b>Spell Damage</b>)</i>.
    events = OWN_TURN_END.on(Hit(ENEMY_MINIONS, SPELL_DAMAGE(1)))


class SCH_535:
    """Tidal Wave"""

    # <b>Lifesteal</b> Deal $3 damage to all minions.
    play = Hit(ALL_MINIONS, 3)


##
# Weapons


class SCH_301:
    """Rune Dagger"""

    # After your hero attacks, gain <b>Spell Damage +1</b> this turn.
    events = Attack(FRIENDLY_HERO).after(Buff(SELF, "SCH_301e"))


class SCH_301e:
    tags = {GameTag.SPELLPOWER: 1}
