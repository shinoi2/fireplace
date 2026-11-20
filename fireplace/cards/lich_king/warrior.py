from ..utils import *

ELUSIVE = {
    GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
    GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
}


def training_session():
    return Discover(CONTROLLER, RandomMinion(taunt=True)).then(
        Buff(Discover.CARD, "NX2_029e"), Give(CONTROLLER, Discover.CARD)
    )


##
# Minions


class RLK_602:
    """Silverfury Stalwart"""

    # <b><b>Taunt</b>, Rush</b> Can't be targeted by spells or Hero Powers.
    tags = ELUSIVE


class RLK_607:
    """Disruptive Spellbreaker"""

    # At the end of your turn, your opponent discards a spell.
    events = OWN_TURN_END.on(Discard(RANDOM(ENEMY_HAND + SPELL)))


class RLK_608:
    """Asvedon, the Grandshield"""

    # <b>Taunt</b> <b>Battlecry:</b> Cast a copy of the last spell your
    # opponent played.
    def play(self):
        spells = self.controller.opponent.cards_played_this_game.filter(
            type=CardType.SPELL
        )
        if spells:
            yield CastSpell(Copy(spells[-1]))


class RLK_609:
    """Sunfury Champion"""

    # [x]After you cast a Fire spell, deal 1 damage to all minions.
    events = Play(CONTROLLER, SPELL + FIRE).after(Hit(ALL_MINIONS, 1))


class NX2_027:
    """Fleshshaper"""

    # <b>Taunt</b>. <b>Battlecry:</b> If you have 5 or more Armor, summon a
    # copy of this.
    play = (ARMOR(FRIENDLY_HERO) >= 5) & Summon(CONTROLLER, ExactCopy(SELF))


class NX2_028:
    """Hookfist-3000"""

    # After your hero attacks, gain 4 Armor and draw a card.
    events = Attack(FRIENDLY_HERO).after(GainArmor(FRIENDLY_HERO, 4), Draw(CONTROLLER))


class RLK_604:
    """Thori'belore"""

    # [x]<b>Rush</b>. <b>Deathrattle:</b> Go <b>Dormant</b>. Cast a Fire spell
    # to revive Thori'belore! <i>(Revives 2 times.)</i>
    deathrattle = Summon(CONTROLLER, "RLK_604t")


##
# Spells


class RLK_600:
    """Sunfire Smithing"""

    # Equip a 4/2 Sword. Give a random minion in your hand +4/+2.
    play = Summon(CONTROLLER, "RLK_600t"), Buff(
        RANDOM(FRIENDLY_HAND + MINION), "RLK_600e"
    )


class RLK_601:
    """Last Stand"""

    # Draw a <b>Taunt</b> minion. <b>Manathirst (7):</b> Double its stats.
    play = FORCE_DRAW(MINION + TAUNT).then(
        Manathirst(7) & Buff(ForceDraw.TARGET, "RLK_601e")
    )


class RLK_605:
    """Blazing Power"""

    # [x]Give a minion +1/+1. Repeat for each damaged friendly character.
    requirements = MINION_TARGET
    play = Buff(TARGET, "RLK_605e") * (Count(FRIENDLY_CHARACTERS + DAMAGED) + 1)


class RLK_603:
    """Light of the Phoenix"""

    # Draw 2 cards. Costs (1) less for each damaged friendly character.
    cost_mod = -Count(FRIENDLY_CHARACTERS + DAMAGED)
    play = Draw(CONTROLLER) * 2


class RLK_960:
    """Embers of Strength"""

    # [x]Summon two 1/2 Guards with <b>Taunt</b>. <b>Manathirst (6):</b> Give
    # them +1/+2.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}

    def play(self):
        player = self.controller
        for _ in range(min(2, player.minion_slots)):
            guard = player.card("RLK_960t", self)
            if player.max_mana >= 6:
                yield Buff(guard, "RLK_960e")
            yield Summon(CONTROLLER, guard)


class NX2_029:
    """Training Session"""

    # <b>Discover</b> a <b>Taunt</b> minion. If you play it this turn, repeat
    # this.
    play = training_session()


class RLK_604a:
    deathrattle = Summon(CONTROLLER, "RLK_604t2")


class RLK_604t:
    tags = {GameTag.DORMANT: True}
    dormant_events = Play(CONTROLLER, SPELL + FIRE).after(Morph(SELF, "RLK_604a"))


class RLK_604t2:
    tags = {GameTag.DORMANT: True}
    dormant_events = Play(CONTROLLER, SPELL + FIRE).after(Morph(SELF, "RLK_604b"))


RLK_600e = buff(4, 2)
RLK_605e = buff(1, 1)
RLK_960e = buff(1, 2)


class RLK_601e:
    atk = lambda self, value: value * 2
    max_health = lambda self, value: value * 2


class NX2_029e:
    tags = {GameTag.TAG_ONE_TURN_EFFECT: True}

    class Hand:
        events = Play(CONTROLLER, OWNER).on(
            lambda source, player, card, target: [training_session(), Destroy(SELF)]
        )
