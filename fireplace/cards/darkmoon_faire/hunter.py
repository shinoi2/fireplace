from ..utils import *

##
# Minions


class DMF_083:
    """Dancing Cobra"""

    # <b>Corrupt:</b> Gain <b>Poisonous</b>.
    corrupt_card = "DMF_083t"


class DMF_085:
    """Darkmoon Tonk"""

    # <b>Deathrattle:</b> Fire four  missiles at random enemies that deal 2
    # damage each.
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 2) * 4


class DMF_087:
    """Trampling Rhino"""

    # <b>Rush</b>. After this attacks and kills a minion, excess damage hits
    # the enemy hero.
    events = Attack(SELF, MINION).after(
        Dead(Attack.DEFENDER) & Hit(ENEMY_HERO, -CURRENT_HEALTH(Attack.DEFENDER))
    )


class DMF_089:
    """Maxima Blastenheimer"""

    # [x]<b>Battlecry:</b> Summon a minion from your deck. It attacks the enemy
    # hero, then dies.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(
        Attack(Summon.CARD, ENEMY_HERO), Destroy(Summon.CARD)
    )


class DMF_122:
    """Mystery Winner"""

    # <b>Battlecry:</b> <b>Discover</b> a <b>Secret.</b>
    play = DISCOVER(RandomSpell(secret=True))


class YOP_028:
    """Saddlemaster"""

    # After you play a Beast, add_a random Beast to_your hand.
    events = Play(CONTROLLER, BEAST).after(Give(CONTROLLER, RandomBeast()))


class YOP_030:
    """Felfire Deadeye"""

    # Your Hero Power costs (1) less.
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: -1})


##
# Spells


class DMF_084:
    """Jewel of N'Zoth"""

    # Summon three friendly <b>Deathrattle</b> minions that died this game.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
        PlayReq.REQ_FRIENDLY_DEATHRATTLE_MINION_DIED_THIS_GAME: 0,
    }
    play = Summon(CONTROLLER, RANDOM(FRIENDLY + KILLED + MINION) * 3)


class DMF_086:
    """Petting Zoo"""

    # Summon a 3/3 Strider. Repeat for each <b>Secret</b> you control.
    play = Summon(CONTROLLER, "DMF_086e"), Summon(CONTROLLER, "DMF_086e") * Count(
        FRIENDLY_SECRETS
    )


class DMF_090:
    """Don't Feed the Animals"""

    # Give all Beasts in your hand +1/+1. <b>Corrupt:</b> Give them +2/+2
    # instead.
    play = Buff(FRIENDLY_HAND + BEAST, "DMF_090e")
    corrupt_card = "DMF_090t"


class DMF_090t:
    play = Buff(FRIENDLY_HAND + BEAST, "DMF_090e2")


DMF_090e = buff(+1, +1)


DMF_090e2 = buff(+2, +2)


class DMF_123:
    """Open the Cages"""

    # [x]<b>Secret:</b> When your turn starts, if you control two minions,
    # summon an Animal Companion.
    entourage = ["NEW1_032", "NEW1_033", "NEW1_034"]
    secret = OWN_TURN_BEGIN.on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, RandomEntourage()))
    )


class YOP_027:
    """Bola Shot"""

    # Deal $1 damage to a minion and $2 damage to its neighbors.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), Hit(TARGET_ADJACENT, 2)


##
# Weapons


class DMF_088:
    """Rinling's Rifle"""

    # After your hero attacks, <b>Discover</b> a <b>Secret</b> and cast it.
    events = Attack(FRIENDLY_HERO).after(
        DISCOVER(RandomSpell(secret=True)).then(CastSpell(Discover.CARD))
    )
