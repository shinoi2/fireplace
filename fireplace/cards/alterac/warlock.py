from ..utils import *

##
# Minions


class AV_312:
    """Sacrificial Summoner"""

    # <b>Battlecry:</b> Destroy a friendly minion. Summon a minion from your
    # deck that costs (1) more.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Destroy(TARGET), Summon(
        CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST == (COST(TARGET) + 1)))
    )


class AV_313:
    """Hollow Abomination"""

    # [x]<b>Battlecry:</b> Deal 1 damage to all enemy minions. <b>Honorable
    # Kill:</b> Gain the minion's Attack.
    play = Hit(ENEMY_MINIONS, 1)

    def honorable_kill(self, target):
        yield Buff(SELF, "AV_313e", atk=ATK(target))


class AV_308:
    """Grave Defiler"""

    # <b>Battlecry:</b> Copy a Fel spell in your hand.
    play = Give(CONTROLLER, RANDOM(FRIENDLY_HAND + FEL))


class AV_286:
    """Felwalker"""

    # <b>Taunt</b>. <b>Battlecry</b>: Cast the highest Cost Fel spell from your
    # hand.
    play = CastSpell(RANDOM(HIGHEST_COST(FRIENDLY_HAND + FEL)))


class ONY_035:
    """Spawn of Deathwing"""

    # <b>Battlecry:</b> Destroy a random enemy minion. Discard a random card.
    play = Destroy(RANDOM(ENEMY_MINIONS)), Discard(RANDOM(FRIENDLY_HAND))


##
# Spells


class ONY_033:
    """Impfestation"""

    # Summon a 3/3 Dread Imp to attack each enemy minion.
    def play(self):
        for minion in ENEMY_MINIONS.eval(self.game, self):
            yield Summon(CONTROLLER, "AV_316t").then(Attack(Summon.CARD, minion))


class AV_317:
    """Tamsin's Phylactery"""

    # <b>Discover</b> a friendly <b>Deathrattle</b> minion that died this game.
    # Give your minions its <b>Deathrattle</b>.
    requirements = {
        PlayReq.REQ_FRIENDLY_DEATHRATTLE_MINION_DIED_THIS_GAME: 0,
    }
    play = GenericChoice(
        CONTROLLER,
        Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + DEATHRATTLE + MINION)) * 3),
    ).then(CopyDeathrattleBuff(FRIENDLY_MINIONS, "AV_317e", source=GenericChoice.CARD))


class AV_277:
    """Seeds of Destruction"""

    # [x]Shuffle four Rifts into your deck. They summon a 3/3 Dread Imp when
    # drawn.
    play = Shuffle(CONTROLLER, "AV_316t4") * 4


class AV_281:
    """Felfire in the Hole!"""

    # Draw a spell and deal $2 damage to all enemies. If it's a Fel spell, deal
    # $1 more.
    play = FORCE_DRAW(SPELL).then(
        Find(ForceDraw.TARGET + FEL) & (Hit(ENEMY_CHARACTERS, 3))
        | (Hit(ENEMY_CHARACTERS, 2))
    )


class AV_285:
    """Full-Blown Evil"""

    # Deal $5 damage randomly split among all enemy minions. Repeatable this
    # turn.
    tags = {GameTag.ECHO: True}
    play = Hit(RANDOM_ENEMY_MINION, 1) * SPELL_DAMAGE(5)


class ONY_034:
    """Curse of Agony"""

    # [x]Shuffle three Agonies into the opponent's deck. They deal Fatigue
    # damage when drawn.
    play = Shuffle(OPPONENT, "ONY_034t") * 3


class ONY_034t:
    play = Fatigue(CONTROLLER)


class AV_657:
    """Desecrated Graveyard"""

    # [x]At the end of your turn, destroy your lowest Attack minion to summon a
    # 4/4 Shade. Lasts 3 turns.
    events = OWN_TURN_END.on(
        Destroy(RANDOM(LOWEST_ATK(FRIENDLY_MINIONS))).then(
            Summon(CONTROLLER, "AV_657t")
        )
    )


##
# Heros


class AV_316:
    """Dreadlich Tamsin"""

    # [x]<b>Battlecry:</b> Deal 3 damage to all minions. Shuffle 3 Rifts into
    # your deck. Draw 3 cards.
    play = (
        Hit(ALL_MINIONS, 3),
        Shuffle(CONTROLLER, "AV_316t4") * 3,
        Draw(CONTROLLER) * 3,
    )


class AV_316hp:
    """Chains of Dread"""

    # <b>Hero Power</b> Shuffle a Rift into your deck. Draw a card.
    activate = Shuffle(CONTROLLER, "AV_316t4"), Draw(CONTROLLER)


class AV_316t4:
    """Fel Rift"""

    # <b>Casts When Drawn</b> Summon a 3/3 Dread Imp.
    play = Summon(CONTROLLER, "AV_316t")
