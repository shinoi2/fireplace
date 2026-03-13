from ..utils import *

##
# Minions


class BAR_316:
    """Oil Rig Ambusher"""

    # [x]<b>Battlecry:</b> Deal 2 damage. If this entered your hand _this turn,
    # deal 4 instead.
    play = Find(DRAWN_THIS_TURN + SELF) & Hit(TARGET, 4) | Hit(TARGET, 2)


class BAR_317:
    """Field Contact"""

    # [x]After you play a <b>Battlecry</b> or <b>Combo</b> card, draw a card.
    events = Play(CONTROLLER, (BATTLECRY | COMBO)).after(Draw(CONTROLLER))


class BAR_320:
    """Efficient Octo-bot"""

    # <b>Frenzy:</b> Reduce the cost of cards in your hand by (1).
    frenzy = Buff(FRIENDLY_HAND, "BAR_320e")


class BAR_320e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class BAR_324:
    """Apothecary Helbrim"""

    # <b>Battlecry and Deathrattle:</b> Add a random Poison to your hand.
    entourage = POISONS
    play = deathrattle = Give(CONTROLLER, RandomEntourage())


class BAR_552:
    """Scabbs Cutterbutter"""

    # [x]<b>Combo:</b> The next two cards you play this turn cost (3) less.
    combo = Buff(CONTROLLER, "BAR_552e")


class BAR_552e:
    tags = {GameTag.TAG_ONE_TURN_EFFECT: True}
    update = Refresh(FRIENDLY_HAND, {GameTag.COST: -3})
    events = Play(CONTROLLER, (BATTLECRY | COMBO)).after(
        Destroy(SELF), Buff(CONTROLLER, "BAR_552o")
    )


class BAR_552o:
    update = Refresh(FRIENDLY_HAND, {GameTag.COST: -3})
    events = Play(CONTROLLER, (BATTLECRY | COMBO)).after(Destroy(SELF))


class WC_015:
    """Water Moccasin"""

    # [x]<b>Stealth</b> Has <b>Poisonous</b> while you _have no other minions.
    update = Find(FRIENDLY_MINIONS - SELF) | Refresh(SELF, {GameTag.POISONOUS: True})


##
# Spells


class BAR_318:
    """Silverleaf Poison"""

    # [x]Give your weapon "After your hero attacks, draw a card."
    play = Buff(FRIENDLY_WEAPON, "BAR_318e")


class BAR_318e:
    events = Attack(FRIENDLY_HERO).after(Draw(CONTROLLER))


class BAR_319:
    """Wicked Stab (Rank 1)"""

    # Deal $2 damage. <i>(Upgrades when you have 5 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_319t")

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2)


class BAR_319t:
    """Wicked Stab (Rank 2)"""

    # Deal $4 damage. <i>(Upgrades when you have 10 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_319t2")

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4)


class BAR_319t2:
    """Wicked Stab (Rank 3)"""

    # Deal $6 damage.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 6)


class BAR_321:
    """Paralytic Poison"""

    # [x]Give your weapon +1 Attack and "Your hero is <b>Immune</b> while
    # attacking."
    play = Buff(FRIENDLY_WEAPON, "BAR_321e")


class BAR_321e:
    tags = {GameTag.ATK: 1}
    update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class BAR_323:
    """Yoink!"""

    # <b>Discover</b> a Hero Power and set its Cost to (0). Swap back after 2
    # uses.
    def play(self):
        player = self.controller
        old_hero_power = player.hero_power
        yield GenericChoice(CONTROLLER, RandomBasicHeroPower() * 3).then(
            StoringBuff(GenericChoice.CARD, "BAR_323e", [old_hero_power])
        )


class BAR_323e:
    cost = SET(0)
    events = Activate(FRIENDLY_HERO_POWER).after(
        (Attr(FRIENDLY_HERO_POWER, "activations_this_game") >= 2)
        & (Summon(CONTROLLER, STORE_CARD), Destroy(SELF))
    )


class WC_016:
    """Shroud of Concealment"""

    # Draw 2 minions. Any played this turn gain <b>Stealth</b> for 1 turn.
    play = (
        ForceDraw(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)).then(
            Buff(ForceDraw.TARGET, "WC_016e")
        )
        * 2
    )


class WC_016e:
    events = Play(CONTROLLER, OWNER).after(
        Stealth(OWNER),
        Buff(OWNER, "WC_016e2"),
        Destroy(SELF),
    )


class WC_016e2:
    events = OWN_TURN_BEGIN.on(
        Unstealth(OWNER),
        Destroy(SELF),
    )


class WC_017:
    """Savory Deviate Delight"""

    # [x]Transform a minion in both players' hands into a Pirate or
    # <b>Stealth</b> minion.
    play = Morph(
        RANDOM(FRIENDLY_HAND + MINION),
        RandomMinion(
            custom_filter=lambda card: (Race.PIRATE in card.races) or (card.stealth)
        ),
    ), Morph(
        RANDOM(ENEMY_HAND + MINION),
        RandomMinion(
            custom_filter=lambda card: (Race.PIRATE in card.races) or (card.stealth)
        ),
    )


##
# Weapons


class BAR_322:
    """Swinetusk Shank"""

    # [x]After you play a Poison, _gain +1 Durability.
    events = Play(CONTROLLER, IDS(POISONS)).after(Buff(FRIENDLY_WEAPON, "BAR_322e"))


BAR_322e = buff(health=1)
