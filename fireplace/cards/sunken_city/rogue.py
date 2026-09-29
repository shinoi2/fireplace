from ..utils import *

##
# Minions


class TSC_933:
    """Bootstrap Sunkeneer"""

    # [x]<b>Combo:</b> Put an enemy minion on the bottom of _your opponent's
    # deck.
    requirements = {
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    combo = PutOnBottom(OPPONENT, TARGET)


class TSC_934(CustomThresholdUtils("times_pirate_summoned_this_game", 8)):
    """Pirate Admiral Hooktusk"""

    # <b>Battlecry:</b> If you've summoned 8 other Pirates this game, plunder
    # the enemy!@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = Choice(CONTROLLER, ["TSC_934t", "TSC_934t2", "TSC_934t3"]).then(
        Battlecry(Choice.CARD, None)
    )


class TSC_934t:
    """Take their Supplies!"""

    # Take 5 cards from your opponent's deck.
    play = Give(CONTROLLER, RANDOM(ENEMY_DECK, 5))


class TSC_934t2:
    """Take their Gold!"""

    # Take 2 cards from your opponent's hand.
    play = Give(CONTROLLER, RANDOM(ENEMY_HAND, 2))


class TSC_934t3:
    """Take their Ship!"""

    # Take control of your opponent's highest Attack minion.
    play = Steal(RANDOM(HIGHEST_ATK(ENEMY_MINIONS)))


class TSC_936:
    """Swiftscale Trickster"""

    # <b>Battlecry:</b> Your next spell this turn costs (0).
    play = Buff(CONTROLLER, "TSC_936e")


class TSC_936e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: SET(0)})
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class TSC_937:
    """Crabatoa"""

    # <b>Colossal +2</b> Your Crabatoa Claws have +2 Attack.
    colossal = SummonBothSides(CONTROLLER, "TSC_937t", "TSC_937t3")
    update = Refresh(
        FRIENDLY + IDS(["TSC_937t", "TSC_937t2", "TSC_937t3"]), {GameTag.ATK: +2}
    )


class TSC_937t:
    """Crabatoa's Claw"""

    # <b>Rush</b> <b>Deathrattle:</b>  Equip a 2/1 Claw.
    deathrattle = Summon(CONTROLLER, "TSC_937t2")


class TSC_937t3(TSC_937t):
    """Crabatoa's Claw"""

    # <b>Rush</b> <b>Deathrattle:</b>  Equip a 2/1 Claw.
    pass


class TSC_963:
    """Filletfighter"""

    # <b>Battlecry:</b> Deal 1 damage.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 1)


class TID_078:
    """Shattershambler"""

    # <b>Battlecry:</b> Your next <b>Deathrattle</b> minion costs (1) less, but
    # immediately dies when played.
    play = Buff(CONTROLLER, "TID_078e")


class TID_078e:
    update = Refresh(FRIENDLY_HAND + DEATHRATTLE, {GameTag.COST: -1})
    events = Play(CONTROLLER, DEATHRATTLE).after(Destroy(Play.CARD), Destroy(SELF))


class TID_080:
    """Inkveil Ambusher"""

    # <b>Stealth</b> Has +3 Attack and <b>Immune</b> while attacking.
    update = Attacking(SELF) & Refresh(SELF, buff="TID_080e2")


TID_080e2 = buff(atk=3)


class TSC_085:
    """Cutlass Courier"""

    # After your hero attacks, draw a Pirate.
    events = Attack(FRIENDLY_HERO).after(FORCE_DRAW(PIRATE))


##
# Spells


class TSC_912:
    """Azsharan Vessel"""

    # Summon two 3/3 Pirates with <b>Stealth</b>. Put a 'Sunken Vessel' on the
    # bottom of your deck.
    play = Summon(CONTROLLER, ["TSC_912t2", "TSC_912t3"]), PutOnBottom(
        CONTROLLER, "TSC_912t"
    )


class TSC_912t:
    """Sunken Vessel"""

    # <b>Casts When Drawn</b> Summon two 3/3 Pirates with <b>Stealth</b>.
    play = Summon(CONTROLLER, ["TSC_912t2", "TSC_912t3"])


class TSC_916:
    """Gone Fishin'"""

    # <b>Dredge</b>. <b>Combo:</b> Draw a card.
    play = Dredge(CONTROLLER)
    combo = Dredge(CONTROLLER), Draw(CONTROLLER)


class TSC_932:
    """Blood in the Water"""

    # Deal $3 damage to an enemy. Summon a 5/5 Shark with <b>Rush</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Hit(TARGET, 3), Summon(CONTROLLER, "TSC_932t")


class TID_931:
    """Jackpot!"""

    # Add two random spells from other classes that cost (5) or more to your
    # hand.
    play = Give(
        CONTROLLER, RandomSpell(card_class=ANOTHER_CLASS, cost=range(5, 100)) * 2
    )


##
# Weapons


class TSC_086:
    """Swordfish"""

    # <b>Battlecry:</b> <b>Dredge</b>. If it's a Pirate, give this weapon and
    # the Pirate +2 Attack.
    play = Dredge(CONTROLLER).then(
        Find(Dredge.CARD + PIRATE)
        & (Buff(SELF, "TSC_086e"), Buff(Dredge.CARD, "TSC_086e"))
    )


TSC_086e = buff(atk=2)
