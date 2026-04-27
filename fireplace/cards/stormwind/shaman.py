from ..utils import *

##
# Minions


class SW_026:
    """Spirit Alpha"""

    # [x]After you play a card with <b>Overload</b>, summon a 2/3 Spirit Wolf
    # with <b>Taunt</b>.
    events = Play(CONTROLLER, OVERLOAD).after(Summon(CONTROLLER, "DRG_217t"))


class SW_032:
    """Granite Forgeborn"""

    # <b>Battlecry:</b> Reduce the cost of Elementals in your hand and deck by
    # (1).
    play = Buff((FRIENDLY_HAND | FRIENDLY_DECK) + ELEMENTAL, "SW_032e")


class SW_032e:
    tag = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class SW_115:
    """Bolner Hammerbeak"""

    # [x]After you play a <b>Battlecry</b> minion, repeat the first
    # __<b>Battlecry</b> played this turn._
    events = Play(CONTROLLER, BATTLECRY + MINION).after(
        ExtraBattlecry((CARDS_PLAYED_THIS_TURN + BATTLECRY)[:1], None)
    )


class DED_509:
    """Brilliant Macaw"""

    # <b>Battlecry:</b> Repeat the last <b>Battlecry</b> you played.
    def play(self):
        if getattr(self, "_last_card", None) is None:
            self._last_card = ((CARDS_PLAYED_THIS_GAME + BATTLECRY)[-1:]).eval(
                self.game, self
            )
        yield ExtraBattlecry(self._last_card, None)


class DED_511:
    """Suckerhook"""

    # [x]At the end of your turn, transform your weapon into one that costs (1)
    # more.
    events = OWN_TURN_END.on(Evolve(FRIENDLY_WEAPON, 1))


class DED_522:
    """Cookie the Cook"""

    # [x]<b>Lifesteal</b> <b>Deathrattle:</b> Equip a 2/3 __Stirring Rod with
    # <b>Lifesteal</b>._
    deathrattle = Summon(CONTROLLER, "DED_522t")


##
# Spells


class SW_031:
    """Command the Elements"""

    # [x]<b>Questline:</b> Play 3 cards with <b>Overload</b>. <b>Reward:</b>
    # Unlock your <b>Overloaded</b> Mana Crystals.
    quest = Play(CONTROLLER, OVERLOAD).after(AddProgress(SELF, Play.CARD))
    reward = UnlockOverload(CONTROLLER), Summon(CONTROLLER, "SW_031t")


class SW_031t:
    """Stir the Stones"""

    # [x]<b>Questline:</b> Play 3 cards with <b>Overload</b>. <b>Reward:</b>
    # Summon a 3/3 Elemental with <b>Taunt</b>.
    quest = Play(CONTROLLER, OVERLOAD).after(AddProgress(SELF, Play.CARD))
    reward = Summon(CONTROLLER, "SW_031t8"), Summon(CONTROLLER, "SW_031t2")


class SW_031t2(QuestRewardProtect):
    """Tame the Flames"""

    # [x]<b>Questline:</b> Play 3 cards with <b>Overload</b>. <b>Reward:</b>
    # Stormcaller Bru'kan.
    quest = Play(CONTROLLER, OVERLOAD).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "SW_031t7")


class SW_031t7:
    """Stormcaller Bru'kan"""

    # [x]<b>Battlecry:</b> For the rest of the game, your spells cast twice.
    play = Buff(CONTROLLER, "SW_031t7e")


SW_031t7e = buff(spells_cast_twice=True)


class SW_034:
    """Tiny Toys"""

    # Summon four random 5-Cost minions. Make them 2/2.
    play = (
        Summon(CONTROLLER, RandomMinion(cost=5)).then(Buff(Summon.CARD, "SW_034e")) * 4
    )


class SW_034e:
    atk = SET(2)
    max_health = SET(2)


class SW_035:
    """Charged Call"""

    # [x]<b>Discover</b> a @-Cost minion and summon it. <i>(Upgraded for each
    # <b>Overload</b> card you played this game!)</i>
    play = DISCOVER(
        RandomCollectible(cost=(Count(CARDS_PLAYED_THIS_GAME + OVERLOAD) + 1))
    )


class SW_114:
    """Overdraft"""

    # [x]<b>Tradeable</b> Unlock your <b>Overloaded</b> Mana Crystals to deal
    # that much damage.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = (
        Hit(TARGET, OVERLOAD_LOCKED(CONTROLLER) + OVERLOAD_OWED(CONTROLLER)),
        UnlockOverload(CONTROLLER),
    )


class SW_095:
    """Investment Opportunity"""

    # [x]Draw an <b>Overload</b> card.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + OVERLOAD))


##
# Weapons


class SW_025:
    """Auctionhouse Gavel"""

    # [x]After your hero attacks, reduce the Cost of a <b>Battlecry</b> minion
    # in your hand by (1).
    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_HAND + BATTLECRY + MINION), "SW_025e")
    )


class SW_025e:
    tag = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY
