from ..utils import *

##
# Minions


class TSC_029:
    """Gaia, the Techtonic"""

    # [x]<b>Colossal +2</b> After a friendly Mech attacks, deal 1 damage to all
    # enemies.
    colossal = SummonBothSides(CONTROLLER, ["TSC_029t", "TSC_029t2"])
    events = Attack(FRIENDLY_MINIONS + MECH).after(Hit(ENEMY_CHARACTERS, 1))


class TSC_620:
    """Spitelash Siren"""

    # [x]After you play a Naga, refresh two Mana Crystals. <i>(Then switch to
    # spell!)</i>@[x]After you cast a spell, refresh two Mana Crystals.
    # <i>(Then switch to Naga!)</i>
    events = (
        Play(CONTROLLER, NAGA).after(
            (DATA_NUM_1(SELF) == 2)
            & (
                FillMana(CONTROLLER, 2),
                SetTags(SELF, {GameTag.TAG_SCRIPT_DATA_NUM_1: 1}),
            )
        ),
        Play(CONTROLLER, SPELL).after(
            (DATA_NUM_1(SELF) == 1)
            & (
                FillMana(CONTROLLER, 2),
                SetTags(SELF, {GameTag.TAG_SCRIPT_DATA_NUM_1: 2}),
            )
        ),
    )


class TID_709:
    """Lady Naz'jar"""

    # [x]While in your hand, this ___transforms after you cast a___ Fire,
    # Frost, or Arcane spell.
    class Hand:
        events = (
            Play(CONTROLLER, FIRE).after(Morph(SELF, "TID_709t2")),
            Play(CONTROLLER, FROST).after(Morph(SELF, "TID_709t3")),
            Play(CONTROLLER, ARCANE).after(Morph(SELF, "TID_709t")),
        )


class TID_709t:
    """Lady Naz'jar"""

    # [x]<b>Battlecry:</b> Reduce the Cost of spells in your hand by (1).
    play = Buff(FRIENDLY_HAND + SPELL, "TID_709e")


TID_709e = cost_buff(-1)


class TID_709t2:
    """Lady Naz'jar"""

    # [x]<b>Battlecry:</b> Deal 5 damage to an enemy minion and 2 to adjacent
    # minions.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Hit(TARGET, 5), Hit(TARGET_ADJACENT, 2)


class TID_709t3:
    """Lady Naz'jar"""

    # <b>Battlecry:</b> Gain 8 Armor.
    play = GainArmor(FRIENDLY_HERO, 8)


class TSC_054:
    """Mecha-Shark"""

    # [x]After you summon a Mech, deal 3 damage randomly _split among all
    # enemies.
    events = Summon(CONTROLLER, MECH).after(Hit(RANDOM_ENEMY_CHARACTER, 1) * 3)


class TSC_643:
    """Spellcoiler"""

    # [x]<b>Battlecry:</b> If you've cast a spell while holding this,
    # <b>Discover</b> a spell.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + SPELL)
    play = powered_up & DISCOVER(RandomSpell())


class TSC_642:
    """Trench Surveyor"""

    # <b>Battlecry:</b> <b>Dredge</b>. If it's a Mech, draw it.
    play = Dredge(CONTROLLER).then(Find(Dredge.CARD + MECH) & ForceDraw(Dredge.CARD))


class TID_707:
    """Submerged Spacerock"""

    # [x]<b>Deathrattle:</b> Add two Arcane Mage spells to your hand. At the
    # end of your turn, discard them.
    deathrattle = Give(
        CONTROLLER,
        RandomSpell(spell_school=SpellSchool.ARCANE, card_class=CardClass.MAGE) * 2,
    ).then(Buff(Give.CARD, "TID_707e"))


class TID_707e:
    events = OWN_TURN_END.on(Discard(OWNER))


class TSC_776:
    """Azsharan Sweeper"""

    # <b>Battlecry:</b> Put a 'Sunken Sweeper' on the bottom of your deck.
    play = PutOnBottom(CONTROLLER, "TSC_776t")


class TSC_776t:
    """Sunken Sweeper"""

    # <b>Battlecry:</b> Add 3 random Mechs to your hand.
    play = Give(CONTROLLER, RandomMech() * 3)


class TSC_087(HoldingSpellThresholdUtils):
    """Commander Sivara"""

    # [x]<b>Battlecry:</b> If you've cast three spells while holding this, add
    # those spells back to your hand.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = Give(CONTROLLER, Copy((CARDS_PLAYED_WHEN_HOLDING + SPELL)[:3]))


##
# Spells


class TSC_055:
    """Seafloor Gateway"""

    # Draw a Mech. Reduce the Cost of Mechs in your hand by (1).
    play = FORCE_DRAW(MECH), Buff(FRIENDLY_HAND + MECH, "TSC_055e")


TSC_055e = cost_buff(-1)


class TSC_056:
    """Volcanomancy"""

    # Choose a minion. When it dies, deal 3 damage to all other minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "TSC_056e")


class TSC_056e:
    events = Death(OWNER).on(Hit(ALL_MINIONS - OWNER, 3))


class TSC_948:
    """Gifts of Azshara"""

    # Draw a card. If you played a Naga while holding this, do it again.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + NAGA)
    play = Draw(CONTROLLER), powered_up & Draw(CONTROLLER)


class TID_708:
    """Polymorph: Jellyfish"""

    # Transform a minion into a 4/1 Jellyfish with <b>Spell Damage +2</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Morph(TARGET, "TID_708t")
