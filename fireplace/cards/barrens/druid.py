from ..utils import *

##
# Minions


class BAR_535:
    """Thickhide Kodo"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Gain 5 Armor.
    deathrattle = GainArmor(FRIENDLY_HERO, 5)


class BAR_537:
    """Razormane Battleguard"""

    # The first <b>Taunt</b> minion you_play each turn costs_(2) less.
    update = Find(CARDS_PLAYED_THIS_TURN + MINION + TAUNT) | (
        Refresh(FRIENDLY_HAND + MINION + TAUNT, "BAR_537e")
    )


class BAR_537e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class BAR_538:
    """Druid of the Plains"""

    # <b>Rush</b> <b>Frenzy:</b> Transform into a 6/7 Kodo with <b>Taunt</b>.
    frenzy = Morph(SELF, "BAR_538t")


class BAR_540:
    """Plaguemaw the Rotting"""

    # [x]After a friendly minion with <b>Taunt</b> dies, summon a new _copy of
    # it without <b>Taunt</b>.
    events = Death(FRIENDLY_MINIONS + TAUNT).after(
        Summon(CONTROLLER, Copy(Death.ENTITY)).then(
            UnsetTag(Summon.CARD, GameTag.TAUNT)
        )
    )


class BAR_720:
    """Guff Runetotem"""

    # After you cast a Nature spell, give another friendly minion +2/+2.
    events = CastSpell(CONTROLLER, SPELL + NATURE).after(
        Buff(RANDOM(FRIENDLY_MINIONS - SELF), "BAR_720e")
    )


class BAR_720e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class WC_004:
    """Fangbound Druid"""

    # <b>Taunt</b> <b>Deathrattle:</b> Reduce the Cost of a Beast in your hand
    # by (2).
    deathrattle = Buff(RANDOM(FRIENDLY_HAND + BEAST), "BAR_540e")


BAR_540e = buff(cost=-2)


class WC_006:
    """Lady Anacondra"""

    # Your Nature spells cost (2) less.
    update = Refresh(FRIENDLY_HAND + SPELL + NATURE, {GameTag.COST: -2})


class WC_036:
    """Deviate Dreadfang"""

    # After you cast a Nature spell, summon a 4/2 Viper with <b>Rush</b>.
    events = Play(CONTROLLER, SPELL + NATURE).after(Summon(CONTROLLER, "WC_036t1"))


##
# Spells


class BAR_533:
    """Thorngrowth Sentries"""

    # Summon two 1/2 Turtles with <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_533t") * 2


class BAR_534:
    """Pride's Fury"""

    # Give your minions +1/+3.
    play = Buff(FRIENDLY_MINIONS, "BAR_534e")


BAR_534e = buff(+1, +3)


class BAR_536:
    """Living Seed (Rank 1)"""

    # Draw a Beast. Reduce its Cost by (1). <i>(Upgrades when you have 5
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_536t")

    play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(ForceDraw.TARGET, "BAR_536e")
    )


class BAR_536e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class BAR_536t:
    """Living Seed (Rank 2)"""

    # Draw a Beast. Reduce its Cost by (2). <i>(Upgrades when you have 10
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_536t2")

    play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(ForceDraw.TARGET, "BAR_536te")
    )


class BAR_536te:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class BAR_536t2:
    """Living Seed (Rank 3)"""

    # Draw a Beast. Reduce its Cost by (3).
    play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(ForceDraw.TARGET, "BAR_536t2e")
    )


class BAR_536t2e:
    tags = {GameTag.COST: -3}
    events = REMOVED_IN_PLAY


class BAR_539:
    """Celestial Alignment"""

    # Set each player to 0 Mana Crystals. Set the Cost of cards in all hands
    # and decks to (1).
    play = SetMana(ALL_PLAYERS, 0), Buff(IN_HAND | IN_DECK, "BAR_539e")


class BAR_539e:
    tags = {GameTag.COST: SET(1)}
    events = REMOVED_IN_PLAY


class BAR_549:
    """Mark of the Spikeshell"""

    # Give a minion +2/+2. If it has <b>Taunt</b>, add a copy of it to your
    # hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BAR_549e"), Find(TARGET + TAUNT) & (
        Give(CONTROLLER, Copy(TARGET))
    )


BAR_549e = buff(+2, +2)
