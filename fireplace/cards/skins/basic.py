from ..utils import *

##
# Hero Powers


class HERO_01bp:
    """Armor Up! (Garrosh Hellscream)"""

    activate = GainArmor(FRIENDLY_HERO, 2)


class HERO_02bp:
    """Totemic Call (Thrall)"""

    requirements = {
        PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    entourage = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]
    activate = Summon(CONTROLLER, RandomEntourage(exclude=FRIENDLY_MINIONS))


class NEW1_009:
    """Healing Totem"""

    events = OWN_TURN_END.on(Heal(FRIENDLY_MINIONS, 1))


class HERO_03bp:
    """Dagger Mastery (Valeera Sanguinar)"""

    activate = Summon(CONTROLLER, "CS2_082")


class HERO_04bp:
    """Reinforce (Uther Lightbringer)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "CS2_101t")


class HERO_05bp:
    """Steady Shot (Rexxar)"""

    requirements = {PlayReq.REQ_MINION_OR_ENEMY_HERO: 0, PlayReq.REQ_STEADY_SHOT: 0}
    powered_up = Find(SELF + EnumSelector(GameTag.STEADY_SHOT_CAN_TARGET))
    activate = powered_up & Hit(TARGET, 2) | Hit(ENEMY_HERO, 2)


class HERO_06bp:
    """Shapeshift (Malfurion Stormrage)"""

    activate = Buff(FRIENDLY_HERO, "CS2_017o"), GainArmor(FRIENDLY_HERO, 1)


CS2_017o = buff(atk=1)


class HERO_07bp:
    """Life Tap (Gul'dan)"""

    activate = Hit(FRIENDLY_HERO, 2), Draw(CONTROLLER)


class HERO_08bp:
    """Fireblast (Jaina Proudmoore)"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 1)


class HERO_09bp:
    """Lesser Heal (Anduin Wrynn)"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Heal(TARGET, 2)


class HERO_10bp:
    """Demon Claws (Illidan Stormrage)"""

    activate = Buff(FRIENDLY_HERO, "HERO_10bpe")


HERO_10bpe = buff(atk=1)


##
# Upgraded Hero Powers


class HERO_01bp2:
    """Tank Up! (Garrosh Hellscream)"""

    activate = GainArmor(FRIENDLY_HERO, 4)


class HERO_02bp2:
    """Totemic Slam (Thrall)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    choose = ("AT_132_SHAMANa", "AT_132_SHAMANb", "AT_132_SHAMANc", "AT_132_SHAMANd")


class AT_132_SHAMANa:
    """Healing Totem"""

    activate = Summon(CONTROLLER, "NEW1_009")


class AT_132_SHAMANb:
    """Searing Totem"""

    activate = Summon(CONTROLLER, "CS2_050")


class AT_132_SHAMANc:
    """Stoneclaw Totem"""

    activate = Summon(CONTROLLER, "CS2_051")


class AT_132_SHAMANd:
    """Wrath of Air Totem"""

    activate = Summon(CONTROLLER, "CS2_052")


class HERO_03bp2:
    """Poisoned Daggers (Valeera Sanguinar)"""

    activate = Summon(CONTROLLER, "AT_132_ROGUEt")


class HERO_04bp2:
    """The Silver Hand (Uther Lightbringer)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "CS2_101t") * 2


class HERO_05bp2:
    """Ballista Shot (Rexxar)"""

    requirements = {PlayReq.REQ_MINION_OR_ENEMY_HERO: 0, PlayReq.REQ_STEADY_SHOT: 0}
    powered_up = Find(SELF + EnumSelector(GameTag.STEADY_SHOT_CAN_TARGET))
    activate = powered_up & Hit(TARGET, 3) | Hit(ENEMY_HERO, 3)


class HERO_06bp2:
    """Dire Shapeshift (Malfurion Stormrage)"""

    activate = Buff(FRIENDLY_HERO, "AT_132_DRUIDe"), GainArmor(FRIENDLY_HERO, 2)


AT_132_DRUIDe = buff(atk=2)


class HERO_07bp2:
    """Soul Tap (Gul'dan)"""

    activate = Draw(CONTROLLER)


class HERO_08bp2:
    """Fireblast (Jaina Proudmoore)"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Hit(TARGET, 2)


class HERO_09bp2:
    """Heal (Anduin Wrynn)"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Heal(TARGET, 4)


class HERO_10bp2:
    """Demon's Bite (Illidan Stormrage)"""

    activate = Buff(FRIENDLY_HERO, "HERO_10pe2")


HERO_10pe2 = buff(atk=2)
