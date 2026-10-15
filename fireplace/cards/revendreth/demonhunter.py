from ..utils import *

##
# Minions


class REV_937:
    """Artificer Xy'mox"""

    # [x]<b>Battlecry:</b> <b>Discover</b> and cast a Relic. <b>Infuse (@):</b>
    # Cast all three instead.
    infuse_card = "REV_937t"
    play = Choice(CONTROLLER, RELICS).then(CastSpell(Choice.CARD))


class REV_937t:
    """Artificer Xy'mox"""

    # [x]<b>Infused</b> <b>Battlecry:</b> Cast all three Relics.
    play = CastSpell(RELICS)


class REV_510:
    """Kryxis the Voracious"""

    # [x]<b>Battlecry</b>: Discard your hand. <b>Deathrattle:</b> Draw 3 cards.
    play = Discard(FRIENDLY_HAND)
    deathrattle = Draw(CONTROLLER) * 3


class REV_511:
    """Bibliomite"""

    # [x]<b>Battlecry</b>: Choose a card in your hand to shuffle into your
    # deck.
    play = Choice(CONTROLLER, FRIENDLY_HAND).then(Shuffle(CONTROLLER, Choice.CARD))


class MAW_008:
    """Sightless Magistrate"""

    # <b>Battlecry:</b> Both players draw until they have 5 cards.
    play = DrawUntil(ALL_PLAYERS, 5)


class MAW_014:
    """Prosecutor Mel'tranix"""

    # [x]<b>Battlecry:</b> Your opponent can only play their left- and right-
    # most cards on their next turn.
    play = Buff(OPPONENT, "MAW_014e2")


class MAW_014e2:
    update = Refresh(
        FRIENDLY_HAND - OUTERMOST(FRIENDLY_HAND), {GameTag.CANT_PLAY: True}
    )
    events = OWN_TURN_END.on(Destroy(SELF))


##
# Spells


class REV_943:
    """Relic of Phantasms"""

    # Summon two @/@ Spirits. Improve your future Relics.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = (
        SummonCustomMinion(
            CONTROLLER,
            "REV_943t",
            AttrValue(enums.RELIC_LEVEL)(CONTROLLER),
            AttrValue(enums.RELIC_LEVEL)(CONTROLLER),
            AttrValue(enums.RELIC_LEVEL)(CONTROLLER),
        )
        * 2,
        AddTag(CONTROLLER, {enums.RELIC_LEVEL: 1}),
    )


class REV_506:
    """Sinful Brand"""

    # [x]Brand an enemy minion. Whenever it takes damage, deal 2 damage to the
    # enemy hero.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Buff(TARGET, "REV_506e")


class REV_506e:
    events = Damage(OWNER).on(Hit(FRIENDLY_HERO, 2))


class REV_507:
    """Dispose of Evidence"""

    # Give your hero +3 Attack this turn. Choose a card in your hand to shuffle
    # into your deck.
    play = Buff(FRIENDLY_HERO, "REV_507e"), Choice(CONTROLLER, FRIENDLY_HAND).then(
        Shuffle(CONTROLLER, Choice.CARD)
    )


REV_507e = buff(atk=3)


class REV_508:
    """Relic of Dimensions"""

    # [x]Draw two cards and reduce their Cost by (@). Improve your future
    # Relics.
    play = (
        Draw(CONTROLLER).then(
            Buff(Draw.CARD, "REV_508e") * AttrValue(enums.RELIC_LEVEL)(CONTROLLER)
        )
        * 2,
        AddTag(CONTROLLER, {enums.RELIC_LEVEL: 1}),
    )


REV_508e = buff(cost=-1)


class REV_834:
    """Relic of Extinction"""

    # Deal $@ damage to a random enemy minion, twice. Improve your future
    # Relics.
    play = (
        Hit(RANDOM_ENEMY_MINION, AttrValue(enums.RELIC_LEVEL)(CONTROLLER)),
        AddTag(CONTROLLER, {enums.RELIC_LEVEL: 1}),
    )


class MAW_012:
    """All Fel Breaks Loose"""

    # [x]Summon a friendly Demon that died this game. <b>Infuse (@ Demons):</b>
    # Summon three instead.
    requirements = {
        PlayReq.REQ_FRIENDLY_MINIONS_OF_RACE_DIED_THIS_GAME: Race.DEMON,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + DEMON)))


class MAW_012t:
    """All Fel Breaks Loose"""

    # <b>Infused</b> Summon three friendly Demons that died this game.
    requirements = {
        PlayReq.REQ_FRIENDLY_MINIONS_OF_RACE_DIED_THIS_GAME: Race.DEMON,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + DEMON, 3)))


##
# Weapons


class REV_509:
    """Magnifying Glaive"""

    # [x]After your hero attacks, draw until you have 3 cards.
    events = Attack(FRIENDLY_HERO).after(DrawUntil(CONTROLLER, 3))


##
# Locations


class REV_942:
    """Relic Vault"""

    # The next Relic you play this turn casts twice.
    activate = Buff(CONTROLLER, "REV_942e")


class REV_942e:
    events = Play(CONTROLLER, IDS(RELICS)).after(
        CastSpell(Copy(Play.CARD)),
        Destroy(SELF),
    )
