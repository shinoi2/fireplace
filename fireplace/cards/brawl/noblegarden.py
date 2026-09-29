"""
Everybunny Get in Here!
"""

from ..utils import *


EGG = "TB_Noblegarden_002"
BUNNY = "TB_Noblegarden_002t1"
DYES = tuple("TB_Noblegarden_003t%i" % n for n in range(1, 9))
# The egg a dye leaves ("Blue Egg": "The minion inside has Windfury."), and
# what the minion inside gets when it hatches ("Blue Hatchling": Windfury).
HATCHLING = {"TB_Noblegarden_003t%ie" % n: "TB_Noblegarden_003t%ie2" % n for n in range(1, 9)}
RandomDye = RandomID(*DYES)


class Hatch(TargetedAction):
    """
    Hatch Noblegarden Egg targets: each becomes a Bunny, which gets what the
    dyes of its egg grant. The wiki (Everybunny Get in Here!): "Without any
    dyes applied, it will always spawn a Bunny"; "Eggs with dyes applied will
    summon a larger variety of 'cute' minions", a variety the page does not
    list: a dyed egg hatches into a Bunny too, with its dyes (one per dye,
    they stack).
    """

    TARGET = ActionArg()

    def do(self, source, target):
        if target.id != EGG or target.zone != Zone.PLAY:
            return
        hatchlings = [HATCHLING[b.id] for b in target.buffs if b.id in HATCHLING]
        action = Morph(target, BUNNY)
        if hatchlings:
            then = [Buff(Morph.CARD, h) for h in hatchlings]
            then += [ON_THE_MINION[h](Morph.CARD) for h in hatchlings if h in ON_THE_MINION]
            action = action.then(*then)
        source.game.queue_actions(source, [action])


class TB_Noblegarden_002:
    """Noblegarden Egg"""

    # Stealth. At the start of your turn, hatch this into something cute.
    # An Egg, for the dyes ("Dye an Egg"); the wiki gives it the Egg race.
    tags = {GameTag.CARDRACE: Race.EGG}
    events = OWN_TURN_BEGIN.on(Hatch(SELF))


SHIFT = Morph(SELF, RandomDye).then(Buff(Morph.CARD, "TB_Noblegarden_003e"))


class TB_Noblegarden_003:
    """Shifting Dye"""

    # Each turn this is in your hand, transform it into a random dye. The
    # wiki: "Unlike other cards that transform into other cards like Shifter
    # Zerus and Molten Blade, Shifting Dye can change on the same turn it's
    # drawn": when drawn, then at the start of each of your turns.
    draw = SHIFT

    class Hand:
        events = OWN_TURN_BEGIN.on(SHIFT)


class TB_Noblegarden_003e:
    """Shifting"""

    # Transforming into random dyes: the dye keeps shifting, each turn.
    class Hand:
        events = OWN_TURN_BEGIN.on(
            Morph(OWNER, RandomDye).then(Buff(Morph.CARD, "TB_Noblegarden_003e"))
        )

    events = REMOVED_IN_PLAY


def _dye(n):
    class Dye:
        # Dye an Egg. When it hatches, it grants ...
        requirements = {
            PlayReq.REQ_TARGET_TO_PLAY: 0,
            PlayReq.REQ_MINION_TARGET: 0,
            PlayReq.REQ_TARGET_WITH_RACE: Race.EGG,
        }
        play = Buff(TARGET, "TB_Noblegarden_003t%ie" % n)

    Dye.__name__ = "TB_Noblegarden_003t%i" % n
    return Dye


TB_Noblegarden_003t1 = _dye(1)  # Blue: Windfury
TB_Noblegarden_003t2 = _dye(2)  # Purple: Lifesteal
TB_Noblegarden_003t3 = _dye(3)  # Green: Poisonous
TB_Noblegarden_003t4 = _dye(4)  # Silver: Stealth
TB_Noblegarden_003t5 = _dye(5)  # Orange: Rush
TB_Noblegarden_003t6 = _dye(6)  # Pink: Taunt
TB_Noblegarden_003t7 = _dye(7)  # Gold: Divine Shield
TB_Noblegarden_003t8 = _dye(8)  # Red: +2/+2

TB_Noblegarden_003t1e2 = buff(windfury=True)
TB_Noblegarden_003t2e2 = buff(lifesteal=True)
TB_Noblegarden_003t3e2 = buff(poisonous=True)
TB_Noblegarden_003t5e2 = buff(rush=True)
TB_Noblegarden_003t6e2 = buff(taunt=True)
TB_Noblegarden_003t8e2 = buff(+2, +2)

# Silver (Stealth) and Gold (Divine Shield): their Hatchling enchantment is
# only the record; the keyword goes on the minion, as fireplace gives it (it
# reads Divine Shield on the minion only, and a Stealth carried by an
# enchantment would not be lost when the minion attacks).
ON_THE_MINION = {
    "TB_Noblegarden_003t4e2": lambda card: SetTag(card, GameTag.STEALTH),
    "TB_Noblegarden_003t7e2": lambda card: GiveDivineShield(card),
}


class TB_Noblegarden_004:
    """Noblegarden Spoon"""

    # Hatch your Noblegarden Eggs!
    play = Hatch(FRIENDLY_MINIONS + ID(EGG))


class TB_Noblegarden_005:
    """Carrots"""

    # Give friendly minions +1/+1 or +2/+2 if it's a Bunny.
    play = (
        Buff(FRIENDLY_MINIONS - ID(BUNNY), "TB_Noblegarden_005e", atk=1, max_health=1),
        Buff(FRIENDLY_MINIONS + ID(BUNNY), "TB_Noblegarden_005e", atk=2, max_health=2),
    )


class TB_Noblegarden_006:
    """Hawkstrider Hen"""

    # Battlecry and Deathrattle: Summon a Noblegarden Egg.
    play = Summon(CONTROLLER, EGG)
    deathrattle = Summon(CONTROLLER, EGG)
