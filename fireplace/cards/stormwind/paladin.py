from ..utils import *

##
# Minions


class SW_305:
    """First Blade of Wrynn"""

    # [x]<b>Divine Shield</b> <b>Battlecry:</b> Gain <b>Rush</b> if this has at
    # least 4 Attack.
    play = (ATK(SELF) >= 4) & GiveRush(SELF)


class SW_315:
    """Alliance Bannerman"""

    # [x]<b>Battlecry:</b> Draw a minion. Give minions in your hand +1/+1.
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + MINION)),
        Buff(FRIENDLY_HAND + MINION, "SW_315e"),
    )


SW_315e = buff(+1, +1)


class SW_317:
    """Catacomb Guard"""

    # [x]<b>Lifesteal</b> <b>Battlecry:</b> Deal damage equal to this minion's
    # Attack to an enemy minion.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, ATK(SELF))


class SW_047:
    """Highlord Fordragon"""

    # [x]<b>Divine Shield</b> After a friendly minion loses <b>Divine
    # Shield</b>, give a minion __in your hand +5/+5.
    events = LosesDivineShield(FRIENDLY_MINIONS).after(
        Buff(RANDOM(FRIENDLY_HAND + MINION), "SW_047e")
    )


SW_047e = buff(+5, +5)


class DED_500:
    """Wealth Redistributor"""

    # [x]<b>Taunt</b>. <b>Battlecry:</b> Swap the Attack of the highest and
    # lowest Attack minion.
    play = SwapStateBuff(
        RANDOM(HIGHEST_ATK(ALL_MINIONS)), RANDOM(LOWEST_ATK(ALL_MINIONS)), "DED_500e"
    )


class DED_500e:
    atk = lambda self, i: self._xatk


class DED_501:
    """Sunwing Squawker"""

    # [x]<b>Battlecry:</b> Repeat the last spell you've cast on a __friendly
    # minion on this.
    play = CastSpell((CARDS_PLAYED_THIS_GAME + CAST_ON_FRIENDLY_MINIONS)[-1:], SELF)


##
# Spells


class SW_313:
    """Rise to the Occasion"""

    # <b>Questline:</b> Play 3 different 1-Cost cards. <b>Reward:</b> Equip a
    # 1/4 Light's Justice.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        if card not in self.entourage:
            self.entourage.append(card)

    quest = Play(CONTROLLER, COST == 1).on(AddProgress(SELF, Play.CARD))
    reward = Summon(CONTROLLER, "CS2_091"), Summon(CONTROLLER, "SW_313t")


class SW_313t:
    """Pave the Way"""

    # <b>Questline: </b> Play 3 different 1-Cost cards. <b>Reward:</b> Upgrade
    # your Hero Power.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        if card not in self.entourage:
            self.entourage.append(card)

    quest = Play(CONTROLLER, COST == 1).on(AddProgress(SELF, Play.CARD))
    reward = UPGRADE_HERO_POWER, Summon(CONTROLLER, "SW_313t2")


class SW_313t2(QuestRewardProtect):
    """Avenge the Fallen"""

    # <b>Questline:</b> Play 3 different 1-Cost cards. <b>Reward:</b> Lightborn
    # Cariel.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        if card not in self.entourage:
            self.entourage.append(card)

    quest = Play(CONTROLLER, COST == 1).on(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "SW_313t4")


class SW_313t4:
    """Lightborn Cariel"""

    # [x]<b>Battlecry:</b> For the rest of the game, your Silver Hand Recruits
    # have +2/+2.
    play = Buff(CONTROLLER, "SW_313t4e")


class SW_313t4e:
    update = Refresh(FRIENDLY_MINIONS + ID("CS2_101t"), buff="SW_313t4ee")


SW_313t4ee = buff(+2, +2)


class SW_046:
    """City Tax"""

    # [x]<b>Tradeable</b> <b>Lifesteal</b>. Deal $1 damage to all enemy
    # minions.
    play = Hit(ENEMY_MINIONS, 1)


class SW_316:
    """Noble Mount"""

    # G[x]ive a minion +1/+1 and <b>Divine Shield</b>. When it dies, summon a
    # Warhorse.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "SW_316e"), GiveDivineShield(TARGET)


class SW_316e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Summon(CONTROLLER, "SW_316t")


class SW_049:
    """Blessed Goods"""

    # <b>Discover</b> a <b>Secret</b>, weapon, or <b>Divine Shield</b> minion.
    play = GenericChoice(
        CONTROLLER,
        [RandomSpell(secret=True), RandomWeapon(), RandomMinion(divine_shield=True)],
    )


class DED_502:
    """Righteous Defense"""

    # Set a minion's Attack and Health to 1. Give the stats it lost to a minion
    # in your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }

    def play(self):
        atk = self.target.atk
        health = self.target.health
        yield Buff(TARGET, "DED_502e")
        yield Buff(
            RANDOM(FRIENDLY_HAND + MINION),
            "DED_502e2",
            atk=atk - 1,
            max_health=health - 1,
        )


class DED_502e:
    atk = SET(1)
    max_health = SET(1)


##
# Weapons


class SW_314:
    """Lightbringer's Hammer"""

    # <b>Lifesteal</b> Can't attack heroes.
    tags = {GameTag.CANNOT_ATTACK_HEROES: True}


class SW_048:
    """Prismatic Jewel Kit"""

    # [x]After a friendly minion loses <b>Divine Shield</b>, give minions in
    # your hand  +1/+1. Lose 1 Durability.
    events = LosesDivineShield(FRIENDLY_MINIONS).after(
        Buff(RANDOM(FRIENDLY_HAND + MINION), "SW_048e").then(Hit(SELF, 1))
    )


SW_048e = buff(+1, +1)
