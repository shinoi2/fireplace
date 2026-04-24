from ..utils import *

##
# Minions


class BAR_912:
    """Apothecary's Caravan"""

    # [x]At the start of your turn, summon a 1-Cost minion from your deck.
    events = OWN_TURN_BEGIN.on(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST == 1)))
    )


class BAR_915:
    """Kabal Outfitter"""

    # [x]<b>Battlecry and Deathrattle:</b> Give another random _friendly minion
    # +1/+1.
    play = deathrattle = Buff(RANDOM(FRIENDLY_MINIONS - SELF), "BAR_915e")


BAR_915e = buff(+1, +1)


class BAR_916:
    """Blood Shard Bristleback"""

    # [x]<b>Lifesteal</b>. <b>Battlecry:</b> If your deck contains 10 or fewer
    # cards, deal 6 damage to a minion.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DECK_LESS_OR_EQUAL: 10,
    }
    play = Hit(TARGET, 6)


class BAR_917:
    """Barrens Scavenger"""

    # [x]<b>Taunt</b> Costs (1) while your deck has 10 or fewer cards.
    class Hand:
        update = (Count(FRIENDLY_DECK) <= 10) & Refresh(SELF, {GameTag.COST: SET(0)})


class BAR_918:
    """Tamsin Roame"""

    # [x]Whenever you cast a Shadow spell that costs (1) or more, add a copy to
    # your hand that costs (0).
    events = Play(CONTROLLER, SHADOW + (COST >= 1)).after(
        Give(CONTROLLER, Copy(Play.CARD)).then(Buff(Give.CARD, "BAR_918e"))
    )


class BAR_918e:
    cost = SET(0)
    events = REMOVED_IN_PLAY


class BAR_919:
    """Neeru Fireblade"""

    # <b>Battlecry:</b> If your deck is empty, open a portal that fills your
    # board with 3/2 Imps each turn.
    play = (Count(FRIENDLY_DECK) == 0) & Summon(CONTROLLER, "BAR_919t")


class BAR_919t:
    events = OWN_TURN_END.on(SummonBothSides(CONTROLLER, "BAR_914t3") * 7)


class WC_023:
    """Stealer of Souls"""

    # After you draw a card, change its Cost to Health instead of Mana.
    events = Draw(CONTROLLER).on(Buff(Draw.CARD, "WC_023e"))


class WC_023e:
    tags = {GameTag.CARD_COSTS_HEALTH: True}


##
# Spells


class BAR_910:
    """Grimoire of Sacrifice"""

    # Destroy a friendly minion. Deal $2 damage to all enemy minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Hit(ENEMY_MINIONS, 2)


class BAR_911:
    """Soul Rend"""

    # [x]Deal $5 damage to all minions. Destroy a card in your deck for each
    # killed.
    play = Hit(ALL_MINIONS, 5).then(
        Destroy(RANDOM(FRIENDLY_DECK)) * Count(ALL_MINIONS + DEAD)
    )


class BAR_913:
    """Altar of Fire"""

    # Destroy the top 3 cards of each deck.
    play = Mill(CONTROLLER, 3), Mill(OPPONENT, 5)


class BAR_914:
    """Imp Swarm (Rank 1)"""

    # Summon a 3/2 Imp. <i>(Upgrades when you have 5 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_914t")

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_914t3")


class BAR_914t:
    """Imp Swarm (Rank 2)"""

    # Summon two 3/2 Imps. <i>(Upgrades when you have 10 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_914t2")

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_914t3") * 2


class BAR_914t2:
    """Imp Swarm (Rank 3)"""

    # Summon three 3/2 Imps.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_914t3") * 3


class WC_021:
    """Unstable Shadow Blast"""

    # [x]Deal $6 damage to a minion. Excess damage hits your hero.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(FRIENDLY_HERO, HitExcessDamage(TARGET, SPELL_DAMAGE(6)))


class WC_022:
    """Final Gasp"""

    # [x]Deal $1 damage to a minion. If it dies, summon a 2/2 Adventurer with a
    # random bonus effect.
    entourage = ADVENTURERS
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), Dead(TARGET) & Summon(CONTROLLER, RandomEntourage())
