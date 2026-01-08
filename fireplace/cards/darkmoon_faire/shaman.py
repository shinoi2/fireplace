from ..utils import *


##
# Minions


class DMF_703:
    """Pit Master"""

    # <b>Battlecry:</b> Summon a 3/2_Duelist. <b>Corrupt:</b> Summon two.
    play = Summon(CONTROLLER, "DMF_703t2")
    corrupt_card = "DMF_703t"


class DMF_703t:
    play = SummonBothSides(CONTROLLER, "DMF_703t2") * 2


class DMF_704:
    """Cagematch Custodian"""

    # <b>Battlecry:</b> Draw a weapon.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON))


class DMF_707:
    """Magicfin"""

    # After a friendly Murloc dies, add a random Legendary minion to your hand.
    events = Death(FRIENDLY + MURLOC).after(Give(CONTROLLER, RandomLegendaryMinion()))


class DMF_708:
    """Inara Stormcrash"""

    # On your turn, your hero has +2 Attack and <b>Windfury</b>.
    update = Find(CURRENT_PLAYER + CONTROLLER) & Refresh(FRIENDLY_HERO, buff="DMF_708e")


DMF_708e = buff(atk=2, windfury=True)


class DMF_709:
    """Grand Totem Eys'or"""

    # At the end of your turn, give +1/+1 to all other Totems in your hand,
    # deck and battlefield.
    events = OWN_TURN_END.on(Buff((FRIENDLY_HAND | FRIENDLY_DECK) + TOTEM, "DMF_709e"))


DMF_709e = buff(+1, +1)


class YOP_022:
    """Mistrunner"""

    # <b>Battlecry:</b> Give a friendly minion +3/+3. <b>Overload:</b> (1)
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "YOP_022e")


##
# Spells


class DMF_700:
    """Revolve"""

    # Transform all minions into random ones with the same Cost.
    play = Evolve(ALL_MINIONS, 0)


class DMF_701:
    """Dunk Tank"""

    # Deal $4 damage. <b>Corrupt:</b> Then deal $2 damage to all enemy minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    corrupt_card = "DMF_701t"
    play = Hit(TARGET, 4)


class DMF_701t:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4), Hit(ENEMY_MINIONS, 2)


class DMF_702:
    """Stormstrike"""

    # Deal $3 damage to a minion. Give your hero +3 Attack this turn.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Buff(FRIENDLY_HERO, "DMF_702e")


DMF_702e = buff(atk=3)


class DMF_706:
    """Deathmatch Pavilion"""

    # Summon a 3/2 Duelist. If your hero attacked this turn, summon another.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    powered_up = NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) > 0
    play = powered_up & (Summon(CONTROLLER, "DMF_706t") * 2) | (
        Summon(CONTROLLER, "DMF_706t")
    )


class YOP_023:
    """Landslide"""

    # [x]Deal $1 damage to all enemy minions. If you're <b>Overloaded</b>, deal
    # $1 damage again.
    powered_up = OVERLOADED(CONTROLLER)
    play = powered_up & (Hit(ENEMY_MINIONS, 1) * 2) | (Hit(ENEMY_MINIONS, 1))


##
# Weapons


class DMF_705:
    """Whack-A-Gnoll Hammer"""

    # After your hero attacks, give a random friendly minion +1/+1.
    events = Attack(FRIENDLY_HERO).after(Buff(RANDOM_FRIENDLY_MINION, "DMF_705e"))


DMF_705e = buff(+1, +1)
