from ..utils import *

##
# Minions


class SW_006:
    """Stubborn Suspect"""

    # <b>Deathrattle:</b> Summon a random 3-Cost minion.
    deathrattle = Summon(CONTROLLER, RandomMinion(cost=3))


class SW_307:
    """Traveling Merchant"""

    # [x]<b>Tradeable</b> <b>Battlecry:</b> Gain +1/+1 for each other friendly
    # _minion you control.
    play = Buff(
        SELF,
        "SW_307e",
        atk=Count(FRIENDLY_MINIONS - SELF),
        max_health=Count(FRIENDLY_MINIONS - SELF),
    )


class SW_418:
    """SI:7 Skulker"""

    # [x]<b>Stealth</b> <b>Battlecry:</b> The next card __you draw costs (1)
    # less.
    play = Buff(CONTROLLER, "SW_418e")


class SW_418e:
    events = Draw(CONTROLLER).on(Buff(Draw.CARD, "SW_418e2"), Destroy(SELF))


class SW_418e2:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class SW_319:
    """Peasant"""

    # At the start of your turn, draw a card.
    events = OWN_TURN_BEGIN.on(Draw(CONTROLLER))


class SW_054:
    """Stormwind Guard"""

    # <b>Taunt</b> <b>Battlecry:</b> Give adjacent minions +1/+1.
    play = Buff(TARGET_ADJACENT, "SW_054e")


SW_054e = buff(+1, +1)


class SW_056:
    """Spice Bread Baker"""

    # <b>Battlecry:</b> Restore Health to your hero equal to your hand size.
    play = Heal(FRIENDLY_HERO, Count(FRIENDLY_HAND))


class SW_057:
    """Package Runner"""

    # Can only attack if you have at least 8 cards in hand.
    update = (Count(FRIENDLY_HAND) >= 8) | Refresh(SELF, {GameTag.CANT_ATTACK: True})


class SW_059:
    """Deeprun Engineer"""

    # <b>Battlecry:</b> <b>Discover</b> a Mech. It costs (1) less.
    play = DISCOVER(RandomMech()).then(Buff(Discover.CARD, "SW_059e"))


class SW_059e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class SW_060:
    """Florist"""

    # [x]At the end of your turn, reduce the cost of a Nature _spell in your
    # hand by (1).
    events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_HAND + NATURE + SPELL), "SW_060t"))


class SW_060t:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class SW_063:
    """Battleground Battlemaster"""

    # Adjacent minions have <b>Windfury</b>.
    update = Refresh(SELF, buff="SW_063e")


SW_063e = buff(windfury=True)


class SW_064:
    """Northshire Farmer"""

    # <b>Battlecry:</b> Choose a friendly Beast. Shuffle three 3/3
    # copies_into_your_deck.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = Shuffle(CONTROLLER, Buff(Copy(TARGET), "SW_064e")) * 3


class SW_064e:
    atk = SET(3)
    max_health = SET(3)


class SW_065:
    """Pandaren Importer"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a spell that didn't start in your
    # deck.
    play = DISCOVER(RandomSpell(exclude=STARTING_DECK))


class SW_066:
    """Royal Librarian"""

    # [x]<b>Tradeable</b> <b>Battlecry:</b> <b>Silence</b> a minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Silence(TARGET)


class SW_067:
    """Stockades Guard"""

    # [x]<b>Battlecry:</b> Give a friendly minion <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Taunt(TARGET)


class SW_068:
    """Mo'arg Forgefiend"""

    # <b>Taunt</b> <b>Deathrattle:</b> Gain 8 Armor.
    deathrattle = GainArmor(FRIENDLY_HERO, 8)


class SW_071:
    """Lion's Guard"""

    # [x]<b>Battlecry:</b> If you have 15 or less Health, gain +2/+4 and
    # <b>Taunt</b>.
    play = (CURRENT_HEALTH(FRIENDLY_HERO) <= 15) & Buff(SELF, "SW_071e")


SW_071e = buff(+2, +4, taunt=True)


class SW_072:
    """Rustrot Viper"""

    # [x]<b>Tradeable</b> <b>Battlecry:</b> Destroy your opponent's weapon.
    play = Destroy(ENEMY_WEAPON)


class SW_076:
    """City Architect"""

    # [x]<b>Battlecry:</b> Summon two 0/5 Castle Walls with <b>Taunt</b>.
    play = SummonBothSides(CONTROLLER, "SW_076t") * 2


class DED_523:
    """Golakka Glutton"""

    # <b>Battlecry:</b> Destroy a Beast and gain +1/+1.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = Destroy(TARGET), Buff(SELF, "DED_523e")


DED_523e = buff(+1, +1)
