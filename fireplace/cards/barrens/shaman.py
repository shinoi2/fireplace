from pkg_resources import Requirement
from ..utils import *

##
# Minions


class BAR_040:
    """South Coast Chieftain"""

    # <b>Battlecry:</b> If you control another Murloc, deal 2_damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_CONTROLLER_OTHER_WITH_RACE: Race.MURLOC
    }
    play = Hit(TARGET, 2)


class BAR_043:
    """Tinyfin's Caravan"""

    # At the start of your turn, draw a Murloc.
    events = OWN_TURN_BEGIN.on(ForceDraw(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)))


class BAR_045:
    """Arid Stormer"""

    # <b>Battlecry:</b> If you played an Elemental last turn, gain <b>Rush</b>
    # and <b>Windfury</b>.
    play = ELEMENTAL_PLAYED_LAST_TURN & (GiveRush(SELF), GiveWindfury(SELF))


class BAR_750:
    """Earth Revenant"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Deal 1 damage to all enemy minions.
    play = Hit(ENEMY_MINIONS, 1)


class BAR_751:
    """Spawnpool Forager"""

    # <b>Deathrattle:</b> Summon a 1/1 Tinyfin.
    deathrattle = Summon(CONTROLLER, "BAR_751t")


class BAR_848:
    """Lilypad Lurker"""

    # [x]<b>Battlecry:</b> If you played an Elemental last turn, transform an
    # enemy minion into a 0/1 Frog with <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_ELEMENTAL_PLAYED_LAST_TURN: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Morph(TARGET, "hexfrog")


class BAR_860:
    """Firemancer Flurgl"""

    # [x]After you play a Murloc, deal 1 damage to all enemies.
    events = Play(CONTROLLER, MURLOC).after(Hit(ENEMY_CHARACTERS, 1))


class WC_005:
    """Primal Dungeoneer"""

    # [x]<b>Battlecry:</b> Draw a spell. If it's a Nature spell, also draw an
    # Elemental.
    play = ForceDraw(CONTROLLER, RANDOM(FRIENDLY_DECK + SPELL)).then(
        Find(ForceDraw.TARGET + NATURE)
        & (ForceDraw(CONTROLLER, RANDOM(FRIENDLY_DECK + ELEMENTAL)))
    )


class WC_042:
    """Wailing Vapor"""

    # [x]After you play an Elemental, gain +1 Attack.
    events = Play(CONTROLLER, ELEMENTAL).after(Buff(SELF, "WC_042e"))


WC_042e = buff(atk=1)


##
# Spells


class BAR_041:
    """Nofin Can Stop Us"""

    # [x]Give your minions +1/+1. Give your Murlocs an extra +1/+1.
    play = Buff(FRIENDLY_MINIONS, "BAR_041e"), Buff(
        FRIENDLY_MINIONS + MURLOC, "BAR_041e"
    )


BAR_041e = buff(+1, +1)


class BAR_044:
    """Chain Lightning (Rank 1)"""

    # Deal $2 damage to a minion and a random adjacent one. <i>(Upgrades when
    # you have 5 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_044t")

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), Hit(RANDOM(TARGET_ADJACENT), 2)


class BAR_044t:
    """Chain Lightning (Rank 2)"""

    # Deal $3 damage to a minion and a random adjacent one. <i>(Upgrades when
    # you have 10 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_044t2")

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Hit(RANDOM(TARGET_ADJACENT), 3)


class BAR_044t2:
    """Chain Lightning (Rank 3)"""

    # Deal $4 damage to a minion and a random adjacent one.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), Hit(RANDOM(TARGET_ADJACENT), 4)


class WC_020:
    """Perpetual Flame"""

    # Deal $3 damage to a random enemy minion. If it dies, recast this.
    # <b>Overload:</b> (1)
    play = Hit(RANDOM_ENEMY_MINION, 3).then(
        Find(Hit.TARGET + DEAD) & Battlecry(SELF, None)
    )
