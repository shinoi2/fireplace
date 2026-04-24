from ..utils import *

##
# Minions


class SW_084:
    """Bloodbound Imp"""

    # Whenever this attacks, deal 2 damage to your_hero.
    events = Attack(SELF).after(Hit(FRIENDLY_HERO, 2))


class SW_086:
    """Shady Bartender"""

    # <b>Tradeable</b> <b>Battlecry:</b> Give your Demons +2/+2.
    play = Buff(FRIENDLY_MINIONS + DEMON, "SW_086e")


SW_086e = buff(+2, +2)


class SW_089:
    """Entitled Customer"""

    # <b>Battlecry:</b> Deal damage equal to your hand size to all other
    # minions.
    play = Hit(ALL_MINIONS - SELF, Count(FRIENDLY_HAND))


class SW_092:
    """Anetheron"""

    # [x]Costs (1) if your hand is full.
    update = FULL_HAND & Refresh(SELF, {GameTag.COST: SET(1)})


class DED_503:
    """Shadowblade Slinger"""

    # [x]<b>Battlecry:</b> If you've taken damage this turn, deal that _much to
    # an enemy minion.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_HERO_DAMAGED_THIS_TURN: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, DAMAGED_THIS_TURN(FRIENDLY_HERO))


class DED_505:
    """Hullbreaker"""

    # [x]<b>Battlecry and Deathrattle:</b> Draw a spell. Your hero takes damage
    # equal to its Cost.
    play = deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)).then(
        Hit(FRIENDLY_HERO, COST(ForceDraw.TARGET))
    )


##
# Spells


class SW_085:
    """Dark Alley Pact"""

    # [x]Summon a Fiend with stats equal to your hand size.
    play = SummonCustomMinion(
        CONTROLLER,
        "SW_085t",
        Count(FRIENDLY_HAND),
        Count(FRIENDLY_HAND),
        Count(FRIENDLY_HAND),
    )


class SW_087:
    """Dreaded Mount"""

    # [x]Give a minion +1/+1. When it dies, summon an endless Dreadsteed.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "SW_087e")


class SW_087e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.DEATHRATTLE: 1,
    }
    deathrattle = Summon(CONTROLLER, "SW_087t")


class SW_087t:
    deathrattle = Buff(CONTROLLER, "SW_087e2")


class SW_087e2:
    events = OWN_TURN_END.on(
        Summon(CONTROLLER, "SW_087t"),
        Destroy(SELF),
    )


class SW_088:
    """Demonic Assault"""

    # [x]Deal $3 damage. Summon two 1/3 Voidwalkers with <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 3), (Summon(CONTROLLER, "CS2_065") * 2)


class SW_090:
    """Touch of the Nathrezim"""

    # [x]Deal $2 damage to a minion. If it dies, restore 4 Health to your hero.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), Dead(TARGET) & Heal(FRIENDLY_HERO, 4)


class SW_091:
    """The Demon Seed"""

    # [x]<b>Questline:</b> Take 8 damage on your turns. <b>Reward:</b>
    # <b>Lifesteal</b>. Deal $3 damage to the enemy hero.
    quest = Damage(FRIENDLY_HERO).after(
        CurrentPlayer(OWNER) & AddProgress(SELF, SELF, Damage.AMOUNT)
    )
    reward = Hit(ENEMY_HERO, 3), Summon(CONTROLLER, "SW_091t")


class SW_091t:
    """Establish the Link"""

    # [x]<b>Questline:</b> Take 8 damage on your turns. <b>Reward:</b>
    # <b>Lifesteal</b>. Deal $3 damage to the enemy hero.
    quest = Damage(FRIENDLY_HERO).after(
        CurrentPlayer(OWNER) & AddProgress(SELF, SELF, Damage.AMOUNT)
    )
    reward = Hit(ENEMY_HERO, 3), Summon(CONTROLLER, "SW_091t")


class SW_091t3(QuestRewardProtect):
    """Complete the Ritual"""

    # [x]<b>Questline:</b> Take 8 damage on your turns. <b>Reward:</b>
    # Blightborn Tamsin.
    quest = Damage(FRIENDLY_HERO).after(
        CurrentPlayer(OWNER) & AddProgress(SELF, SELF, Damage.AMOUNT)
    )
    reward = Give(CONTROLLER, "SW_091t4")


class SW_091t4:
    """Blightborn Tamsin"""

    # [x]<b>Battlecry:</b> For the rest of the game, damage you take on your
    # turn damages your __opponent instead.
    play = Buff(CONTROLLER, "SW_091t5")


class SW_091t5:
    events = Predamage(FRIENDLY_HERO).on(
        CurrentPlayer(OWNER) & (Predamage(FRIENDLY_HERO, 0), Hit(ENEMY_HERO, 1))
    )


class DED_504:
    """Wicked Shipment"""

    # [x]<b>Tradeable</b> Summon @ 1/1 |4(Imp, Imps). <i>(Upgrades by 2 when
    # <b>Traded</b>!)</i>
    trade = AddProgress(SELF, SELF, 2)
    play = Summon(CONTROLLER, "DED_504t") * (CURRENT_PROGRESS(SELF) + 1)


##
# Weapons


class SW_003:
    """Runed Mithril Rod"""

    # [x]After you draw 4 cards, reduce the Cost of cards in your hand by (1).
    # Lose 1 Durability.
    progress_total = 4
    events = Draw(CONTROLLER).after(AddProgress(SELF))
    reward = Buff(FRIENDLY_HAND, "SW_003e"), Hit(SELF, 1)


class SW_003e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY
