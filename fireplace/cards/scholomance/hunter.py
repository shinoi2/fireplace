from ..utils import *


##
# Minions


class SCH_133:
    """Wolpertinger"""

    # <b>Battlecry:</b> Summon a copy of this.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class SCH_239:
    """Krolusk Barkstripper"""

    # <b>Spellburst:</b> Destroy a random enemy minion.
    spellburst = Destroy(RANDOM(ENEMY_MINIONS))


class SCH_244:
    """Teacher's Pet"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a random 3-Cost Beast.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST + (COST == 3)))


class SCH_340:
    """Bloated Python"""

    # <b>Deathrattle:</b> Summon a 4/4 Hapless Handler.
    deathrattle = Summon(CONTROLLER, "SCH_340t")


class SCH_539:
    """Professor Slate"""

    # Your spells are <b>Poisonous</b>.
    update = Refresh(FRIENDLY + SPELL, {GameTag.POISONOUS: True})


class SCH_607:
    """Shan'do Wildclaw"""

    # [x]<b>Choose One -</b> Give Beasts in your deck +1/+1; or Transform into
    # a copy of a friendly Beast.
    choose = ("SCH_607a", "SCH_607b")


class SCH_607a:
    # Give Beasts in your deck +1/+1
    update = Buff(FRIENDLY_DECK + BEAST, "SCH_607e")


SCH_607e = buff(+1, +1)


class SCH_607b:
    # Transform into a copy of a friendly Beast
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = Morph(SELF, ExactCopy(TARGET))


##
# Spells


class SCH_300:
    """Carrion Studies"""

    # <b>Discover</b> a <b>Deathrattle</b> minion. Your next one costs (1)
    # less.
    play = DISCOVER(RandomMinion(deathrattle=True)).then(Buff(CONTROLLER, "SCH_300e"))


class SCH_300e:
    # Your next <b>Deathrattle</b> minion costs (1) less
    update = Buff(FRIENDLY_HAND + MINION + DEATHRATTLE, "SCH_300e2")
    events = Play(CONTROLLER, MINION + DEATHRATTLE).after(Destroy(SELF))


class SCH_300e2:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class SCH_604:
    """Overwhelm"""

    # Deal $2 damage to a minion. Deal one more damage for each Beast you
    # control.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, Count(FRIENDLY_MINIONS + BEAST) + 2)


class SCH_610:
    """Guardian Animals"""

    # Summon two Beasts that cost (5) or less from your deck. Give_them
    # <b>Rush</b>.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST + (COST <= 5), 2)).then(
        GiveRush(Summon.CARD)
    )


class SCH_617:
    """Adorable Infestation"""

    # Give a minion +1/+1. Summon a 1/1 Cub. Add a Cub to your hand.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Buff(TARGET, "SCH_617e").then(
        Summon(CONTROLLER, "SCH_617t"), Give(CONTROLLER, "SCH_617t")
    )


SCH_617e = buff(+1, +1)
