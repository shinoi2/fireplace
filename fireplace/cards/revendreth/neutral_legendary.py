from ..utils import *

##
# Minions


class REV_018:
    """Prince Renathal"""

    # [x]Your deck size and starting Health are 40.
    class Hand:
        events = GameStart().on(Buff(FRIENDLY_HERO, "REV_018e"))

    class Deck:
        events = GameStart().on(Buff(FRIENDLY_HERO, "REV_018e"))


@custom_card
class REV_018e:
    tags = {
        GameTag.CARDNAME: "Prince Renathal Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    max_health = SET(40)


class REV_906:
    """Sire Denathrius"""

    # <b><b>Lifesteal</b>.</b> <b>Battlecry:</b> Deal 5 damage amongst enemies.
    # <b>Endlessly Infuse (1):</b> Deal 1 more.
    def infuse_card(self):
        card = self.controller.card("REV_906t", self)
        card.data_num_2 = self.data_num_2 + 1
        return card

    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * Attr(SELF, "data_num_2")


class REV_238:
    """Theotar, the Mad Duke"""

    # <b>Battlecry:</b> <b>Discover</b> a card in each player's hand and swap
    # them.
    def choose_enemy(self, player, cards, chosen):
        yield Choice(CONTROLLER, RANDOM(ENEMY_HAND, 3)).then(Swap(chosen, Choice.CARD))

    play = Find(ENEMY_HAND) & Choice(CONTROLLER, RANDOM(FRIENDLY_HAND, 3)).then(
        choose_enemy
    )


class MAW_033:
    """Sylvanas, the Accused"""

    # [x]<b>Battlecry:</b> Destroy an enemy minion. <b>Infuse (@):</b> Take
    # control of it instead.
    requirements = ENEMY_MINION_BATTLECRY
    infuse_card = "MAW_033t"
    play = Destroy(TARGET)


class MAW_034:
    """The Jailer"""

    # <b>Battlecry:</b> Destroy your  deck. For the rest of the game, your
    # minions are <b>Immune</b>.
    play = Destroy(FRIENDLY_DECK), Buff(CONTROLLER, "MAW_034e")


class REV_021:
    """Kael'thas Sinstrider"""

    # Every third minion you play each turn costs (0).
    update = Refresh(FRIENDLY_HAND + MINION, buff="REV_021e")


class REV_022:
    """Murloc Holmes"""

    # [x]<b>Battlecry:</b> Solve 3 Clues about your opponent's cards to get
    # copies of them.
    def play(self):
        pools = [
            DeDuplicate(selector).eval(self.game, self)
            for selector in (ENEMY_STARTING_HAND, ENEMY_HAND, ENEMY_DECK)
        ]

        def choice(stage, solved):
            if stage == len(pools):
                yield Give(CONTROLLER, solved)
                return

            correct = pools[stage]
            correct_ids = {card.id for card in correct}
            wrong = DeDuplicate(Selector()).eval(
                [
                    card
                    for index, pool in enumerate(pools)
                    if index != stage
                    for card in pool
                    if card.id not in correct_ids
                ],
                self,
            )
            if correct and len(wrong) >= 2:
                correct_card = self.game.random.choice(correct)
                wrong_cards = self.game.random.sample(wrong, 2)
                cards = Copy([correct_card] + wrong_cards).evaluate(self)
                correct_card = cards[0]
                self.game.random.shuffle(cards)

                def choose(source, player, cards, card):
                    if card is correct_card:
                        yield from choice(stage + 1, solved + [card])

                yield Choice(CONTROLLER, cards).then(choose)

        yield from choice(0, [])


class REV_906t(REV_906):
    """Sire Denathrius"""


class MAW_033t:
    requirements = ENEMY_MINION_BATTLECRY
    play = Steal(TARGET)


class MAW_034e:
    update = Refresh(
        FRIENDLY_MINIONS,
        {GameTag.CANT_BE_DAMAGED: True, GameTag.CANT_BE_TARGETED_BY_OPPONENTS: True},
    )


class REV_021e:
    def cost(self, value):
        if self.controller.minions_played_this_turn % 3 == 2:
            return 0
        return value
