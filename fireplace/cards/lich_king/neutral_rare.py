from ..utils import *

##
# Minions


class RLK_830:
    """Flesh Behemoth"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Draw another Undead and summon a copy
    # of it.
    deathrattle = FORCE_DRAW(UNDEAD + MINION - ID("RLK_830")).then(
        Summon(CONTROLLER, ExactCopy(ForceDraw.TARGET))
    )


class RLK_653:
    """Infectious Ghoul"""

    # [x]<b>Deathrattle:</b> Give a random friendly minion "<b>Deathrattle:</b>
    # Summon an Infectious Ghoul."
    deathrattle = Buff(RANDOM(FRIENDLY_MINIONS - DEAD), "RLK_653e")


class RLK_950:
    """Translocation Instructor"""

    # [x]<b>Battlecry:</b> Choose an enemy minion. Swap it with a random one in
    # their deck.
    requirements = ENEMY_MINION_BATTLECRY
    play = Swap(TARGET, RANDOM(ENEMY_DECK + MINION))


class RLK_951:
    """Coroner"""

    # <b>Battlecry:</b> <b>Freeze</b> an enemy minion. <b>Manathirst (6):</b>
    # <b>Silence</b> it first.
    requirements = ENEMY_MINION_BATTLECRY
    play = Manathirst(6) & Silence(TARGET), Freeze(TARGET)


class RLK_957:
    """Banshee"""

    # <b>Deathrattle:</b> Give a random friendly Undead +2/+1.
    deathrattle = Buff(RANDOM(FRIENDLY_MINIONS + UNDEAD - DEAD), "RLK_957e")


class RLK_220:
    """Tenacious San'layn"""

    # <b>Lifesteal</b> Whenever this attacks, deal 2 damage to the enemy hero.
    events = Attack(SELF).on(Hit(ENEMY_HERO, 2))


class NX2_032:
    """Lost Exarch"""

    # [x]<b>Deathrattle</b>: Spend all your Mana. Summon that many _2/2 Zombies
    # with <b>Rush</b>.
    def deathrattle(self):
        player = self.controller
        mana = player.mana
        yield SpendMana(player, mana)
        yield Summon(player, "NX2_032t") * mana


class RLK_653e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "RLK_653")


RLK_957e = buff(2, 1)
