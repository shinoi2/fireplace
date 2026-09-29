from ..utils import *

##
# Minions


class TSC_945:
    """Azsharan Saber"""

    # [x]<b><b>Rush</b>.</b> <b>Deathrattle:</b> Put a 'Sunken Saber' on the
    # bottom of your deck.
    deathrattle = PutOnBottom(CONTROLLER, "TSC_945t")


class TSC_945t:
    """Sunken Saber"""

    # <b><b>Rush</b>.</b> <b>Deathrattle:</b> Summon a Beast from your deck.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST))


class TSC_950:
    """Hydralodon"""

    # [x]<b>Colossal +2</b> <b>Battlecry:</b> Give your _Hydralodon Heads
    # <b>Rush</b>.
    colossal = SummonBothSides(CONTROLLER, ["TSC_950t", "TSC_950t2"])
    play = GiveRush(FRIENDLY_MINIONS + IDS(["TSC_950t", "TSC_950t2"]))


class TSC_950t:
    """Hydralodon Head"""

    # <b>Deathrattle:</b> If you control Hydralodon, summon 2 Hydralodon Heads.
    deathrattle = Find(FRIENDLY_MINIONS + ID("TSC_950")) & Summon(
        CONTROLLER, ["TSC_950t", "TSC_950t2"]
    )


class TSC_950t2(TSC_950t):
    """Hydralodon Head"""

    # <b>Deathrattle:</b> If you control Hydralodon, summon 2 Hydralodon Heads.
    pass


class TSC_071:
    """Twinbow Terrorcoil"""

    # [x]<b>Battlecry:</b> If you've cast a spell while holding this, your next
    # spell casts twice.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + SPELL)
    play = powered_up & Buff(CONTROLLER, "TSC_071e")


class TSC_071e:
    events = Play(CONTROLLER, SPELL).after(
        Battlecry(Play.CARD, Play.TARGET), Destroy(SELF)
    )


class TSC_073:
    """Raj Naz'jan"""

    # After you cast a spell, deal damage equal to its Cost to the enemy Hero.
    events = Play(CONTROLLER, SPELL).after(Hit(ENEMY_HERO, COST(Play.CARD)))


class TID_099:
    """K9-0tron"""

    # [x]<b>Battlecry:</b> <b>Dredge</b>. If it's a 1-Cost minion, summon it.
    play = Dredge(CONTROLLER).then(
        Find(Dredge.CARD + (COST == 1)) & Summon(CONTROLLER, Dredge.CARD)
    )


class TID_074(HoldingSpellThresholdUtils):
    """Ancient Krakenbane"""

    # [x]<b>Battlecry:</b> If you've cast three spells while holding this, deal
    # 5 damage.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Hit(TARGET, 5)


##
# Spells


class TSC_023:
    """Barbed Nets"""

    # [x]Deal $2 damage to an enemy. If you played a Naga while holding this,
    # choose a second target.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + NAGA)
    play = (
        Hit(TARGET, 2),
        powered_up
        & ChoiceTarget(CONTROLLER, ENEMY_CHARACTERS).then(Hit(ChoiceTarget.CARD, 2)),
    )


class TSC_929:
    """Emergency Maneuvers"""

    # <b>Secret:</b> When a friendly minion dies, summon a copy of it. It's
    # <b>Dormant</b> for 1 turn.
    secret = Death(FRIENDLY + MINION).on(
        Reveal(SELF),
        Summon(CONTROLLER, Copy(Death.ENTITY)).then(Dormant(Summon.CARD, 1)),
    )


class TSC_946:
    """Urchin Spines"""

    # Your spells this turn are <b>Poisonous</b>.
    play = Buff(CONTROLLER, "TSC_946e")


class TSC_946e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.POISONOUS: True})


class TSC_947:
    """Naga's Pride"""

    # Summon two 2/2 Lionfish. If you played a Naga while holding this, give
    # them +1/+1.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + NAGA)
    play = (
        Summon(CONTROLLER, "TSC_947t").then(powered_up & Buff(Summon.CARD, "TSC_947e"))
        * 2
    )


TSC_947e = buff(+1, +1)


class TSC_072:
    """Conch's Call"""

    # Draw a Naga and a spell.
    play = FORCE_DRAW(NAGA), FORCE_DRAW(SPELL)


class TID_075:
    """Shellshot"""

    # [x]Deal $3 damage to a random enemy minion. Repeat this with 1 less
    # damage.
    def play(self):
        damage = SPELL_DAMAGE(3).eval(self.game, self)
        while damage > 0:
            yield Hit(RANDOM_ENEMY_MINION, damage)
            damage -= 1


##
# Weapons


class TSC_070:
    """Harpoon Gun"""

    # After your hero attacks, <b>Dredge</b>. If it's a Beast, reduce its Cost
    # by (3).
    events = Attack(FRIENDLY_HERO).after(
        Dredge(CONTROLLER).then(
            Find(Dredge.CARD + BEAST) & Buff(Dredge.CARD, "TSC_070e")
        )
    )


@custom_card
class TSC_070e:
    tags = {
        GameTag.CARDNAME: "Harpoon Gun Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -3,
    }
    events = REMOVED_IN_PLAY
