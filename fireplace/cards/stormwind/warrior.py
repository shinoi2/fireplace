from ..utils import *

##
# Minions


class SW_021:
    """Cowardly Grunt"""

    # <b>Deathrattle:</b> Summon a minion from your deck.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))


class SW_024:
    """Lothar"""

    # At the end of your turn, attack a random enemy minion. If it dies, gain
    # +3/+3.
    events = OWN_TURN_END.on(
        Find(ENEMY_MINIONS)
        & Attack(SELF, RANDOM(ENEMY_MINIONS)).then(
            Dead(Attack.DEFENDER) & Buff(SELF, "SW_024e")
        )
    )


SW_024e = buff(+3, +3)


class SW_029:
    """Harbor Scamp"""

    # <b>Battlecry:</b> Draw a Pirate.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE + MINION))


class SW_030:
    """Cargo Guard"""

    # At the end of your turn, gain 3 Armor.
    events = OWN_TURN_END.on(GainArmor(FRIENDLY_HERO, 3))


class SW_093:
    """Stormwind Freebooter"""

    # <b>Battlecry:</b> Give your hero +2 Attack this turn.
    play = Buff(FRIENDLY_HERO, "SW_093e")


SW_093e = buff(atk=2)


class DED_519:
    """Defias Cannoneer"""

    # [x]After your hero attacks, deal 2 damage to a random enemy twice.
    events = Attack(FRIENDLY_HERO).after(
        Hit(RANDOM_ENEMY_CHARACTER, 2), Hit(RANDOM_ENEMY_CHARACTER, 2)
    )


class SW_097:
    """Remote-Controlled Golem"""

    # [x]After this takes damage, shuffle two Golem Parts into your deck. When
    # drawn, __summon a 2/1 Mech.
    events = SELF_DAMAGE.on(
        Shuffle(CONTROLLER, "SW_097t"), Shuffle(CONTROLLER, "SW_097t")
    )


class SW_097t:
    play = Summon(CONTROLLER, "skele21")


##
# Spells


class SW_023:
    """Provoke"""

    # [x]<b>Tradeable</b> Choose a friendly minion. Enemy minions attack it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        for attacker in ENEMY_MINIONS.eval(self.game, self):
            if attacker.dead:
                continue
            yield Attack(attacker, TARGET)


class SW_027:
    """Shiver Their Timbers!"""

    # Deal $2 damage to a minion. If you control a Pirate, deal $5 instead.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    powered_up = Find(FRIENDLY_MINIONS + PIRATE)
    play = powered_up & Hit(TARGET, 5) | Hit(TARGET, 2)


class SW_028:
    """Raid the Docks"""

    # [x]<b>Questline:</b> Play 3 Pirates. <b>Reward:</b> Draw a weapon.
    progress_total = 3
    quest = Play(CONTROLLER, PIRATE + MINION).after(AddProgress(SELF, Play.CARD))
    reward = (
        ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON)),
        Summon(CONTROLLER, "SW_028t"),
    )


class SW_028t:
    """Create a Distraction"""

    # [x]<b>Questline:</b> Play 2 Pirates. <b>Reward:</b> Deal $2 damage to a
    # random enemy twice.
    progress_total = 2
    quest = Play(CONTROLLER, PIRATE + MINION).after(AddProgress(SELF, Play.CARD))
    reward = (
        Hit(RANDOM_ENEMY_CHARACTER, 2),
        Hit(RANDOM_ENEMY_CHARACTER, 2),
        Summon(CONTROLLER, "SW_028t2"),
    )


class SW_028t2(QuestRewardProtect):
    """Secure the Supplies"""

    # [x]<b>Questline:</b> Play 2 Pirates. <b>Reward:</b> Cap'n Rokara.
    progress_total = 2
    quest = Play(CONTROLLER, PIRATE + MINION).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "SW_028t5")


class SW_028t5:
    """Cap'n Rokara"""

    # <b>Battlecry:</b> Summon The Juggernaut!
    play = Summon(CONTROLLER, "SW_028t6")


class SW_028t6:
    """The Juggernaut"""

    # [x]<b>Start of Your Turn:</b> Summon a Pirate, equip a Warrior weapon,
    # and fire two cannons that deal 2 damage!
    events = OWN_TURN_BEGIN.on(
        Summon(CONTROLLER, RandomMinion(race=Race.PIRATE)),
        Summon(CONTROLLER, RandomWeapon(card_class=CardClass.WARRIOR)),
        Hit(RANDOM_ENEMY_CHARACTER, 2),
        Hit(RANDOM_ENEMY_CHARACTER, 2),
    )


class SW_094:
    """Heavy Plate"""

    # <b>Tradeable</b> Gain 8 Armor.
    play = GainArmor(FRIENDLY_HERO, 8)


class DED_518:
    """Man the Cannons"""

    # Deal $3 damage to a minion and $1 damage to all other minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Hit(ENEMY_MINIONS - TARGET, 1)


##
# Weapons


class DED_527:
    """Blacksmithing Hammer"""

    # [x]<b>Tradeable</b> After you <b>Trade</b> this, _gain +2 Durability.
    trade = Buff(SELF, "DED_527e")


DED_527e = buff(health=2)
