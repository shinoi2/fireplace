from ..utils import *

##
# Minions


class SCH_182:
    """Speaker Gidra"""

    # [x]<b><b>Rush</b>, Windfury</b> <b><b>Spellburst</b>:</b> Gain Attack and
    # Health equal to the spell's Cost.
    def spellburst(self, spell):
        yield Buff(SELF, "SCH_182e", atk=spell.cost, max_health=spell.cost)


class SCH_242:
    """Gibberling"""

    # <b>Spellburst:</b> Summon a Gibberling.
    spellburst = Summon(CONTROLLER, "SCH_242")


class SCH_613:
    """Groundskeeper"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If you're holding a spell that costs
    # (5) or more, restore 5 Health.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_COST_5_OR_MORE_SPELL_IN_HAND: 0,
    }
    powered_up = Find(FRIENDLY_HAND + SPELL + (COST >= 5))
    play = powered_up & Heal(TARGET, 5)


class SCH_614:
    """Forest Warden Omu"""

    # <b>Spellburst:</b> Refresh your Mana Crystals.
    spellburst = FillMana(CONTROLLER, USED_MANA(CONTROLLER))


class SCH_616:
    """Twilight Runner"""

    # <b>Stealth</b> Whenever this attacks, draw 2 cards.
    events = Attack(SELF).on(Draw(CONTROLLER) * 2)


##
# Spells


class SCH_333:
    """Nature Studies"""

    # <b>Discover</b> a spell. Your next one costs (1) less.
    play = DISCOVER(RandomSpell()), Buff(CONTROLLER, "SCH_333e")


class SCH_333e:
    update = Refresh(FRIENDLY_HAND + SPELL, buff="SCH_333e2")
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class SCH_333e2:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class SCH_427:
    """Lightning Bloom"""

    # Gain 2 Mana Crystals this turn only. <b>Overload:</b> (2)
    play = ManaThisTurn(CONTROLLER, 2)


class SCH_606:
    """Partner Assignment"""

    # Add a random 2-Cost and 3-Cost Beast to_your hand.
    play = (
        Give(CONTROLLER, RandomBeast(cost=2)),
        Give(CONTROLLER, RandomBeast(cost=3)),
    )


class SCH_609:
    """Survival of the Fittest"""

    # Give +4/+4 to all minions in your hand, deck, and battlefield.
    play = Buff(FRIENDLY + (IN_HAND | IN_DECK | IN_PLAY) + MINION, "SCH_609e")


SCH_609e = buff(+4, +4)


class SCH_612:
    """Runic Carvings"""

    # <b>Choose One -</b> Summon four 2/2 Treant Totems; or <b>Overload:</b>
    # (2) to summon them with <b>Rush</b>.
    choose = ("SCH_612a", "SCH_612b")


class SCH_612a:
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "SCH_612t") * 4


class SCH_612b:
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "SCH_612t").then(GiveRush(Summon.CARD)) * 4
