from ..utils import *


##
# Minions


class DMF_064:
    """Carousel Gryphon"""

    # <b>Divine Shield</b> <b>Corrupt:</b> Gain +3/+3 and_<b>Taunt</b>.
    corrupt_card = "DMF_064t"


class DMF_194:
    """Redscale Dragontamer"""

    # <b>Deathrattle:</b> Draw a Dragon.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + DRAGON))


class DMF_235:
    """Balloon Merchant"""

    # <b>Battlecry:</b> Give your Silver Hand Recruits +1 Attack and <b>Divine
    # Shield</b>.
    play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "DMF_235e").then(
        GiveDivineShield(Buff.TARGET)
    )


DMF_235e = buff(atk=1)


class DMF_237:
    """Carnival Barker"""

    # Whenever you summon a 1-Health minion, give it +1/+2.
    play = Summon(CONTROLLER, MINION + (CURRENT_HEALTH == 1)).on(
        Buff(Summon.CARD, "DMF_237e")
    )


DMF_237e = buff(+2, +2)


class DMF_240:
    """Lothraxion the Redeemed"""

    # [x]<b>Battlecry:</b> For the rest of the game, after you summon a Silver
    # Hand Recruit, give it <b>Divine Shield</b>.
    play = Buff(CONTROLLER, "DMF_240e")


class DMF_240e:
    events = Summon(CONTROLLER, ID("CS2_101t")).after(GiveDivineShield(Summon.CARD))


class DMF_241:
    """High Exarch Yrel"""

    # [x]<b>Battlecry:</b> If your deck has no Neutral cards, gain <b>Rush</b>,
    # <b>Lifesteal</b>, <b>Taunt</b>, and <b>Divine Shield</b>.
    powered_up = -Find(FRIENDLY_DECK + NEUTRAL)
    play = powered_up & (
        SetTags(
            SELF,
            {
                GameTag.RUSH: True,
                GameTag.LIFESTEAL: True,
                GameTag.TAUNT: True,
                GameTag.DIVINE_SHIELD: True,
            },
        )
    )


class YOP_010:
    """Imprisoned Celestial"""

    # [x]<b>Dormant</b> for 2 turns. <b>Spellburst</b>: Give your minions
    # <b>Divine Shield</b>.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    spellburst = GiveDivineShield(FRIENDLY_MINIONS)


##
# Spells


class DMF_195:
    """Snack Run"""

    # <b>Discover</b> a spell. Restore Health to your hero equal to its Cost.
    play = DISCOVER(RandomSpell()).then(Heal(FRIENDLY_HERO, COST(Discover.CARD)))


class DMF_236:
    """Oh My Yogg!"""

    # [x]<b>Secret:</b> When your opponent casts a spell, they instead cast a
    # random one of the same Cost.
    secret = Play(OPPONENT, SPELL).on(
        Reveal(SELF), CastSpell(RandomSpell(cost=COST(Play.CARD)))
    )


class DMF_244:
    """Day at the Faire"""

    # Summon 3 Silver Hand Recruits. <b>Corrupt:</b> Summon 5.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "CS2_101t") * 3
    corrupt_card = "DMF_244t"


class DMF_244t:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "CS2_101t") * 5


class YOP_005:
    """Barricade"""

    # Summon a 2/4 Guard with <b>Taunt</b>. If it's_your only minion, summon
    # another.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Find(FRIENDLY_MINIONS) & (Summon(CONTROLLER, "YOP_005t")) | (
        Summon(CONTROLLER, "YOP_005t") * 2
    )


class YOP_009:
    """Rally!"""

    # Resurrect a friendly 1-Cost, 2-Cost, and 3-Cost minion.
    play = (
        Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION + (COST == 1))),
        Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION + (COST == 2))),
        Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION + (COST == 3))),
    )


##
# Weapons


class DMF_238:
    """Hammer of the Naaru"""

    # <b>Battlecry:</b> Summon a 6/6 Holy Elemental with <b>Taunt</b>.
    play = Summon(CONTROLLER, "DMF_238t")


class YOP_011:
    """Libram of Judgment"""

    # <b>Corrupt:</b> Gain <b>Lifesteal</b>.
    corrupt_card = "YOP_011t"
