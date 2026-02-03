from ..utils import *

##
# Minions


class SCH_241:
    """Firebrand"""

    # <b><b>Spellburst</b>:</b> Deal 4 damage randomly split among all_enemy
    # minions.
    spellburst = Hit(RANDOM_ENEMY_MINION, 1) * 4


class SCH_243:
    """Wyrm Weaver"""

    # <b>Spellburst:</b> Summon two 1/3 Mana Wyrms.
    spellburst = SummonBothSides(CONTROLLER, "NEW1_012") * 2


class SCH_350:
    """Wand Thief"""

    # <b>Combo:</b> <b>Discover</b> a Mage_spell.
    combo = DISCOVER(RandomSpell(card_class=CardClass.MAGE))


class SCH_351:
    """Jandice Barov"""

    # [x]<b>Battlecry:</b> Summon two random 5-Cost minions. Secretly pick one
    # that dies _when it takes damage.

    # TODO need to be tested
    play = (
        SetTags(
            SELF,
            {
                GameTag.TAG_SCRIPT_DATA_ENT_1: RandomMinion(cost=5),
                GameTag.TAG_SCRIPT_DATA_ENT_2: RandomMinion(cost=5),
            },
        ),
        Summon(CONTROLLER, GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1)),
        Summon(CONTROLLER, GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_2)),
        Choice(
            CONTROLLER,
            (
                GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1),
                GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_2),
            ),
        ).then(Buff(Choice.CARD, "SCH_351e")),
        UnsetTags(SELF, (GameTag.TAG_SCRIPT_DATA_ENT_1, GameTag.TAG_SCRIPT_DATA_ENT_2)),
    )


class SCH_351e:
    events = Damage(OWNER).on(Destroy(OWNER))


class SCH_352:
    """Potion of Illusion"""

    # Add 1/1 copies of your minions to your hand. They cost (1).
    play = Give(
        CONTROLLER, MultiBuff(Copy(FRIENDLY_MINIONS), ["SCH_352e", "SCH_352e2"])
    )


class SCH_352e:
    atk = SET(1)
    max_health = SET(1)


class SCH_352e2:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class SCH_400:
    """Mozaki, Master Duelist"""

    # After you cast a spell, gain <b>Spell Damage +1</b>.
    events = Play(CONTROLLER, SPELL).after(Buff(SELF, "SCH_400e2"))


class SCH_400e2:
    tags = {GameTag.SPELLPOWER: 1}


##
# Spells


class SCH_348:
    """Combustion"""

    # [x]Deal $4 damage to a minion. Any excess damages both neighbors.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET_ADJACENT, HitExcessDamage(TARGET, SPELL_DAMAGE(4)))


class SCH_353:
    """Cram Session"""

    # Draw $1 |4(card, cards) <i>(improved by <b>Spell Damage</b>)</i>.
    play = Draw(CONTROLLER) * SPELL_DAMAGE(1)


class SCH_509:
    """Brain Freeze"""

    # <b>Freeze</b> a minion. <b>Combo:</b> Also deal $3 damage to it.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Freeze(TARGET)
    combo = Freeze(TARGET), Hit(TARGET, 3)
