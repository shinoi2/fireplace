from ..utils import *

##
# Minions


class TSC_917:
    """Blackscale Brute"""

    # <b>Taunt</b>. <b>Battlecry:</b> If you have a weapon equipped, summon a
    # 5/6 Naga with <b>Rush</b>.
    powered_up = Find(FRIENDLY_WEAPON)
    play = powered_up & Summon(CONTROLLER, "TSC_917t")


class TSC_942:
    """Obsidiansmith"""

    # [x]<b>Battlecry:</b> <b>Dredge</b>. If it's a minion or a weapon, give it
    # +1/+1.
    play = Dredge(CONTROLLER).then(
        Find(Dredge.CARD + (MINION | WEAPON)) & Buff(Dredge.CARD, "TSC_942e")
    )


class TSC_943:
    """Lady Ashvane"""

    # <b>Battlecry:</b> Give all weapons in your hand, deck, and battlefield
    # +1/+1.
    play = (
        Buff(FRIENDLY_HAND + WEAPON, "TSC_943e"),
        Buff(FRIENDLY_DECK + WEAPON, "TSC_943e"),
        Buff(FRIENDLY_WEAPON, "TSC_943e"),
    )


TSC_943e = buff(+1, +1)


class TSC_659:
    """Trenchstalker"""

    # <b>Battlecry:</b> Attack three different random enemies.
    play = Attack(SELF, RANDOM_ENEMY_CHARACTER * 3)


class TSC_660:
    """Nellie, the Great Thresher"""

    # [x]<b>Colossal +1</b> <b>Battlecry:</b> <b>Discover</b> 3 Pirates to crew
    # Nellie's Ship!
    colossal = Summon(CONTROLLER, "TSC_660t").then(Retarget(Summon.CARD))
    play = Discover(CONTROLLER, RandomMinion(race=Race.PIRATE)).then(
        StoringBuff(TARGET, "TSC_660e", Discover.CARD)
    )


class TSC_660e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, STORE_CARD).then(Buff(Give.CARD, "TSC_660e2"))


TSC_660e2 = cost_buff(SET(1))


class TID_714:
    """Igneous Lavagorger"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> <b>Dredge</b>. Gain _Armor equal to its
    # Cost.
    play = Dredge(CONTROLLER).then(GainArmor(FRIENDLY_HERO, COST(Dredge.CARD)))


class TID_716:
    """Tidal Revenant"""

    # <b>Battlecry:</b> Deal 5 damage. Gain 5 Armor.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 5), GainArmor(FRIENDLY_HERO, 5)


##
# Spells


class TSC_939:
    """Forged in Flame"""

    # Destroy your weapon, then draw cards equal to its Attack.
    play = Destroy(FRIENDLY_WEAPON).then(Draw(CONTROLLER) * ATK(Destroy.TARGET))


class TSC_940:
    """From the Depths"""

    # [x]Reduce the Cost of the bottom five cards in your _deck by (3), then
    # <b>Dredge</b>.
    play = Buff(FRIENDLY_DECK[:5], "TSC_940e2").then(Dredge(CONTROLLER))


TSC_940e2 = cost_buff(-3)


class TSC_941:
    """Guard the City"""

    # Gain 3 Armor. Summon a 2/3 Naga with <b>Taunt</b>.
    play = GainArmor(FRIENDLY_HERO, 3), Summon(CONTROLLER, "TSC_941t")


class TSC_944:
    """The Fires of Zin-Azshari"""

    # Replace your deck with minions that cost (5) or more. They cost (5).
    play = Morph(FRIENDLY_DECK, RandomMinion(cost=range(5, 100))).then(
        Buff(Morph.CARD, "TSC_944e")
    )


TSC_944e = cost_buff(SET(5))


class TID_715:
    """Clash of the Colossals"""

    # Add a random <b>Colossal</b> minion to both players' hands. Yours costs
    # (2) less.
    play = Give(
        ALL_PLAYERS, RandomMinion(colossal=True, can_pick_from_subsets=True)
    ).then(Buff(Give.CARD, "TID_715e"))


TID_715e = cost_buff(-2)


##
# Weapons


class TSC_913:
    """Azsharan Trident"""

    # [x]<b>Deathrattle:</b> Put a 'Sunken Trident' on the _bottom of your
    # deck.
    deathrattle = PutOnBottom(CONTROLLER, "TSC_913t")


class TSC_913t:
    """Sunken Trident"""

    # After your hero attacks, deal 2 damage to all enemy minions.
    events = Attack(FRIENDLY_HERO).after(Hit(ENEMY_MINIONS, 2))
