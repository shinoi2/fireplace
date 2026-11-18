from ..utils import *

##
# Minions


class REV_900:
    """Scuttlebutt Ghoul"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> If you control a <b>Secret</b>, summon
    # a copy of this.
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


class REV_916:
    """Creepy Painting"""

    # After another minion dies, become a copy of it.
    def copy_dead_minion(self, minion):
        copy = ExactCopy(minion).evaluate(self)[0]
        copy.damage = 0
        yield Morph(SELF, copy)

    events = Death(MINION - SELF).after(copy_dead_minion)


class REV_251:
    """Sinrunner"""

    # <b>Deathrattle:</b> Destroy a random enemy minion.
    deathrattle = Destroy(RANDOM_ENEMY_MINION)


class REV_308:
    """Maze Guide"""

    # <b>Battlecry</b>: Summon a random 2-Cost minion.
    play = Summon(CONTROLLER, RandomMinion(cost=2))


class REV_945:
    """Sketchy Stranger"""

    # <b>Battlecry:</b> <b>Discover</b> a <b>Secret</b> from another class.
    play = DISCOVER(RandomSpell(secret=True, card_class=ANOTHER_CLASS))


class REV_837:
    """Muck Plumber"""

    # ALL minions cost (2) more.
    update = Refresh(IN_HAND + MINION, {GameTag.COST: +2})


class REV_956:
    """Priest of the Deceased"""

    # <b>Taunt</b> <b>Infuse (@):</b> Gain +2/+2.
    infuse_card = "REV_956t"


class REV_957:
    """Murlocula"""

    # <b>Lifesteal</b> <b>Infuse (@):</b> This costs (0).
    infuse_card = "REV_957t"


class REV_351:
    """Roosting Gargoyle"""

    # <b>Battlecry:</b> Give a friendly Beast +2 Attack.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = Buff(TARGET, "REV_351e")


REV_351e = buff(atk=2)


class REV_338:
    """Dredger Staff"""

    # [x]<b>Battlecry:</b> Give minions in your hand +1 Health.
    play = Buff(FRIENDLY_HAND + MINION, "REV_338e")


REV_338e = buff(health=1)


class REV_839:
    """Sinstone Totem"""

    # At the end of your turn, gain +1 Health.
    events = OWN_TURN_END.on(Buff(SELF, "REV_839e"))


REV_839e = buff(health=1)


class REV_841:
    """Anonymous Informant"""

    # <b>Battlecry:</b> The next <b>Secret</b> you play costs (0).
    play = Buff(CONTROLLER, "REV_841e")


class REV_841e:
    update = Refresh(FRIENDLY_HAND + SECRET, buff="REV_841e2")
    events = Play(CONTROLLER, SECRET).on(Destroy(SELF))


class REV_841e2:
    cost = SET(0)


class REV_375:
    """Stoneborn General"""

    # [x]<b>Rush</b> __<b>Deathrattle:</b> Summon an ___8/8 Gravewing with
    # <b>Rush</b>._
    deathrattle = Summon(CONTROLLER, "REV_375t")


class MAW_004:
    """Soul Seeker"""

    # <b>Battlecry:</b> Swap this with a random minion from your opponent's
    # deck.
    play = Swap(SELF, RANDOM(ENEMY_DECK + MINION))


class REV_012:
    """Bog Beast"""

    # [x]<b><b>Taunt</b></b> <b>Deathrattle:</b> Summon a 2/4 Muckmare with
    # <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "REV_012t")


class REV_013:
    """Stoneborn Accuser"""

    # [x]<b>Infuse (@):</b> Gain "<b>Battlecry:</b> Deal 5 damage."
    infuse_card = "REV_013t"


class REV_013t:
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 5)


class REV_014:
    """Red Herring"""

    # [x]<b>Taunt</b> Your non-Red Herring minions have <b>Stealth</b>.
    update = Refresh(FRIENDLY_MINIONS - ID("REV_014"), {GameTag.STEALTH: True})


class REV_015:
    """Masked Reveler"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Summon a 2/2 copy of another minion in
    # your deck.
    deathrattle = Summon(
        CONTROLLER, Buff(Copy(RANDOM(FRIENDLY_DECK + MINION)), "REV_015t")
    )


class REV_015t:
    atk = SET(2)
    max_health = SET(2)


class REV_378:
    """Forensic Duster"""

    # [x]<b>Battlecry:</b> Your opponent's minions cost (1) more next turn.
    play = Buff(OPPONENT, "REV_378e")


class REV_378e:
    update = Refresh(ENEMY_HAND + MINION, {GameTag.COST: 1})
    events = EndTurn(OPPONENT).on(Destroy(SELF))


class REV_020:
    """Dinner Performer"""

    # [x]<b>Battlecry:</b> Summon a random minion from your deck that you can
    # afford to play.
    play = Summon(
        CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST <= CURRENT_MANA(CONTROLLER)))
    )


class REV_845:
    """Volatile Skeleton"""

    # <b>Deathrattle:</b> Deal 2 damage to a random enemy.
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 2)
