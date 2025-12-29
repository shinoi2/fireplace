from ..utils import *


##
# Minions


class SCH_276:
    """Magehunter"""

    # <b>Rush</b> Whenever this attacks a minion, <b>Silence</b> it.
    events = Attack(SELF, MINION).on(Silence(Attack.DEFENDER))


class SCH_354:
    """Ancient Void Hound"""

    # [x]At the end of your turn, steal 1 Attack and Health from all enemy
    # minions.
    events = OWN_TURN_END.on(
        Buff(ENEMY_MINIONS + (ATK <= 0) + (CURRENT_HEALTH == 0), "SCH_354ea").then(
            Buff(SELF, "SCH_354e2a")
        ),
        Buff(ENEMY_MINIONS + (ATK == 0) + (CURRENT_HEALTH <= 0), "SCH_354e2b").then(
            Buff(SELF, "SCH_354e2b")
        ),
        Buff(ENEMY_MINIONS + (ATK > 0) + (CURRENT_HEALTH > 0), "SCH_354e").then(
            Buff(SELF, "SCH_354e2")
        ),
    )


SCH_354e = buff(-1, -1)
SCH_354e2 = buff(+1, +1)
SCH_354e2a = buff(atk=+1)
SCH_354e2b = buff(health=+1)
SCH_354ea = buff(atk=-1)
SCH_354eb = buff(health=-1)


class SCH_355:
    """Shardshatter Mystic"""

    # <b>Battlecry:</b> Destroy a Soul Fragment in your deck to deal 3 damage
    # to all other minions.
    powered_up = Find(FRIENDLY_DECK + ID(SOUL_FRAGMENT))
    play = powered_up & (
        Destroy(RANDOM(FRIENDLY_DECK + ID(SOUL_FRAGMENT))),
        Hit(ALL_MINIONS - SELF, 3),
    )


class SCH_538:
    """Ace Hunter Kreen"""

    # Your other characters are <b>Immune</b> while attacking.
    update = Refresh(FRIENDLY_CHARACTERS - SELF, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class SCH_603:
    """Star Student Stelina"""

    # [x]<b>Outcast:</b> Look at 3 cards in your opponent's hand. Shuffle one
    # of them into their deck.
    outcast = Choice(CONTROLLER, RANDOM(ENEMY_HAND, 3)).then(
        Shuffle(OPPONENT, Choice.CARD)
    )


class SCH_618:
    """Blood Herald"""

    # Whenever a friendly minion dies while this is in your hand, gain +1/+1.
    class Hands:
        events = Death(FRIENDLY_MINIONS).on(Buff(SELF, "SCH_618e"))


SCH_618e = buff(+1, +1)


class SCH_704:
    """Soulshard Lapidary"""

    # [x]<b>Battlecry:</b> Destroy a Soul Fragment in your deck to give your
    # hero +5 Attack this turn.
    powered_up = Find(FRIENDLY_DECK + ID(SOUL_FRAGMENT))
    play = powered_up & Buff(FRIENDLY_HERO, "SCH_074e")


SCH_074e = buff(atk=5)


class SCH_705:
    """Vilefiend Trainer"""

    # <b>Outcast:</b> Summon two 1/1_Demons.
    outcast = SummonBothSides(CONTROLLER, "SCH_705t") * 2


##
# Spells


class SCH_253:
    """Cycle of Hatred"""

    # Deal $3 damage to all minions. Summon a 3/3 Spirit for every minion
    # killed.
    play = Hit(ALL_MINIONS, 3), Summon(CONTROLLER, "SCH_253t") * Count(
        ALL_MINIONS + DEAD
    )


class SCH_356:
    """Glide"""

    # [x]Shuffle your hand into your deck. Draw 4 cards. <b>Outcast:</b> Your
    # opponent does the same.
    play = Shuffle(CONTROLLER, FRIENDLY_HAND), (Draw(CONTROLLER) * 4)
    outcast = (
        Shuffle(CONTROLLER, FRIENDLY_HAND),
        Shuffle(OPPONENT, ENEMY_HAND),
        (Draw(CONTROLLER) * 4),
        (Draw(OPPONENT) * 4),
    )


class SCH_357:
    """Fel Guardians"""

    # Summon three 1/2 Demons with <b>Taunt</b>. Costs (1) less whenever
    # a_friendly minion dies.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    cost_mod = -Count(FRIENDLY + KILLED + MINION)
    play = Summon(CONTROLLER, "SCH_357t") * 3


class SCH_422:
    """Double Jump"""

    # Draw an <b>Outcast</b> card from your deck.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + OUTCAST))


class SCH_600:
    """Demon Companion"""

    # Summon a random Demon Companion.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    entourage = ["SCH_600t1", "SCH_600t2", "SCH_600t3"]
    play = Summon(CONTROLLER, RandomEntourage())


class SCH_600t3:
    """Kolek"""

    # Your other minions have +1 Attack.
    update = Refresh(FRIENDLY_MINIONS - SELF, "SCH_600t3e")


SCH_600t3e = buff(atk=1)


##
# Weapons


class SCH_252:
    """Marrowslicer"""

    # <b>Battlecry:</b> Shuffle 2 Soul Fragments into your deck.
    play = Shuffle(CONTROLLER, SOUL_FRAGMENT) * 2


class SCH_279:
    """Trueaim Crescent"""

    # After your Hero attacks a minion, your minions attack it too.
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Dead(Attack.DEFENDER) | Attack(FRIENDLY_MINIONS, Attack.DEFENDER)
    )
