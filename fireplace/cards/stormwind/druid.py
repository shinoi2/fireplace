from ..utils import *

##
# Minions


class SW_419:
    """Oracle of Elune"""

    # [x]After you play a minion that costs (2) or less, summon a copy of it.
    events = Play(FRIENDLY_MINIONS + (COST <= 2)).after(
        Summon(CONTROLLER, ExactCopy(Play.CARD))
    )


class SW_431:
    """Park Panther"""

    # [x]<b>Rush</b>. Whenever this attacks, give your hero +3 Attack this
    # turn.
    events = Attack(SELF).after(Buff(FRIENDLY_HERO, "SW_431e"))


SW_431e = buff(atk=3)


class SW_436:
    """Wickerclaw"""

    # After your hero gains Attack, this minion gains +2 Attack.
    events = Buff(FRIENDLY_HERO, ATK > 0).after(Buff(SELF, "SW_436e"))


SW_436e = buff(atk=2)


class SW_439:
    """Vibrant Squirrel"""

    # [x]<b>Deathrattle:</b> Shuffle 4 Acorns into your deck. When drawn,
    # summon a 2/1 Squirrel.
    deathrattle = Shuffle(CONTROLLER, "SW_439t") * 4


class SW_439t:
    """Acorn"""

    play = Summon(CONTROLLER, "SW_439t2")


class SW_447:
    """Sheldras Moontree"""

    # [x]<b>Battlecry:</b> The next 3 spells you draw are <b>Cast When
    # Drawn</b>.
    play = Buff(CONTROLLER, "SW_447e")


class SW_447e:
    progress_total = 3
    events = Draw(CONTROLLER).on(
        (CURRENT_PROGRESS(SELF) < 3) & Buff(Draw.CARD, "SW_447e2"),
        AddProgress(SELF, Draw.CARD),
    )
    reward = Destroy(SELF)


SW_447e2 = buff(casts_when_drawn=True)


class DED_001:
    """Druid of the Reef"""

    # [x]<b>Choose One - </b>Transform into a 3/1 Shark with <b>Rush</b>; or a
    # 1/3 Turtle with <b>Taunt</b>.
    choose = ("DED_001a", "DED_001b")
    play = ChooseBoth(CONTROLLER) & Morph(SELF, "DED_001c")


class DED_001a:
    play = Morph(SELF, "DED_001at")


class DED_001b:
    play = Morph(SELF, "DED_001bt")


class DED_003:
    """Jerry Rig Carpenter"""

    # <b>Battlecry:</b> Draw a <b>Choose One</b> spell and split it.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + CHOOSE_ONE + SPELL)).then(
        Give(CONTROLLER, Copy(CHOOSE_CARDS(ForceDraw.TARGET))), Remove(ForceDraw.TARGET)
    )


##
# Spells


class SW_422:
    """Sow the Soil"""

    # <b>Choose One</b> - Give your minions +1 Attack; or_ Summon a 2/2 Treant.
    choose = ("SW_422a", "SW_422b")
    play = ChooseBoth(CONTROLLER) & (
        Summon(CONTROLLER, "SW_422t"),
        Buff(FRIENDLY_MINIONS, "SW_422e"),
    )


class SW_422a:
    play = Buff(FRIENDLY_MINIONS, "SW_422e")


class SW_422b:
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "SW_422t")


class SW_428:
    """Lost in the Park"""

    # <b>Questline:</b> Gain 4 Attack with your hero. <b>Reward:</b> Gain 5
    # Armor.
    quest = Buff(FRIENDLY_HERO, ATK > 0).after(
        AddProgress(SELF, Buff.TARGET, ATK(Buff.BUFF))
    )
    reward = (GainArmor(FRIENDLY_HERO, 5), Summon(CONTROLLER, "SW_428t"))


class SW_428t:
    """Defend the Squirrels"""

    # <b>Questline:</b> Gain 5 Attack with your hero. <b>Reward:</b> Gain 5
    # Armor and draw a card.
    quest = Buff(FRIENDLY_HERO, ATK > 0).after(
        AddProgress(SELF, Buff.TARGET, ATK(Buff.BUFF))
    )
    reward = (
        GainArmor(FRIENDLY_HERO, 5),
        Draw(CONTROLLER),
        Summon(CONTROLLER, "SW_428t"),
    )


class SW_428t2(QuestRewardProtect):
    """Feral Friendsy"""

    # [x]<b>Questline:</b> Gain 6 Attack with your hero. <b>Reward:</b> Guff
    # the Tough.
    quest = Buff(FRIENDLY_HERO, ATK > 0).after(
        AddProgress(SELF, Buff.TARGET, ATK(Buff.BUFF))
    )
    reward = Give(CONTROLLER, "SW_428t4")


class SW_428t4:
    """Guff the Tough"""

    # [x]<b>Taunt</b>. <b>Battlecry:</b> Give your hero +8 Attack this turn.
    # Gain 8 Armor.
    play = Buff(FRIENDLY_HERO, "SW_428t4e"), GainArmor(FRIENDLY_HERO, 8)


SW_428t4e = buff(atk=8)


class SW_429:
    """Best in Shell"""

    # [x]<b>Tradeable</b> Summon two 2/7 _Turtles with <b>Taunt</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "SW_429t") * 2


class SW_432:
    """Kodo Mount"""

    # Give a minion +4/+2 and <b>Rush</b>. When it dies, summon a Kodo.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 1,
    }
    play = Buff(TARGET, "SW_432e")


class SW_432e:
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.RUSH: True,
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Summon(CONTROLLER, "SW_432t")


class SW_437:
    """Composting"""

    # Give your minions "<b>Deathrattle:</b> Draw __a card."
    play = Buff(FRIENDLY_MINIONS, "SW_437e")


class SW_437e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Draw(CONTROLLER)


class DED_002:
    """Moonlit Guidance"""

    # [x]<b>Discover</b> a copy of a card in your deck. If you play it this
    # turn, draw the original.
    play = Choice(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK))).then(
        Give(CONTROLLER, StoringBuff(Copy(Choice.CARD), "DED_002e", Choice.CARD))
    )


class DED_002e:
    event = Play(OWNER).on(
        Find(FRIENDLY_DECK + STORE_CARD) & ForceDraw(STORE_CARD),
        Destroy(SELF),
    )
