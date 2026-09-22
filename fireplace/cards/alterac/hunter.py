from ..utils import *

##
# Minions


class AV_334:
    """Stormpike Battle Ram"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Your next Beast costs (2) less.
    deathrattle = Buff(CONTROLLER, "AV_334e")


class AV_334e:
    update = Refresh(FRIENDLY_HAND + BEAST, {GameTag.COST: -2})
    events = Play(CONTROLLER, BEAST).after(Destroy(SELF))


class AV_335:
    """Ram Tamer"""

    # [x]<b>Battlecry:</b> If you control a <b>Secret</b>, gain +1/+1 and
    # <b>Stealth</b>.
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Buff(SELF, "AV_335e")


AV_335e = buff(atk=1, health=1, stealth=True)


class AV_336:
    """Wing Commander Ichman"""

    # [x]<b>Battlecry:</b> Summon a Beast from your deck and give it
    # <b>Rush</b>. If it kills a minion this turn, repeat.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(Summon.CARD, "AV_336e")
    )


class AV_336e:
    tags = {GameTag.RUSH: True}
    events = Attack(OWNER, ALL_MINIONS).after(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST)).then(
            Buff(Summon.CARD, "AV_336e")
        )
    )


class AV_337:
    """Mountain Bear"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Summon two 2/4 Cubs with
    # <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "AV_337t") * 2


class ONY_009:
    """Pet Collector"""

    # <b>Battlecry:</b> Summon a Beast from your deck that costs (5) or less.
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST + (COST <= 5)))


##
# Spells


class AV_224:
    """Spring the Trap"""

    # Deal $3 damage to a minion and cast a <b>Secret</b> from your deck.
    # <b>Honorable Kill:</b> Cast 2.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3), Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))
    honorable_kill = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


class AV_226:
    """Ice Trap"""

    # <b>Secret:</b> When your opponent casts a spell, return it to their hand
    # instead. It costs (1) more.
    secret = Play(OPPONENT, SPELL).on(
        Reveal(SELF),
        Counter(Play.CARD),
        Give(OPPONENT, Copy(Play.CARD)).then(Buff(Give.CARD, "AV_226e")),
    )


class AV_226e:
    tags = {GameTag.COST: +1}
    events = REMOVED_IN_PLAY


class AV_333:
    """Revive Pet"""

    # <b>Discover</b> a friendly Beast that died this game. Summon it.
    play = GenericChoice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION + BEAST)) * 3)
    ).then(Summon(GenericChoice.CARD))


class ONY_008:
    """Furious Howl"""

    # Draw a card. Repeat until you have at least 3 cards.
    def play(self):
        yield Draw(CONTROLLER)
        while len(self.controller.hand) < 3 and len(self.controller.deck) > 0:
            yield Draw(CONTROLLER)


class ONY_010:
    """Dragonbane Shot"""

    # [x]Deal $2 damage. <b>Honorable Kill:</b> Add a Dragonbane Shot to your
    # hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2)
    honorable_kill = Give(CONTROLLER, "ONY_010")


class AV_147:
    """Dun Baldar Bunker"""

    # [x]At the end of your turn, draw a <b>Secret</b> and set its Cost to (1).
    # Lasts 3 turns.
    events = OWN_TURN_END.on(
        ForceDraw(RANDOM(FRIENDLY_DECK + SECRET)).then(
            Buff(ForceDraw.TARGET, "AV_147e")
        )
    )


class AV_147e:
    tags = {GameTag.COST: SET(1)}
    events = REMOVED_IN_PLAY


##
# Weapons


class AV_244:
    """Bloodseeker"""

    # <b>Honorable Kill:</b> Gain +1/+1.
    honorable_kill = Buff(SELF, "AV_244e")


AV_244e = buff(+1, +1)


##
# Heros


class AV_113:
    """Beaststalker Tavish"""

    # [x]<b>Battlecry:</b> <b>Discover</b> and cast 2 Improved <b>Secrets</b>.
    entourage = ["AV_113t1", "AV_113t2", "AV_113t3", "AV_113t7", "AV_113t8", "AV_113t9"]
    play = GenericChoice(CONTROLLER, RandomEntourage() * 3).then(
        Summon(GenericChoice.CARD)
    )


class AV_113t1:
    """Improved Explosive Trap"""

    # <b>Secret:</b> When your hero is attacked, deal $3 damage to all enemies.
    secret = Attack(ENEMY_CHARACTERS, FRIENDLY_HERO).on(
        Reveal(SELF), Hit(ENEMY_CHARACTERS, 3)
    )


class AV_113t2:
    """Improved Freezing Trap"""

    # <b>Secret:</b> When an enemy minion attacks, return it to its owner's
    # hand. It costs (4) more.
    secret = Attack(ENEMY_MINIONS).on(
        Reveal(SELF), Bounce(Attack.ATTACKER), Buff(Attack.ATTACKER, "AV_113t2e")
    )


class AV_113t2e:
    """Freezing"""

    # Costs (4) more.
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: +4}


class AV_113p:
    """Summon Pet"""

    # <b>Hero Power</b> Summon an Animal Companion.
    entourage = ["NEW1_032", "NEW1_033", "NEW1_034"]
    activate = Summon(CONTROLLER, RandomEntourage())


class AV_113t3:
    """Improved Snake Trap"""

    # <b>Secret:</b> When one of your minions is attacked, summon three 2/2
    # Snakes.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "AV_113t3t2") * 3)
    )


class AV_113t7:
    """Improved Pack Tactics"""

    # <b>Secret:</b> When a friendly minion is attacked, summon two 3/3 copies.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD
        | (
            Reveal(SELF),
            Summon(CONTROLLER, ExactCopy(Attack.DEFENDER)).then(
                Buff(Summon.CARD, "BT_203e")
            )
            * 2,
        )
    )


class AV_113t8:
    """Improved Open the Cages"""

    # [x]<b>Secret:</b> When your turn starts, if you control two minions,
    # summon two Animal Companions.
    entourage = ["NEW1_032", "NEW1_033", "NEW1_034"]
    secret = OWN_TURN_BEGIN.on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, RandomEntourage() * 2))
    )


class AV_113t9:
    """Improved Ice Trap"""

    # <b>Secret:</b> When your opponent casts a spell, return it to their hand
    # instead. It costs (2) more.
    secret = Play(OPPONENT, SPELL).on(
        Reveal(SELF),
        Counter(Play.CARD),
        Give(OPPONENT, Copy(Play.CARD)).then(Buff(Give.CARD, "AV_113t9e")),
    )


class AV_113t9e:
    """Mega Frosty"""

    # Costs (2) more.
    tags = {GameTag.COST: +2}
    events = REMOVED_IN_PLAY
