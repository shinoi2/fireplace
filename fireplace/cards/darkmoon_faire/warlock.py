from ..utils import *

##
# Minions


class DMF_110:
    """Fire Breather"""

    # <b>Battlecry:</b> Deal 2 damage to all minions except Demons.
    play = Hit(ALL_MINIONS - DEMON, 2)


class DMF_111:
    """Man'ari Mosher"""

    # <b>Battlecry:</b> Give a friendly Demon +3 Attack and <b>Lifesteal</b>
    # this turn.
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET, "DMF_111e")


DMF_111e = buff(atk=3, lifesteal=True)


class DMF_115:
    """Revenant Rascal"""

    # <b>Battlecry:</b> Destroy a Mana Crystal for each player.
    play = GainEmptyMana(ALL_PLAYERS, -1)


class DMF_533:
    """Ring Matron"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon two 3/2 Imps.
    deathrattle = Summon(CONTROLLER, "DMF_533t") * 2


class YOP_003:
    """Luckysoul Hoarder"""

    # [x]<b>Battlecry:</b> Shuffle 2 Soul Fragments into your deck.
    # <b>Corrupt:</b> Draw a card.
    play = Shuffle(CONTROLLER, SOUL_FRAGMENT) * 2
    corrupt_card = "YOP_003t"


class YOP_003t:
    play = (Shuffle(CONTROLLER, SOUL_FRAGMENT) * 2, Draw(CONTROLLER))


class YOP_004:
    """Envoy Rustwix"""

    # [x]<b>Deathrattle:</b> Shuffle 3 random Prime Legendary minions into your
    # deck.
    entourage = [
        "BT_136t",
        "BT_210t",
        "BT_028t",
        "BT_019t",
        "BT_197t",
        "BT_713t",
        "BT_109t",
        "BT_309t",
        "BT_123t",
    ]
    deathrattle = Shuffle(CONTROLLER, RandomEntourage() * 3)


##
# Spells


class DMF_113:
    """Free Admission"""

    # Draw 2 minions. If they're both Demons, reduce their Costs by (2).
    def play(self):
        game = self.game
        cards = (RANDOM(FRIENDLY_DECK + MINION) * 2).eval(game, self)
        yield ForceDraw(cards)
        if len(cards) == 2 and all(Race.DEMON in card.races for card in cards):
            yield Buff(cards, "DMF_113e")


class DMF_113e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class DMF_117:
    """Cascading Disaster"""

    # [x]Destroy a random enemy minion. <b>Corrupt:</b> Destroy 2. <b>Corrupt
    # Again:</b> Destroy 3.
    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Destroy(RANDOM_ENEMY_MINION)
    corrupt_card = "DMF_117t"


class DMF_117t:
    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Destroy(RANDOM_ENEMY_MINION * 2)
    corrupt_card = "DMF_117t2"


class DMF_117t2:
    requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
    play = Destroy(RANDOM_ENEMY_MINION * 3)


class DMF_118:
    """Tickatus"""

    # [x]<b>Battlecry:</b> Remove the top 5 cards from your deck.
    # <b>Corrupt:</b> Your opponent's deck instead.
    play = Mill(CONTROLLER, 5)
    corrupt_card = "DMF_118t"


class DMF_118t:
    play = Mill(OPPONENT, 5)


class DMF_119:
    """Wicked Whispers"""

    # Discard your lowest Cost card. Give your minions +1/+1.
    play = Discard(RANDOM(LOWEST_COST(FRIENDLY_HAND))), Buff(
        FRIENDLY_MINIONS, "DMF_119e"
    )


DMF_119e = buff(+1, +1)


class DMF_534:
    """Deck of Chaos"""

    # Swap the Cost and Attack of all minions in_your deck.
    play = Buff(FRIENDLY_DECK + MINION, "DMF_534e")


class DMF_534e:
    atk = lambda self, i: self._xatk
    cost = lambda self, i: self._xcost

    def apply(self, target):
        self._xatk = target.cost
        self._xcost = target.atk


class YOP_033:
    """Backfire"""

    # Draw 3 cards. Deal $3 damage to your hero.
    play = (Draw(CONTROLLER) * 3, Hit(FRIENDLY_HERO, 3))
