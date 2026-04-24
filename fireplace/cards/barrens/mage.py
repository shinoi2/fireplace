from ast import For
from ..utils import *

##
# Minions


class BAR_544:
    """Reckless Apprentice"""

    # <b>Battlecry:</b> Fire your Hero Power at all enemies.
    play = PlayHeroPower(FRIENDLY_HERO_POWER, ENEMY_CHARACTERS)


class BAR_545:
    """Arcane Luminary"""

    # Cards that didn't start in your deck cost (2) less, but not less than
    # (1).
    update = Refresh(FRIENDLY_HAND - STARTING_DECK, buff="BAR_545e")


class BAR_545e:
    cost = lambda self, i: min(i, max(i - 2, 1))
    events = REMOVED_IN_PLAY


class BAR_547(metaclass=ThresholdUtils):
    """Mordresh Fire Eye"""

    # [x]<b>Battlecry:</b> If you've dealt 10 damage with your Hero Power this
    # game, deal 10 damage to all enemies.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = Hit(ENEMY_CHARACTERS, 10)


class BAR_748:
    """Varden Dawngrasp"""

    # [x]<b>Battlecry:</b> <b>Freeze</b> all enemy minions. If any are already
    # <b>Frozen</b>, deal 4 damage to them instead.
    play = Hit(ENEMY_MINIONS + FROZEN, 4), Freeze(ENEMY_MINIONS + FROZEN)


class BAR_888:
    """Rimetongue"""

    # After you cast a Frost spell, summon a 1/1 Elemental that
    # <b><b>Freeze</b>s</b>.
    events = Play(CONTROLLER, SPELL + FROST).after(Summon(CONTROLLER, "BAR_888t"))


class WC_805:
    """Frostweave Dungeoneer"""

    # [x]<b>Battlecry:</b> Draw a spell. If it's a Frost spell, summon two 1/1
    # ___Elementals that <b>Freeze</b>.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)).then(
        Find(ForceDraw.TARGET + FROST) & (SummonBothSides(CONTROLLER, "BAR_888t") * 2)
    )


class WC_806:
    """Floecaster"""

    # Costs (2) less for each <b>Frozen</b> enemy.
    cost_mod = -Count(ENEMY_MINIONS + FROZEN) * 2


##
# Spells


class BAR_305:
    """Flurry (Rank 1)"""

    # <b>Freeze</b> a random enemy minion. <i>(Upgrades when you have 5
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_305t")

    play = Freeze(RANDOM_ENEMY_MINION)


class BAR_305t:
    """Flurry (Rank 2)"""

    # [x]<b>Freeze</b> two random enemy minions. <i>(Upgrades when you have 10
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_305t2")

    play = Freeze(RANDOM_ENEMY_MINION * 2)


class BAR_305t2:
    """Flurry (Rank 3)"""

    # <b>Freeze</b> three random enemy minions.
    play = Freeze(RANDOM_ENEMY_MINION * 3)


class BAR_541:
    """Runed Orb"""

    # Deal $2 damage. <b>Discover</b> a spell.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 2), DISCOVER(RandomSpell())


class BAR_542:
    """Refreshing Spring Water"""

    # Draw 2 cards. Refresh 2 Mana Crystals for each spell drawn.
    play = (
        Draw(CONTROLLER).then(Find(Draw.CARD + SPELL) & FillMana(CONTROLLER, 2))
    ) * 2


class BAR_546:
    """Wildfire"""

    # [x]Increase the damage of your Hero Power by 1.
    play = Buff(CONTROLLER, "BAR_546e")


BAR_546e = buff(heropower_damage=1)


class BAR_812:
    """Oasis Ally"""

    # [x]<b>Secret:</b> When a friendly minion is attacked, summon a 3/6 Water
    # Elemental.
    secret = Attack(None, FRIENDLY_MINIONS).on(
        FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "CS2_033"))
    )


class WC_041:
    """Shattering Blast"""

    # Destroy all <b>Frozen</b> minions.
    play = Destroy(ALL_MINIONS + FROZEN)
