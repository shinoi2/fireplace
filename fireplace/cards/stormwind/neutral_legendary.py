from ..utils import *


class SW_079:
    """Flightmaster Dungar"""

    # [x]<b>Battlecry:</b> Choose a flightpath and go <b>Dormant. </b> Awaken
    # with a bonus __when you complete it!
    play = Choice(CONTROLLER, ["SW_079t", "SW_079t2", "SW_079t3"]).then(
        Battlecry(Choice.CARD, None)
    )


class SW_079t:
    """Westfall"""

    # [x]In 1 turn, summon a 2/2 Adventurer with _a random bonus effect.
    play = Dormant(SELF, 1), Buff(SELF, "SW_079te")


class SW_079t2:
    """Ironforge"""

    # In 3 turns, restore 10 Health to your hero.
    play = Dormant(SELF, 3), Buff(SELF, "SW_079t2e")


class SW_079t3:
    """Eastern Plaguelands"""

    # In 5 turns, deal 12 damage randomly split among enemies.
    play = Dormant(SELF, 5), Buff(SELF, "SW_079t3e")


class SW_079te:
    """Westfall Flight"""

    # Next turn, summon a 2/2 Adventurer.
    entourage = ADVENTURERS
    events = Awaken(OWNER).on(
        Summon(CONTROLLER, RandomEntourage()),
        Destroy(SELF),
    )


class SW_079t2e:
    """Ironforge Flight"""

    # In 3 turns, restore 10 Health to your hero.
    events = Awaken(OWNER).on(
        Heal(FRIENDLY_HERO, 10),
        Destroy(SELF),
    )


class SW_079t3e:
    """Plaguelands Flight"""

    # In 5 turns, deal 12 damage randomly split among enemies.
    events = Awaken(OWNER).on(
        Hit(RANDOM_ENEMY_CHARACTER, 1) * 12,
        Destroy(SELF),
    )
