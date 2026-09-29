"""
Monster Smash

The heroes of the brawl (TB_BountyHunt_*) are the bosses of the Monster Hunt
of The Witchwood; each one's HERO_POWER in CardDefs.xml names its power, most
of them the boss's own (GILA_BOSS_*p), and its deck plays cards of that boss.
"""

from ..utils import *


class ShuffleHandAndDraw(TargetedAction):
    """
    Player targets shuffle their hand into their deck and draw that many
    cards.
    """

    TARGET = ActionArg()

    def do(self, source, target):
        hand = list(target.hand)
        if not hand:
            return
        source.game.queue_actions(source, [Shuffle(target, hand)])
        source.game.queue_actions(source, [Draw(target) * len(hand)])


class AttackRandomEnemyMinions(TargetedAction):
    """
    Each minion in play (in the order they came into play) attacks a random
    minion of its opponent, if it has one.
    """

    TARGET = ActionArg()

    def do(self, source, target):
        for minion in list(source.game.board):
            if minion.zone != Zone.PLAY or minion.dead or minion.dormant:
                continue
            enemies = [
                m
                for m in minion.controller.opponent.field
                if not m.dead and not m.dormant
            ]
            if not enemies:
                continue
            defender = source.game.random.choice(enemies)
            source.game.queue_actions(source, [Attack(minion, defender)])


class DestroyWispsAndSteal(TargetedAction):
    """
    Soul Assimilation: destroy the Wisps of player targets, then take control
    of a random enemy minion for each (as many as the board takes).
    """

    TARGET = ActionArg()

    def do(self, source, target):
        wisps = [m for m in target.field if m.name_enUS == "Wisp" and not m.dead]
        if not wisps:
            return
        source.game.queue_actions(source, [Destroy(w) for w in wisps])
        source.game.process_deaths()
        for _ in wisps:
            enemies = [m for m in target.opponent.field if not m.dead and not m.dormant]
            if not enemies or len(target.field) >= source.game.MAX_MINIONS_ON_FIELD:
                break
            source.game.queue_actions(source, [Steal(source.game.random.choice(enemies))])


class Amalgamate(TargetedAction):
    """
    Destroy all minions, then summon for player targets an Amalgamation with
    their combined Attack and Health.
    """

    TARGET = ActionArg()

    def do(self, source, target):
        minions = [m for m in source.game.board if not m.dormant]
        atk = sum(m.atk for m in minions)
        health = sum(max(0, m.health) for m in minions)
        source.game.queue_actions(source, [Destroy(m) for m in minions])
        source.game.process_deaths()
        card = target.card("GILA_BOSS_27t2", source=source)
        # Its own Attack and Health: the combined ones (at least 1 Health).
        card.atk = atk
        card.max_health = max(1, health)
        source.game.queue_actions(source, [Summon(target, card)])


##
# Hero powers


class TB_Chupacabran_HP:
    """Bloodthirst"""

    # Hero Power: Give a friendly minion +1/+1 and Lifesteal.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    activate = Buff(TARGET, "TB_Chupacabran_HP_E")


TB_Chupacabran_HP_E = buff(+1, +1, lifesteal=True)


class GILA_BOSS_64p:
    """Hypnotize"""

    # Hero Power: Each player shuffles their hand into their deck and draws
    # that many cards.
    activate = ShuffleHandAndDraw(ALL_PLAYERS)


class TB_BountyHunt_Hypnotize(GILA_BOSS_64p):
    """Hypnotize (Tavern Brawl)"""


class GILA_BOSS_27p:
    """Consume"""

    # Hero Power: Destroy a friendly minion, then draw 3 cards.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    activate = Destroy(TARGET), Draw(CONTROLLER) * 3


class TB_BountyHunt_Consume(GILA_BOSS_27p):
    """Consume (Tavern Brawl)"""


class GILA_BOSS_37p:
    """It's Raining Fin"""

    # Hero Power: Draw 3 Murlocs from your deck.
    activate = ForceDraw(RANDOM(FRIENDLY_DECK + MURLOC)) * 3


class GILA_BOSS_55p:
    """Unfinished Business"""

    # Hero Power: Summon three 1/1 Wisps.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "GILA_BOSS_55t") * 3


class GILA_BOSS_30p:
    """Blood Red Apple"""

    # Passive Hero Power: Spells cost Health instead of Mana.
    update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class GILA_BOSS_47p:
    """Frumiousity"""

    # Passive Hero Power: All Battlecries trigger twice. All: those of both
    # players, as Brann Bronzebeard does for his own.
    update = Refresh(ALL_PLAYERS, {enums.EXTRA_BATTLECRIES: True})


class GILA_BOSS_68p:
    """Poison Flask"""

    # Hero Power: Deal 2 damage to a minion. If it survives, give it
    # Poisonous.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    activate = Hit(TARGET, 2), Dead(TARGET) | Buff(TARGET, "GILA_BOSS_68e")


GILA_BOSS_68e = buff(poisonous=True)


class GILA_BOSS_41p:
    """Survival of the Fittest"""

    # Hero Power: All minions attack random enemy minions. (The power of
    # Brushwood Centurion, TB_BountyHunt_Brushwood, by its HERO_POWER; the
    # wiki calls it "Axe Around", and "Survival of the Fittest!" is what he
    # says when he uses it.)
    activate = AttackRandomEnemyMinions(CONTROLLER)


##
# The cards of the bosses' decks


class GILA_BOSS_27t:
    """Amalgamate"""

    # Destroy all minions. Summon an Amalgamation with the combined Attack and
    # Health.
    play = Amalgamate(CONTROLLER)


class GILA_BOSS_41t:
    """Hack"""

    # Deal $1 damage to a minion. Then do it four more times.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Hit(TARGET, 1) * 5


class GILA_BOSS_55t2:
    """Soul Assimilation"""

    # Destroy your Wisps. Gain control of a random enemy minion for each Wisp
    # destroyed.
    play = DestroyWispsAndSteal(CONTROLLER)


class GILA_BOSS_68t:
    """Infected Quillflinger"""

    # Whenever this minion takes damage, deal 1 damage to a random enemy
    # minion.
    events = SELF_DAMAGE.on(Hit(RANDOM_ENEMY_MINION, 1))


class GILA_BOSS_99t:
    """Witchwood's Touch"""

    # Draw a card. Gain 6 Armor.
    play = Draw(CONTROLLER), GainArmor(FRIENDLY_HERO, 6)
