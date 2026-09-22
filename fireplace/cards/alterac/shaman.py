from ..utils import *

##
# Minions


class AV_251:
    """Cheaty Snobold"""

    # After an enemy is <b>Frozen</b>, deal 3 damage to it.
    events = SetTags(ENEMY_MINIONS, (GameTag.FROZEN,)).after(Hit(SetTags.TARGET, 3))


class AV_255:
    """Snowfall Guardian"""

    # <b>Battlecry:</b> <b>Freeze</b> all other minions. Gain +1/+1 for each
    # <b>Frozen</b> minion.
    play = Freeze(ALL_MINIONS - SELF).then(Buff(ALL_MINIONS + FROZEN, "AV_255e"))


AV_255e = buff(+1, +1)


class AV_257:
    """Bearon Gla'shear"""

    # [x]<b>Battlecry:</b> For each Frost spell you've cast this game, summon a
    # 3/4 Elemental that <b>Freezes</b>.@ <i>(@)</i>
    play = SummonBothSides(CONTROLLER, "AV_257t") * Count(
        CARDS_PLAYED_THIS_GAME + FROST
    )


class AV_260:
    """Sleetbreaker"""

    # <b>Battlecry:</b> Add a Windchill to your hand.
    play = Give(CONTROLLER, "AV_266")


##
# Spells


class AV_107:
    """Glaciate"""

    # <b>Discover</b> an 8-Cost minion. Summon and <b>Freeze</b> it.
    play = Discover(CONTROLLER, RandomMinion(cost=8)).then(
        Summon(CONTROLLER, Discover.CARD), Freeze(Discover.CARD)
    )


class AV_250:
    """Snowball Fight!"""

    # Deal $1 damage to a minion and <b>Freeze</b> it. If it survives, repeat
    # this on another minion!
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

    def play(self):
        play_targets = self.play_targets
        yield Hit(TARGET, 1), Freeze(TARGET)
        play_targets.remove(self.target)
        while not self.target.dead and play_targets:
            self.target = self.game.random.choice(play_targets)
            yield Hit(TARGET, 1), Freeze(TARGET)
            play_targets.remove(self.target)


class AV_259:
    """Frostbite"""

    # Deal $3 damage. <b>Honorable Kill:</b> Your opponent's next spell costs
    # (2) more.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)
    honorable_kill = Buff(OPPONENT, "AV_259e")


class AV_259e:
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: +2})
    events = Play(CONTROLLER, SPELL).after(Destroy(SELF))


class AV_266:
    """Windchill"""

    # <b>Freeze</b> a minion. Draw a card.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Freeze(TARGET), Draw(CONTROLLER)


class AV_268:
    """Wildpaw Cavern"""

    # [x]At the end of your turn, summon a 3/4 Elemental that <b>Freezes</b>.
    # Lasts 3 turns.
    events = OWN_TURN_END.on(Summon(CONTROLLER, "AV_257t"))


class ONY_011:
    """Don't Stand in the Fire!"""

    # Deal $10 damage randomly split among all enemy minions. <b>Overload:</b>
    # (1)
    play = Hit(RANDOM_ENEMY_MINION, 1) * SPELL_DAMAGE(10)


class ONY_012:
    """Spirit Mount"""

    # [x]Give a minion +1/+2 and <b>Spell Damage +1</b>. When it dies, summon a
    # Spirit Raptor.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "ONY_012e")


class ONY_012e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 2,
        GameTag.SPELLPOWER: 1,
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Summon(CONTROLLER, "ONY_012t")


class ONY_013:
    """Bracing Cold"""

    # [x]Restore #5 Health to your hero. Reduce the Cost of a random spell in
    # your hand by (2).
    play = Heal(FRIENDLY_HERO, 5), Buff(RANDOM(FRIENDLY_HAND + SPELL), "ONY_013e")


class ONY_013e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY


##
# Heros


class AV_258:
    """Bru'kan of the Elements"""

    # [x]<b>Battlecry:</b> Call upon the power of two Elements!
    class ElementalMasteryAction(MultipleChoice):
        PLAYER = ActionArg()
        choose_times = 2
        elemental_ids = ["AV_258t", "AV_258t2", "AV_258t3", "AV_258t4"]

        def do_step1(self):
            self.cards = [self.player.card(id) for id in self.elemental_ids]

        def do_step2(self):
            self.cards.remove(self.choosed_cards[0])

        def done(self):
            for card in self.choosed_cards:
                self.source.game.queue_actions(card, [Battlecry(card, self.source)])

    entourage = ["AV_258pt", "AV_258p2", "AV_258pt3", "AV_258pt4"]
    play = ElementalMasteryAction(CONTROLLER), Summon(CONTROLLER, RandomEntourage())


class AV_258t:
    """Earth Invocation"""

    # Summon two 2/3 Elementals with <b>Taunt</b>.
    play = Summon(CONTROLLER, "AV_258t6") * 2


class AV_258t2:
    """Water Invocation"""

    # Restore 6 Health to all friendly characters.
    play = Heal(FRIENDLY_CHARACTERS, 6)


class AV_258t3:
    """Fire Invocation"""

    # Deal 6 damage to the enemy hero.
    play = Hit(ENEMY_HERO, 6)


class AV_258t4:
    """Lightning Invocation"""

    # Deal 2 damage to all enemy minions.
    play = Hit(ENEMY_MINIONS, 2)


class AV_258pt7:
    """Command the Elements"""

    # [x]<b>Hero Power</b> Call upon a different Element every turn!
    entourage = AV_258.entourage
    events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage(exclude=SELF)))


class AV_258pt(AV_258pt7):
    """Earth Invocation"""

    # [x]<b>Hero Power</b> Summon two 2/3 Elementals with <b>Taunt</b>. Swaps
    # each turn.
    activate = Summon(CONTROLLER, "AV_258t6") * 2


class AV_258p2(AV_258pt7):
    """Water Invocation"""

    # <b>Hero Power</b> Restore #6 Health to all friendly characters. Swaps
    # each turn.
    activate = Heal(FRIENDLY_CHARACTERS, 6)


class AV_258pt3(AV_258pt7):
    """Fire Invocation"""

    # <b>Hero Power</b> Deal $6 damage to the enemy hero. Swaps each turn.
    activate = Hit(ENEMY_HERO, 6)


class AV_258pt4(AV_258pt7):
    """Lightning Invocation"""

    # <b>Hero Power</b> Deal $2 damage to all enemy minions. Swaps each turn.
    activate = Hit(ENEMY_MINIONS, 2)
