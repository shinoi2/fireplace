from ..utils import *

##
# Minions


class CS3_013:
    """Shadowed Spirit"""

    # [x]<b>Deathrattle:</b> Deal 3 damage to the enemy hero.
    deathrattle = Hit(ENEMY_HERO, 3)


class CS3_014:
    """Crimson Clergy"""

    # After a friendly character is healed, gain +1 Attack.
    events = Heal(FRIENDLY_CHARACTERS).after(Buff(SELF, "CS3_014e"))


CS3_014e = buff(atk=1)


##
# Spells


class CS3_027:
    """Focused Will"""

    # <b>Silence</b> a minion, then give it +3 Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Silence(TARGET), Buff(TARGET, "CS3_027e")


class CS3_028:
    """Thrive in the Shadows"""

    # <b>Discover</b> a spell from your deck.
    play = GenericChoice(CONTROLLER, DeDuplicate(RANDOM(FRIENDLY_DECK + SPELL, 3)))
