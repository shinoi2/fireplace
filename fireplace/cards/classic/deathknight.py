from ..utils import *

##
# Minions


class RLK_061:
    """Battlefield Necromancer"""

    # [x]At the end of your turn, raise a <b>Corpse</b> as a 1/3 __Risen
    # Footman with <b>Taunt</b>.__
    events = OWN_TURN_END.on(RaiseCorpses(CONTROLLER, 1, "RLK_061t"))


class RLK_071:
    """Patchwerk"""

    # [x]<b>Battlecry:</b> Destroy a random minion in your opponent's _hand,
    # deck, and battlefield._
    play = (
        Destroy(RANDOM(ENEMY_HAND + MINION)),
        Destroy(RANDOM(ENEMY_DECK + MINION)),
        Destroy(RANDOM_ENEMY_MINION),
    )


class RLK_077:
    """Possessifier"""

    # <b>Battlecry:</b> Summon two 1/1 Fighters with <b>Rush</b> and
    # <b>Reborn</b>.
    play = Summon(CONTROLLER, "RLK_077t") * 2


class RLK_079:
    """Noxious Cadaver"""

    # [x]<b>Battlecry</b>: Deal 2 damage to an enemy and your hero.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_ENEMY_TARGET: 0}
    play = Hit(TARGET, 2), Hit(FRIENDLY_HERO, 2)


class RLK_082:
    """Deathbringer Saurfang"""

    # [x]<b>Taunt</b> <b>Deathrattle:</b> Return this to your hand. It costs
    # Health instead of Mana.
    deathrattle = Bounce(SELF), Find(FRIENDLY_HAND + SELF) & Buff(SELF, "DMF_056e")


class RLK_085:
    """Lord Marrowgar"""

    # [x]<b>Battlecry:</b> Raise ALL of your <b>Corpses</b> as 1/1 Risen Golems
    # with <b>Rush</b>. For each that can't fit, give one +2/+2.
    def play(self):
        player = self.controller
        corpses = player.corpses
        yield SpendCorpses(player, corpses)
        golems = []
        for _ in range(min(corpses, player.minion_slots)):
            golem = player.card("RLK_085t", self)
            yield Summon(player, golem)
            if golem.zone == Zone.PLAY:
                golems.append(golem)
        for _ in range(corpses - len(golems)):
            living = [
                golem for golem in golems if not golem.dead and golem.zone == Zone.PLAY
            ]
            if not living:
                break
            yield Buff(self.game.random.choice(living), "RLK_085e")


class RLK_115:
    """Repulsive Gargantuan"""

    # Enemy characters can't be healed.
    update = Refresh(ENEMY_CHARACTERS, {GameTag.CANT_BE_HEALED: True})


class RLK_708:
    """Chillfallen Baron"""

    # <b>Battlecry and Deathrattle:</b> Draw a card.
    play = deathrattle = Draw(CONTROLLER)


class RLK_503:
    """Body Bagger"""

    # <b>Battlecry</b>: Gain a <b>Corpse</b>.
    play = GainCorpses(CONTROLLER, 1)


class RLK_720:
    """Gnome Muncher"""

    # [x]<b>Taunt</b>, <b>Lifesteal</b> At the end of your turn, attack the
    # lowest Health enemy.
    events = OWN_TURN_END.on(Attack(SELF, LOWEST_HEALTH(ENEMY_CHARACTERS - DEAD)))


class RLK_511:
    """Harbinger of Winter"""

    # <b>Deathrattle:</b> Draw a Frost spell.
    deathrattle = FORCE_DRAW(FROST + SPELL)


class RLK_744:
    """Stitched Giant"""

    # [x]Costs (1) less for each <b>Corpse</b> you've spent this game.
    cost_mod = -Attr(CONTROLLER, GameTag.CORPSES_SPENT_THIS_GAME)


class RLK_752:
    """Rime Sculptor"""

    # [x]<b>Battlecry:</b> Summon two 2/1 Rime Elementals with
    # "<b>Deathrattle:</b> Deal 2 damage to a random enemy."
    play = Summon(CONTROLLER, "RLK_907t") * 2


class RLK_753:
    """Bonedigger Geist"""

    # <b>Battlecry:</b> Spend a <b>Corpse</b> to gain +1/+2.
    play = SpendCorpses(CONTROLLER, 1).then(Buff(SELF, "RLK_753e"))


class RLK_958:
    """Skeletal Sidekick"""

    # <b>Battlecry:</b> Give a friendly Undead +2 Attack.
    requirements = FRIENDLY_UNDEAD_BATTLECRY
    play = Buff(TARGET, "RLK_958e")


class RLK_223:
    """Thassarian"""

    # <b>Reborn</b> <b>Battlecry and Deathrattle:</b> Deal 2 damage to a random
    # enemy.
    play = deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 2)


class RLK_224:
    """Overseer Frigidara"""

    # <b>Battlecry:</b> Draw 2 spells. If they're both Frost spells, deal 2
    # damage to all enemies.
    def play(self):
        drawn = []
        for _ in range(2):
            spells = self.controller.deck.filter(type=CardType.SPELL)
            if not spells:
                break
            card = self.game.random.choice(spells)
            yield ForceDraw(card)
            drawn.append(card)
        if len(drawn) == 2 and all(
            card.spell_school == SpellSchool.FROST for card in drawn
        ):
            yield Hit(ENEMY_CHARACTERS, 2)


class RLK_226:
    """Ymirjar Deathbringer"""

    # [x]<b>Taunt</b>. <b>Deathrattle:</b> Spend 3 <b>Corpses</b> to summon a
    # 3/3 Risen Ymirjar with <b>Taunt</b>.
    deathrattle = -FULL_BOARD & SpendCorpses(CONTROLLER, 3).then(
        Summon(CONTROLLER, "RLK_226t")
    )


##
# Spells


class RLK_024:
    """Death Strike"""

    # <b>Lifesteal</b> Deal $6 damage to a minion.
    requirements = MINION_TARGET
    play = Hit(TARGET, 6)


class RLK_025:
    """Frost Strike"""

    # Deal $3 damage to a minion. If that kills it, <b>Discover</b> a Frost
    # Rune card.
    requirements = MINION_TARGET
    play = Hit(TARGET, 3), Dead(TARGET) & DISCOVER(
        RandomCollectible(
            card_class=CardClass.DEATHKNIGHT,
            cost_frost=range(1, 3),
        )
    )


class RLK_034:
    """Heart Strike"""

    # Deal $3 damage to a minion. If that kills it, gain a <b>Corpse</b>.
    requirements = MINION_TARGET
    play = Hit(TARGET, 3), Dead(TARGET) & GainCorpses(CONTROLLER, 1)


class RLK_039:
    """Plagued Grain"""

    # Gain 4 <b>Corpses</b>. Shuffle four Crates into your deck that summon a
    # 2/2 Undead when drawn.
    play = GainCorpses(CONTROLLER, 4), Shuffle(CONTROLLER, "RLK_039t") * 4


class RLK_048:
    """Anti-Magic Shell"""

    # Give your minions +1/+1 and "Can't be targeted by spells or Hero Powers."
    play = Buff(FRIENDLY_MINIONS, "RLK_048e")


class RLK_060:
    """Army of the Dead"""

    # Raise up to 5 <b>Corpses</b> as 2/2 Risen Ghouls with <b>Rush</b>.
    play = RaiseCorpses(CONTROLLER, 5, "RLK_008t")


class RLK_101:
    """Defrost"""

    # Draw a card. Spend 2 <b>Corpses</b> to draw another.
    play = Draw(CONTROLLER), SpendCorpses(CONTROLLER, 2).then(Draw(CONTROLLER))


class RLK_705:
    """Graveyard Shift"""

    # [x]Summon two 1/1 Zombies with <b>Reborn</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "RLK_705t") * 2


class RLK_707:
    """Grave Strength"""

    # [x]Give your minions +1 Attack. Spend 5 <b>Corpses</b> to give them +3
    # instead.
    play = (CORPSES >= 5) & (
        SpendCorpses(CONTROLLER, 5),
        Buff(FRIENDLY_MINIONS, "RLK_707e2"),
    ) | Buff(FRIENDLY_MINIONS, "RLK_707e")


class RLK_709:
    """Remorseless Winter"""

    # Deal $2 damage to all enemies. Draw a card.
    play = Hit(ENEMY_CHARACTERS, 2), Draw(CONTROLLER)


class RLK_715:
    """Runeforging"""

    # Draw a weapon. Spend a <b>Corpse</b> to reduce its Cost by (1).
    play = FORCE_DRAW(WEAPON).then(
        lambda source, weapon: [
            SpendCorpses(CONTROLLER, 1).then(Buff(weapon, "RLK_715e"))
        ]
    )


class RLK_125:
    """Obliterate"""

    # Destroy a minion. Deal_3 damage to your hero.
    requirements = MINION_TARGET
    play = Destroy(TARGET), Hit(FRIENDLY_HERO, 3)


##
# Weapons


class RLK_710:
    """Rimefang Sword"""

    # [x]After your hero attacks, reduce the Cost of a spell in your hand by
    # (1).
    events = Attack(FRIENDLY_HERO).after(
        Buff(RANDOM(FRIENDLY_HAND + SPELL), "RLK_710e")
    )


class RLK_039t:
    tags = {GameTag.CASTSWHENDRAWN: True}
    play = Summon(CONTROLLER, "RLK_070t")


class RLK_061t:
    tags = {enums.LEAVES_NO_CORPSE: True}


RLK_008t = RLK_085t = RLK_226t = RLK_061t
RLK_085e = buff(2, 2)


class RLK_048e:
    tags = {
        GameTag.ATK: 1,
        GameTag.HEALTH: 1,
        GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
        GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
    }


RLK_707e = buff(atk=1)
RLK_707e2 = buff(atk=3)
RLK_710e = RLK_715e = buff(cost=-1)
RLK_753e = buff(1, 2)
RLK_958e = buff(atk=2)


class RLK_907t:
    deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 2)
