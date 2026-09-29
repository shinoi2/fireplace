from ..utils import *

##
# Minions


class TSC_610:
    """Glaiveshark"""

    # [x]<b>Battlecry:</b> If your hero attacked this turn, deal 2 damage to
    # all enemies.
    powered_up = NUM_ATTACKS_THIS_TURN(FRIENDLY_HERO) > 0
    play = powered_up & Hit(ENEMY_CHARACTERS, 2)


class TSC_609(HoldingSpellThresholdUtils):
    """Coilskar Commander"""

    # [x]<b>Taunt</b>. <b>Battlecry:</b> If you've cast three spells while
    # holding this, summon two __copies of this.@ <i>({0} left!)</i>@
    # <i>(Ready!)</i>
    play = Summon(CONTROLLER, ExactCopy(SELF))


class TSC_057:
    """Azsharan Defector"""

    # [x]<b>Rush</b>. <b>Deathrattle:</b> Put a 'Sunken Defector' on the_
    # bottom of your deck.
    deathrattle = PutOnBottom(CONTROLLER, "TSC_057t")


class TSC_057t:
    """Sunken Defector"""

    # <b>Charge</b>. After this attacks, deal 5 damage to a random enemy
    # minion.
    events = Attack(SELF).after(Hit(RANDOM(ENEMY_MINIONS), 5))


class TSC_217:
    """Wayward Sage"""

    # [x]<b>Outcast:</b> Reduce the Cost of the left and right-most _cards in
    # your hand by (1).
    outcast = Buff(OUTERMOST(FRIENDLY_HAND), "TSC_217e")


TSC_217e = cost_buff(cost=-1)


class TSC_218:
    """Lady S'theno"""

    # [x]<b>Immune</b> while attacking. After you cast a spell, attack the
    # lowest Health enemy.
    events = Play(CONTROLLER, SPELL).after(
        Attack(SELF, RANDOM(LOWEST_HEALTH(ENEMY_CHARACTERS)))
    )


class TSC_219:
    """Xhilag of the Abyss"""

    # [x]<b>Colossal +4</b> At the start of your turn, increase the damage of
    # Xhilag's Stalks by 1.
    colossal = (
        SummonLeft(CONTROLLER, ["TSC_219t", "TSC_219t2"]),
        Summon(CONTROLLER, ["TSC_219t3", "TSC_219t4"]),
    )
    events = OWN_TURN_BEGIN.on(
        AddTag(
            FRIENDLY_MINIONS + IDS(["TSC_219t", "TSC_219t2", "TSC_219t3", "TSC_219t4"]),
            GameTag.TAG_SCRIPT_DATA_NUM_1,
            1,
        )
    )


class TSC_219t:
    """Xhilag's Stalk"""

    # At the end of your turn, deal @ damage to a random enemy.
    events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER, DATA_NUM_1(SELF)))


class TSC_219t2(TSC_219t):
    """Xhilag's Stalk"""

    # At the end of your turn, deal @ damage to a random enemy.
    pass


class TSC_219t3(TSC_219t):
    """Xhilag's Stalk"""

    # At the end of your turn, deal @ damage to a random enemy.
    pass


class TSC_219t4(TSC_219t):
    """Xhilag's Stalk"""

    # At the end of your turn, deal @ damage to a random enemy.
    pass


class TID_704:
    """Fossil Fanatic"""

    # After your hero attacks, draw a Fel spell.
    events = Attack(FRIENDLY_HERO).after(FORCE_DRAW(FEL))


class TID_706:
    """Herald of Chaos"""

    # [x]<b>Lifesteal</b> <b>Battlecry:</b> If you've cast a Fel spell while
    # holding this, gain <b>Rush</b>.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + FEL)
    play = powered_up & GiveRush(SELF)


##
# Spells


class TSC_006:
    """Multi-Strike"""

    # Give your hero +2 Attack this turn. They may attack an additional enemy
    # minion.
    play = Buff(FRIENDLY_HERO, "TSC_006e"), ExtraAttackOnlyMinion(FRIENDLY_HERO)


TSC_006e = buff(atk=2)


class TSC_608:
    """Abyssal Depths"""

    # Draw your two lowest Cost minions.
    play = ForceDraw(CONTROLLER, RANDOM(LOWEST_COST(FRIENDLY_DECK))) * 2


class TSC_058:
    """Predation"""

    # Deal $3 damage. Costs (0) if you played a Naga while holding this.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    class Hand:
        update = Find(CARDS_PLAYED_WHEN_HOLDING + NAGA) & Refresh(
            SELF, {GameTag.COST: SET(0)}
        )

    play = Hit(TARGET, 3)


class TID_703:
    """Topple the Idol"""

    # [x]<b>Dredge</b>. Reveal it and deal damage equal to _its Cost to all
    # minions.
    play = Dredge(CONTROLLER).then(
        Reveal(Dredge.CARD), Hit(ALL_MINIONS, COST(Dredge.CARD))
    )


##
# Weapons


class TSC_915:
    """Bone Glaive"""

    # <b>Battlecry:</b> <b>Dredge</b>.
    play = Dredge(CONTROLLER)
