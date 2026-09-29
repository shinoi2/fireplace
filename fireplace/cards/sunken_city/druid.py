from ..utils import *

##
# Minions


class TSC_026:
    """Colaque"""

    # [x]<b>Colossal +1</b> <b>Immune</b> while you control Colaque's Shell.
    colossal = Summon(CONTROLLER, "TSC_026t")
    update = Find(FRIENDLY_MINIONS + ID("TSC_026t")) & Refresh(
        SELF, {GameTag.IMMUNE: True}
    )


class TSC_026t:
    """Colaque's Shell"""

    # <b>Taunt</b> <b>Deathrattle:</b> Gain 8 Armor.
    deathrattle = GainArmor(FRIENDLY_HERO, 8)


class TSC_652:
    """Green-Thumb Gardener"""

    # [x]<b>Battlecry:</b> Refresh empty Mana Crystals equal to the Cost of the
    # most expensive spell in your hand.
    play = FillMana(CONTROLLER, COST(RANDOM(HIGHEST_COST(FRIENDLY_HAND + SPELL))))


class TSC_653:
    """Bottomfeeder"""

    # <b>Deathrattle:</b> Add a Bottomfeeder to the bottom of your deck with
    # permanent +2/+2.
    def deathrattle(self):
        def create_custom_card(self):
            card = self.controller.card("TSC_653")
            card.custom_card = True
            if hasattr(self, "_buff_times"):
                card._buff_times = self._buff_times + 1
            else:
                card._buff_times = 1

            def create_custom_card(card):
                card.atk = card.atk + card._buff_times * 2
                card.max_health = card.max_health + card._buff_times * 2

            card.create_custom_card = create_custom_card
            card.create_custom_card(card)
            return card

        yield PutOnBottom(CONTROLLER, create_custom_card(self))


class TSC_657:
    """Dozing Kelpkeeper"""

    # [x]<b>Rush</b>. Starts <b>Dormant</b>. After you've cast 5 Mana _worth of
    # spells, awaken.
    tags = {GameTag.DORMANT: True}
    progress_total = 5
    sidequest = SpendMana(CONTROLLER, source=SPELL).after(
        AddProgress(SELF, CONTROLLER, SpendMana.AMOUNT)
    )
    reward = Awaken(SELF)


class TSC_658:
    """Hedra the Heretic"""

    # [x]<b>Battlecry:</b> For each spell you've cast while holding this,
    # summon a minion of that spell's Cost.
    def play(self):
        spells = self.cards_played_when_holding.filter(type=CardType.SPELL)
        self.game.random.shuffle(spells)
        for spell in spells:
            yield Summon(CONTROLLER, RandomMinion(cost=spell.cost))


class TID_000:
    """Spirit of the Tides"""

    # [x]If you have any unspent Mana at the end of _your turn, gain +1/+2.
    events = OWN_TURN_END.on((CURRENT_MANA(CONTROLLER) > 0) & Buff(SELF, "TID_000e"))


TID_000e = buff(+1, +2)


class TID_002:
    """Herald of Nature"""

    # <b>Battlecry:</b> If you've cast a Nature spell while holding this, give
    # your other minions +1/+2.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + NATURE)
    play = powered_up & Buff(FRIENDLY_MINIONS - SELF, "TID_002e")


TID_002e = buff(+1, +2)


##
# Spells


class TSC_927:
    """Azsharan Gardens"""

    # Give all minions in your hand +1/+1. Put a 'Sunken Gardens' on the bottom
    # of your deck.
    play = Buff(FRIENDLY_HAND, "TSC_927e"), PutOnBottom(CONTROLLER, "TSC_927t")


TSC_927e = buff(+1, +1)


class TSC_927t:
    """Sunken Gardens"""

    # Give +1/+1 to all minions in your hand, deck, and battlefield.
    play = Buff(FRIENDLY + (IN_DECK | IN_HAND | IN_PLAY) + MINION - DORMANT, "TSC_927e")


class TSC_650:
    """Flipper Friends"""

    # [x]<b>Choose One</b> - Summon a 6/6 Orca with <b>Taunt</b>; or six 1/1
    # Otters with <b>Rush</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    choose = ("TSC_650a", "TSC_650d")
    play = ChooseBoth(CONTROLLER) & (
        Summon(CONTROLLER, "TSC_650t"),
        Summon(CONTROLLER, "TSC_650t4") * 6,
    )


class TSC_650a:
    """Order the Orca"""

    # Summon a 6/6 Orca with <b>Taunt</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "TSC_650t")


class TSC_650d:
    """Romp of Otters"""

    # Summon six 1/1 Otters with <b>Rush</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "TSC_650t4") * 6


class TSC_651:
    """Seaweed Strike"""

    # [x]Deal $4 damage to a minion. If you played a Naga while holding this,
    # also give your hero +4 Attack this turn.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 1, PlayReq.REQ_MINION_TARGET: 1}
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + NAGA)
    play = (Hit(TARGET, 4), powered_up & Buff(FRIENDLY_HERO, "TSC_651e"))


TSC_651e = buff(atk=+4)


class TSC_656:
    """Miracle Growth"""

    # [x]Draw 3 cards. Summon a Plant with <b>Taunt</b> and stats equal to your
    # hand size.
    play = (
        Draw(CONTROLLER) * 3,
        SummonCustomMinion(
            CONTROLLER,
            "TSC_656t",
            Count(FRIENDLY_HAND),
            Count(FRIENDLY_HAND),
            Count(FRIENDLY_HAND),
        ),
    )


class TSC_654:
    """Aquatic Form"""

    # <b>Dredge</b>. If you have the Mana to play the card this turn, draw it.
    play = Dredge(CONTROLLER).then(
        (CURRENT_MANA(CONTROLLER) >= COST(Dredge.CARD)) & ForceDraw(Dredge.CARD)
    )


class TID_001:
    """Moonbeam"""

    # Deal $1 damage to an enemy, twice.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 1, PlayReq.REQ_ENEMY_TARGET: 1}
    play = Hit(TARGET, 1) * 2
