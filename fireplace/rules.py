"""
Base game rules (events, etc)
"""

from .cards.utils import *


class WeaponRules:
    base_events = [Attack(FRIENDLY_HERO).after(Hit(SELF, 1))]


class SigilRules:
    base_events = [OWN_TURN_BEGIN.on(Destroy(SELF))]


class ObjectiveRules:
    base_events = [OWN_TURN_END.on(AddProgress(SELF))]
