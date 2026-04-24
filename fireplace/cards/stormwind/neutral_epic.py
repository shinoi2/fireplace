from ..utils import *

##
# Minions


class SW_069:
    """Enthusiastic Banker"""

    # [x]At the end of your turn, store a card from your deck.
    # <b>Deathrattle:</b> Add the stored cards to your hand.
    events = OWN_TURN_END.on(
        Remove(RANDOM(FRIENDLY_DECK)).then(StoringBuff(SELF, "SW_069e", Remove.TARGET))
    )


class SW_069e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, Copy(STORE_CARD))


class SW_073:
    """Cheesemonger"""

    # [x]Whenever your opponent casts a spell, add a random spell with the same
    # Cost to your hand.
    events = Play(OPPONENT, SPELL).on(
        Give(CONTROLLER, RandomSpell(cost=COST(Play.CARD)))
    )


class SW_074:
    """Nobleman"""

    # <b>Battlecry:</b> Create a Golden copy of a random card in your hand.
    play = Give(CONTROLLER, ExactCopy(RANDOM(FRIENDLY_HAND)))


class SW_075:
    """Elwynn Boar"""

    # [x]<b>Deathrattle:</b> If you had 7 Elwynn Boars die this game, equip a
    # 15/3 Sword of a ___Thousand Truths.@ <i>(@/7)</i>
    deathrattle = (Count(FRIENDLY + KILLED + ID("SW_075")) >= 7) & Summon(
        CONTROLLER, "SW_075t"
    )


class SW_075t:
    """Sword of a Thousand Truths"""

    # [x]After your hero attacks, destroy your opponent's Mana Crystals.
    events = Attack(FRIENDLY_HERO).after(SetMana(OPPONENT, 0))


class SW_077:
    """Stockades Prisoner"""

    # [x]Starts <b>Dormant</b>. After you play 3 cards, this awakens.
    tags = {GameTag.DORMANT: True}
    progress_total = 3
    dormant_events = (Play(CONTROLLER).after(AddProgress(SELF, Play.CARD)),)
    reward = Awaken(SELF)


class DED_521:
    """Maddest Bomber"""

    # <b>Battlecry:</b> Deal 12 damage randomly split among all other
    # characters.
    play = Hit(RANDOM_OTHER_CHARACTER, 1) * 12
