from ..utils import *

##
# Minions


class REV_826:
    """Private Eye"""

    # [x]<b>Battlecry:</b> Cast a <b>Secret</b> from your deck. _<b>Combo:</b>
    # Cast 2 instead.
    play = CastSpell(RANDOM(FRIENDLY_DECK + SECRET + IS_SUMMONABLE))
    combo = CastSpell(RANDOM(FRIENDLY_DECK + SECRET + IS_SUMMONABLE)) * 2


class REV_829:
    """Halkias"""

    # [x]<b>Stealth</b>. <b>Deathrattle:</b> Store Halkias's soul inside of a
    # friendly <b>Secret</b>. It resummons Halkias when triggered.
    deathrattle = Buff(RANDOM(FRIENDLY_SECRETS), "REV_829e")


class REV_940:
    """Necrolord Draka"""

    # [x]<b>Battlecry:</b> Equip a @/3 Dagger. <i>(+1 Attack for each other
    # card you played this turn!)</i>
    play = Summon(CONTROLLER, "REV_940t").then(
        SetStats(Summon.CARD, "REV_940e", NUM_CARDS_PLAYED_THIS_TURN + 1, 3)
    )


class REV_959:
    """Ghastly Gravedigger"""

    # [x]<b>Battlecry:</b> If you control a <b>Secret</b>, choose a card in
    # your opponent's hand to _shuffle into their deck.
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Choice(CONTROLLER, RANDOM(ENEMY_HAND, 3)).then(
        Shuffle(OPPONENT, Choice.CARD)
    )


class MAW_020:
    """Scribbling Stenographer"""

    # <b>Rush</b>. Costs (1) less for each card you've played this turn.
    cost_mod = -NUM_CARDS_PLAYED_THIS_TURN


##
# Spells


class REV_825:
    """Double Cross"""

    # <b>Secret:</b> When your opponent spends all their Mana, draw two cards.
    secret = SpendMana(OPPONENT).after(
        (SpendMana.AMOUNT > 0)
        & ((CURRENT_MANA(OPPONENT) == 0) & (Reveal(SELF), Draw(CONTROLLER) * 2))
    )


class REV_827:
    """Sticky Situation"""

    # <b>Secret:</b> After your opponent casts a spell, summon a 3/4 Spider
    # with <b>Stealth</b>.
    secret = Play(OPPONENT, SPELL).after(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "REV_827t"))
    )


class REV_828:
    """Kidnap"""

    # <b>Secret:</b> After your opponent plays a minion, stuff it in a 0/4
    # Sack.
    def kidnap(self, player, card, target):
        if self.controller.minion_slots and card.zone == Zone.PLAY:
            yield Reveal(SELF)
            yield Summon(CONTROLLER, "REV_828t").then(
                StoringBuff(Summon.CARD, "REV_828e", card), Remove(card)
            )

    secret = Play(OPPONENT, MINION).after(kidnap)


class REV_938:
    """Door of Shadows"""

    # Draw a spell. <b>Infuse (@):</b> Add a temporary copy of it to your hand.
    infuse_card = "REV_938t"
    play = FORCE_DRAW(SPELL)


class REV_939:
    """Serrated Bone Spike"""

    # [x]Deal $3 damage to a minion. If it dies, your next card this turn costs
    # (2) less.
    requirements = MINION_TARGET
    play = Hit(TARGET, 3), Find(TARGET + DEAD) & Buff(CONTROLLER, "REV_939e")


class MAW_018:
    """Perjury"""

    # [x]<b>Secret:</b> When your turn starts, <b>Discover</b> and cast a
    # <b>Secret</b> from another class.
    events = OWN_TURN_BEGIN.on(
        Reveal(SELF),
        Discover(CONTROLLER, RandomSpell(secret=True, card_class=ANOTHER_CLASS)).then(
            CastSpell(Discover.CARD)
        ),
    )


class MAW_019:
    """Murder Accusation"""

    # Choose a minion. Destroy it after another enemy minion dies.
    requirements = MINION_TARGET
    play = Buff(TARGET, "MAW_019e2")


##
# Locations


class REV_750:
    """Sinstone Graveyard"""

    # [x]Summon a @/@ Ghost. <i>(Has +1/+1 for each other card
    # you played this turn!)</i>
    activate = Summon(CONTROLLER, "REV_750t2").then(
        SetStats(
            Summon.CARD,
            "REV_750e",
            NUM_CARDS_PLAYED_THIS_TURN + 1,
            NUM_CARDS_PLAYED_THIS_TURN + 1,
        )
    )


class REV_829e:
    events = Reveal(OWNER).on(Summon(CONTROLLER, "REV_829"))


class REV_828e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Bounce(STORE_CARD)


class REV_938t:
    play = FORCE_DRAW(SPELL).then(
        Give(CONTROLLER, Copy(ForceDraw.TARGET)).then(GiveTemporary(Give.CARD))
    )


class REV_939e:
    update = Refresh(FRIENDLY_HAND, {GameTag.COST: -2})
    events = Play(CONTROLLER).on(Destroy(SELF)), OWN_TURN_END.on(Destroy(SELF))


class MAW_019e2:
    events = Death(ENEMY + MINION - OWNER).after(Destroy(OWNER))


@custom_card
class REV_940e(FixedStats):
    tags = {
        GameTag.CARDNAME: "Necrolord Draka's Dagger",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }


@custom_card
class REV_750e(FixedStats):
    tags = {
        GameTag.CARDNAME: "Haunted Conscience Stats",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
