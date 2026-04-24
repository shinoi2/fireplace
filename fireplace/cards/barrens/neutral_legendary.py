from ..utils import *

##
# Minions


class BAR_080:
    """Shadow Hunter Vol'jin"""

    # <b>Battlecry:</b> Choose a minion. Swap it with a random one in its
    # owners hand.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Find(TARGET + FRIENDLY) & Swap(
        TARGET, RANDOM(FRIENDLY_HAND + MINION)
    ) | Swap(TARGET, RANDOM(ENEMY_HAND + MINION))


class BAR_077:
    """Kargal Battlescar"""

    # [x]<b>Battlecry:</b> Summon a 5/5 Lookout for each Watch Post you've
    # __summoned this game.
    play = Summon(CONTROLLER, "BAR_077t") * Count(
        CARDS_PLAYED_THIS_GAME + IDS(WATCH_POSTS)
    )


class BAR_078:
    """Blademaster Samuro"""

    # [x]<b>Rush</b> <b>Frenzy:</b> Deal damage equal to this minion's Attack
    # _to all enemy minions.
    frenzy = Hit(ENEMY_MINIONS, ATK(SELF))


class BAR_079:
    """Kazakus, Golem Shaper"""

    # <b>Battlecry:</b> If your deck has no 4-Cost cards, build a custom Golem.
    class KazakusAction(MultipleChoice):
        PLAYER = ActionArg()
        choose_times = 3
        first_choices = [
            "BAR_079_m1",
            "BAR_079_m2",
            "BAR_079_m3",
        ]
        second_choices = [
            "BAR_079t4",
            "BAR_079t5",
            "BAR_079t6",
            "BAR_079t7",
            "BAR_079t8",
            "BAR_079t9",
        ]
        cost_1_choices = [
            "BAR_079t10",
            "BAR_079t11",
            "BAR_079t12",
            "BAR_079t13",
            "BAR_079t14",
            "BAR_079t15",
        ]
        cost_5_choices = [
            "BAR_079t10b",
            "BAR_079t11",
            "BAR_079t12b",
            "BAR_079t13b",
            "BAR_079t14b",
            "BAR_079t15b",
        ]
        cost_10_choices = [
            "bar_079t10c",
            "BAR_079t11",
            "BAR_079t12c",
            "BAR_079t13c",
            "BAR_079t14c",
            "BAR_079t15c",
        ]

        def do_step1(self):
            self.cards = [self.player.card(card) for card in self.first_choices]

        def do_step2(self):
            self.cards = [
                self.player.card(card)
                for card in self.source.game.random.sample(self.second_choices, 3)
            ]

        def do_step3(self):
            third_choices = []
            if self.choosed_cards[0].cost == 1:
                third_choices = self.cost_1_choices
            elif self.choosed_cards[0].cost == 5:
                third_choices = self.cost_5_choices
            elif self.choosed_cards[0].cost == 10:
                third_choices = self.cost_10_choices
            self.cards = [
                self.player.card(card)
                for card in self.source.game.random.sample(third_choices, 3)
            ]

        def done(self):
            golem = self.choosed_cards[0]
            card1 = self.choosed_cards[1]
            card2 = self.choosed_cards[2]
            golem.custom_card = True

            def create_custom_card(golem):
                if card1 == "BAR_079t4":
                    golem.rush = True
                elif card1 == "BAR_079t5":
                    golem.taunt = True
                elif card1 == "BAR_079t6":
                    golem.divine_shield = True
                elif card1 == "BAR_079t7":
                    golem.lifesteal = True
                elif card1 == "BAR_079t8":
                    golem.stealth = True
                elif card1 == "BAR_079t9":
                    golem.poisonous = True

                if card2 == "BAR_079t14":
                    golem.spellpower = 1
                elif card2 == "BAR_079t14b":
                    golem.spellpower = 2
                elif card2 == "BAR_079t14c":
                    golem.spellpower = 4
                else:
                    golem.data.scripts.play = card2.data.scripts.play

                golem.tags[GameTag.CARDTEXT_ENTITY_0] = card1.description
                golem.tags[GameTag.CARDTEXT_ENTITY_1] = card2.description

            golem.create_custom_card = create_custom_card
            golem.create_custom_card(golem)
            self.player.give(golem)

    powered_up = -Find(FRIENDLY_DECK + (COST == 4))
    play = powered_up & KazakusAction(CONTROLLER)


class BAR_721:
    """Mankrik"""

    # [x]<b>Battlecry:</b> Help Mankrik find his wife! She was last seen
    # somewhere in your deck.
    play = Shuffle(CONTROLLER, "BAR_721t")


class BAR_721t:
    play = Summon(CONTROLLER, "BAR_721t2").then(Attack(Summon.CARD, ENEMY_HERO))


class WC_030:
    """Mutanus the Devourer"""

    # [x]<b>Battlecry:</b> Eat a minion in your opponent's hand. Gain its
    # stats.
    play = Destroy(RANDOM(ENEMY_HAND + MINION)).then(
        Buff(
            SELF,
            "WC_030e",
            atk=ATK(Destroy.TARGET),
            max_health=CURRENT_HEALTH(Destroy.TARGET),
        )
    )


class WC_035:
    """Archdruid Naralex"""

    # [x]<b>Dormant</b> for 2 turns. While <b>Dormant</b>, add a Dream card to
    # your hand __at the end of your turn.
    dormant_turns = 2
    dormant_events = OWN_TURN_END.on(
        Give(CONTROLLER, RandomCard(card_class=CardClass.DREAM))
    )
