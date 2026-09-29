from ..utils import *

##
# Minions


class TSC_032:
    """Blademaster Okani"""

    # [x]<b>Battlecry:</b> <b>Secretly</b> choose to <b>Counter</b> the next
    # minion or spell your opponent plays while this is alive.
    play = Choice(CONTROLLER, ["TSC_032t", "TSC_032t2"]).then(
        StoringBuff(SELF, "TSC_032e3", Choice.CARD)
    )


class TSC_032e3:
    """Blade Counter"""

    # This <b>Counters</b> the next <b>Secretly</b> chosen minion or spell your
    # opponent plays.@Okani will <b>Secretly</b> counter the next minion your
    # opponent plays.@Okani will <b>Secretly</b> counter the next spell your
    # opponent plays.
    events = (
        Play(OPPONENT, MINION).on(
            FindId(STORE_CARD, "TSC_032t") & (Counter(Play.CARD), Destroy(SELF))
        ),
        Play(OPPONENT, SPELL).on(
            FindId(STORE_CARD, "TSC_032t") & (Counter(Play.CARD), Destroy(SELF))
        ),
    )


class TSC_908:
    """Sir Finley, Sea Guide"""

    # [x]<b>Battlecry:</b> Swap your hand with the bottom of your deck.
    play = Swap(FRIENDLY_HAND, FRIENDLY_DECK[: Count(FRIENDLY_HAND)])


class TSC_641(HoldingSpellThresholdUtils):
    """Queen Azshara"""

    # <b>Battlecry:</b> If you've cast three spells while holding this, choose
    # an Ancient Relic.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = GenericChoice(
        CONTROLLER, ["TSC_641ta", "TSC_641tb", "TSC_641tc", "TSC_641td"]
    )


TSC_641tde = cost_buff(SET(1))


class TSC_641ta:
    """Ring of Tides"""

    # After you cast a spell, this becomes a copy of it that costs (1).
    class Hand:
        events = Play(FRIENDLY, SPELL).after(
            Morph(SELF, Copy(Play.CARD)).then(Buff(Morph.CARD, "TSC_641tde"))
        )


class TSC_641tb:
    """Horn of Ancients"""

    # Add a random <b>Colossal</b> minion to your hand. It costs (1).
    play = Give(
        CONTROLLER, RandomCollectible(can_pick_from_subsets=True, colossal=True)
    ).then(Buff(Morph.CARD, "TSC_641tae"), Buff(Morph.CARD, "TSC_641tde"))


class TSC_641tc:
    """Xal'atath"""

    # After you cast a spell, deal 2 damage to the enemy hero and lose 1
    # Durability.
    events = Play(FRIENDLY, SPELL).after(Hit(ENEMY_HERO, 2), Hit(SELF, 1))


class TSC_641td:
    """Tidestone of Golganneth"""

    # Shuffle 5 random spells into your deck. Set their Cost to (1). Draw two
    # cards.
    play = (
        Shuffle(FRIENDLY_DECK, RandomSpell()).then(Buff(Shuffle.CARD, "TSC_641tde"))
        * 5,
        Draw(CONTROLLER) * 2,
    )


class TSC_641tae:
    """Shifting"""

    # Transforming into your spells.
    class Hand:
        events = Play(CONTROLLER).after(
            Morph(OWNER, Copy(Play.CARD)).then(
                Buff(Morph.CARD, "TSC_641tae"), Buff(Morph.CARD, "TSC_641tde")
            )
        )


class TSC_649:
    """Ini Stormcoil"""

    # [x]<b>Battlecry:</b> Choose a friendly Mech. Summon a copy of it with
    # <b>Rush</b>, <b>Windfury</b>, and <b>Divine Shield</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.MECHANICAL,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET)).then(
        GiveRush(Summon.CARD),
        GiveWindfury(Summon.CARD),
        GiveDivineShield(Summon.CARD),
    )


class TSC_067:
    """Ambassador Faelin"""

    # <b>Battlecry:</b> Put 3 <b>Colossal</b> minions on the bottom of your
    # deck.
    play = (
        PutOnBottom(
            CONTROLLER, RandomCollectible(can_pick_from_subsets=True, colossal=True)
        )
        * 3
    )


class TID_711:
    """Ozumat"""

    # [x]<b>Colossal +6</b> <b>Deathrattle:</b> For each of Ozumat's Tentacles,
    # destroy a random enemy minion.
    colossal = (
        SummonLeft(CONTROLLER, ["TID_711t", "TID_711t2", "TID_711t3"]),
        Summon(CONTROLLER, ["TID_711t4", "TID_711t5", "TID_711t6"]),
    )
    deathrattle = Destroy(RANDOM_ENEMY_MINION) * Count(
        FRIENDLY
        + ID(
            [
                "TID_711t",
                "TID_711t2",
                "TID_711t3",
                "TID_711t4",
                "TID_711t5",
                "TID_711t6",
            ]
        )
    )


class TID_712:
    """Neptulon the Tidehunter"""

    # [x]<b>Colossal +2</b>, <b>Rush</b>, <b>Windfury</b> Whenever Neptulon
    # attacks, if you control any Hands, they attack instead.
    colossal = (SummonLeft(CONTROLLER, "TID_712t"), Summon(CONTROLLER, "TID_712t2"))
    events = Attack(CONTROLLER).on(
        Find(FRIENDLY_MINIONS + ID(["TID_712t", "TID_712t2"]))
        & (
            Attack(FRIENDLY_MINIONS + ID(["TID_712t", "TID_712t2"]), Attack.DEFENDER),
            Retarget(SELF, None),
            AddTag(SELF, GameTag.NUM_ATTACKS_THIS_TURN, 1),
        )
    )
