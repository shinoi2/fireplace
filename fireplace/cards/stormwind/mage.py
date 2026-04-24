from ..utils import *

##
# Minions


class SW_109:
    """Clumsy Courier"""

    # <b>Battlecry:</b> Cast the highest Cost spell from your hand.
    play = CastSpell(RANDOM(HIGHEST_COST(FRIENDLY_HAND + SPELL)))


class SW_111:
    """Sanctum Chandler"""

    # After you cast a Fire spell, draw a spell.
    events = Play(CONTROLLER, FIRE + SPELL).after(
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))
    )


class SW_112:
    """Prestor's Pyromancer"""

    # <b>Battlecry:</b> Your next Fire spell has <b>Spell Damage +2</b>.
    play = Buff(CONTROLLER, "SW_112e")


class SW_112e:
    update = Refresh(CONTROLLER, {GameTag.SPELLPOWER_FIRE: 2})
    events = Play(CONTROLLER, FIRE).after(Destroy(SELF))


class SW_113:
    """Grand Magus Antonidas"""

    # [x]<b>Battlecry:</b> If you've cast a Fire spell on each of your last
    # three turns, cast 3 Fireballs at ___random enemies.@ <i>(@/3)</i>
    def progress(self):
        player = self.controller
        count = 0
        turns = player.turns[-3:]
        if player.turn == self.game.turn:
            turns = player.turns[-4:-1]
        for turn in turns:
            for card in player.cards_played_this_game:
                if card.turn_played == turn:
                    count += 1
                    break
        return count

    powered_up = CURRENT_PROGRESS(SELF) >= 3
    play = powered_up & (CastSpell("CS2_029", RANDOM_ENEMY_CHARACTER) * 3)


class DED_515:
    """Grey Sage Parrot"""

    # <b>Battlecry:</b> Repeat the last spell you've cast that costs (5) or
    # more.
    play = CastSpell(Copy((CARDS_PLAYED_THIS_GAME + SPELL + (COST >= 5))[-1:]))


class DED_516:
    """Deepwater Evoker"""

    # [x]<b>Battlecry:</b> Draw a spell. Gain Armor equal to its Cost.
    play = ForceDraw(FRIENDLY_DECK + SPELL).then(
        GainArmor(FRIENDLY_HERO, COST(ForceDraw.TARGET))
    )


##
# Spells


class SW_107:
    """Fire Sale"""

    # <b>Tradeable</b> Deal $3 damage to all minions.
    play = Hit(ALL_MINIONS, 3)


class SW_108:
    """First Flame"""

    # Deal $2 damage to a minion. Add a Second Flame to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), Give(CONTROLLER, "SW_108t")


class SW_108t:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2)


class SW_110:
    """Ignite"""

    # Deal $@ damage. Shuffle an Ignite into your deck that deals one more
    # damage.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        amount = getattr(self, "_amount", 2)
        yield Hit(TARGET, amount)
        card = self.controller.card("SW_110", source=self)
        card._amount = amount + 1
        yield Shuffle(CONTROLLER, card)


class SW_450:
    """Sorcerer's Gambit"""

    # <b>Questline:</b> Cast a Fire, Frost, and Arcane spell. <b>Reward:
    # </b>Draw a spell.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        for spell_school in [SpellSchool.FIRE, SpellSchool.FROST, SpellSchool.ARCANE]:
            if card.spell_school == spell_school:
                if not any(e.spell_school == spell_school for e in self.entourage):
                    self.entourage.append(card)
                    break

    quest = Play(CONTROLLER, FIRE | FROST | ARCANE).after(AddProgress(SELF, Play.CARD))
    reward = Summon(CONTROLLER, "SW_450t"), ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))


class SW_450t:
    """Stall for Time"""

    # <b>Questline:</b> Cast a Fire, Frost, and Arcane spell. <b>Reward:</b>
    # <b>Discover</b> one.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        for spell_school in [SpellSchool.FIRE, SpellSchool.FROST, SpellSchool.ARCANE]:
            if card.spell_school == spell_school:
                if not any(e.spell_school == spell_school for e in self.entourage):
                    self.entourage.append(card)
                    break

    quest = Play(CONTROLLER, FIRE | FROST | ARCANE).after(AddProgress(SELF, Play.CARD))
    reward = Summon(CONTROLLER, "SW_450t2"), GenericChoice(CONTROLLER, ENTOURAGE)


class SW_450t2(QuestRewardProtect):
    """Reach the Portal Room"""

    # [x]<b>Questline:</b> Cast a Fire, Frost, and Arcane spell. <b>Reward:</b>
    # Arcanist Dawngrasp.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        for spell_school in [SpellSchool.FIRE, SpellSchool.FROST, SpellSchool.ARCANE]:
            if card.spell_school == spell_school:
                if not any(e.spell_school == spell_school for e in self.entourage):
                    self.entourage.append(card)
                    break

    quest = Play(CONTROLLER, FIRE | FROST | ARCANE).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "SW_450t4")


class SW_450t4:
    """Arcanist Dawngrasp"""

    # [x]<b>Battlecry:</b> For the rest of the game, you have <b>Spell Damage
    # +2</b>.
    play = Buff(CONTROLLER, "SW_450t4e")


SW_450t4e = buff(spellpower=2)


class SW_462:
    """Hot Streak"""

    # Your next Fire spell this turn costs (2) less.
    play = Buff(CONTROLLER, "SW_462e")


class SW_462e:
    update = Refresh(FRIENDLY_HAND + FIRE, {GameTag.COST: -2})
    events = Play(CONTROLLER, FIRE).after(Destroy(SELF))


class DED_517:
    """Arcane Overflow"""

    # [x]Deal $8 damage to an enemy minion. Summon a Remnant with stats equal
    # to the excess damage.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = HitExcessDamage(TARGET, 8).then(
        SummonCustomMinion(
            CONTROLLER,
            "DED_517t",
            HitExcessDamage.EXCEDSS_AMOUNT,
            HitExcessDamage.EXCEDSS_AMOUNT,
            HitExcessDamage.EXCEDSS_AMOUNT,
        )
    )


##
# Weapons


class SW_001:
    """Celestial Ink Set"""

    # [x]After you spend 5 Mana on spells, reduce the cost of a spell in your
    # hand by (5). Lose 1 Durability.
    progress_total = 5
    events = Play(CONTROLLER, SPELL).after(
        AddProgress(SELF, Play.CARD, COST(Play.CARD))
    )
    reward = Buff(RANDOM(FRIENDLY_HAND + SPELL), "SW_001e")


class SW_001e:
    tags = {GameTag.COST: -2}
    events = REMOVED_IN_PLAY
