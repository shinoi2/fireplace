from ..utils import *

##
# Minions


class TSC_922:
    """Anchored Totem"""

    # After you summon a 1-Cost minion, give it +2/+1.
    events = Summon(CONTROLLER, COST == 1).after(Buff(Summon.CARD, "TSC_922e"))


TSC_922e = buff(2, 1)


class TSC_630:
    """Wrathspine Enchanter"""

    # <b>Battlecry:</b> Cast a copy of a Fire, Frost, and Nature spell in your
    # hand <i>(targets chosen randomly).</i>
    play = (
        CastSpell(Copy(RANDOM(FRIENDLY_HAND + FIRE))),
        CastSpell(Copy(RANDOM(FRIENDLY_HAND + FROST))),
        CastSpell(Copy(RANDOM(FRIENDLY_HAND + NATURE))),
    )


class TSC_633:
    """Piranha Poacher"""

    # At the end of your turn, add a 1/1 Piranha Swarmer to your hand.
    events = OWN_TURN_END.on(Give(CONTROLLER, "TSC_638"))


class TSC_635:
    """Radiance of Azshara"""

    # [x]<b>Fire Spell Damage +2</b> Your Nature spells cost (1) less. After
    # you cast a Frost spell, gain 3 Armor.
    update = Refresh(FRIENDLY_HAND + NATURE, {GameTag.COST: -1})
    events = Play(CONTROLLER, FROST).after(GainArmor(FRIENDLY_HERO, 3))


class TSC_639:
    """Glugg the Gulper"""

    # [x]<b>Colossal +3</b> After a friendly minion dies, gain its original
    # stats.
    colossal = Summon(CONTROLLER, ["TSC_639t", "TSC_639t2", "TSC_639t3"])
    events = Death(FRIENDLY_MINIONS - SELF).after(
        Buff(
            SELF,
            "TSC_639e",
            atk=ORIGIN_ATK(Death.ENTITY),
            max_health=ORIGIN_MAX_HEALTH(Death.ENTITY),
        )
    )


class TSC_648:
    """Coral Keeper"""

    # [x]<b>Battlecry:</b> Summon a 3/3 Elemental for each spell school you've
    # cast this game.
    play = (
        Find(CARDS_PLAYED_THIS_GAME + EnumSelector(school))
        & Summon(CONTROLLER, "TSC_648t")
        for school in SPELL_SCHOOLS
    )


class TID_003:
    """Tidelost Burrower"""

    # <b>Battlecry:</b> <b>Dredge</b>. If it's a Murloc, summon a 2/2 copy of
    # it.
    play = Dredge(CONTROLLER).then(
        Find(Dredge.CARD + MURLOC)
        & Summon(CONTROLLER, Buff(ExactCopy(Dredge.CARD), "TID_003e2"))
    )


class TID_003e2:
    atk = SET(2)
    max_health = SET(2)


class TID_004:
    """Clownfish"""

    # <b>Battlecry:</b> Your next two Murlocs cost (2) less.
    play = Buff(CONTROLLER, "TID_004e")


class TID_004e:
    update = Refresh(FRIENDLY_HAND + MURLOC, {GameTag.COST: -2})
    events = Play(CONTROLLER, MURLOC).after(
        Buff(CONTROLLER, "TID_004e2"), Destroy(SELF)
    )


class TID_004e2:
    update = Refresh(FRIENDLY_HAND + MURLOC, {GameTag.COST: -2})
    events = Play(CONTROLLER, MURLOC).after(Destroy(SELF))


##
# Spells


class TSC_923:
    """Bioluminescence"""

    # Give your minions <b>Spell Damage +1</b>.
    update = Refresh(FRIENDLY_MINIONS, {GameTag.SPELLPOWER: +1})


class TSC_631:
    """Schooling"""

    # Add three 1/1 Piranha Swarmers to your hand.
    play = Give(CONTROLLER, "TSC_638") * 3


class TSC_637:
    """Scalding Geyser"""

    # [x]Deal $2 damage. <b>Dredge</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2), Dredge(CONTROLLER)


class TID_005:
    """Command of Neptulon"""

    # Summon two 5/4 Elementals with <b>Rush</b>. <b>Overload:</b> (1)
    play = Summon(CONTROLLER, "TID_005t") * 2


class TSC_772:
    """Azsharan Scroll"""

    # <b>Discover</b> a Fire, Frost or Nature spell. Put a 'Sunken Scroll' on
    # the bottom of your deck.
    play = GenericChoice(
        CONTROLLER,
        [
            RandomSpell(spell_school=SpellSchool.FIRE),
            RandomSpell(spell_school=SpellSchool.FROST),
            RandomSpell(spell_school=SpellSchool.NATURE),
        ],
    ), PutOnBottom(CONTROLLER, "TSC_772t")


class TSC_772t:
    """Sunken Scroll"""

    # Add a Fire, Frost, and Nature spell from your class to your hand.
    play = Give(
        CONTROLLER,
        [
            RandomSpell(spell_school=SpellSchool.FIRE),
            RandomSpell(spell_school=SpellSchool.FROST),
            RandomSpell(spell_school=SpellSchool.NATURE),
        ],
    )
