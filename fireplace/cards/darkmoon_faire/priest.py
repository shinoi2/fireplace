from ..utils import *


##
# Minions


class DMF_053:
    """Blood of G'huun"""

    # [x]<b>Taunt</b> At the end of your turn, summon a 5/5 copy of a minion in
    # your deck.
    events = OWN_TURN_END.on(
        Summon(CONTROLLER, Copy(RANDOM(FRIENDLY_DECK + MINION))).then(
            Buff(Summon.CARD, "DMF_053e")
        )
    )


class DMF_053e:
    atk = SET(5)
    max_health = SET(5)


class DMF_056:
    """G'huun the Blood God"""

    # <b>Battlecry:</b> Draw 2 cards. They cost Health instead of Mana.
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DMF_056e")) * 2


class DMF_056e:
    tags = {GameTag.CARD_COSTS_HEALTH: True}


class DMF_116:
    """The Nameless One"""

    # <b>Battlecry:</b> Choose a minion. Become a 4/4 copy of it, then
    # <b>Silence</b> it.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = (
        Morph(SELF, ExactCopy(TARGET)).then(Buff(Morph.CARD, "DMF_116e")),
        Silence(TARGET),
    )


class DMF_116e:
    atk = SET(4)
    max_health = SET(4)


class DMF_120:
    """Nazmani Bloodweaver"""

    # [x]After you cast a spell, reduce the cost of a random card in your hand
    # by (1).
    events = Play(CONTROLLER, SPELL).after(Buff(RANDOM(FRIENDLY_HAND), "DMF_120e2"))


class DMF_120e2:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class DMF_121:
    """Fortune Teller"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Gain +1/+1 for each spell in your hand.
    play = Buff(SELF, "DMF_121e") * Count(FRIENDLY_HAND + SPELL)


DMF_121e = buff(+1, +1)


class DMF_184:
    """Fairground Fool"""

    # <b>Taunt</b> <b>Corrupt:</b> Gain +4 Health.
    corrupt_card = "DMF_184t"


class YOP_007:
    """Dark Inquisitor Xanesh"""

    # [x]<b>Battlecry:</b> Reduce the Cost of all <b>Corrupt</b> cards in your
    # hand and deck by (2).
    play = Buff(FRIENDLY_HAND + FRIENDLY_DECK + CORRUPTED, "YOP_007e")


class YOP_007e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class YOP_008:
    """Lightsteed"""

    # Your healing effects also give affected minions +2_Health.
    events = Heal(CONTROLLER, MINION).on(Buff(Heal.TARGET, "YOP_008e"))


YOP_008e = buff(health=2)


##
# Spells


class DMF_054:
    """Insight"""

    # Draw a minion. <b>Corrupt:</b> Reduce its Cost by (2).
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION))
    corrupt_card = "DMF_054t"


class DMF_054t:
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
        Buff(ForceDraw.TARGET, "DMF_054e")
    )


class DMF_054e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


class DMF_055:
    """Idol of Y'Shaarj"""

    # Summon a 10/10 copy_of a minion in your deck.
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY_DECK + MINION))).then(
        Buff(Summon.CARD, "DMF_055e")
    )


class DMF_055e:
    atk = SET(10)
    max_health = SET(10)


class DMF_186:
    """Auspicious Spirits"""

    # Summon a random 4-Cost minion. <b>Corrupt:</b> Summon a 7-Cost minion
    # instead.
    play = Summon(CONTROLLER, RandomMinion(cost=4))
    corrupt_card = "DMF_186t"


class DMF_186t:
    play = Summon(CONTROLLER, RandomMinion(cost=7))


class DMF_187:
    """Palm Reading"""

    # <b>Discover</b> a spell. Reduce the Cost of spells in your hand by (1).
    play = (DISCOVER(RandomSpell()), Buff(FRIENDLY_HAND + SPELL, "DMF_187e"))


class DMF_187e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class YOP_006:
    """Hysteria"""

    # [x]Choose an enemy minion. It attacks random minions until it dies.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }

    def play(self):
        times = 0
        while not self.target.dead:
            yield Attack(self.target, RANDOM(ALL_MINIONS - DEAD - TARGET))
            times += 1
            if times >= 30:
                break
