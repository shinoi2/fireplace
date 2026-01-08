from ..utils import *


##
# Minions


class SCH_147:
    """Boneweb Egg"""

    # [x]<b>Deathrattle:</b> Summon two 2/1 Spiders. If you discard this,
    # trigger its <b>Deathrattle</b>.
    deathrattle = discard = Summon(CONTROLLER, "SCH_147t") * 2


class SCH_181:
    """Archwitch Willow"""

    # <b>Battlecry:</b> Summon a random Demon from your hand and deck.
    play = (
        Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON)),
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + DEMON)),
    )


class SCH_343:
    """Void Drinker"""

    # [x]<b>Taunt</b>. <b>Battlecry:</b> Destroy a Soul Fragment in your deck
    # to gain +3/+3.
    powered_up = Find(FRIENDLY_DECK + ID(SOUL_FRAGMENT))
    play = (
        powered_up
        & Destroy(RANDOM(FRIENDLY_DECK + ID(SOUL_FRAGMENT)))
        & Buff(SELF, "SCH_343e")
    )


SCH_343e = buff(+3, +3)


class SCH_517:
    """Shadowlight Scholar"""

    # <b>Battlecry:</b> Destroy a Soul Fragment in your deck to deal 3 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_SOUL_FRAGMENT_IN_DECK: 0,
    }
    powered_up = Find(FRIENDLY_DECK + ID(SOUL_FRAGMENT))
    play = Destroy(RANDOM(FRIENDLY_DECK + ID(SOUL_FRAGMENT))), Hit(TARGET, 3)


class SCH_700:
    """Spirit Jailer"""

    # <b>Battlecry:</b> Shuffle 2 Soul Fragments into your deck.
    play = Shuffle(CONTROLLER, SOUL_FRAGMENT) * 2


class SCH_703:
    """Soulciologist Malicia"""

    # <b>Battlecry:</b> For each Soul Fragment in your deck, summon a 3/3 Soul
    # with <b>Rush</b>.@ <i>(@)</i>
    play = SummonBothSides(CONTROLLER, "SCH_703t") * Count(
        FRIENDLY_DECK + ID(SOUL_FRAGMENT)
    )


##
# Spells


class SCH_158:
    """Demonic Studies"""

    # <b>Discover</b> a Demon. Your next one costs (1) less.
    play = DISCOVER(RandomDemon()), Buff(CONTROLLER, "SCH_158e")


class SCH_158e:
    update = Refresh(FRIENDLY_HAND + DEMON, buff="SCH_158e2")
    events = Play(CONTROLLER, DEMON).after(Destroy(SELF))


class SCH_158e2:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class SCH_307:
    """School Spirits"""

    # [x]Deal $2 damage to all minions. Shuffle 2 Soul Fragments into your
    # deck.
    play = Hit(ALL_MINIONS, 2), Shuffle(CONTROLLER, SOUL_FRAGMENT) * 2


class SCH_701:
    """Soul Shear"""

    # [x]Deal $3 damage to a minion. Shuffle 2 Soul Fragments into your deck.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Shuffle(CONTROLLER, SOUL_FRAGMENT) * 2


class SCH_702:
    """Felosophy"""

    # [x]Copy the lowest Cost Demon in your hand. <b>Outcast:</b> Give both
    # +1/+1.
    play = Give(CONTROLLER, ExactCopy(LOWEST_COST(FRIENDLY_HAND + DEMON)))
    outcast = Buff(LOWEST_COST(FRIENDLY_HAND + DEMON), "SCH_702e").then(
        Give(CONTROLLER, ExactCopy(Buff.TARGET))
    )


SCH_702e = buff(+1, +1)
