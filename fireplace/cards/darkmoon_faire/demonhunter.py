from ..utils import *


##
# Minions


class DMF_217:
    """Line Hopper"""

    # Your <b>Outcast</b> cards cost (1)_less.
    update = Refresh(FRIENDLY_HAND + OUTCAST, {GameTag.COST: -1})


class DMF_222:
    """Redeemed Pariah"""

    # After you play an <b>Outcast</b> card, gain +1/+1.
    event = Play(OUTCAST).after(Buff(SELF, "DMF_222e"))


DMF_222e = buff(atk=1, health=1)


class DMF_223:
    """Renowned Performer"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Summon two __1/1 Assistants with
    # <b>Taunt</b>.__
    deathrattle = Summon(CONTROLLER, "DMF_223t") * 2


class DMF_226:
    """Bladed Lady"""

    # [x]<b>Rush</b> Costs (1) if your hero has 6 or more Attack.
    class Hand:
        update = (ATK(FRIENDLY_HERO) >= 6) & Refresh(SELF, {GameTag.COST: SET(1)})


class DMF_229:
    """Stiltstepper"""

    # [x]<b>Battlecry:</b> Draw a card. If you play it this turn, give your
    # hero +4 Attack this turn.
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DMF_229e2"))


class DMF_229e2:
    events = Play(OWNER).after(Buff(FRIENDLY_HERO, "DMF_229e"))


DMF_229e = buff(atk=4)


class DMF_230:
    """Il'gynoth"""

    # [x]<b>Lifesteal</b> Your <b>Lifesteal</b> damages the enemy hero instead
    # of healing you.
    update = Refresh(
        CONTROLLER,
        {
            GameTag.LIFESTEAL_DAMAGES_OPPOSING_HERO: True,
        },
    )


class DMF_231:
    """Zai, the Incredible"""

    # <b>Battlecry:</b> Copy the left- and right-most cards in your hand.
    play = Give(CONTROLLER, Copy(OUTERMOST(FRIENDLY_HAND)))


class DMF_247:
    """Insatiable Felhound"""

    # <b>Taunt</b> <b>Corrupt:</b> Gain +1/+1 and_<b>Lifesteal</b>.
    corrupt_card = "DMF_247t"


class DMF_248:
    """Felsteel Executioner"""

    # <b>Corrupt:</b> Become a weapon.
    corrupted_card = "DMF_248t"


class YOP_002:
    """Felsaber"""

    # Can only attack if your hero attacked this turn.
    update = (NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) == 0) | Refresh(
        SELF, {GameTag.CANT_ATTACK: True}
    )


##
# Spells


class DMF_219:
    """Relentless Pursuit"""

    # Give your hero +4 Attack and <b>Immune</b> this turn.
    play = Buff(FRIENDLY_HERO, "DMF_219e")


DMF_219e = buff(atk=4, immune=True)


class DMF_221:
    """Felscream Blast"""

    # <b>Lifesteal</b>. Deal $1 damage to a minion and its neighbors.
    play = Hit(TARGET, 1), Hit(TARGET_ADJACENT, 1)


class DMF_224:
    """Expendable Performers"""

    # Summon seven 1/1 Illidari with <b>Rush</b>. If_they all die this turn,
    # summon seven more.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = (Summon(CONTROLLER, "BT_036t") * 7).then(
        StoringBuff(SELF, "DMF_224e", Summon.CARD)
    )


class DMF_224e:
    update = Find(FRIENDLY_MINIONS + STORE_CARD) | (
        Summon(CONTROLLER, "BT_036t") * 7,
        Destroy(SELF),
    )


class DMF_225:
    """Throw Glaive"""

    # Deal $2 damage to a minion. If it dies, add a_temporary copy of this to
    # your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), Dead(TARGET) & Give(CONTROLLER, Copy(SELF)).then(
        GiveTemporary(Give.CARD)
    )


class DMF_249:
    """Acrobatics"""

    # Draw 2 cards. If you play both this turn, draw 2 more.
    play = (Draw(CONTROLLER) * 2).then(StoringBuff(SELF, "DMF_249e", Draw.CARD))


class DMF_249e:
    update = (Count(CARDS_PLAYED_THIS_TURN + STORE_CARD) == 2) & (
        Draw(CONTROLLER) * 2,
        Destroy(SELF),
    )


class YOP_001:
    """Illidari Studies"""

    # <b>Discover</b> an <b>Outcast</b> card. Your next one costs (1) less.
    play = (
        Discover(CONTROLLER, RandomCollectible(outcast=True)),
        Buff(CONTROLLER, "YOP_001e"),
    )


class YOP_001e:
    update = Refresh(FRIENDLY_HAND + OUTCAST, {GameTag.COST: -1})
    events = Play(CONTROLLER, OUTCAST).after(Destroy(SELF))


##
# Weapons


class DMF_227:
    """Dreadlord's Bite"""

    # [x]<b>Outcast:</b> Deal 1 damage to all enemies.
    outcast = Hit(ENEMY_CHARACTERS, 1)
