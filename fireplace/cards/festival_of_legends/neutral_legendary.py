from ..utils import *

##
# Minions


class BandMembers(LazyValue):
    def evaluate(self, source):
        player = source.controller
        band = player.sideboards.get("ETC_080", ())
        return [player.card(card_id, source) for card_id in dict.fromkeys(band)]


class ETC_080:
    """E.T.C., Band Manager"""

    # [x]While building your deck, assemble a band of 3 cards. _<b>Battlecry:
    # Discover</b> one!
    def take_member(source, player, cards, chosen):
        player.sideboards["ETC_080"].remove(chosen.id)
        return [Give(player, chosen)]

    play = Choice(CONTROLLER, BandMembers()).then(take_member)
