from ..utils import *

##
# Minions


class RLK_527:
    """Timewarden"""

    # [x]<b>Battlecry:</b> Until the end of your next turn, Dragons you summon
    # gain <b>Taunt</b> and <b>Divine Shield</b>.
    play = Buff(CONTROLLER, "RLK_527e2")


class RLK_916:
    """Daring Drake"""

    # [x]<b>Rush</b> <b>Battlecry:</b> If you're holding a Dragon, gain +1/+1.
    play = HOLDING_DRAGON & Buff(SELF, "RLK_916e")


class RLK_919:
    """Anachronos"""

    # [x]<b>Battlecry:</b> Send all other minions 2 turns into the future.
    def play(self):
        minions = [
            (minion, minion.zone_position - 1)
            for minion in (ALL_MINIONS - SELF - DEAD).eval(self.game, self)
        ]
        for minion, position in sorted(minions, key=lambda item: item[1]):
            keeper = minion.controller
            yield Remove(minion)
            yield Buff(keeper, "RLK_919e", store_card=minion, return_position=position)


class RLK_921:
    """Sanguine Soldier"""

    # <b>Divine Shield</b> <b>Battlecry:</b> Deal 2 damage to your hero.
    play = Hit(FRIENDLY_HERO, 2)


class RLK_924:
    """Blood Matriarch Liadrin"""

    # After you summon a minion with less Attack than this, give it <b>Divine
    # Shield</b> and <b>Rush</b>.
    events = Summon(CONTROLLER, MINION).after(
        (ATK(Summon.CARD) < ATK(SELF)) & Buff(Summon.CARD, "RLK_924e")
    )


class RLK_927:
    """Blood Crusader"""

    # [x]<b>Battlecry:</b> Your next Paladin minion this turn costs Health
    # instead of Mana.
    play = Buff(CONTROLLER, "RLK_927e")


class NX2_021:
    """Knight of the Dead"""

    # [x]<b>Battlecry:</b> Deal 5 damage to your hero. <b>Manathirst (7):</b>
    # Restore 5 Health to your hero instead.
    play = Manathirst(7) & Heal(FRIENDLY_HERO, 5) | Hit(FRIENDLY_HERO, 5)


class NX2_022:
    """Goldwing"""

    # [x]<b>Rush</b> <b>Battlecry:</b> If you're holding a Mech, gain
    # <b>Windfury</b>.
    play = Find(FRIENDLY_HAND + MECH) & GiveWindfury(SELF)


class NX2_023:
    """The Purator"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If your deck has no Neutral cards, draw
    # a minion of each minion type.
    def play(self):
        if any(card.card_class == CardClass.NEUTRAL for card in self.controller.deck):
            return
        drawn = set()
        for minion in self.controller.deck.filter(type=CardType.MINION):
            races = set(minion.races) - {Race.INVALID}
            if races - drawn:
                drawn.update(races)
                yield ForceDraw(minion)


##
# Spells


class RLK_917:
    """Flight of the Bronze"""

    # [x]<b>Discover</b> a Dragon. <b>Manathirst (7):</b> Summon a 5/5 Drake
    # with <b>Taunt</b>.
    play = DISCOVER(RandomDragon()), Manathirst(7) & Summon(CONTROLLER, "RLK_917t")


class RLK_918:
    """For Quel'Thalas!"""

    # [x]Give a friendly minion +3 Attack. Give your hero +2 Attack this turn.
    requirements = FRIENDLY_MINION_TARGET
    play = Buff(TARGET, "RLK_918e"), Buff(FRIENDLY_HERO, "RLK_918e2")


class RLK_922:
    """Seal of Blood"""

    # Give a minion +3/+3 and <b>Divine Shield</b>. Deal $3 damage to your
    # hero.
    requirements = MINION_TARGET
    play = Buff(TARGET, "RLK_922e"), GiveDivineShield(TARGET), Hit(FRIENDLY_HERO, 3)


class RLK_923:
    """Feast and Famine"""

    # Give your hero +3 Attack this turn. <b>Manathirst (4):</b> And
    # <b>Lifesteal</b>.
    play = Buff(FRIENDLY_HERO, "RLK_923e1"), Manathirst(4) & Buff(
        FRIENDLY_HERO, "RLK_923e3"
    )


class RLK_527e2:
    def apply(self, target):
        self.expires = self.game.turn + 2

    def expire(self, player):
        if self.game.turn >= self.expires:
            return Destroy(SELF)

    events = (
        Summon(CONTROLLER, MINION + DRAGON).after(
            Taunt(Summon.CARD), GiveDivineShield(Summon.CARD)
        ),
        OWN_TURN_END.on(expire),
    )


class RLK_919e:
    def apply(self, target):
        self.return_turn = self.game.turn + 4

    def restore(self, player):
        if self.game.turn < self.return_turn:
            return
        minion = self.store_card
        if self.owner.minion_slots:
            minion._summon_index = self.return_position
            yield Summon(self.owner, minion)
        else:
            yield Destroy(minion)
        yield Destroy(SELF)

    events = TURN_BEGIN.on(restore)


PALADIN_MINION = MINION + PALADIN


class RLK_927e:
    update = Refresh(FRIENDLY_HAND + PALADIN_MINION, {GameTag.CARD_COSTS_HEALTH: True})
    events = Play(CONTROLLER, PALADIN_MINION).on(Destroy(SELF)), OWN_TURN_END.on(
        Destroy(SELF)
    )


RLK_916e = buff(1, 1)
RLK_918e = buff(atk=3)
RLK_918e2 = buff(atk=2, tag_one_turn_effect=True)
RLK_922e = buff(3, 3)
RLK_923e1 = buff(atk=3, tag_one_turn_effect=True)
RLK_923e3 = buff(lifesteal=True, tag_one_turn_effect=True)
RLK_924e = buff(rush=True, divine_shield=True)
