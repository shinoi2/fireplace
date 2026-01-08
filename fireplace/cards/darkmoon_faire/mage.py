from ..utils import *


##
# Minions


class DMF_100:
    """Confection Cyclone"""

    # <b>Battlecry:</b> Add two 1/2 Sugar Elementals to your_hand.
    play = Give(CONTROLLER, "DMF_100t") * 2


class DMF_101:
    """Firework Elemental"""

    # [x]<b>Battlecry:</b> Deal 3 damage to a minion. <b>Corrupt:</b> Deal 12
    # instead.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 3)
    corrupt_card = "DMF_101t"


class DMF_101t:
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 12)


class DMF_102:
    """Game Master"""

    # The first <b>Secret</b> you play each turn costs (1).
    update = Find(CARDS_PLAYED_THIS_TURN + SECRET) | (
        Refresh(FRIENDLY_HAND + SECRET, {GameTag.COST: SET(1)})
    )


class DMF_106:
    """Occult Conjurer"""

    # <b>Battlecry:</b> If you control a <b>Secret</b>, summon a copy of_this.
    play = Find(FRIENDLY_SECRETS) & (Summon(CONTROLLER, ExactCopy(SELF)))


class DMF_109:
    """Sayge, Seer of Darkmoon"""

    # <b>Battlecry:</b> Draw @ |4(card, cards). <i>(Upgraded for each friendly
    # <b>Secret</b> that has triggered this game!)</i>
    play = Draw(CONTROLLER), Draw(CONTROLLER) * Count(FRIENDLY + TRIGGERED_SECRET)


class YOP_018:
    """Keywarden Ivory"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a dual-class spell from any class.
    # <b><b>Spellburst</b>:</b> Get another copy.
    play = GenericChoice(
        CONTROLLER,
        RandomCollectible(
            multiple_classes=[
                MultiClassGroup.PALADIN_PRIEST,
                MultiClassGroup.PRIEST_WARLOCK,
                MultiClassGroup.WARLOCK_DEMONHUNTER,
                MultiClassGroup.HUNTER_DEMONHUNTER,
                MultiClassGroup.DRUID_HUNTER,
                MultiClassGroup.DRUID_SHAMAN,
                MultiClassGroup.MAGE_SHAMAN,
                MultiClassGroup.MAGE_ROGUE,
                MultiClassGroup.ROGUE_WARRIOR,
                MultiClassGroup.PALADIN_WARRIOR,
                MultiClassGroup.MAGE_HUNTER,
                MultiClassGroup.HUNTER_DEATHKNIGHT,
                MultiClassGroup.DEATHKNIGHT_PALADIN,
                MultiClassGroup.PALADIN_SHAMAN,
                MultiClassGroup.SHAMAN_WARRIOR,
                MultiClassGroup.WARRIOR_DEMONHUNTER,
                MultiClassGroup.DEMONHUNTER_ROGUE,
                MultiClassGroup.ROGUE_PRIEST,
                MultiClassGroup.PRIEST_DRUID,
                MultiClassGroup.DRUID_WARLOCK,
                MultiClassGroup.WARLOCK_MAGE,
            ]
        )
        * 3,
    ).then(SetTags(SELF, {GameTag.TAG_SCRIPT_DATA_ENT_1: GenericChoice.CARD}))
    spellburst = (
        Give(CONTROLLER, Copy(GetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1))),
        UnsetTag(SELF, GameTag.TAG_SCRIPT_DATA_ENT_1),
    )


class YOP_020:
    """Glacier Racer"""

    # <b>Spellburst</b>: Deal 3 damage to all <b>Frozen</b> enemies.
    spellburst = Hit(ENEMY_CHARACTERS + FROZEN, 3)


class YOP_021:
    """Imprisoned Phoenix"""

    # <b>Dormant</b> for 2 turns. <b>Spell Damage +2</b>
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2


##
# Spells


class DMF_103:
    """Mask of C'Thun"""

    # Deal $10 damage randomly split among all enemies.
    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * SPELL_DAMAGE(10)


class DMF_104:
    """Grand Finale"""

    # Summon an 8/8 Elemental. Repeat for each Elemental you played last turn.
    play = Summon(CONTROLLER, "DMF_104t") * (
        Attr(CONTROLLER, enums.ELEMENTAL_PLAYED_LAST_TURN) + 1
    )


class DMF_105:
    """Ring Toss"""

    # <b>Discover</b> a <b>Secret</b> and cast it. <b>Corrupt:</b>
    # <b>Discover</b> 2 instead.
    play = DISCOVER(RandomSpell(secret=True)).then(CastSpell(Discover.CARD))


class DMF_105t:
    play = DISCOVER(RandomSpell(secret=True)).then(CastSpell(Discover.CARD)) * 2


class DMF_107:
    """Rigged Faire Game"""

    # <b>Secret:</b> If you didn't take any damage during your opponent's turn,
    # draw 3 cards.
    secret = OWN_TURN_BEGIN.on(
        (DAMAGED_THIS_TURN(FRIENDLY_HERO) == 0) & (Reveal(SELF), Draw(CONTROLLER) * 3)
    )


class DMF_108:
    """Deck of Lunacy"""

    # Transform spells in your deck into ones that cost (3) more. <i>(They keep
    # their original Cost.)</i>
    def play(self):
        spells = (FRIENDLY_DECK + SPELL).eval(self.game, self)
        for spell in spells:
            origin_cost = spell.cost
            yield Morph(spell, RandomSpell(cost=origin_cost + 3)).then(
                Buff(Morph.CARD, "DMF_108e", cost=SET(origin_cost))
            )


class YOP_019:
    """Conjure Mana Biscuit"""

    # Add a Biscuit to your hand that refreshes 2 Mana Crystals.
    play = Give(CONTROLLER, "YOP_019t")


class YOP_019t:
    play = ManaThisTurn(CONTROLLER, 2)
