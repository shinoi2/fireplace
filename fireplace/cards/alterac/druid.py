from ..utils import *

##
# Minions


class AV_210:
    """Pathmaker"""

    # [x]<b>Battlecry:</b> Cast the other choice from the last <b>Choose
    # One</b> spell you've cast. @<b>Battlecry:</b> {0}
    def play(self):
        if spell := self.controller.other_choice_from_the_last_choose_one_spell:
            yield CastSpell(CONTROLLER, spell)


class AV_211:
    """Dire Frostwolf"""

    # <b>Stealth</b> <b>Deathrattle:</b> Summon a 2/2 Wolf with <b>Stealth</b>.
    deathrattle = Summon(CONTROLLER, "AV_211t") * 2


class AV_291:
    """Frostsaber Matriarch"""

    # [x]<b>Taunt</b>. Costs (1) less for each Beast you've _summoned this
    # game.
    cost_mod = -Attr(CONTROLLER, "times_beast_summoned_this_game")


class AV_293:
    """Wing Commander Mulverick"""

    # [x]<b>Rush</b>. Your minions have "<b>Honorable Kill:</b> Summon a_ 2/2
    # Wyvern with <b>Rush</b>."
    update = Refresh(FRIENDLY_MINIONS, buff="AV_293e")


class AV_293e:
    tags = {GameTag.HONORABLE_KILL: True}
    honorable_kill = Summon(CONTROLLER, "AV_293t")


class AV_294:
    """Clawfury Adept"""

    # <b>Battlecry:</b> Give all other friendly characters +1 Attack this turn.
    play = Buff(FRIENDLY_CHARACTERS - SELF, "AV_294e")


AV_294e = buff(atk=1)


class AV_296:
    """Pride Seeker"""

    # [x]<b>Battlecry:</b> Your next <b>Choose One</b> card costs (2) less.
    play = Buff(CONTROLLER, "AV_296e")


class AV_296e:
    update = Refresh(FRIENDLY_HAND + CHOOSE_ONE, {GameTag.COST: -2})
    events = Play(CONTROLLER, CHOOSE_ONE).after(Destroy(SELF))


class ONY_018:
    """Boomkin"""

    # <b>Choose One - </b>Restore 8 Health to your hero; or Deal 4 damage.
    choose = ("ONY_018t", "ONY_018t2")
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = ChooseBoth(CONTROLLER) & (Heal(FRIENDLY_HERO, 8), Hit(TARGET, 4))


class ONY_018t:
    """Eyes of the Moon"""

    # Restore 8 Health to your hero.
    play = Heal(FRIENDLY_HERO, 8)


class ONY_018t2:
    """Heart of the Sun"""

    # Deal 4 damage.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)


class ONY_019:
    """Raid Negotiator"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a <b>Choose One</b> card. It has
    # both effects combined.
    play = Discover(
        CONTROLLER, RandomCollectible(choose_one=True, card_class=CardClass.DRUID)
    ).then(
        Give(CONTROLLER, Discover.CARD),
        Buff(Discover.CARD, "ONY_019e"),
        # Give(CONTROLLER, Buff(Discover.CARD, "ONY_019e"))
    )


ONY_019e = buff(choose_both=True)


##
# Spells


class AV_292:
    """Heart of the Wild"""

    # Give a minion +2/+2, then give your Beasts +1/+1.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "AV_292e"), Buff(FRIENDLY_MINIONS + BEAST, "AV_292e2")


AV_292e = buff(+2, +2)
AV_292e2 = buff(+1, +1)


class AV_295:
    """Capture Coldtooth Mine"""

    # <b>Choose One -</b> Draw your lowest Cost card; or Draw your highest Cost
    # card.
    choose = ("AV_295a", "AV_295b")
    play = ChooseBoth(CONTROLLER) & (
        ForceDraw(CONTROLLER, RANDOM(LOWEST_COST(FRIENDLY_DECK))),
        ForceDraw(CONTROLLER, RANDOM(HIGHEST_COST(FRIENDLY_DECK))),
    )


class AV_295a:
    """More Resources"""

    # Draw your lowest Cost card.
    play = ForceDraw(CONTROLLER, RANDOM(LOWEST_COST(FRIENDLY_DECK)))


class AV_295b:
    """More Supplies"""

    # Draw your highest Cost card.
    play = ForceDraw(CONTROLLER, RANDOM(HIGHEST_COST(FRIENDLY_DECK)))


class ONY_021:
    """Scale of Onyxia"""

    # Fill your board with 2/1 Whelps with <b>Rush</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "ONY_001t") * 7


class AV_360:
    """Frostwolf Kennels"""

    # [x]At the end of your turn, summon a 2/2 Wolf with <b>Stealth</b>. Lasts
    # 3 turns.
    events = OWN_TURN_END.on(Summon(CONTROLLER, "AV_211t"))


##
# Heros


class AV_205:
    """Wildheart Guff"""

    # [x]<b>Battlecry:</b> Set your maximum Mana to 20. Gain a Mana Crystal.
    # Draw a card.
    play = (
        SetTags(CONTROLLER, {GameTag.MAXRESOURCES: SET(20)}),
        GainMana(CONTROLLER, 1),
        Draw(CONTROLLER, 1),
    )


class AV_205p:
    """Nurture"""

    # [x]<b>Hero Power</b> <b>Choose One -</b> Draw a card; or Gain a Mana
    # Crystal.
    choose = ("AV_205a", "AV_205pb")
    activate = ChooseBoth(CONTROLLER) & (GainMana(CONTROLLER, 1), Draw(CONTROLLER, 1))


class AV_205a:
    """Ice Blossom"""

    # Gain a Mana Crystal.
    activate = GainMana(CONTROLLER, 1)


class AV_205pb:
    """Valley Root"""

    # Draw a card.
    activate = Draw(CONTROLLER, 1)
