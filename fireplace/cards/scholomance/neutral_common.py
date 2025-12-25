from ..utils import *


##
# Minions


class SCH_160:
    """Wandmaker"""

    # <b>Battlecry:</b> Add a 1-Cost spell from your class to_your hand.
    play = Give(CONTROLLER, RandomSpell(cost=1, card_class=FRIENDLY_CLASS))


class SCH_230:
    """Onyx Magescribe"""

    # <b>Spellburst:</b> Add 2 random spells from your class to_your hand.
    play = Give(CONTROLLER, RandomSpell(card_class=FRIENDLY_CLASS)) * 2


class SCH_231:
    """Intrepid Initiate"""

    # <b>Spellburst:</b> Gain +2_Attack.
    spellburst = Buff(SELF, "SCH_231e")


SCH_231e = buff(atk=+2)


class SCH_232:
    """Crimson Hothead"""

    # <b>Spellburst:</b> Gain +1 Attack and <b>Taunt</b>.
    spellburst = Buff(SELF, "SCH_232e")


class SCH_232e:
    tags = {GameTag.ATK: 1, GameTag.TAUNT: True}


class SCH_245:
    """Steward of Scrolls"""

    # <b>Spell Damage +1</b> <b>Battlecry:</b> <b>Discover</b> a spell.
    play = DISCOVER(RandomSpell())


class SCH_248:
    """Pen Flinger"""

    # <b>Battlecry:</b> Deal 1 damage. <b>Spellburst:</b> Return this to_your
    # hand.
    play = Hit(SELF, 1)
    spellburst = Bounce(SELF)


class SCH_283:
    """Manafeeder Panthara"""

    # <b>Battlecry:</b> If you've used your Hero Power this turn, draw a card.
    powered_up = Attr(FRIENDLY_HERO_POWER, enums.ACTIVATIONS_THIS_TURN) > 0
    play = powered_up & Draw(CONTROLLER)


class SCH_311:
    """Animated Broomstick"""

    # <b>Rush</b> <b>Battlecry:</b> Give your other minions <b>Rush</b>.
    play = GiveRush(FRIENDLY_MINIONS - SELF)


class SCH_312:
    """Tour Guide"""

    # <b>Battlecry:</b> Your next Hero Power costs (0).
    play = Buff(CONTROLLER, "SCH_312e")


class SCH_312e:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})
    events = Activate(CONTROLLER, HERO_POWER).after(Destroy(SELF))


class SCH_313:
    """Wretched Tutor"""

    # <b>Spellburst:</b> Deal 2 damage to all other minions.
    spellburst = Hit(ALL_MINIONS - SELF, 2)


class SCH_530:
    """Sorcerous Substitute"""

    # <b>Battlecry:</b> If you have <b>Spell Damage</b>, summon a copy of this.
    powered_up = powered_up = Find(FRIENDLY + SPELLPOWER)
    play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


class SCH_605:
    """Lake Thresher"""

    # Also damages the minions next to whomever this attacks.
    events = Attack(SELF).on(CLEAVE)


class SCH_707:
    """Fishy Flyer"""

    # <b>Rush</b>. <b>Deathrattle:</b> Add a_4/3 Ghost with <b>Rush</b> to_your
    # hand.
    deathrattle = Give(CONTROLLER, "SCH_707t")


class SCH_708:
    """Sneaky Delinquent"""

    # <b>Stealth</b>. <b>Deathrattle:</b> Add a 3/1 Ghost with <b>Stealth</b>
    # to your hand.
    deathrattle = Give(CONTROLLER, "SCH_708t")


class SCH_709:
    """Smug Senior"""

    # <b>Taunt</b>. <b>Deathrattle:</b> Add a_5/7 Ghost with <b>Taunt</b>
    # to_your hand.
    deathrattle = Give(CONTROLLER, "SCH_709t")


class SCH_710:
    """Ogremancer"""

    # [x]Whenever your opponent casts a spell, summon a 2/2 Skeleton with
    # <b>Taunt</b>.
    events = Play(OPPONENT, SPELL).on(Summon(CONTROLLER, "SCH_710t"))


class SCH_711:
    """Plagued Protodrake"""

    # <b>Deathrattle:</b> Summon a random 7-Cost minion.
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=7))
