from ..utils import *

##
# Minions


class AV_114:
    """Shivering Sorceress"""

    # [x]<b>Battlecry:</b> Reduce the Cost of the highest Cost spell in your
    # hand by (1).
    play = Buff(RANDOM(HIGHEST_COST(FRIENDLY_HAND + SPELL)), "AV_114e")


class AV_114e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class AV_115:
    """Amplified Snowflurry"""

    # <b>Battlecry:</b> Your next Hero Power costs (0) and <b>Freezes</b> the
    # target.
    play = Buff(CONTROLLER, "AV_115e5")


class AV_115e5:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})
    events = Activate(FRIENDLY_HERO_POWER).after(Freeze(Activate.TARGET), Destroy(SELF))


class AV_284:
    """Balinda Stonehearth"""

    # <b>Battlecry:</b> Draw 2 spells. Swap their Costs with this minion's
    # stats.
    def play(self):
        spells = RANDOM(FRIENDLY_DECK + SPELL, 2).eval(self.game, self)
        yield ForceDraw(spells)
        if len(spells) == 1:
            spell = spells[0]
            # Swap the cost of the spell with this minion's atk
            spell_buff = self.controller.card("AV_284e")
            spell_buff._xcost = self.atk
            atk_buff = self.controller.card("AV_284e2")
            atk_buff._xatk = spell.cost
            yield Buff(spell, spell_buff)
            yield Buff(self, atk_buff)
        elif len(spells) == 2:
            spell1, spell2 = spells
            spell1_buff = self.controller.card("AV_284e")
            spell1_buff._xcost = self.atk
            spell2_buff = self.controller.card("AV_284e")
            spell2_buff._xcost = self.health
            atk_buff = self.controller.card("AV_284e2")
            atk_buff._xatk = spell1.cost
            health_buff = self.controller.card("AV_284e3")
            health_buff._xhealth = spell2.cost
            yield Buff(spell1, spell1_buff)
            yield Buff(spell2, spell2_buff)
            yield Buff(self, atk_buff)
            yield Buff(self, health_buff)


class AV_284e:
    """Arcane Swap"""

    # Cost swapped.
    cost = lambda self, _: self._xcost
    events = REMOVED_IN_PLAY


class AV_284e2:
    """Magical Shift"""

    # Swapped Attack.
    atk = lambda self, _: self._xatk


class AV_284e3:
    """Magical Shift"""

    # Swapped Health.
    max_health = lambda self, _: self._xhealth


class ONY_007:
    """Haleh, Matron Protectorate"""

    # After you cast a spell, deal 4 damage randomly split among all enemies.
    events = OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1) * 4)


##
# Spells


class AV_212:
    """Siphon Mana"""

    # Deal $2 damage. <b>Honorable Kill</b>: Reduce the Cost of spells in your
    # hand by (1).
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2)
    honorable_kill = Buff(FRIENDLY_HAND + SPELL, "AV_212e")


class AV_212e:
    tags = {GameTag.COST: SET(1)}
    events = REMOVED_IN_PLAY


class AV_218:
    """Mass Polymorph"""

    # Transform all minions into 1/1 Sheep.
    play = Morph(ALL_MINIONS, "AV_218t")


class AV_116:
    """Arcane Brilliance"""

    # Add a copy of a 7, 8, 9, and 10-Cost spell in your deck to your hand.
    play = (
        Give(CONTROLLER, Copy(RANDOM(FRIENDLY_DECK + SPELL + (COST == cost))))
        for cost in (7, 8, 9, 10)
    )


class AV_282:
    """Build a Snowman"""

    # Summon a 3/3 Snowman that <b>Freezes</b>. Add "Build a Snowbrute" to your
    # hand._
    play = Summon(CONTROLLER, "AV_282t"), Give(CONTROLLER, "AV_282t2")


class AV_282t:
    """Snowman"""

    # <b>Freeze</b> any character damaged by this minion.
    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class AV_282t2:
    """Build a Snowbrute"""

    # Summon a 6/6 Snowbrute that <b>Freezes</b>. Add "Build a Snowgre" to your
    # hand._
    play = Summon(CONTROLLER, "AV_282t3"), Give(CONTROLLER, "AV_282t4")


class AV_282t3:
    """Snowbrute"""

    # <b>Freeze</b> any character damaged by this minion.
    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class AV_282t4:
    """Build a Snowgre"""

    # Summon a 9/9 Snowgre that <b>Freezes</b>.
    play = Summon(CONTROLLER, "AV_282t5")


class AV_282t5:
    """Snowgre"""

    # <b>Freeze</b> any character damaged by this minion.
    events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class AV_283:
    """Rune of the Archmage"""

    # [x]Cast 20 Mana worth of Mage spells at enemies.
    def play(self):
        total = 20
        while total > 0:
            spell = RandomSpell(
                card_class=CardClass.MAGE, cost=range(total + 1)
            ).evaluate(self)[0]
            total -= spell.cost
            yield CastSpellTargetsEnemiesIfPossible(spell)


class AV_290:
    """Iceblood Tower"""

    # [x]At the end of your turn, cast another spell from your deck. Lasts 3
    # turns.
    events = OWN_TURN_END.on(CastSpell(RANDOM(FRIENDLY_DECK + SPELL - ID("AV_290"))))


class ONY_006:
    """Deep Breath"""

    # [x]Deal $@ damage to a minion and its neighbors. <i>(Improved by number
    # of_ other spells in your hand.)</i>
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = (
        Hit(TARGET, Count(FRIENDLY_HAND + SPELL - SELF) + 1),
        Hit(TARGET_ADJACENT, Count(FRIENDLY_HAND + SPELL - SELF) + 1),
    )


class ONY_029:
    """Drakefire Amulet"""

    # <b>Tradeable</b> <b>Discover</b> 2 Dragons. Summon them.
    play = (
        Discover(CONTROLLER, RandomDragon()).then(Summon(CONTROLLER, Discover.CARD)) * 2
    )


##
# Heros


class AV_200:
    """Magister Dawngrasp"""

    # [x]<b>Battlecry:</b> Recast a spell from each spell school you've cast
    # this game.
    play = (
        CastSpell(RANDOM(CARDS_PLAYED_THIS_GAME + SPELL + EnumSelector(school)))
        for school in SPELL_SCHOOLS
    )


class AV_200p2:
    """Arcane Burst"""

    # [x]<b>Hero Power</b> Deal $@ damage. <b>Honorable Kill:</b> Gain +2
    # damage.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def activate(self):
        yield Hit(TARGET, self.data_num_1)

    def honorable_kill(self, target):
        self.data_num_1 += 2
