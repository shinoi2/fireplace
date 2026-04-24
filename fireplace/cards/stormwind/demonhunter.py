from ..utils import *

##
# Minions


class SW_037:
    """Irebound Brute"""

    # [x]<b>Taunt</b> Costs (1) less for each card drawn this turn.
    cost_mod = -Count(DRAWN_THIS_TURN)


class SW_042:
    """Persistent Peddler"""

    # <b>Tradeable</b> <b>Deathrattle:</b> Summon a Persistent Peddler from
    # your deck.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + ID("SW_042")))


class SW_043:
    """Felgorger"""

    # <b>Battlecry:</b> Draw a Fel spell. Reduce its Cost by (2).
    play = ForceDraw(RANDOM(FRIENDLY_DECK + FEL + SPELL)).then(
        Buff(ForceDraw.TARGET, "SW_043e")
    )


class SW_043e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class SW_044:
    """Jace Darkweaver"""

    # <b>Battlecry:</b> Cast all Fel spells you've played this game <i>(targets
    # enemies if possible)</i>.
    play = CastSpellTargetsEnemiesIfPossible(
        Copy(SHUFFLE(CARDS_PLAYED_THIS_GAME + FEL + SPELL))
    )


class SW_451:
    """Metamorfin"""

    # <b>Taunt</b> <b>Battlecry:</b> If you've cast a Fel spell this turn, gain
    # +2/+2.
    powered_up = Find(CARDS_PLAYED_THIS_TURN + FEL + SPELL)
    play = powered_up & Buff(SELF, "SW_451e")


SW_451e = buff(+2, +2)


class DED_507:
    """Crow's Nest Lookout"""

    # [x]<b>Battlecry:</b> Deal 2 damage to the left and right-most enemy
    # minions.
    play = Hit(LEFTMOST(ENEMY_MINIONS), 2), Hit(RIGHTMOST(ENEMY_MINIONS), 2)


##
# Spells


class SW_039:
    """Final Showdown"""

    # <b>Questline:</b> Draw 4 cards in one turn. <b>Reward:</b> Reduce the
    # Cost of the cards drawn by (1).
    quest = (
        Draw(CONTROLLER).on(AddProgress(SELF, 1)),
        OWN_TURN_END.on(ClearProgress(SELF)),
    )
    reward = (
        Buff(DRAWN_THIS_TURN[-CURRENT_PROGRESS(SELF) :] + FRIENDLY_HAND, "SW_039te"),
        Summon(CONTROLLER, "SW_039t"),
    )


class SW_039t:
    """Gain Momentum"""

    # <b>Questline:</b> Draw 5 cards in one turn. <b>Reward:</b> Reduce the
    # Cost of the cards drawn by (1).
    quest = (
        Draw(CONTROLLER).on(AddProgress(SELF, 1)),
        OWN_TURN_END.on(ClearProgress(SELF)),
    )
    reward = (
        Buff(DRAWN_THIS_TURN[-CURRENT_PROGRESS(SELF) :] + FRIENDLY_HAND, "SW_039te"),
        Summon(CONTROLLER, "SW_039t3"),
    )


class SW_039t3(QuestRewardProtect):
    """Close the Portal"""

    # <b>Questline:</b> Draw 5 cards in one turn. <b>Reward:</b> Demonslayer
    # Kurtrus.
    quest = (
        Draw(CONTROLLER).on(AddProgress(SELF, 1)),
        OWN_TURN_END.on(ClearProgress(SELF)),
    )
    reward = Give(CONTROLLER, "SW_039t3_t")


class SW_039te:
    """Fast Moves"""

    # Costs (1) less.
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class SW_039t3_t:
    """Demonslayer Kurtrus"""

    # <b>Battlecry:</b> For the rest of the game, cards you draw cost (2) less.
    play = Buff(CONTROLLER, "SW_039t2e")


class SW_039t2e:
    """Faster Moves"""

    # Costs (2) less.
    events = Draw(CONTROLLER).on(Buff(Draw.TARGET, "SW_039t3_te"))


class SW_039t3_te:
    """Ludicrous Speed"""

    # Costs (2) less.
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class SW_040:
    """Fel Barrage"""

    # [x]Deal $2 damage to the lowest Health enemy, twice.
    play = Hit(RANDOM(LOWEST_HEALTH(ENEMY_MINIONS)), 2) * 2


class SW_041:
    """Sigil of Alacrity"""

    # [x]At the start of your next turn, draw a card and _reduce its Cost by
    # (1).
    events = OWN_TURN_BEGIN.on(Draw(CONTROLLER).then(Buff(Draw.TARGET, "SW_041e2")))


class SW_041e2:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class SW_452:
    """Chaos Leech"""

    # <b>Lifesteal</b>. Deal $3 damage to a minion. <b>Outcast:</b> Deal $5
    # instead.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)
    outcast = Hit(TARGET, 5)


class DED_506:
    """Need for Greed"""

    # <b>Tradeable</b> Draw 3 cards. If drawn this turn, this costs (3).
    update = Find(DRAWN_THIS_TURN + SELF) & Refresh(SELF, {GameTag.COST: 3})
    play = Draw(CONTROLLER) * 3


class DED_508:
    """Proving Grounds"""

    # Summon two minions from your deck. They fight!
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Attack(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
    )


##
# Weapons


class SW_454:
    """Lion's Frenzy"""

    # Has Attack equal to the number of cards you've drawn this turn.
    update = Refresh(SELF, {GameTag.ATK: Count(DRAWN_THIS_TURN)})
