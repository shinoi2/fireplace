from typing import TypeVar

from .utils import CardList


class Deck(CardList[TypeVar("PlayableCard")]):
    """Main deck with optional sideboard card IDs keyed by the owning card ID."""

    MAX_CARDS = 30
    MAX_UNIQUE_CARDS = 2
    MAX_UNIQUE_LEGENDARIES = 1

    def __init__(self, cards=None, *, sideboards=None):
        super().__init__(cards or [])
        self.hero = None
        self.sideboards = {
            owner: list(cards) for owner, cards in (sideboards or {}).items()
        }

    def __repr__(self):
        return "<Deck (%i cards)>" % (len(self))
