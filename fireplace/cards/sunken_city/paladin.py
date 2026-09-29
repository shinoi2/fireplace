from ..utils import *

##
# Minions


class TSC_030:
    """The Leviathan"""

    # [x]<b>Colossal +1</b> <b>Rush</b>, <b>Divine Shield</b> After this
    # attacks, <b>Dredge</b>.
    colossal = Summon(CONTROLLER, "TSC_030t2")
    events = Attack(SELF).after(Dredge(CONTROLLER))


class TSC_030t2:
    """The Leviathan's Claw"""

    # [x]<b>Rush</b>, <b>Divine Shield</b> After this attacks, draw a card.
    events = Attack(SELF).after(Draw(CONTROLLER))


class TSC_644:
    """Azsharan Mooncatcher"""

    # [x]<b>Divine Shield</b>. <b>Battlecry:</b> Put a 'Sunken Mooncatcher' on
    # the bottom of your deck.
    play = PutOnBottom(CONTROLLER, "TSC_644t")


class TSC_644t:
    """Sunken Mooncatcher"""

    # <b>Divine Shield</b>. <b>Battlecry:</b> Summon a copy of this.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class TID_098:
    """Myrmidon"""

    # After you cast a spell on this minion, draw a card.
    events = Play(CONTROLLER, SPELL, SELF).after(Draw(CONTROLLER))


class TSC_059:
    """Bubblebot"""

    # [x]<b>Battlecry:</b> Give your other Mechs <b>Divine Shield</b> and
    # <b>Taunt</b>.
    play = GiveDivineShield(FRIENDLY_MINIONS + MECH - SELF), Taunt(
        FRIENDLY_MINIONS + MECH - SELF
    )


class TSC_060:
    """Shimmering Sunfish"""

    # <b>Battlecry:</b> If you're holding a Holy Spell, gain <b>Taunt</b> and
    # <b>Divine Shield</b>.
    powered_up = Find(FRIENDLY_HAND + HOLY)
    play = powered_up & (Taunt(SELF), GiveDivineShield(SELF))


class TID_077:
    """Lightray"""

    # <b>Taunt</b> Costs (1) less for each Paladin card you've played this
    # game.
    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + PALADIN)


class TSC_083:
    """Seafloor Savior"""

    # [x]<b>Battlecry:</b> <b>Dredge</b>. If it's a minion, give it this
    # minion's Attack and Health.
    play = Dredge(CONTROLLER).then(
        Find(Dredge.CARD + MINION)
        & (
            Buff(
                SELF,
                "TSC_083e",
                atk=ATK(Dredge.CARD),
                max_health=CURRENT_HEALTH(Dredge.CARD),
            )
        )
    )


class TSC_074:
    """Kotori Lightblade"""

    # [x]After you cast a Holy spell on this, cast it again on __another
    # friendly minion.
    play = Play(CONTROLLER, HOLY, SELF).after(
        CastSpell(Play.CARD, RANDOM(FRIENDLY_MINIONS - SELF))
    )


##
# Spells


class TSC_952:
    """Holy Maki Roll"""

    # Restore #2 Health. Repeatable this turn.
    tags = {GameTag.ECHO: True}
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 2)


class TSC_061:
    """The Garden's Grace"""

    # [x]Give a minion +5/+5 and <b>Divine Shield</b>. Costs (1) less for each
    # Mana you've spent on Holy spells this game.
    cost_mod = -Attr(CONTROLLER, "holy_spells_spent_this_game")
    play = Buff(TARGET, "TSC_061e"), GiveDivineShield(TARGET)


TSC_061e = buff(+5, +5)


class TSC_079:
    """Radar Detector"""

    # [x]Scan the bottom 5 cards of your deck. Draw any Mechs found this way,
    # then shuffle your deck.
    play = ForceDraw(FRIENDLY_DECK[:5] + MECH), Shuffle(FRIENDLY_DECK)


class TSC_076:
    """Immortalized in Stone"""

    # Summon a 1/2, 2/4 and 4/8 Elemental with <b>Taunt</b>.
    play = (
        Summon(CONTROLLER, "TSC_076t"),
        Summon(CONTROLLER, "TSC_076t2"),
        Summon(CONTROLLER, "TSC_076t3"),
    )


class TID_949:
    """Front Lines"""

    # [x]Summon a minion from each player's deck. Repeat until either side of
    # the battlefield is full.
    def play(self):
        for _ in range(7):
            yield Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
            yield Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
            if (
                len(self.controller.field) >= 7
                or len(self.controller.opponent.field) >= 7
            ):
                break
