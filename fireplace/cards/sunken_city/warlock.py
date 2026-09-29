from ..utils import *

##
# Minions


class TSC_614:
    """Voidgill"""

    # <b>Deathrattle:</b> Give all Murlocs in your hand +1/+1.
    deathrattle = Buff(FRIENDLY_HAND + MURLOC, "TSC_614e")


TSC_614e = buff(+1, +1)


class TSC_039:
    """Azsharan Scavenger"""

    # <b>Battlecry:</b> Put a 'Sunken Scavenger' on the bottom of your deck.
    play = PutOnBottom(CONTROLLER, "TSC_039t")


class TSC_039t:
    """Sunken Scavenger"""

    # <b>Battlecry:</b> Give your other Murlocs +1/+1 <i>(wherever they
    # are)</i>.
    play = Buff(FRIENDLY + MURLOC - SELF, "TSC_039te")


TSC_039te = buff(+1, +1)


class TSC_955:
    """Sira'kess Cultist"""

    # <b>Battlecry:</b> Give your opponent an Abyssal Curse.
    play = GiveAbyssalCurse(OPPONENT)


class TSC_955t:
    """Abyssal Curse"""

    # [x]At the start of your turn, take {0} damage. Each Curse is worse than
    # the last. <i>({1} |4(turn,turns) remaining).</i>
    tags = {GameTag.IMMOLATESTAGE: 2}

    class Hand:
        events = OWN_TURN_BEGIN.on(
            Hit(FRIENDLY_HERO, DATA_NUM_1(SELF)),
        )


class TID_717:
    """Herald of Shadows"""

    # <b>Battlecry:</b> If you've cast a Shadow spell while holding this, steal
    # 2 Health from a minion.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + SHADOW)
    play = Buff(TARGET, "TID_717e").then(Buff(SELF, "TID_717e2"))


TID_717e = buff(health=-2)
TID_717e2 = buff(health=+2)


class TSC_959:
    """Za'qul"""

    # [x]Your Abyssal Curses heal you for the damage they deal.
    # <b>Battlecry:</b> Give your opponent an Abyssal Curse.
    events = Damage(source=ENEMY_HAND + ID("TSC_955t")).then(
        Heal(FRIENDLY_HERO, Damage.AMOUNT)
    )
    play = GiveAbyssalCurse(OPPONENT)


class TSC_962:
    """Gigafin"""

    # [x]<b>Colossal +1</b>. <b>Battlecry:</b> Devour all enemy minions.
    # <b>Deathrattle:</b> Spit them back out.
    colossal = Summon(CONTROLLER, "TSC_962t")
    play = StoringBuff(SELF, "TSC_962e", ENEMY_MINIONS), Destroy(ENEMY_MINIONS)


class TSC_962e:
    tags = {
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Summon(OPPONENT, STORE_CARD), Destroy(SELF)


class TSC_962t:
    def deathrattle(self):
        buff = ID("TSC_962e").eval(self.creator.buffs, self)
        yield Destroy(buff)


class TID_719:
    """Commander Ulthok"""

    # <b>Battlecry:</b> Your opponent's cards cost Health instead of Mana next
    # turn.
    play = Buff(OPPONENT, "TID_719e")


class TID_719e:
    update = Refresh(FRIENDLY_HAND, {GameTag.CARD_COSTS_HEALTH: True})
    events = OWN_TURN_END.on(Destroy(SELF))


class TSC_753:
    """Bloodscent Vilefin"""

    # [x]<b>Battlecry:</b> <b>Dredge</b>. If it's a Murloc, change its Cost to
    # _Health instead of Mana.
    play = Dredge(CONTROLLER).then(
        Find(Dredge.CARD + MURLOC) & Buff(TARGET, "TSC_753e")
    )


TSC_753e = buff(card_costs_health=True)


##
# Spells


class TSC_924:
    """Abyssal Wave"""

    # [x]Deal $4 damage to all minions. Give your opponent an Abyssal Curse.
    play = Hit(ALL_MINIONS, 4), GiveAbyssalCurse(OPPONENT)


class TSC_925:
    """Rock Bottom"""

    # [x]Summon a 1/1 Murloc, then <b>Dredge</b>. If it's also a Murloc, summon
    # one more.
    play = Summon(CONTROLLER, "TSC_925t"), Dredge(CONTROLLER).then(
        Find(Dredge.CARD + MURLOC) & Summon(CONTROLLER, "TSC_925t")
    )


class TSC_956:
    """Dragged Below"""

    # [x]Deal $4 damage to a minion. Give your opponent an Abyssal Curse.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 4), GiveAbyssalCurse(OPPONENT)


class TSC_957:
    """Chum Bucket"""

    # [x]Give all Murlocs in your hand +1/+1. Repeat for each Murloc you
    # control.
    play = Buff(FRIENDLY_HAND + MURLOC, "TSC_957e") * (
        Count(FRIENDLY_MINIONS + MURLOC) + 1
    )


TSC_957e = buff(+1, +1)


class TID_718:
    """Immolate"""

    # Light every card in the opponent's hand on fire. In 3 turns, any still in
    # hand are destroyed!
    play = SetTag(ENEMY_HAND, {GameTag.IMMOLATESTAGE: 3})
