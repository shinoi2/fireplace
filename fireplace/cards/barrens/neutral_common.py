from ..utils import *

##
# Minions


class BAR_020:
    """Razormane Raider"""

    # <b>Frenzy:</b> Attack a random enemy.
    frenzy = Attack(SELF, RANDOM_ENEMY_CHARACTER)


class BAR_021:
    """Gold Road Grunt"""

    # [x]<b>Taunt</b> <b>Frenzy:</b> Gain Armor equal to the damage taken.
    # def frenzy(self, amount):
    #     yield GainArmor(FRIENDLY_HERO, amount)
    frenzy = GainArmor(FRIENDLY_HERO, Frenzy.AMOUNT)


class BAR_022:
    """Peon"""

    # [x]<b>Frenzy:</b> Add a random spell from your class to your hand.
    frenzy = Give(CONTROLLER, RandomSpell(card_class=FRIENDLY_CLASS))


class BAR_024:
    """Oasis Thrasher"""

    # <b>Frenzy:</b> Deal 3 damage to the enemy Hero.
    frenzy = Hit(ENEMY_HERO, 3)


class BAR_025:
    """Sunwell Initiate"""

    # <b>Frenzy:</b> Gain <b>Divine Shield</b>.
    frenzy = GiveDivineShield(SELF)


class BAR_026:
    """Death's Head Cultist"""

    # <b>Taunt</b> <b>Deathrattle:</b> Restore 4 Health to your hero.
    deathrattle = Heal(FRIENDLY_HERO, 4)


class BAR_027:
    """Darkspear Berserker"""

    # <b>Deathrattle:</b> Deal 5 damage to your hero.
    deathrattle = Hit(FRIENDLY_HERO, 5)


class BAR_060:
    """Hog Rancher"""

    # <b>Battlecry:</b> Summon a 2/1 Hog with <b>Rush</b>.
    play = Summon(CONTROLLER, "BAR_060t")


class BAR_061:
    """Ratchet Privateer"""

    # <b>Battlecry:</b> Give your weapon +1 Attack.
    play = Buff(FRIENDLY_WEAPON, "BAR_061e")


BAR_061e = buff(atk=1)


class BAR_062:
    """Lushwater Murcenary"""

    # <b>Battlecry:</b> If you control a Murloc, gain +1/+1.
    powered_up = Find(FRIENDLY_MINIONS + MURLOC)
    play = powered_up & Buff(SELF, "BAR_062e")


BAR_062e = buff(+1, +1)


class BAR_063:
    """Lushwater Scout"""

    # After you summon a Murloc, give it +1 Attack and <b>Rush</b>.
    events = Summon(CONTROLLER, MURLOC).after(Buff(Summon.CARD, "BAR_063e"))


BAR_063e = buff(atk=1, rush=True)


class BAR_064:
    """Talented Arcanist"""

    # <b>Battlecry:</b> Your next spell_this turn has <b>Spell_Damage +2</b>.
    play = Buff(CONTROLLER, "BAR_064e")


class BAR_064e:
    tags = {GameTag.SPELLPOWER: 2}
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class BAR_065:
    """Venomous Scorpid"""

    # <b>Poisonous</b> <b>Battlecry:</b> <b>Discover</b> a spell.
    play = DISCOVER(RandomSpell())


class BAR_069:
    """Injured Marauder"""

    # <b>Taunt</b> <b>Battlecry:</b> Deal 6 damage to this minion.
    play = Hit(SELF, 6)


class BAR_070:
    """Gruntled Patron"""

    # <b>Frenzy:</b> Summon another Gruntled Patron.
    frenzy = Summon(CONTROLLER, "BAR_070")


class BAR_074:
    """Far Watch Post"""

    # [x]Can't attack. After your opponent draws a card, it ___costs (1) more
    # <i>(up to 10)</i>.__
    events = Draw(OPPONENT).after(Buff(Draw.CARD, "BAR_074e"))


class BAR_074e:
    cost = lambda self, i: i if i >= 10 else i + 1
    events = REMOVED_IN_PLAY


class BAR_082:
    """Barrens Trapper"""

    # Your <b>Deathrattle</b> cards cost (1) less.
    update = Refresh(FRIENDLY_HAND + DEATHRATTLE, {GameTag.COST: -1})


class BAR_743:
    """Toad of the Wilds"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If you're holding a Nature spell, gain
    # +2 Health.
    powered_up = Find(FRIENDLY_HAND + SPELL + NATURE)
    play = powered_up & Buff(SELF, "BAR_743e")


BAR_743e = buff(health=2)


class BAR_854:
    """Kindling Elemental"""

    # [x]<b>Battlecry:</b> The next Elemental you play costs (1) less.
    play = Buff(CONTROLLER, "BAR_854e")


class BAR_854e:
    update = Refresh(FRIENDLY_HAND + ELEMENTAL, {GameTag.COST: -1})
    events = Play(CONTROLLER, ELEMENTAL).after(Destroy(SELF))


class BAR_890:
    """Crossroads Gossiper"""

    # After a friendly <b>Secret</b> is revealed, gain +2/+2.
    events = Reveal(FRIENDLY_SECRETS).after(Buff(SELF, "BAR_890e"))


BAR_890e = buff(+2, +2)


class WC_027:
    """Devouring Ectoplasm"""

    # [x]<b>Deathrattle:</b> Summon a 2/2 Adventurer with _a random bonus
    # effect.
    entourage = ADVENTURERS
    deathrattle = Summon(CONTROLLER, RandomEntourage())


class WC_028:
    """Meeting Stone"""

    # [x]At the end of your turn, add a 2/2 Adventurer with a random bonus
    # effect to your hand.
    entourage = ADVENTURERS
    events = OWN_TURN_END.on(Give(CONTROLLER, RandomEntourage()))


class WC_029:
    """Selfless Sidekick"""

    # <b>Battlecry:</b> Equip a random weapon from your deck.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + WEAPON))
