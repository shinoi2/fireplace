from ..utils import *

##
# Minions


class REV_000:
    """Suspicious Alchemist"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a spell. If your opponent guesses
    # your choice, they get a copy.
    play = Discover(CONTROLLER, RandomSpell()).then(
        Give(CONTROLLER, Discover.CARD),
        lambda source, *args: (
            yield Choice(OPPONENT, args[Discover.CARDS]).then(
                lambda source2, *args2: (
                    (yield Give(OPPONENT, Copy(Choice.CARD)))
                    if args[Discover.CARD] == args2[Choice.CARD]
                    else None
                )
            )
        ),
    )


class REV_513:
    """Chatty Bartender"""

    # [x]At the end of your turn, if you control a <b>Secret</b>, deal 2 damage
    # to all enemies.
    events = OWN_TURN_END.on(Find(FRIENDLY_SECRETS) & Hit(ENEMY_CHARACTERS, 2))


class REV_514:
    """Kel'Thuzad, the Inevitable"""

    # [x]<b>Battlecry:</b> Resurrect your Volatile Skeletons. Any that can't
    # fit on the battlefield instantly explode! @<i>(@)</i>
    def play(self):
        minions = self.controller.graveyard.filter(id="REV_845")
        if len(minions) <= self.controller.minion_slots:
            yield SummonBothSides(CONTROLLER, "REV_845") * len(minions)
        else:
            yield SummonBothSides(CONTROLLER, "REV_845") * self.controller.minion_slots
            yield Hit(RANDOM_ENEMY_CHARACTER, 2) * (
                len(minions) - self.controller.minion_slots
            )


class REV_515:
    """Orion, Mansion Manager"""

    # After a friendly <b>Secret</b> is revealed, cast a different Mage
    # <b>Secret</b> and gain +2/+2.
    events = Reveal(FRIENDLY_SECRETS).on(
        CastSpell(
            RandomSpell(
                secret=True, card_class=CardClass.MAGE, exclude=FRIENDLY_SECRETS
            )
        ),
        Buff(SELF, "REV_515e"),
    )


REV_515e = buff(+2, +2)


class MAW_101:
    """Contract Conjurer"""

    # Costs (3) less for each <b>Secret</b> you control.
    cost_mod = -Count(FRIENDLY_SECRETS) * 3


##
# Spells


class REV_504:
    """Solid Alibi"""

    # Until your next turn, your hero can only take 1 damage at a time.
    play = Buff(CONTROLLER, "REV_504e")


class REV_504e:
    events = OWN_TURN_BEGIN.on(Destroy(SELF))
    update = Refresh(FRIENDLY_HERO, {GameTag.HEAVILY_ARMORED: True})


class REV_505:
    """Cold Case"""

    # Summon two 2/2 Volatile Skeletons. Gain 4 Armor.
    play = Summon(CONTROLLER, "REV_845") * 2, GainArmor(FRIENDLY_HERO, 4)


class REV_516:
    """Vengeful Visage"""

    # [x]<b>Secret:</b> After an enemy minion attacks your hero, summon a copy
    # of it to attack the enemy hero.
    secret = Attack(ENEMY_MINIONS, FRIENDLY_HERO).after(
        FULL_BOARD
        | (
            Reveal(SELF),
            Summon(CONTROLLER, Copy(Attack.ATTACKER)).then(
                Attack(Summon.CARD, ENEMY_HERO)
            ),
        )
    )


class REV_840:
    """Deathborne"""

    # Deal $2 damage to all minions. Summon a 2/2 Volatile Skeleton for each
    # killed.
    play = (
        Hit(ALL_MINIONS, 2),
        Summon(CONTROLLER, "REV_845") * Count(ALL_MINIONS + DEAD),
    )


class MAW_006:
    """Objection!"""

    # <b>Secret:</b> When your opponent plays a _minion, <b>Counter</b> it.
    secret = Play(OPPONENT, MINION).before(Reveal(SELF), Counter(Play.CARD))


class MAW_013:
    """Life Sentence"""

    # Remove a minion from the game.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    activate = Remove(TARGET)


class REV_601:
    """Frozen Touch"""

    # Deal $3 damage. <b>Infuse (@):</b> Add a Frozen Touch to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    infuse_card = "REV_601t"
    play = Hit(TARGET, 3)


class REV_601t:
    """Frozen Touch"""

    # [x]<b>Infused</b> Deal $3 damage. Add a Frozen Touch to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 3), Give(CONTROLLER, "REV_601")


##
# Locations


class REV_602:
    """Nightcloak Sanctum"""

    # <b>Freeze</b> a minion. Summon a 2/2 Volatile Skeleton.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    activate = Freeze(TARGET), Summon(CONTROLLER, "REV_845")
