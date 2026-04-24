from ..utils import *

##
# Minions


class BAR_334:
    """Overlord Saurfang"""

    # <b>Battlecry:</b> Resurrect 2 friendly <b>Frenzy</b> minions. Deal 1
    # damage to all other minions.
    play = (
        Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION + FRENZY) * 2)),
        Hit(ALL_MINIONS - SELF, 1),
    )


class BAR_840:
    """Whirling Combatant"""

    # [x]<b>Battlecry and Frenzy:</b> Deal 1 damage to all other minions.
    play = frenzy = Hit(ALL_MINIONS - SELF, 1)


class BAR_843:
    """Warsong Envoy"""

    # [x]<b>Frenzy:</b> Gain +1  Attack for each damaged character.
    frenzy = Buff(SELF, "BAR_843e", atk=Count(ALL_CHARACTERS + DAMAGED))


@custom_card
class BAR_843e:
    tags = {
        GameTag.CARDNAME: "Warsong Envoy Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


class BAR_846:
    """Mor'shan Elite"""

    # [x]<b>Taunt</b>. <b>Battlecry:</b> If your hero attacked this turn,
    # summon a copy of this.
    powered_up = NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) > 0
    play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


class BAR_847:
    """Rokara"""

    # [x]<b>Rush</b> After a friendly minion attacks and survives, give it
    # +1/+1.
    events = Attack(FRIENDLY_MINIONS).after(
        Dead(Attack.ATTACKER) | Buff(Attack.ATTACKER, "BAR_847e")
    )


BAR_847e = buff(+1, +1)


class BAR_896:
    """Stonemaul Anchorman"""

    # [x]<b>Rush</b> <b>Frenzy:</b> Draw a card.
    frenzy = Draw(CONTROLLER)


class WC_024:
    """Man-at-Arms"""

    # <b>Battlecry:</b> If you have a weapon equipped, gain +1/+1.
    play = Find(FRIENDLY_WEAPON) & Buff(SELF, "WC_024e")


WC_024e = buff(+1, +1)


class WC_026:
    """Kresh, Lord of Turtling"""

    # <b>Frenzy:</b> Gain 8 Armor. <b>Deathrattle:</b> Equip a 2/5 Turtle
    # Spike.
    frenzy = GainArmor(FRIENDLY_HERO, 8)
    deathrattle = Summon(CONTROLLER, "WC_026t")


##
# Spells


class BAR_841:
    """Bulk Up"""

    # Give a random <b>Taunt</b> minion in your hand +1/+1 and copy it.
    play = Buff(RANDOM(FRIENDLY_HAND + MINION + TAUNT), "BAR_841e").then(
        Give(CONTROLLER, ExactCopy(Buff.TARGET))
    )


BAR_841e = buff(+1, +1)


class BAR_842:
    """Conditioning (Rank 1)"""

    # Give minions in your hand +1/+1. <i>(Upgrades when you have 5 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_842t")

    play = Buff(FRIENDLY_HAND + MINION, "BAR_842e")


BAR_842e = buff(+1, +1)


BAR_842e2 = buff(+2, +2)


BAR_842e3 = buff(+3, +3)


class BAR_842t:
    """Conditioning (Rank 2)"""

    # [x]Give minions in your hand +2/+2. <i>(Upgrades when you have 10
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_842t2")

    play = Buff(FRIENDLY_HAND + MINION, "BAR_842e2")


class BAR_842t2:
    """Conditioning (Rank 3)"""

    # Give minions in your hand +3/+3.
    play = Buff(FRIENDLY_HAND + MINION, "BAR_842e3")


class BAR_845:
    """Rancor"""

    # [x]Deal $2 damage to all minions. Gain 2 Armor for each destroyed.
    play = Hit(ALL_MINIONS, 2).then(
        GainArmor(FRIENDLY_HERO, Count(ALL_MINIONS + DEAD) * 2)
    )


##
# Weapons


class BAR_844:
    """Outrider's Axe"""

    # After your hero attacks and kills a minion, draw a card.
    events = Attack(FRIENDLY_HERO, MINION).after(
        Dead(Attack.DEFENDER) & Draw(CONTROLLER)
    )


class WC_025:
    """Whetstone Hatchet"""

    # After your hero attacks, give a minion in your hand +1 Attack.
    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_HAND + MINION), "WC_025e")
    )


WC_025e = buff(atk=1)
