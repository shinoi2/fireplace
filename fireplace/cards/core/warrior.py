from ..utils import *

##
# Minions


class CS3_008:
    """Bloodsail Deckhand"""

    # [x]<b>Battlecry:</b> The next weapon you play costs (1) less.
    play = Buff(CONTROLLER, "CS3_008e")


class CS3_008e:
    update = Refresh(FRIENDLY_HAND + WEAPON, {GameTag.COST: -1})
    events = Play(CONTROLLER, WEAPON).after(Destroy(SELF))


##
# Spells


class CS3_009:
    """War Cache"""

    # Add a random Warrior minion, spell, and weapon to your hand.
    play = (
        Give(CONTROLLER, RandomMinion(card_class=CardClass.WARRIOR)),
        Give(CONTROLLER, RandomSpell(card_class=CardClass.WARRIOR)),
        Give(CONTROLLER, RandomWeapon(card_class=CardClass.WARRIOR)),
    )
