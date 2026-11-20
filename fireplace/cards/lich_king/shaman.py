from ..utils import *

##
# Minions


class RLK_912:
    """Scourge Troll"""

    # <b>Deathrattles</b> given to this minion trigger twice.
    tags = {enums.EXTRA_GRANTED_DEATHRATTLES: True}


class RLK_913:
    """Overlord Drakuru"""

    # [x]<b>Rush</b>, <b>Windfury</b> After this attacks and kills a minion,
    # resurrect it on your side.
    events = Attack(SELF, ALL_MINIONS).after(
        Dead(Attack.DEFENDER) & Summon(CONTROLLER, Copy(Attack.DEFENDER))
    )


class RLK_550:
    """Rotgill"""

    # [x]<b>Battlecry:</b> Give your other minions "<b>Deathrattle:</b> Give
    # __your minions +1/+1."
    play = Buff(FRIENDLY_MINIONS - SELF, "RLK_550e")


class RLK_551:
    """Blightblood Berserker"""

    # <b>Taunt</b>, <b>Lifesteal</b>, <b>Reborn</b> <b>Deathrattle:</b> Deal 3
    # damage to a random enemy.
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 3)


class RLK_552:
    """Unliving Champion"""

    # [x]<b>Battlecry:</b> If a friendly Undead died after your last turn,
    # summon two 3/2 Zombies.
    play = FRIENDLY_UNDEAD_DIED & (Summon(CONTROLLER, "RLK_909t") * 2)


class RLK_554:
    """Harkener of Dread"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a 6/6 Undead with
    # <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "RLK_554t")


class NX2_007:
    """Frostfin Chomper"""

    # [x]<b>Battlecry:</b> If you played an Elemental last turn, summon three
    # 1/1 Murlocs.
    play = ELEMENTAL_PLAYED_LAST_TURN & (Summon(CONTROLLER, "NX2_007t") * 3)


##
# Spells


class RLK_909:
    """Deathweaver Aura"""

    # Give a minion "<b>Deathrattle:</b> Summon two 3/2 Zombies."
    # <b>Overload:</b> (1)
    requirements = MINION_TARGET
    play = Buff(TARGET, "RLK_909e")


class RLK_910:
    """Shadow Suffusion"""

    # [x]Give your minions "<b>Deathrattle:</b> Deal 3 damage to a random
    # enemy."
    play = Buff(FRIENDLY_MINIONS, "RLK_910e")


class RLK_911:
    """From De Other Side"""

    # Summon a copy of each minion in your hand. They attack random enemy
    # minions, then die.
    def play(self):
        player = self.controller
        copies = ExactCopy(FRIENDLY_HAND + MINION).evaluate(self)
        summoned = []
        for minion in copies:
            if not player.minion_slots:
                break
            yield Summon(player, minion)
            if minion.zone == Zone.PLAY:
                summoned.append(minion)
        for minion in summoned:
            if minion.zone == Zone.PLAY and not minion.dead and minion.atk:
                yield Attack(minion, RANDOM_ENEMY_MINION)
                self.game.process_deaths()
        yield Destroy([minion for minion in summoned if minion.zone == Zone.PLAY])


class RLK_553:
    """Prescience"""

    # Draw 2 minions. For each that costs (5) or more, summon a_ 2/3 Spirit
    # with <b>Taunt</b>.
    play = (
        FORCE_DRAW(MINION).then(
            (COST(ForceDraw.TARGET) >= 5) & Summon(CONTROLLER, "RLK_553t")
        )
        * 2
    )


class NX2_008:
    """Blazing Transmutation"""

    # [x]Choose a minion. <b>Discover</b> one that costs (1) more to transform
    # it into.
    requirements = MINION_TARGET
    play = Discover(
        CONTROLLER, RandomMinion(cost=COST(TARGET) + 1, card_class=list(CardClass)[1:])
    ).then(Morph(TARGET, Discover.CARD))


class NX2_009:
    """Cold Storage"""

    # <b>Freeze</b> a minion. Add a copy of it to your hand.
    requirements = MINION_TARGET
    play = Freeze(TARGET), Give(CONTROLLER, Copy(TARGET))


class RLK_550e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Buff(FRIENDLY_MINIONS, "RLK_550e2")


RLK_550e2 = buff(1, 1)


class RLK_909e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(Controller(OWNER), "RLK_909t") * 2


class RLK_910e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 3)
