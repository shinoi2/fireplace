import functools

from ..utils import *

##
# Minions


class RLK_803:
    """Grand Magister Rommath"""

    # [x]<b>Battlecry:</b> Recast each spell you've cast this game that didn't
    # start in your deck.
    def play(self):
        for spell in self.controller.cards_played_this_game[:]:
            if spell.type == CardType.SPELL and all(
                spell is not card for card in self.controller.starting_deck
            ):
                yield CastSpell(Copy(spell))


class RLK_541:
    """Vexallus"""

    # Your Arcane spells cast twice.
    update = Refresh(CONTROLLER, {enums.ARCANE_SPELLS_CAST_TWICE: True})


class RLK_542:
    """Arcsplitter"""

    # <b>Deathrattle:</b> Add 2 Arcane Bolts to your hand.
    deathrattle = Give(CONTROLLER, "RLK_843") * 2


class RLK_543:
    """Magister's Apprentice"""

    # Your Arcane spells cost (1) less.
    update = Refresh(FRIENDLY_HAND + SPELL + ARCANE, {GameTag.COST: -1})


class RLK_545:
    """Energy Shaper"""

    # [x]<b>Battlecry:</b> Transform all spells in your hand into ones that
    # cost (2) more. <i>(They keep their original Cost.)</i>
    def play(self):
        for spell in self.controller.hand.filter(type=CardType.SPELL):
            cost = spell.cost
            ids = RandomSpell(cost=cost + 2).evaluate(self)
            if ids:
                result = self.controller.card(ids[0], self)
                yield Morph(spell, result)
                # Replace the base cost so previously applied discounts are counted once.
                result.cost = result._cost + cost - result.cost


class RLK_547:
    """Prismatic Elemental"""

    # <b>Battlecry:</b> <b>Discover</b> a spell from any class. It costs (1)
    # less.
    play = Discover(CONTROLLER, RandomSpell(card_class=list(CardClass)[1:])).then(
        Buff(Discover.CARD, "RLK_547e"), Give(CONTROLLER, Discover.CARD)
    )


class RLK_548:
    """Arcane Wyrm"""

    # <b>Battlecry:</b> Add an Arcane Bolt to your hand.
    play = Give(CONTROLLER, "RLK_843")


class NX2_002:
    """Spectral Trainee"""

    # After you cast a spell, deal 1 damage to all enemy minions.
    events = OWN_SPELL_PLAY.after(Hit(ENEMY_MINIONS, 1))


class NX2_003:
    """Whirlweaver"""

    # [x]<b>Battlecry:</b> If you've cast a spell last turn, <b>Discover</b> an
    # Elemental.
    play = Find(
        CARDS_PLAYED_THIS_GAME
        + SPELL
        + FilterSelector(
            lambda card, source: getattr(card, "turn_played", -1)
            == source.game.turn - 2
        )
    ) & DISCOVER(RandomMinion(race=Race.ELEMENTAL))


##
# Spells


class RLK_544:
    """Arcane Defenders"""

    # Summon two 5/6 Golems with <b>Taunt</b> and "Can't be targeted by spells
    # or Hero Powers."
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "RLK_544t") * 2


class RLK_546:
    """Vast Wisdom"""

    # <b>Discover</b> two spells that cost (3) or less. Swap their Costs.
    def pick_second(self, player, cards, first):
        yield Discover(CONTROLLER, RandomSpell(cost=range(4))).then(
            functools.partial(RLK_546.swap_costs, first)
        )

    @staticmethod
    def swap_costs(first, source, player, cards, second):
        first_cost, second_cost = first.cost, second.cost
        yield Buff(first, "RLK_546e", _xcost=second_cost)
        yield Buff(second, "RLK_546e", _xcost=first_cost)
        yield Give(player, [first, second])

    play = Discover(CONTROLLER, RandomSpell(cost=range(4))).then(pick_second)


class RLK_843:
    """Arcane Bolt"""

    # Deal $2 damage. <b>Manathirst (8):</b> Deal $3 damage instead.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Manathirst(8) & Hit(TARGET, 3) | Hit(TARGET, 2)


class NX2_001:
    """Tear Reality"""

    # [x]Add 2 random Mage spells from the past to your hand. They cost (2)
    # less.
    play = (
        Give(
            CONTROLLER,
            Buff(
                RandomSpell(card_class=CardClass.MAGE, is_standard=False),
                "NX2_001e",
            ),
        )
        * 2
    )


RLK_547e = buff(cost=-1)
NX2_001e = buff(cost=-2)


class RLK_544t:
    tags = {
        GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
        GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
    }


class RLK_546e:
    def cost(self, cost):
        return self._xcost
