from ..utils import *

##
# Minions


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


class SW_045:
    """Auctioneer Jaxon"""

    # [x]Whenever you <b>Trade</b>, <b>Discover</b> a card from your _deck to
    # draw instead.
    events = Trade(FRIENDLY).on(
        Choice(RANDOM(FRIENDLY_DECK, 3)).then(PutOnTop(Choice.CARD))
    )


class SW_078:
    """Lady Prestor"""

    # [x]<b>Battlecry:</b> Transform minions in your deck into random Dragons.
    # <i>(They keep their __original stats and Cost.)</I>
    def play(self):
        for minion in (FRIENDLY_DECK + MINION).eval(self.game, self):
            cost = minion.cost
            atk = minion.atk
            health = minion.health
            yield Morph(minion, RandomDragon()).then(
                SetStateBuff(Morph.CARD, Morph.TARGET, "SW_078e"),
                SetStateBuff(Morph.CARD, Morph.TARGET, "SW_078e2"),
            )


class SW_078e:
    atk = lambda self, _: self._xatk
    max_health = lambda self, _: self._xhealth


class SW_078e2:
    events = REMOVED_IN_PLAY
    cost = lambda self, _: self._xcost


class SW_080:
    """Cornelius Roame"""

    # [x]At the start and end _of each player's turn, draw a card.
    events = (TURN_BEGIN.on(Draw(CONTROLLER)), TURN_END.on(Draw(CONTROLLER)))


class SW_081:
    """Varian, King of Stormwind"""

    # [x]<b>Battlecry:</b> Draw a <b>Rush</b> minion to gain <b>Rush</b>.
    # Repeat for <b>Taunt</b> and <b>Divine Shield</b>.
    play = (
        Find(FRIENDLY_DECK + RUSH)
        & (ForceDraw(RANDOM(FRIENDLY_DECK + RUSH)), GiveRush(SELF)),
        Find(FRIENDLY_DECK + TAUNT)
        & (ForceDraw(RANDOM(FRIENDLY_DECK + TAUNT)), Taunt(SELF)),
        Find(FRIENDLY_DECK + DIVINE_SHIELD)
        & (ForceDraw(RANDOM(FRIENDLY_DECK + DIVINE_SHIELD)), GiveDivineShield(SELF)),
    )


class DED_006:
    """Mr. Smite"""

    # Your Pirates have <b>Charge</b>.
    update = Refresh(FRIENDLY_MINIONS + PIRATE, buff="DED_006e2")


DED_006e2 = buff(charge=True)


class DED_525:
    """Goliath, Sneed's Masterpiece"""

    # [x]<b>Battlecry:</b> Fire five rockets at enemy minions that deal 2
    # damage each. <i>(You pick the targets!)</i>
    play = ChoiceTarget(CONTROLLER, ENEMY_MINIONS).then(Hit(ChoiceTarget.CARD, 2)) * 5
