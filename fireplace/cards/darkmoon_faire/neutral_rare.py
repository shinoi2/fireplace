from ..utils import *


##
# Minions


class DMF_081:
    """K'thir Ritualist"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Add a random 4-Cost minion to your
    # opponent's hand.
    play = Give(OPPONENT, RandomMinion(cost=4))


class DMF_125:
    """Safety Inspector"""

    # [x]<b>Battlecry:</b> Shuffle the _lowest-Cost card from your hand into
    # your deck. Draw a card.
    play = (
        Shuffle(CONTROLLER, RANDOM(LOWEST_COST(FRIENDLY_HAND))),
        Draw(CONTROLLER),
    )


class DMF_202:
    """Derailed Coaster"""

    # <b>Battlecry:</b> Summon a 1/1 Rider with <b>Rush</b> for each minion in
    # your hand.
    play = Summon(CONTROLLER, "DMF_523t") * Count(FRIENDLY_HAND)


class YOP_032:
    """Armor Vendor"""

    # <b>Battlecry:</b> Give 4 Armor to_each hero.
    play = GainArmor(FRIENDLY_HERO, 4), GainArmor(ENEMY_HERO, 4)


class YOP_034:
    """Runaway Blackwing"""

    # [x]At the end of your turn, deal 9 damage to a random enemy minion.
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_MINION, 9))
