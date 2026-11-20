from ..utils import *

##
# Minions


class RLK_831:
    """Plaguespreader"""

    # <b>Deathrattle:</b> Transform a random minion in your opponent's hand
    # into a Plaguespreader.
    deathrattle = Morph(RANDOM(ENEMY_HAND + MINION), "RLK_831")


class RLK_952:
    """Enchanter"""

    # Enemy minions take double damage during your turn.
    update = CurrentPlayer(CONTROLLER) & Refresh(
        ENEMY_MINIONS, {GameTag.INCOMING_DAMAGE_MULTIPLIER: 1}
    )


class RLK_221:
    """Crystal Broker"""

    # [x]<b>Manathirst (5):</b> Summon a random 3-Cost minion. <b>Manathirst
    # (10):</b> Summon an 8-Cost minion instead.
    play = Manathirst(10) & Summon(CONTROLLER, RandomMinion(cost=8)) | (
        Manathirst(5) & Summon(CONTROLLER, RandomMinion(cost=3))
    )


class RLK_970:
    """Hawkstrider Rancher"""

    # [x]Whenever you play a minion, give it +1/+1 and "<b>Deathrattle:</b>
    # Summon a_ 1/1 Hawkstrider."
    events = OWN_MINION_PLAY.on(Buff(Play.CARD, "RLK_970e"))


class RLK_677:
    """Sanctum Spellbender"""

    # [x]Whenever your opponent targets another minion with a spell, redirect
    # it to this.
    events = Play(OPPONENT, SPELL, ALL_MINIONS - SELF).on(Retarget(Play.CARD, SELF))


class RLK_970e:
    tags = {GameTag.ATK: 1, GameTag.HEALTH: 1, GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "RLK_970t")
