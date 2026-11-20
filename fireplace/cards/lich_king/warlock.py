from ..utils import *

##
# Minions


class RLK_531:
    """Infantry Reanimator"""

    # [x]<b>Battlecry:</b> Resurrect a friendly Undead. Give it <b>Reborn</b>.
    def play(self):
        dead = (FRIENDLY + DEAD_MINIONS + UNDEAD).eval(self.game, self)
        if dead and self.controller.minion_slots:
            minion = self.controller.card(self.game.random.choice(dead).id, self)
            yield GiveReborn(minion)
            yield Summon(CONTROLLER, minion)


class RLK_532:
    """Walking Dead"""

    # <b>Taunt</b> If you discard this minion, summon it.
    discard = Summon(CONTROLLER, ExactCopy(SELF))


class RLK_535:
    """Savage Ymirjar"""

    # <b>Rush</b> <b>Battlecry:</b> Discard 2 cards.
    play = Discard(RANDOM(FRIENDLY_HAND, 2))


class RLK_538:
    """Devourer of Souls"""

    # After a friendly minion dies, gain its <b>Deathrattle</b>.
    events = Death(FRIENDLY + MINION + DEATHRATTLE).on(
        CopyDeathrattleBuff(Death.ENTITY, "RLK_538e", SELF)
    )


class RLK_539:
    """Dar'Khan Drathir"""

    # [x]<b>Lifesteal</b> At the end of your turn, deal 6 damage to the enemy
    # hero.
    events = OWN_TURN_END.on(Hit(ENEMY_HERO, 6))


class RLK_540:
    """Amorphous Slime"""

    # <b>Battlecry:</b> Discard a random Undead. <b>Deathrattle:</b> Summon a
    # copy of it.
    def play(self):
        cards = (FRIENDLY_HAND + MINION + UNDEAD).eval(self.game, self)
        if cards:
            card = self.game.random.choice(cards)
            yield Buff(SELF, "RLK_540e", store_card=card)
            yield Discard(card)

    def deathrattle(self):
        # Each discarded minion supplies its own stored deathrattle on RLK_540e.
        return ()


class NX2_044:
    """Suspicious Peddler"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a 1-Cost card. If your opponent
    # guesses your __choice, they get a copy.
    play = suspicious_discover(RandomCollectible(cost=1))


##
# Spells


class RLK_533:
    """Scourge Supplies"""

    # Draw 3 cards. Choose one to discard.
    def play(self):
        drawn = self.game.queue_actions(self, [Draw(CONTROLLER) * 3])[0]
        cards = [card for draw in drawn for card in draw if card.zone == Zone.HAND]
        yield Choice(CONTROLLER, cards).then(Discard(Choice.CARD))


class RLK_534:
    """Soul Barrage"""

    # When you play or discard this, deal $6 damage randomly split among all
    # enemies.
    play = discard = Hit(RANDOM_ENEMY_CHARACTER, 1) * SPELL_DAMAGE(6)


class RLK_536:
    """Shallow Grave"""

    # Trigger a friendly minion's <b>Deathrattle</b>, then destroy it.
    requirements = FRIENDLY_MINION_TARGET
    play = Deathrattle(TARGET), Destroy(TARGET)


class RLK_537:
    """Twisted Tether"""

    # Destroy a minion. Give its stats to a random Undead in your hand.
    requirements = MINION_TARGET
    play = Buff(
        RANDOM(FRIENDLY_HAND + MINION + UNDEAD),
        "RLK_537e",
        atk=ATK(TARGET),
        max_health=CURRENT_HEALTH(TARGET),
    ), Destroy(TARGET)


class NX2_016:
    """Nofin's Imp-ossible"""

    # Give all friendly Demons and Murlocs "<b>Deathrattle:</b> Summon a 2/2
    # Imploc."
    play = Buff(FRIENDLY_MINIONS + (DEMON | MURLOC), "NX2_016e")


class NX2_017:
    """Plague Eruption"""

    # Deal $2 damage to all minions. If you've discarded a card this game, deal
    # $1 more.
    play = Find(FRIENDLY + DISCARDED) & Hit(ALL_MINIONS, 3) | Hit(ALL_MINIONS, 2)


RLK_537e = buff()
RLK_538e = buff(deathrattle=True)


class RLK_540e:
    tags = {GameTag.DEATHRATTLE: True}

    def deathrattle(self):
        yield Summon(Controller(OWNER), ExactCopy(self.store_card))


class NX2_016e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "NX2_016t")
