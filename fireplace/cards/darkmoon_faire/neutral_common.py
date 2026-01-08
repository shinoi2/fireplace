from ..utils import *


##
# Minions


class DMF_062:
    """Gyreworm"""

    # <b>Battlecry:</b> If you played an Elemental last turn, deal 3_damage.
    requirements = {
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABE_AND_ELEMENTAL_PLAYED_LAST_TURN: 0,
    }
    play = Hit(TARGET, 3)


class DMF_065:
    """Banana Vendor"""

    # <b>Battlecry:</b> Add 2 Bananas to each player's hand.
    play = (Give(CONTROLLER, "DMF_065t") * 2, Give(OPPONENT, "DMF_065t") * 2)


class DMF_065t:
    play = Buff(TARGET, "DMF_065e")


DMF_065e = buff(+1, +1)


class DMF_066:
    """Knife Vendor"""

    # <b>Battlecry:</b> Deal 4 damage to each hero.
    play = Hit(ENEMY_HERO, 4), Hit(FRIENDLY_HERO, 4)


class DMF_067:
    """Prize Vendor"""

    # <b>Battlecry:</b> Each player draws a card.
    play = Draw(CONTROLLER), Draw(OPPONENT)


class DMF_068:
    """Optimistic Ogre"""

    # 50% chance to attack the correct enemy.
    events = FORGETFUL


class DMF_069:
    """Claw Machine"""

    # <b>Rush</b>. <b>Deathrattle:</b> Draw a minion and give it +3/+3.
    deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
        Buff(ForceDraw.TARGET, "DMF_069e")
    )


DMF_069e = buff(+3, +3)


class DMF_073:
    """Darkmoon Dirigible"""

    # <b>Divine Shield</b> <b>Corrupt:</b> Gain <b>Rush</b>.
    corrupt_card = "DMF_073t"


class DMF_078:
    """Strongman"""

    # <b>Taunt</b> <b>Corrupt:</b> This costs (0).
    corrupt_card = "DMF_078t"


class DMF_079:
    """Inconspicuous Rider"""

    # <b>Battlecry:</b> Cast a <b>Secret</b> from your deck.
    play = CastSpell(RANDOM(FRIENDLY_DECK + SECRET))


class DMF_080:
    """Fleethoof Pearltusk"""

    # <b>Rush</b> <b>Corrupt:</b> Gain +4/+4.
    corrupt_card = "DMF_080t"


class DMF_082:
    """Darkmoon Statue"""

    # Your other minions have +1 Attack. <b>Corrupt:</b> This gains +4 Attack.
    update = Refresh(FRIENDLY_MINIONS, buff="DMF_082e")
    corrupt_card = "DMF_082t"


class DMF_082t:
    update = Refresh(FRIENDLY_MINIONS, buff="DMF_082e")


DMF_082e = buff(atk=1)


class DMF_091:
    """Wriggling Horror"""

    # <b>Battlecry:</b> Give adjacent minions +1/+1.
    play = Buff(SELF_ADJACENT, "DMF_091e2")


DMF_091e2 = buff(+1, +1)


class DMF_174:
    """Circus Medic"""

    # <b>Battlecry:</b> Restore #4 Health. <b>Corrupt:</b> Deal 4 damage
    # instead.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Heal(TARGET, 4)
    corrupt_card = "DMF_174t"


class DMF_174t:
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 4)


class DMF_189:
    """Costumed Entertainer"""

    # [x]<b>Battlecry:</b> Give a random minion in your hand +2/+2.
    play = Buff(RANDOM(FRIENDLY_HAND + MINION), "DMF_189e")


DMF_189e = buff(+2, +2)


class DMF_191:
    """Showstopper"""

    # <b>Deathrattle:</b> <b>Silence</b> all_minions.
    deathrattle = Silence(ALL_MINIONS)


class DMF_520:
    """Parade Leader"""

    # After you summon a <b>Rush</b> minion, give it +2 Attack.
    events = Summon(CONTROLLER, RUSH).after(Buff(Summon.CARD, "DMF_520e"))


DMF_520e = buff(atk=2)
