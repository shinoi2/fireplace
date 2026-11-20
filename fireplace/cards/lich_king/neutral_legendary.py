from ..utils import *

HORSEMEN_DIED = FindAll(
    *(
        FRIENDLY + DEAD_MINIONS + ID(card)
        for card in ("NX2_034", "NX2_034t", "NX2_034t1", "NX2_034t2")
    )
)

##
# Minions


class RLK_591:
    """Bonelord Frostwhisper"""

    # <b>Deathrattle:</b> For the rest of the game, your first card each turn
    # costs (0). You die in 3 turns.
    deathrattle = Buff(CONTROLLER, "RLK_591e")


class RLK_592:
    """Invincible"""

    # [x]<b>Reborn</b> <b>Battlecry and Deathrattle:</b> Give a random friendly
    # Undead +5/+5 and <b>Taunt</b>.
    play = deathrattle = Buff(
        RANDOM(FRIENDLY_MINIONS + UNDEAD - SELF - DEAD), "RLK_592e"
    ).then(Taunt(Buff.TARGET))


class RLK_593:
    """Lor'themar Theron"""

    # <b>Battlecry:</b> Double the stats of all minions in your deck.
    play = Buff(FRIENDLY_DECK + MINION, "RLK_593e")


class RLK_222:
    """Astalor Bloodsworn"""

    # <b>Battlecry:</b> Add Astalor, the Protector to your hand. <b>Manathirst
    # (@):</b> Deal 2 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MIN_MANA_CRYSTAL: 5,
        PlayReq.REQ_BATTLECRY_WITHOUT_TARGET: 0,
    }
    play = Give(CONTROLLER, "RLK_222t1"), Manathirst(5) & Hit(TARGET, 2)


class NX2_033:
    """Thaddius, Monstrosity"""

    # [x]<b>Taunt</b> Your odd-Cost cards cost (1). <i>(Swaps polarity each
    # turn!)</i>@[x]<b>Taunt</b> Your even-Cost cards cost (1). <i>(Swaps
    # polarity each turn!)</i>
    update = Refresh(
        FRIENDLY_HAND
        + FilterSelector(
            lambda card, source: getattr(card, "_cost", -1) % 2
            == len(source.controller.turns) % 2
        ),
        {GameTag.COST: SET(1)},
    )


class NX2_034:
    """Rivendare, Warrider"""

    # <b>Deathrattle:</b> Shuffle the other 3 Horsemen into your deck.
    deathrattle = (
        Shuffle(CONTROLLER, "NX2_034t"),
        Shuffle(CONTROLLER, "NX2_034t1"),
        Shuffle(CONTROLLER, "NX2_034t2"),
        HORSEMEN_DIED & Destroy(ENEMY_HERO),
    )


##
# Spells


class RLK_590:
    """The Sunwell"""

    # Fill your hand with random spells. Costs (1) less for each other card in
    # your hand.
    cost_mod = -Count(FRIENDLY_HAND - SELF)
    play = Give(CONTROLLER, RandomSpell()) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class RLK_591e:
    def apply(self, target):
        self.progress = 3
        self.start_turn = self.game.turn

    def count_turn(self, player):
        if self.game.turn == self.start_turn:
            return
        self.progress -= 1
        if not self.progress:
            return Destroy(FRIENDLY_HERO)

    update = -Find(CARDS_PLAYED_THIS_GAME + CARDS_PLAYED_THIS_TURN) & Refresh(
        FRIENDLY_HAND, {GameTag.COST: SET(0)}
    )
    events = OWN_TURN_END.on(count_turn)


RLK_592e = buff(5, 5)


class RLK_593e:
    atk = lambda self, value: value * 2
    max_health = lambda self, value: value * 2


class RLK_222t1:
    play = Give(CONTROLLER, "RLK_222t2"), Manathirst(8) & GainArmor(FRIENDLY_HERO, 5)


class RLK_222t2:
    play = Manathirst(10) & (Hit(RANDOM_ENEMY_CHARACTER, 1) * 14) | (
        Hit(RANDOM_ENEMY_CHARACTER, 1) * 7
    )


class NX2_034t:
    deathrattle = HORSEMEN_DIED & Destroy(ENEMY_HERO)


NX2_034t1 = NX2_034t2 = NX2_034t
