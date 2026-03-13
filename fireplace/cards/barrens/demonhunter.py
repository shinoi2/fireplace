from ..utils import *

##
# Minions


class BAR_325:
    """Razorboar"""

    # <b>Deathrattle:</b> Summon a <b>Deathrattle</b> minion that costs (3) or
    # less from your hand.
    deathrattle = Summon(
        CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + DEATHRATTLE + (COST <= 3))
    )


class BAR_326:
    """Razorfen Beastmaster"""

    # <b>Deathrattle:</b> Summon a <b>Deathrattle</b> minion that costs (4) or
    # less from your hand.
    deathrattle = Summon(
        CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + DEATHRATTLE + (COST <= 4))
    )


class BAR_328:
    """Vengeful Spirit"""

    # <b>Outcast:</b> Draw 2 <b>Deathrattle</b> minions.
    outcast = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE) * 2)


class BAR_329:
    """Death Speaker Blackthorn"""

    # <b>Battlecry:</b> Summon 3 <b>Deathrattle</b> minions that cost (5) or
    # less from your deck.
    play = Summon(
        CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE + (COST <= 5)) * 3
    )


class BAR_333:
    """Kurtrus Ashfallen"""

    # [x]<b>Battlecry:</b> Attack the left and right-most enemy minions.
    # <b>Outcast:</b> <b>Immune</b> this turn.
    play = (
        Attack(SELF, LEFTMOST(ENEMY_MINIONS)),
        Attack(SELF, RIGHTMOST(ENEMY_MINIONS)),
    )
    outcast = (
        Buff(SELF, "BAR_333e"),
        Attack(SELF, LEFTMOST(ENEMY_MINIONS)),
        Attack(SELF, RIGHTMOST(ENEMY_MINIONS)),
    )


BAR_333e = buff(immune=True)


class WC_040:
    """Taintheart Tormenter"""

    # <b>Taunt</b> Your opponent's spells cost (2) more.
    update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: 2})


class WC_701:
    """Felrattler"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Deal 1 damage to all enemy minions.
    deathrattle = Hit(ENEMY_MINIONS, 1)


##
# Spells


class BAR_306:
    """Sigil of Flame"""

    # At the start of your next turn, deal $3 damage to all minions.
    events = OWN_TURN_BEGIN.on(Hit(ALL_MINIONS, 3), Destroy(SELF))


class BAR_327:
    """Vile Call"""

    # Summon two 2/2 Demons with <b>Lifesteal</b>.
    play = Summon(CONTROLLER, "BAR_327t") * 2


class BAR_705:
    """Sigil of Silence"""

    # At the start of your next turn, <b>Silence</b> all enemy minions.
    events = OWN_TURN_BEGIN.on(Silence(ENEMY_MINIONS), Destroy(SELF))


class BAR_891:
    """Fury (Rank 1)"""

    # Give your hero +2 Attack this turn. <i>(Upgrades when you have 5
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_891t")

    play = Buff(FRIENDLY_HERO, "BAR_891e")


BAR_891e = buff(atk=2)


class BAR_891t:
    """Fury (Rank 2)"""

    # [x]Give your hero +3 Attack this turn. <i>(Upgrades when you have 10
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_891t2")

    play = Buff(FRIENDLY_HERO, "BAR_891e2")


BAR_891e2 = buff(atk=3)


class BAR_891t2:
    """Fury (Rank 3)"""

    # Give your hero +4_Attack this turn.
    play = Buff(FRIENDLY_HERO, "BAR_891e3")


BAR_891e3 = buff(atk=4)


class WC_003:
    """Sigil of Summoning"""

    # At the start of your next turn, summon two 2/2 Demons with <b>Taunt</b>.
    events = OWN_TURN_BEGIN.on(Summon(CONTROLLER, "WC_003t") * 2, Destroy(SELF))


##
# Weapons


class BAR_330:
    """Tuskpiercer"""

    # [x]<b>Deathrattle:</b> Draw a <b>Deathrattle</b> minion.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE))
