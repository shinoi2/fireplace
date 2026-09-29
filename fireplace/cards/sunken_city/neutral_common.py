from ..utils import *

##
# Minions


class TID_713:
    """Bubbler"""

    # [x]After this minion takes exactly one damage, destroy it. <i>(Pop!)</i>
    events = Damage(SELF, 1).after(Destroy(SELF))


class TSC_001:
    """Naval Mine"""

    # [x]<b>Deathrattle:</b> Deal 4 damage to the enemy hero.
    deathrattle = Hit(ENEMY_HERO, 4)


class TSC_002:
    """Pufferfist"""

    # After your hero attacks, deal 1 damage to all enemies.
    events = Attack(FRIENDLY_HERO).after(Hit(ENEMY_CHARACTERS, 1))


class TSC_007:
    """Gangplank Diver"""

    # <b>Dormant</b> for 1 turn. <b>Rush</b>. <b>Immune</b> while attacking.
    dormant_turns = 1


class TSC_017:
    """Baba Naga"""

    # <b>Battlecry:</b> If you've cast a spell while holding this, deal 3
    # damage.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_CAST_SPELL_WHILE_HOLDING: 0}
    play = Hit(TARGET, 3)


class TSC_020:
    """Barbaric Sorceress"""

    # <b>Taunt</b>. <b>Battlecry:</b> Swap the Cost of a random spell in each
    # player's hand.
    play = SwapStateBuff(
        RANDOM(FRIENDLY_HAND + SPELL), RANDOM(ENEMY_HAND + SPELL), "TSC_020e"
    )


class TSC_020e:
    cost = lambda self, i: self._xcost
    events = REMOVED_IN_PLAY


class TSC_013:
    """Slimescale Diver"""

    # <b>Dormant</b> for 1 turn. <b>Rush</b>, <b>Poisonous</b>
    dormant_turns = 1


class TSC_823:
    """Murkwater Scribe"""

    # <b>Battlecry:</b> The next spell you play costs (1) less.
    play = Buff(CONTROLLER, "TSC_823e")


class TSC_823e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class TSC_034:
    """Gorloc Ravager"""

    # [x]<b>Battlecry:</b> Draw 3 Murlocs.
    play = FORCE_DRAW(MURLOC) * 3


class TSC_909:
    """Tuskarrrr Trawler"""

    # <b>Battlecry:</b> <b>Dredge</b>.
    play = Dredge(CONTROLLER)


class TSC_911:
    """Excavation Specialist"""

    # <b>Battlecry:</b> <b>Dredge</b>. Reduce its Cost by (1).
    play = Dredge(CONTROLLER).then(Buff(Dredge.CARD, "TSC_911e"))


@custom_card
class TSC_911e:
    tags = {
        GameTag.CARDNAME: "Excavation Specialist Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -1,
    }
    events = REMOVED_IN_PLAY


class TSC_919:
    """Azsharan Sentinel"""

    # [x]<b>Taunt</b>. <b>Deathrattle:</b> Put a 'Sunken Sentinel' on the
    # bottom of your deck.
    deathrattle = PutOnBottom(CONTROLLER, "TSC_919t")


class TSC_928:
    """Security Automaton"""

    # After you summon a Mech, gain +1/+1.
    events = Summon(CONTROLLER, MECH).after(Buff(SELF, "TSC_928e"))


TSC_928e = buff(1, 1)


class TSC_632:
    """Click-Clocker"""

    # [x]<b>Divine Shield</b>. <b>Battlecry:</b> Give a random Mech in your
    # hand +1/+1.
    play = Buff(RANDOM(FRIENDLY_HAND + MECH), "TSC_632e")


TSC_632e = buff(1, 1)


class TSC_935:
    """Selfish Shellfish"""

    # <b>Deathrattle:</b> Your opponent draws 2 cards.
    deathrattle = Draw(OPPONENT) * 2


class TSC_638:
    """Piranha Swarmer"""

    # [x]<b>Rush</b> After you summon a Piranha Swarmer, gain +1 Attack.
    events = Summon(CONTROLLER, ID("TSC_638")).after(Buff(SELF, "TSC_638e"))


TSC_638e = buff(atk=1)


class TSC_938:
    """Treasure Guard"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Draw a card.
    deathrattle = Draw(CONTROLLER)


class TSC_640:
    """Reefwalker"""

    # <b>Battlecry and Deathrattle:</b> Summon a 1/1 Piranha Swarmer.
    play = deathrattle = Summon(CONTROLLER, "TSC_638")


class TSC_646:
    """Seascout Operator"""

    # <b>Battlecry:</b> If you control a Mech, summon two 2/1 Mechafish.
    powered_up = Find(FRIENDLY_MINIONS + MECH)
    play = powered_up & (SummonBothSides(CONTROLLER, "TSC_646t") * 2)


class TSC_647:
    """Pelican Diver"""

    # <b>Dormant</b> for 1 turn. <b>Rush</b>
    dormant_turns = 1
