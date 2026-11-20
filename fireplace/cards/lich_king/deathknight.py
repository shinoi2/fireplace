from ..utils import *

##
# Minions


class RLK_116:
    """Necrotic Mortician"""

    # <b>Battlecry:</b> If a friendly Undead died after your last turn,
    # <b>Discover</b> an Unholy Rune card.
    play = FRIENDLY_UNDEAD_DIED & DISCOVER(
        RandomCollectible(
            card_class=CardClass.DEATHKNIGHT,
            cost_unholy=range(1, 3),
        )
    )


class RLK_120:
    """Meat Grinder"""

    # <b>Battlecry:</b> Shred a random minion in your deck to gain 4
    # <b>Corpses.</b>
    play = Remove(RANDOM(FRIENDLY_DECK + MINION)).then(GainCorpses(CONTROLLER, 4))


class RLK_121:
    """Acolyte of Death"""

    # After a friendly Undead dies, draw a card.
    events = Death(FRIENDLY + MINION + UNDEAD).after(Draw(CONTROLLER))


class RLK_706:
    """Alexandros Mograine"""

    # <b>Battlecry:</b> For the rest of the game, deal 3 damage to your
    # opponent at the end of your turns.
    play = Buff(CONTROLLER, "RLK_706e3")


class RLK_506:
    """Boneguard Commander"""

    # <b>Taunt</b> <b>Battlecry:</b> Raise up to 6 <b>Corpses</b> as 1/3 Risen
    # Footmen with <b>Taunt</b>.
    play = RaiseCorpses(CONTROLLER, 6, "RLK_061t")


class RLK_741:
    """Soulstealer"""

    # [x]<b>Battlecry:</b> Destroy all other minions. Gain 1 <b>Corpse</b> for
    # each enemy destroyed.
    def play(self):
        enemies = (ENEMY_MINIONS - DEAD).eval(self.game, self)
        yield Destroy(ALL_MINIONS - SELF)
        yield GainCorpses(
            CONTROLLER, sum(minion.destroyed_source is self for minion in enemies)
        )


class RLK_225:
    """Blightfang"""

    # [x]<b>Battlecry:</b> Infect all enemy minions. When they die, you summon
    # a 2/2 Zombie with <b>Taunt</b>.
    play = Buff(ENEMY_MINIONS, "RLK_225e")


class NX2_035:
    """Rimescale Siren"""

    # [x]<b>Battlecry:</b> If you've cast three spells while holding this,
    # <b>Freeze</b> 3 random enemy minions.@ <i>({0} left!)</i>@
    # <i>(Ready!)</i>
    powered_up = Count(CARDS_PLAYED_WHEN_HOLDING + SPELL) >= 3
    play = powered_up & Freeze(RANDOM(ENEMY_MINIONS - DEAD, 3))


##
# Spells


class RLK_035:
    """Corpse Explosion"""

    # Detonate a <b>Corpse</b> to deal $1 damage to all minions. If any are
    # still alive, repeat this.
    requirements = {
        PlayReq.REQ_MINIMUM_CORPSES: 1,
        PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 1,
    }

    def play(self):
        while self.controller.corpses and (ALL_MINIONS - DEAD).eval(self.game, self):
            yield SpendCorpses(CONTROLLER, 1)
            yield Hit(ALL_MINIONS - DEAD, 1)
            self.game.process_deaths()


class RLK_051:
    """Vampiric Blood"""

    # [x]Give your hero +5 Health. Spend 3 <b>Corpses</b> to gain 5 more and
    # draw a card.
    play = (
        Buff(FRIENDLY_HERO, "OG_188e"),
        SpendCorpses(CONTROLLER, 3).then(
            Buff(FRIENDLY_HERO, "OG_188e"), Draw(CONTROLLER)
        ),
    )


##
# Weapons


class RLK_012:
    """Soulbreaker"""

    # After your hero attacks and kills a minion, gain 2 <b>Corpses</b>.
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Find(
            Attack.DEFENDER
            + DEAD
            + FilterSelector(
                lambda card, source: getattr(card, "damaged_source", None)
                is source.controller.hero
            )
        )
        & GainCorpses(CONTROLLER, 2)
    )


##
# Locations


class NX2_036:
    """Construct Quarter"""

    # [x]Destroy a friendly minion to summon a 4/5 Undead with <b>Rush</b>.
    requirements = FRIENDLY_MINION_TARGET
    activate = Destroy(TARGET), Deaths(), Summon(CONTROLLER, "NX2_036t")


class RLK_225e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "RLK_118t3")


class RLK_706e3:
    events = OWN_TURN_END.on(Hit(ENEMY_HERO, 3))


class NX2_037:
    """Frost Queen Sindragosa"""

    colossal = SummonBothSides(CONTROLLER, ["NX2_037t2", "NX2_037t"])
    events = SetTags(
        ENEMY_MINIONS + FROZEN, lambda tags: tags.get(GameTag.FROZEN)
    ).after(Destroy(SetTags.TARGET))


class NX2_037t:
    events = Damage(CHARACTER, None, SELF).after(Freeze(Damage.TARGET))


NX2_037t2 = NX2_037t
