from ..utils import *

##
# Minions


class RLK_813:
    """Bonecaller"""

    # [x]<b>Taunt</b> <b>Deathrattle</b>: Resurrect a friendly Undead that died
    # this game.
    deathrattle = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + DEAD_MINIONS + UNDEAD)))


class RLK_814:
    """Crystalsmith Cultist"""

    # <b>Battlecry:</b> If you're holding a Shadow spell, gain +1/+1.
    play = Find(FRIENDLY_HAND + SPELL + SHADOW) & Buff(SELF, "RLK_814e")


class RLK_816:
    """Sister Svalna"""

    # <b>Battlecry:</b> <i>Permanently</i> add a Vision of Darkness to your
    # hand.
    play = Give(CONTROLLER, "RLK_816t3")


class RLK_822:
    """Haunting Nightmare"""

    tags = {GameTag.DEATHRATTLE: True}

    # [x]<b>Deathrattle:</b> Haunt a card in your hand. When you play it,
    # summon a 4/3 Soldier.
    def deathrattle(self):
        if self.controller.hand:
            card = self.game.random.choice(self.controller.hand)
            yield Buff(CONTROLLER, "RLK_822e2", store_card=card)


class RLK_832:
    """High Cultist Basaleph"""

    # <b>Battlecry:</b> Resurrect all friendly Undead that died after your last
    # turn.
    play = Summon(CONTROLLER, Copy(RECENT_FRIENDLY_UNDEAD_DEATHS))


class NX2_018:
    """Rotting Necromancer"""

    # <b>Battlecry:</b> <b>Dredge.</b> If it's an Undead, deal 5 damage to the
    # enemy hero.
    play = Dredge(CONTROLLER).then(Find(Dredge.CARD + UNDEAD) & Hit(ENEMY_HERO, 5))


class RLK_845:
    """Mind Eater"""

    # <b>Deathrattle:</b> Add a copy of a card in your opponent's deck to your
    # hand.
    deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


##
# Spells


class RLK_812:
    """Animate Dead"""

    # Resurrect a friendly minion that costs (3) or less.
    play = Summon(
        CONTROLLER,
        Copy(RANDOM(FRIENDLY + DEAD_MINIONS + (COST <= 3))),
    )


class RLK_815:
    """Shadow Word: Undeath"""

    # Deal $2 damage to all enemies. If a friendly Undead died after your last
    # turn, deal $2 more.
    play = FRIENDLY_UNDEAD_DIED & Hit(ENEMY_CHARACTERS, 4) | Hit(ENEMY_CHARACTERS, 2)


class RLK_823:
    """Undying Allies"""

    # After you play an Undead this turn, give it <b>Reborn</b>.
    play = Buff(CONTROLLER, "RLK_823e")


class RLK_829:
    """Grave Digging"""

    # [x]Draw 2 cards. Costs (1) if a friendly Undead died after your last
    # turn.
    cost_mod = FRIENDLY_UNDEAD_DIED & -3
    play = Draw(CONTROLLER) * 2


class NX2_019:
    """Mind Sear"""

    # Deal $2 damage to a minion. If it dies, deal $3 damage to the enemy hero.
    requirements = MINION_TARGET
    play = Hit(TARGET, 2), Dead(TARGET) & Hit(ENEMY_HERO, 3)


class NX2_020:
    """Cannibalize"""

    # Destroy a minion. Restore its Health to all friendly characters.
    requirements = MINION_TARGET
    play = Destroy(TARGET), Heal(FRIENDLY_CHARACTERS - TARGET, CURRENT_HEALTH(TARGET))


class RLK_816t3:
    play = Give(CONTROLLER, "RLK_816t3"), DISCOVER(
        RandomSpell(spell_school=SpellSchool.SHADOW)
    )


class RLK_822e2:
    def haunt(self, player, card, target):
        haunted = self.store_card
        while haunted.morphed is not None:
            haunted = haunted.morphed
        if card is haunted:
            return [Summon(CONTROLLER, "RLK_822t"), Destroy(SELF)]

    events = OWN_CARD_PLAY.after(haunt)


class RLK_823e:
    tags = {GameTag.TAG_ONE_TURN_EFFECT: True}
    events = Play(CONTROLLER, MINION + UNDEAD).after(GiveReborn(Play.CARD))


RLK_814e = buff(1, 1)
