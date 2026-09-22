from ..utils import *

##
# Minions


class AV_201:
    """Coldtooth Yeti"""

    # <b>Combo:</b> Gain +3 Attack.
    combo = Buff(SELF, "AV_201e")


AV_201e = buff(atk=3)


class AV_711:
    """Double Agent"""

    # [x]<b>Battlecry:</b> If you're holding a card from another class, _summon
    # a copy of this.
    powered_up = Find(FRIENDLY_HAND + ANOTHER_CLASS)
    play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


class AV_298:
    """Wildpaw Gnoll"""

    # [x]<b>Rush</b> Costs (1) less for each card you've added to your hand
    # _from another class.
    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + ANOTHER_CLASS)


class AV_403:
    """Cera'thine Fleetrunner"""

    # [x]<b>Battlecry:</b> Replace your minions in hand and deck with ones from
    # other classes. They cost (2) less.
    play = Morph(
        (FRIENDLY_HAND | FRIENDLY_DECK) + MINION, RandomMinion(card_class=ANOTHER_CLASS)
    )


class ONY_030:
    """SI:7 Smuggler"""

    # [x]<b>Battlecry:</b> Summon a random @-Cost minion. <i>(Upgraded for each
    # other SI:7 card you _have played this game.)</i>
    play = Summon(
        CONTROLLER, RandomMinion(cost=Min(Count(CARDS_PLAYED_THIS_GAME + SI_7) + 1, 10))
    )


class AV_601:
    """Forsaken Lieutenant"""

    # <b><b>Stealth</b>.</b> After you play a <b>Deathrattle</b> minion, become
    # a 2/2 copy of it with <b>Rush</b>.
    events = Play(FRIENDLY + MINION + DEATHRATTLE).after(
        Morph(SELF, ExactCopy(Play.CARD)).then(Buff(Morph.CARD, "AV_601e"))
    )


class AV_601e:
    atk = SET(2)
    max_health = SET(2)


##
# Spells


class AV_710:
    """Reconnaissance"""

    # <b>Discover</b> a <b>Deathrattle</b> minion from another class. It costs
    # (2) less.
    play = Discover(CONTROLLER, RandomMinion(card_class=ANOTHER_CLASS)).then(
        Give(CONTROLLER, Discover.CARD), Buff(Discover.CARD, "AV_710e")
    )


class AV_710e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class AV_400:
    """Snowfall Graveyard"""

    # [x]Your <b>Deathrattles</b> trigger twice. Lasts 3 turns.
    update = Refresh(CONTROLLER, {GameTag.EXTRA_DEATHRATTLES: True})


class AV_405:
    """Contraband Stash"""

    # Replay 5 cards from other classes you've played this game.
    play = Replay(RANDOM(CARDS_PLAYED_THIS_GAME + ANOTHER_CLASS, 5))


class ONY_032:
    """Tooth of Nefarian"""

    # [x]Deal $3 damage. <b>Honorable Kill:</b> <b>Discover</b> a spell from
    # another class.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)
    honorable_kill = DISCOVER(RandomSpell(card_class=ANOTHER_CLASS))


class ONY_031:
    """Smokescreen"""

    # [x]Draw 5 cards. Trigger any <b>Deathrattles</b> drawn.
    play = Draw(CONTROLLER).then(Deathrattle(Draw.CARD)) * 5


##
# Weapons


class AV_402:
    """The Lobotomizer"""

    # [x]<b>Honorable Kill:</b> Get a copy of the top card of your opponent's
    # deck.
    honorable_kill = Give(CONTROLLER, Copy(ENEMY_DECK[-1:]))


##
# Heros


class AV_203:
    """Shadowcrafter Scabbs"""

    # [x]<b>Battlecry:</b> Return all minions to their owner's hands. Summon
    # two 4/2 Shadows with <b>Stealth</b>.
    play = Bounce(ALL_MINIONS), (Summon(CONTROLLER, "AV_203t") * 2)


class AV_203p:
    """Sleight of Hand"""

    # [x]<b>Hero Power</b> The next card you play this turn costs (2) less.
    activate = Buff(CONTROLLER, "AV_203po")


class AV_203pe:
    """Sleight of Hand"""

    # The next card you play this turn costs (2) less.
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class AV_203po:
    """Sleight of Hand"""

    # The next card you play this turn costs (2) less.
    update = Refresh(FRIENDLY_HAND, buff="AV_203pe")
    events = Play(CONTROLLER).after(Destroy(SELF))
