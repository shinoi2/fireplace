from ..utils import *

##
# Minions


class REV_310:
    """Death Blossom Whomper"""

    # <b>Battlecry:</b> Draw a <b>Deathrattle</b> minion and gain its
    # <b>Deathrattle.</b>
    play = FORCE_DRAW(DEATHRATTLE + MINION).then(
        CopyDeathrattleBuff(ForceDraw.TARGET, "REV_310e")
    )


class REV_314:
    """Topior the Shrubbagazzor"""

    # [x]<b>Battlecry:</b> For the rest of the game, after you cast a Nature
    # spell, summon a 3/3 Whelp with <b>Rush</b>.
    play = Buff(CONTROLLER, "REV_314e")


class REV_314e:
    events = Play(CONTROLLER, NATURE).after(Summon(CONTROLLER, "REV_314t"))


class REV_318:
    """Widowbloom Seedsman"""

    # [x]<b>Battlecry:</b> Draw a Nature spell. Gain an empty Mana Crystal.
    play = FORCE_DRAW(NATURE), GainEmptyMana(CONTROLLER, 1)


class REV_319:
    """Sesselie of the Fae Court"""

    # [x]<b>Taunt</b> <b>Deathrattle</b>: Draw a minion. Reduce its Cost by
    # (8).
    deathrattle = FORCE_DRAW(MINION).then(Buff(ForceDraw.TARGET, "REV_319e"))


REV_319e = cost_buff(cost=-8)


class MAW_025:
    """Attorney-at-Maw"""

    # <b>Choose One -</b> <b>Silence</b> a minion; or Give a minion
    # <b>Immune</b> this turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    choose = ("MAW_025a", "MAW_025b")
    play = ChooseBoth(CONTROLLER) & (Silence(TARGET), Buff(TARGET, "MAW_025e"))


MAW_025e = buff(immune=True)


class MAW_025a:
    """Guilty!"""

    # <b>Silence</b> a minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Silence(TARGET)


class MAW_025b:
    """Innocent!"""

    # Give a minion <b>Immune</b> this turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "MAW_025e")


##
# Spells


class MAW_026:
    """Incarceration"""

    # [x]Choose a minion. It goes <b>Dormant</b> for 3 turns.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Dormant(TARGET, 3)


class REV_307:
    """Natural Causes"""

    # Deal $2 damage. Summon a 2/2 Treant.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2), Summon(CONTROLLER, "REV_336t2")


class REV_311:
    """Nightshade Bud"""

    # <b>Choose One - </b><b>Discover</b> a minion from your deck to summon; or
    # a spell to cast.
    choose = ("REV_311t", "REV_311t2")
    play = ChooseBoth(CONTROLLER) & (
        Discover(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + SPELL), 3)).then(
            CastSpell(Discover.CARD)
        ),
        Discover(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + MINION), 3)).then(
            CastSpell(Discover.CARD)
        ),
    )


class REV_311t:
    """Sunlight Blossom"""

    # <b>Discover</b> a spell from your deck to cast.
    play = Discover(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + SPELL), 3)).then(
        CastSpell(Discover.CARD)
    )


class REV_311t2:
    """Moonlight Blossom"""

    # [x]<b>Discover</b> a minion from your deck to summon.
    play = Discover(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + MINION), 3)).then(
        Summon(CONTROLLER, Discover.CARD)
    )


class REV_313:
    """Planted Evidence"""

    # <b>Discover</b> a spell. It costs (2) less this turn.
    play = Discover(CONTROLLER, RandomSpell()).then(Buff(Discover.CARD, "REV_313e"))


REV_313e = cost_buff(cost=-2)


class REV_336:
    """Plot of Sin"""

    # [x]Summon two 2/2 Treants. <b>Infuse (@):</b> Two 5/5 Ancients instead.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    infuse_card = "REV_336t4"
    play = Summon(CONTROLLER, "REV_336t2") * 2


class REV_336t4:
    """Plot of Sin"""

    # <b>Infused</b> Summon two 5/5 Ancients.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "REV_336t3") * 2


class REV_365:
    """Convoke the Spirits"""

    # [x]Cast 8 random Druid spells <i>(targets chosen randomly)</i>.
    play = CastSpell(RandomSpell(card_class=CardClass.DRUID)) * 8


class MAW_024:
    """Dew Process"""

    # [x]For the rest of the game, players draw an extra card at the start of
    # their turn.
    play = Buff(ALL_PLAYERS, "MAW_024e2")


class MAW_024e2:
    events = OWN_TURN_BEGIN.on(Draw(CONTROLLER))


##
# Locations


class REV_333:
    """Hedge Maze"""

    # Trigger a friendly minion's <b>Deathrattle</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    activate = Deathrattle(TARGET)
