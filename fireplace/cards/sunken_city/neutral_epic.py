from ..utils import *

##
# Minions


class TSC_829:
    """Naga Giant"""

    # Costs (1) less for each Mana you've spent on spells this game.
    cost_mod = -AttrValue("spent_mana_on_spells_this_game")(CONTROLLER)


class TSC_926:
    """Smothering Starfish"""

    # <b>Battlecry:</b> <b>Silence</b> ALL other minions.
    play = Silence(ALL_MINIONS - SELF)


class TSC_052:
    """School Teacher"""

    # <b>Battlecry:</b> Add a 1/1 Nagaling to your hand. <b>Discover</b> a
    # spell that costs (3) or less to teach it.
    play = Discover(CONTROLLER, RandomSpell(cost=[0, 1, 2, 3])).then(
        Give(CONTROLLER, Teach(Discover.CARD, "TSC_052t"))
    )


class TSC_052t:
    def play(self):
        if self.entity_1:
            yield CastSpell(self.entity_1, self.target)


class TSC_064(HoldingSpellThresholdUtils):
    """Slithering Deathscale"""

    # <b>Battlecry:</b> If you've cast three spells while holding this, deal 3
    # damage to all enemies.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = Hit(ENEMY_CHARACTERS, 3)


class TSC_069:
    """Amalgam of the Deep"""

    # [x]<b>Battlecry:</b> Choose a friendly minion. <b>Discover</b> a minion
    # of the same minion type.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_HAS_RACE: 0,
    }

    def play(self):
        yield DISCOVER(RandomMinion(race=self.target.race))
