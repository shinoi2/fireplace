from ..utils import *


##
# Minions


class DMF_071:
    """Tenwu of the Red Smoke"""

    # <b>Battlecry:</b> Return a friendly minion to your hand. It costs (1)
    # this turn.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Bounce(TARGET).then(Buff(Bounce.TARGET, "DMF_071e"))


class DMF_071e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class DMF_511:
    """Foxy Fraud"""

    # <b>Battlecry:</b> Your next <b>Combo</b> card this turn costs_(2) less.
    play = Buff(CONTROLLER, "DMF_511e")


class DMF_511e:
    update = Refresh(FRIENDLY_HAND + COMBO, buff="DMF_511e2")
    events = Play(CONTROLLER, COMBO).after(Destroy(SELF))


class DMF_511e2:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class DMF_514:
    """Ticket Master"""

    # [x]<b>Deathrattle:</b> Shuffle 3 Tickets into your deck. When drawn,
    # summon a 3/3 Plush Bear.
    deathrattle = Shuffle(CONTROLLER, "DMF_514t") * 3


class DMF_514t:
    draw = CAST_WHEN_DRAWN
    play = Summon(CONTROLLER, "DMF_514t2")


class DMF_516:
    """Grand Empress Shek'zara"""

    # <b>Battlecry:</b> <b>Discover</b> a card in your deck and draw all copies
    # of it.
    play = Choice(CONTROLLER, RANDOM(FRIENDLY_DECK, 3)).then(
        ForceDraw(CONTROLLER, FRIENDLY_DECK + SameId(Choice.CARD))
    )


class DMF_517:
    """Sweet Tooth"""

    # <b>Corrupt:</b> Gain +2 Attack and <b>Stealth</b>.
    corrupt_card = "DMF_517t"


class DMF_519:
    """Prize Plunderer"""

    # [x]<b>Combo:</b> Deal 1 damage to a minion for each other card you've
    # played this turn.
    requirements = {
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    combo = Hit(TARGET, 1) * NUM_CARDS_PLAYED_THIS_TURN


class YOP_016:
    """Sparkjoy Cheat"""

    # <b>Battlecry:</b> If you're holding a <b>Secret</b>, cast it and draw a
    # card.
    powered_up = Find(FRIENDLY_HAND + SECRET)
    play = powered_up & (CastSpell(RANDOM(FRIENDLY_HAND + SECRET)), Draw(CONTROLLER))


##
# Spells


class DMF_512:
    """Cloak of Shadows"""

    # Give your hero <b>Stealth</b> for 1 turn.
    play = Buff(FRIENDLY_HERO, "DMF_512e")


DMF_512e = buff(stealth=True)


class DMF_513:
    """Shadow Clone"""

    # <b>Secret:</b> After a minion attacks your hero, summon a copy of it
    # with_<b>Stealth</b>.
    secret = Attack(MINION, FRIENDLY_HERO).after(
        Reveal(SELF),
        Summon(CONTROLLER, ExactCopy(Attack.ATTACKER)).then(Stealth(Summon.CARD)),
    )


class DMF_515:
    """Swindle"""

    # Draw a spell. <b>Combo:</b> And a minion.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))
    combo = (
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)),
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)),
    )


class DMF_518:
    """Malevolent Strike"""

    # [x]Destroy a minion. Costs (1) less for each _ card in your deck that _
    # didn't start there.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    cost_mod = -Count(FRIENDLY_DECK - STARTING_DECK)
    play = Destroy(TARGET)


class YOP_015:
    """Nitroboost Poison"""

    # Give a minion +2 Attack. <b>Corrupt:</b> And your weapon.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "YOP_015e")
    corrupt_card = "YOP_015t"


class YOP_015t:
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "YOP_015e"), Buff(FRIENDLY_WEAPON, "YOP_015e")


YOP_015e = buff(atk=2)


class YOP_017:
    """Shenanigans"""

    # <b>Secret:</b> When your opponent draws their second card in a turn,
    # transform it into a Banana.
    secret = Draw(OPPONENT).after(
        (Attr(OPPONENT, GameTag.NUM_CARDS_DRAWN_THIS_TURN) == 2)
        & (Reveal(SELF), Morph(Draw.CARD, "EX1_014t"))
    )
