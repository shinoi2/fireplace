from ..utils import *

##
# Minions


class BAR_307:
    """Void Flayer"""

    # [x]<b>Battlecry:</b> For each spell in your hand, deal 1 damage to a
    # random enemy minion.
    play = Hit(RANDOM(ENEMY_MINIONS), 1) * Count(FRIENDLY_HAND + SPELL)


class BAR_310:
    """Lightshower Elemental"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Restore #8 Health to all friendly
    # characters.
    deathrattle = Heal(FRIENDLY_CHARACTERS, 8)


class BAR_312:
    """Soothsayer's Caravan"""

    # At the start of your turn, copy a spell from your opponent's deck to your
    # hand.
    events = OWN_TURN_BEGIN.on(Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK + SPELL))))


class BAR_313:
    """Priest of An'she"""

    # <b>Taunt</b>. <b>Battlecry:</b> If you've restored Health this turn, gain
    # +3/+3.
    powered_up = Attr(CONTROLLER, "healed_this_turn") > 0
    play = powered_up & Buff(SELF, "BAR_313e")


BAR_313e = buff(+3, +3)


class BAR_315:
    """Serena Bloodfeather"""

    # <b>Battlecry:</b> Choose an enemy minion. Steal Attack and Health from it
    # until this has more.
    def play(self):
        target = self.target
        while self.atk <= target.atk:
            yield Buff(self, "BAR_315e1")
            yield Buff(target, "BAR_315e3")
        while self.health <= target.health:
            yield Buff(self, "BAR_315e2")
            yield Buff(target, "BAR_315e4")


BAR_315e1 = buff(atk=1)
BAR_315e2 = buff(health=1)
BAR_315e3 = buff(atk=-1)
BAR_315e4 = buff(health=-1)


class BAR_735:
    """Xyrella"""

    # <b>Battlecry:</b> If you've restored Health this turn, deal that much
    # damage to all enemy minions.
    powered_up = Attr(CONTROLLER, "healed_this_turn") > 0
    play = powered_up & Hit(ENEMY_MINIONS, Attr(CONTROLLER, "healed_this_turn"))


class WC_013:
    """Devout Dungeoneer"""

    # [x]<b>Battlecry:</b> Draw a spell. If it's a Holy spell, reduce its Cost
    # by (2).
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)).then(
        Find(ForceDraw.TARGET + HOLY) & Buff(ForceDraw.TARGET, "WC_013e")
    )


class WC_013e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class WC_803:
    """Cleric of An'she"""

    # <b>Battlecry:</b> If you've restored Health this turn, <b>Discover</b> a
    # spell from your deck.
    powered_up = Attr(CONTROLLER, "healed_this_turn") > 0
    play = powered_up & GenericChoice(CONTROLLER, RANDOM(FRIENDLY_DECK + SPELL, 3))


##
# Spells


class BAR_308:
    """Power Word: Fortitude"""

    # Give a minion +3/+5. Costs (1) less for each spell in your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    cost_mod = -Count(FRIENDLY_HAND + SPELL)
    play = Buff(TARGET, "BAR_308e")


BAR_308e = buff(+3, +5)


class BAR_309:
    """Desperate Prayer"""

    # Restore #5 Health to each hero.
    play = Heal(ALL_HEROES, 5)


class BAR_311:
    """Devouring Plague"""

    # [x]<b>Lifesteal</b>. Deal $4 damage randomly split among all enemy
    # minions.
    play = Hit(RANDOM(ENEMY_MINIONS, 1)) * SPELL_DAMAGE(4)


class BAR_314:
    """Condemn (Rank 1)"""

    # [x]Deal $1 damage to all enemy minions. <i>(Upgrades when you have 5
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_314t")

    play = Hit(ENEMY_MINIONS, 1)


class BAR_314t:
    """Condemn (Rank 2)"""

    # [x]Deal $2 damage to all enemy minions. <i>(Upgrades when you have 10
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_314t2")

    play = Hit(ENEMY_MINIONS, 2)


class BAR_314t2:
    """Condemn (Rank 3)"""

    # Deal $3 damage to all enemy minions.
    play = Hit(ENEMY_MINIONS, 3)


class WC_014:
    """Against All Odds"""

    # Destroy ALL odd-Attack minions.
    def play(self):
        all_minions = ALL_MINIONS.eval(self.game, self)
        for minion in all_minions:
            if minion.atk % 2 == 1:
                yield Destroy(minion)
