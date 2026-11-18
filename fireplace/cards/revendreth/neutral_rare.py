from ..utils import *

##
# Minions


class REV_901:
    """Dispossessed Soul"""

    # <b>Battlecry:</b> If you control a location, <b>Discover</b> a copy of a
    # card in your deck.
    play = Find(FRIENDLY + ALL_LOCATIONS) & Choice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK), 3))
    ).then(Give(CONTROLLER, Choice.CARD))


class REV_946:
    """Steamcleaner"""

    # <b>Battlecry:</b> Destroy ALL cards in both players' decks that didn't
    # start there.
    def play(self):
        for player in self.game.players:
            originals = STARTING_DECK.eval(self.game, player)
            yield Destroy(
                [
                    card
                    for card in player.deck
                    if not any(card is original for original in originals)
                ]
            )


class REV_377:
    """Invitation Courier"""

    # After a card is added to your hand from another class, copy it.
    events = Give(
        CONTROLLER,
        FRIENDLY_HAND + OTHER_CLASS_CHARACTER,
        source=FRIENDLY - ID("REV_377"),
    ).after(Give(CONTROLLER, Copy(Give.CARD)))


class REV_016:
    """Crooked Cook"""

    # [x]At the end of your turn, if you dealt 3 or more damage to the enemy
    # hero, draw a card.
    events = OWN_TURN_END.on(
        (Attr(CONTROLLER, "damage_dealt_to_enemy_hero_this_turn") >= 3)
        & Draw(CONTROLLER)
    )


class MAW_031:
    """Afterlife Attendant"""

    # Your <b>Infuse</b> cards also <b>Infuse</b> while in your deck.
    update = Refresh(CONTROLLER, {enums.INFUSE_IN_DECK: True})


class REV_019:
    """Famished Fool"""

    # <b>Battlecry:</b> Draw a card. <b>Infuse (@):</b> Draw 3 instead.
    infuse_card = "REV_019t"
    play = Draw(CONTROLLER)


class REV_019t:
    play = Draw(CONTROLLER) * 3
