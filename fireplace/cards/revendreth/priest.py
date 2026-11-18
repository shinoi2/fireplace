from ..utils import *

##
# Minions


class REV_002:
    """Suspicious Usher"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a <b>Legendary</b> minion. If your
    # opponent guesses your __choice, they get a copy.
    play = suspicious_discover(RandomMinion(rarity=Rarity.LEGENDARY))


class REV_246:
    """Mysterious Visitor"""

    # <b>Battlecry:</b> Reduce the Cost of cards copied from your opponent by
    # (2).
    play = Buff(FRIENDLY_HAND + COPIED_FROM_OPPONENT, "REV_246e2")


class REV_247:
    """Partner in Crime"""

    # [x]<b>Battlecry:</b> Summon a copy of this minion at the end of your
    # turn.
    play = Buff(SELF, "REV_247e")


class REV_250:
    """Pelagos"""

    # [x]After you cast a spell on a friendly minion, set its Attack and Health
    # to the higher of the two.
    def equalize(self, player, card, target):
        if (
            target is not None
            and target.type == CardType.MINION
            and target.controller is self.controller
            and target.zone == Zone.PLAY
        ):
            value = max(target.atk, target.health)
            yield SetStats(target, "REV_250e1", value, value)

    events = Play(CONTROLLER, SPELL).after(equalize)


class REV_011:
    """The Harvester of Envy"""

    # After you play a card copied from the opponent, steal the original.
    def steal_original(self, player, card, target):
        original = getattr(card, "copied_from", None)
        while original is not None and getattr(original, "morphed", None) is not None:
            original = original.morphed
        if (
            original is not None
            and original.controller is self.controller.opponent
            and original.zone in (Zone.HAND, Zone.DECK, Zone.PLAY)
        ):
            yield Steal(original)

    events = Play(CONTROLLER, COPIED_FROM_OPPONENT).after(steal_original)


class MAW_022:
    """Incriminating Psychic"""

    # <b>Taunt</b> <b>Deathrattle:</b> Copy a random card from your opponent's
    # hand.
    deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_HAND)))


##
# Spells


class REV_248:
    """Boon of the Ascended"""

    # Give a minion +2 Health. Summon a Kyrian with its stats and <b>Taunt</b>.
    requirements = MINION_TARGET
    play = Buff(TARGET, "REV_248e"), Summon(CONTROLLER, "REV_248t").then(
        SetStats(Summon.CARD, "REV_250e1", ATK(TARGET), CURRENT_HEALTH(TARGET))
    )


class REV_249:
    """The Light! It Burns!"""

    # [x]Deal damage to a minion equal to its Attack.
    requirements = MINION_TARGET
    play = Hit(TARGET, ATK(TARGET))


class REV_253:
    """Identity Theft"""

    # <b>Discover</b> a copy of a card from your opponent's hand and deck.
    play = (
        Choice(CONTROLLER, ExactCopy(RANDOM(DeDuplicate(ENEMY_HAND), 3))).then(
            Give(CONTROLLER, Choice.CARD)
        ),
        Choice(CONTROLLER, Copy(RANDOM(DeDuplicate(ENEMY_DECK), 3))).then(
            Give(CONTROLLER, Choice.CARD)
        ),
    )


class REV_252:
    """Clean the Scene"""

    # Destroy all minions with 3 or less Attack. <b>Infuse (@):</b> 6 or less.
    infuse_card = "REV_252t"
    play = Destroy(ALL_MINIONS + (ATK <= 3))


class MAW_021:
    """Clear Conscience"""

    # [x]Give a friendly minion +2/+3 and "Only you can target this with spells
    # and Hero Powers."
    requirements = FRIENDLY_MINION_TARGET
    play = Buff(TARGET, "MAW_021e")


class MAW_023:
    """Theft Accusation"""

    # [x]Choose a minion. Destroy it after you play a card copied from the
    # opponent.
    requirements = MINION_TARGET
    play = Buff(TARGET, "MAW_023e2")


##
# Locations


class REV_290:
    """Cathedral of Atonement"""

    # Give a minion +2/+1 and draw a card.
    requirements = MINION_TARGET
    activate = Buff(TARGET, "REV_290e"), Draw(CONTROLLER)


REV_246e2 = cost_buff(cost=-2)
REV_248e = buff(health=2)
REV_250e1 = FixedStats
REV_290e = buff(+2, +1)


class REV_247e:
    events = OWN_TURN_END.on(Destroy(SELF), Summon(CONTROLLER, ExactCopy(OWNER)))


class REV_252t:
    play = Destroy(ALL_MINIONS + (ATK <= 6))


class MAW_021e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 3,
        enums.CANT_BE_TARGETED_BY_OPPONENT_ABILITIES: True,
        GameTag.CANT_BE_TARGETED_BY_SPELLS: False,
        GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: False,
    }


class MAW_023e2:
    events = Play(CONTROLLER, COPIED_FROM_OPPONENT).after(Destroy(OWNER))
