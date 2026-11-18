from ..utils import *

##
# Minions


class REV_244:
    """Mischievous Imp"""

    # <b>Battlecry:</b> Summon a copy of this. <b>Infuse (@):</b> Summon two
    # copies instead.
    infuse_card = "REV_244t"
    play = Summon(CONTROLLER, ExactCopy(SELF))


class REV_242:
    """Flustered Librarian"""

    # Has +1 Attack for each Imp you control.
    update = Refresh(SELF, {GameTag.ATK: Count(FRIENDLY_MINIONS + IMPS)})


class REV_835:
    """Imp King Rafaam"""

    # <b>Battlecry:</b> Resurrect four friendly Imps. <b>Infuse (@):</b> Give
    # your Imps +2/+2.
    infuse_card = "REV_835t"
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + DEAD_MINIONS + IMPS, 4)))


class REV_373:
    """Lady Darkvein"""

    # [x]<b>Battlecry:</b> Summon two 2/1 Shades. Each gains a
    # <b>Deathrattle</b> to cast your last Shadow spell.
    def play(self):
        spells = [
            c
            for c in self.controller.cards_played_this_game
            if c.type == CardType.SPELL and c.spell_school == SpellSchool.SHADOW
        ]
        for _ in range(2):
            if spells:
                yield Summon(CONTROLLER, "REV_373t").then(
                    StoringBuff(Summon.CARD, "REV_373e", Copy(spells[-1]))
                )
            else:
                yield Summon(CONTROLLER, "REV_373t")


class REV_374:
    """Shadowborn"""

    # <b>Deathrattle:</b> Reduce the Cost of the highest Cost Shadow spell in
    # your hand by (3).
    deathrattle = Buff(HIGHEST_COST(FRIENDLY_HAND + SHADOW + SPELL), "REV_374e")


class MAW_000:
    """Imp-oster"""

    # <b>Battlecry:</b> Choose a friendly Imp. Transform into a copy of it.
    requirements = dict(FRIENDLY_MINION_TARGET)
    requirements[PlayReq.REQ_TARGET_IF_AVAILABLE] = 0
    requirements.pop(PlayReq.REQ_TARGET_TO_PLAY)
    requirements[enums.REQ_TARGET_IMP] = 0
    play = Morph(SELF, ExactCopy(TARGET))


##
# Spells


class REV_240:
    """Tome Tampering"""

    # [x]Shuffle 1-Cost copies of cards in your hand into your deck, then
    # discard your hand.
    play = Shuffle(CONTROLLER, Buff(Copy(FRIENDLY_HAND), "REV_240e")), Discard(
        FRIENDLY_HAND
    )


class REV_239:
    """Suffocating Shadows"""

    # [x]When you play or discard this, destroy a random enemy minion.
    play = discard = Destroy(RANDOM_ENEMY_MINION)


class REV_245:
    """Impending Catastrophe"""

    # Draw a card. Repeat for each Imp you control.
    play = Draw(CONTROLLER) * (Count(FRIENDLY_MINIONS + IMPS) + 1)


class REV_372:
    """Shadow Waltz"""

    # Summon a 3/5 Shadow with <b>Taunt</b>. If a minion died this turn, summon
    # another.
    play = Summon(CONTROLLER, "REV_372t"), Find(MINION + KILLED_THIS_TURN) & Summon(
        CONTROLLER, "REV_372t"
    )


class MAW_001:
    """Arson Accusation"""

    # Choose a minion. Destroy it after your hero takes damage.
    requirements = MINION_TARGET
    play = Buff(TARGET, "MAW_001e2")


class MAW_002:
    """Habeas Corpses"""

    # <b>Discover</b> a friendly minion to resurrect and give it <b>Rush</b>.
    # It dies at the end of turn.
    play = Choice(
        CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + DEAD_MINIONS), 3))
    ).then(
        Summon(CONTROLLER, Choice.CARD).then(
            GiveRush(Summon.CARD), Buff(Summon.CARD, "MAW_002e")
        )
    )


##
# Locations


class REV_371:
    """Vile Library"""

    # Give a friendly minion +1/+1 for each Imp you control.
    requirements = FRIENDLY_MINION_TARGET
    activate = Buff(
        TARGET,
        "REV_371e",
        atk=Count(FRIENDLY_MINIONS + IMPS),
        max_health=Count(FRIENDLY_MINIONS + IMPS),
    )


class REV_244t:
    play = Summon(CONTROLLER, ExactCopy(SELF)) * 2


class REV_835t:
    play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + DEAD_MINIONS + IMPS, 4))), Buff(
        FRIENDLY_MINIONS + IMPS, "REV_835e"
    )


REV_835e = buff(+2, +2)
REV_374e = cost_buff(cost=-3)


class REV_373e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = CastSpell(STORE_CARD)


class REV_240e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


class MAW_001e2:
    events = Damage(FRIENDLY_HERO).on(Destroy(OWNER))


class MAW_002e:
    events = TURN_END.on(Destroy(OWNER))
