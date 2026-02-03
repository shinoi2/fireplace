from ..utils import *

##
# Minions


class SCH_120:
    """Cabal Acolyte"""

    # [x]<b>Taunt</b> <b>Spellburst:</b> Gain control of a random enemy minion
    # with 2 or less Attack.
    spellburst = Steal(RANDOM(ENEMY_MINIONS + (ATK <= 2)))


class SCH_126:
    """Disciplinarian Gandling"""

    # [x]After you play a minion, destroy it and summon a 4/4 Failed Student.
    events = Play(CONTROLLER, MINION).after(
        Destroy(Play.CARD), Summon(CONTROLLER, "SCH_126t")
    )


class SCH_140:
    """Flesh Giant"""

    # Costs (1) less for each time your hero's Health changed during your
    # turns.
    cost_mod = -Attr(CONTROLLER, enums.HERO_HEALTH_CHANGED_THIS_TURN)


class SCH_159:
    """Mindrender Illucia"""

    # <b>Battlecry:</b> Swap hands and decks with your opponent until your next
    # turn.
    play = SwapDecks(), SwapHands(), Buff(CONTROLLER, "SCH_159e")


class SCH_159e:
    events = OWN_TURN_BEGIN.on(SwapDecks(), SwapHands(), Destroy(SELF))


class SCH_513:
    """Brittlebone Destroyer"""

    # [x]<b>Battlecry:</b> If your hero's Health changed this turn, destroy a
    # minion.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_PLAYER_HEALTH_CHANGED_THIS_TURN: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET)


##
# Spells


class SCH_136:
    """Power Word: Feast"""

    # Give a minion +2/+2. Restore it to full Health at the end of this turn.
    play = MultiBuff(TARGET, ["SCH_136e", "SCH_136e2"])


SCH_136e = buff(+2, +2)


class SCH_136e2:
    events = OWN_TURN_END.on(FullHeal(OWNER), Destroy(SELF))


class SCH_233:
    """Draconic Studies"""

    # [x]<b>Discover</b> a Dragon. Your next one costs (1) less.
    play = Discover(CONTROLLER, RandomDragon()), Buff(CONTROLLER, "SCH_233e")


class SCH_233e:
    update = Refresh(FRIENDLY_HAND + DRAGON, buff="SCH_233e2")
    events = Play(CONTROLLER, DRAGON).on(Destroy(SELF))


class SCH_233e2:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class SCH_512:
    """Initiation"""

    # Deal $4 damage to a minion. If that kills it, summon a new copy.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), Dead(TARGET) & Summon(CONTROLLER, Copy(TARGET))


class SCH_514:
    """Raise Dead"""

    # Deal $3 damage to your hero. Return two friendly minions that died this
    # game to your hand.
    play = Hit(FRIENDLY_HERO, 3), Give(
        CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION, 2)
    )
