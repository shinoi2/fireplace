from ..utils import *

##
# Minions


class RLK_029:
    """Shatterskin Gargoyle"""

    # <b>Taunt</b> <b>Deathrattle:</b> Deal 4 damage to a random enemy.
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 4)


class RLK_070:
    """Infected Peasant"""

    # <b>Deathrattle:</b> Summon a 2/2 Undead Peasant.
    deathrattle = Summon(CONTROLLER, "RLK_070t")


class RLK_104:
    """Street Sweeper"""

    # <b>Battlecry:</b> Deal 2 damage to all other minions.
    play = Hit(ALL_MINIONS - SELF, 2)


class RLK_113:
    """Brittleskin Zombie"""

    # <b>Deathrattle:</b> If it's your opponent's turn, deal 3 damage to them.
    deathrattle = CurrentPlayer(OPPONENT) & Hit(ENEMY_HERO, 3)


class RLK_117:
    """Incorporeal Corporal"""

    # After this minion attacks, destroy it.
    events = Attack(SELF).after(Destroy(SELF))


class RLK_119:
    """Drakkari Embalmer"""

    # <b>Battlecry:</b> Give a friendly Undead <b>Reborn</b>.
    requirements = FRIENDLY_UNDEAD_BATTLECRY
    play = GiveReborn(TARGET)


class RLK_123:
    """Bone Flinger"""

    # [x]<b>Battlecry:</b> If a friendly Undead died after your last turn, deal
    # 2 damage.
    requirements = {enums.REQ_TARGET_IF_AVAILABLE_AND_FRIENDLY_UNDEAD_DIED: 0}
    powered_up = FRIENDLY_UNDEAD_DIED
    play = powered_up & Hit(TARGET, 2)


class RLK_900:
    """Scourge Rager"""

    # <b>Reborn</b> <b>Battlecry:</b> Die.
    play = Destroy(SELF)


class RLK_518:
    """Silvermoon Sentinel"""

    # <b>Taunt</b> <b>Manathirst (@):</b> Gain +2/+2 and <b>Divine Shield</b>.
    play = Manathirst(8) & (Buff(SELF, "RLK_518e"), GiveDivineShield(SELF))


class RLK_914:
    """Umbral Geist"""

    # [x]<b>Deathrattle:</b> Add a random Shadow spell to your hand.
    deathrattle = Give(CONTROLLER, RandomSpell(spell_school=SpellSchool.SHADOW))


class RLK_824:
    """Arms Dealer"""

    # After you summon an Undead, give it +1 Attack.
    events = Summon(CONTROLLER, UNDEAD + MINION).after(Buff(Summon.CARD, "RLK_824e"))


class RLK_915:
    """Amber Whelp"""

    # <b>Battlecry:</b> If you're holding a Dragon, deal 3 damage.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0}
    play = HOLDING_DRAGON & Hit(TARGET, 3)


class RLK_926:
    """Bloodied Knight"""

    # [x]At the end of your turn, deal 2 damage to your hero.
    events = OWN_TURN_END.on(Hit(FRIENDLY_HERO, 2))


class RLK_833:
    """Foul Egg"""

    # <b>Deathrattle:</b> Summon a 3/3 Undead Chicken.
    deathrattle = Summon(CONTROLLER, "RLK_833t")


class RLK_834:
    """Nerubian Vizier"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a spell. If a friendly Undead died
    # after your last turn, it costs (2) less.
    play = Discover(CONTROLLER, RandomSpell()).then(
        FRIENDLY_UNDEAD_DIED & Buff(Discover.CARD, "RLK_834e"),
        Give(CONTROLLER, Discover.CARD),
    )


class RLK_955:
    """Silvermoon Armorer"""

    # [x]<b>Rush</b> <b>Manathirst (@):</b> Gain +2/+2.
    play = Manathirst(7) & Buff(SELF, "RLK_955e")


class RLK_218:
    """Silvermoon Arcanist"""

    # [x]<b>Spell Damage +2</b> <b>Battlecry:</b> Your spells can’t target
    # heroes this turn.
    play = Buff(CONTROLLER, "RLK_218e3")


class RLK_219:
    """Sunfury Clergy"""

    # [x]<b>Battlecry:</b> Restore 3 Health to all friendly characters.
    # <b>Manathirst (6):</b> Restore 6 Health instead.
    play = Manathirst(6) & Heal(FRIENDLY_CHARACTERS, 6) | Heal(FRIENDLY_CHARACTERS, 3)


class RLK_867:
    """Vrykul Necrolyte"""

    # [x]<b>Battlecry:</b> Give a friendly minion "<b>Deathrattle:</b> Summon a
    # 2/2 Zombie with <b>Rush</b>."
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "RLK_867e")


class NX2_050:
    """Mistake"""

    tags = {GameTag.CARDRACE: Race.ALL}


class NX2_051:
    """Darkfallen Shadow"""

    # <b>Rush</b> <b>Manathirst (@):</b> Gain <b>Reborn</b>.
    play = Manathirst(6) & GiveReborn(SELF)


RLK_518e = RLK_955e = buff(2, 2)
RLK_824e = buff(atk=1)
RLK_834e = buff(cost=-2)


class RLK_218e3:
    tags = {GameTag.TAG_ONE_TURN_EFFECT: True}
    update = Refresh(CONTROLLER, {enums.SPELLS_CANT_TARGET_HEROES: True})


class RLK_867e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "RLK_018t")
