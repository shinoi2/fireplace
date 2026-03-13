from ..utils import *

##
# Minions


class DMF_070:
    """Darkmoon Rabbit"""

    # <b>Rush</b>, <b>Poisonous</b> Also damages the minions next to whomever
    # this attacks.
    events = Attack(SELF).on(CLEAVE)


class DMF_124:
    """Horrendous Growth"""

    # <b>Corrupt:</b> Gain +1/+1. Can be <b>Corrupted</b> endlessly.
    corrupt_card = "DMF_124t"


class DMF_124t:
    def corrupt_card(self):
        card = self.controller.card("DMF_124t")
        card.custom_card = True
        if hasattr(self, "_corrupted_times"):
            card._corrupted_times = self._corrupted_times + 1
        else:
            card._corrupted_times = 1
        atk = card.atk + card._corrupted_times
        max_health = card.max_health + card._corrupted_times

        def create_custom_card(card):
            card.atk = atk
            card.max_health = max_health

        card.create_custom_card = create_custom_card
        card.create_custom_card(card)
        copy_buffs(self.controller, self, card)
        return card


class DMF_163:
    """Carnival Clown"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Summon 2 copies of this.
    # <b>Corrupt:</b> Fill your board with copies.
    play = SummonBothSides(CONTROLLER, ExactCopy(SELF)) * 2
    corrupt_card = "DMF_163t"


class DMF_163t:
    play = SummonBothSides(CONTROLLER, ExactCopy(SELF)) * 7


class YOP_012:
    """Deathwarden"""

    # <b>Deathrattles</b> can't trigger.
    update = Refresh(PLAYER, {GameTag.CANT_TRIGGER_DEATHRATTLE: True})
