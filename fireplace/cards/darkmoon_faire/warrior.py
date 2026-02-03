from ..utils import *

##
# Minions


class DMF_521:
    """Sword Eater"""

    # <b>Taunt</b> <b>Battlecry:</b> Equip a 3/2_Sword.
    play = Summon(CONTROLLER, "DMF_521t")


class DMF_523:
    """Bumper Car"""

    # <b>Rush</b> <b>Deathrattle:</b> Add two 1/1 Riders with <b>Rush</b>
    # to_your hand.
    deathrattle = Give(CONTROLLER, "DMF_523t") * 2


class DMF_525:
    """Ringmaster Whatley"""

    # <b>Battlecry:</b> Draw a Mech, Dragon, and Pirate.
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MECH)),
        ForceDraw(RANDOM(FRIENDLY_DECK + DRAGON)),
        ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE)),
    )


class DMF_528:
    """Tent Trasher"""

    # <b><b>Rush</b>.</b> Costs (1) less for each friendly minion with a unique
    # minion type.
    cost_mod = -Count(UniqueRace(FRIENDLY_MINIONS))


class DMF_529:
    """E.T.C., God of Metal"""

    # After a friendly <b>Rush</b> minion attacks, deal 2 damage to the enemy
    # hero.
    events = Attack(FRIENDLY_MINIONS + RUSH).after(Hit(ENEMY_HERO, 2))


class DMF_531:
    """Stage Hand"""

    # [x]<b>Battlecry:</b> Give a random minion in your hand +1/+1.
    play = Buff(RANDOM(FRIENDLY_HAND + MINION), "DMF_531e")


DMF_531e = buff(+1, +1)


class YOP_014:
    """Ironclad"""

    # <b>Battlecry:</b> If your hero has Armor, gain +2/+2.
    powered_up = ARMOR(FRIENDLY_HERO) > 0
    play = powered_up & Buff(SELF, "YOP_014e")


##
# Spells


class DMF_522:
    """Minefield"""

    # Deal $5 damage randomly split among all minions.
    play = Hit(RANDOM_MINION, 1) * SPELL_DAMAGE(5)


class DMF_526:
    """Stage Dive"""

    # Draw a <b>Rush</b> minion. <b>Corrupt:</b> Give it +2/+1.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + RUSH))
    corrupt_card = "DMF_526t"


class DMF_526t:
    play = ForceDraw(RANDOM(FRIENDLY_DECK + RUSH)).then(
        Buff(ForceDraw.TARGET, "DMF_526e")
    )


DMF_526e = buff(+2, +1)


class DMF_530:
    """Feat of Strength"""

    # Give a random <b>Taunt</b> minion in your hand +5/+5.
    play = Buff(RANDOM(FRIENDLY_HAND + MINION + TAUNT), "DMF_530e")


DMF_530e = buff(+5, +5)


##
# Weapons


class DMF_524:
    """Ringmaster's Baton"""

    # After your hero attacks, give a Mech, Dragon, and Pirate in your hand
    # +1/+1.
    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_HAND + MECH), "DMF_524e"),
        Buff(RANDOM(FRIENDLY_HAND + DRAGON), "DMF_524e"),
        Buff(RANDOM(FRIENDLY_HAND + PIRATE), "DMF_524e"),
    )


DMF_524e = buff(+1, +1)


class YOP_013:
    """Spiked Wheel"""

    # Has +3 Attack while your hero has Armor.
    update = (ARMOR(FRIENDLY_HERO) > 0) & Buff(SELF, "YOP_013e")


YOP_013e = buff(atk=3)
