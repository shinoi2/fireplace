from ..utils import *

##
# Minions


class BAR_071:
    """Taurajo Brave"""

    # <b>Frenzy:</b> Destroy a random enemy minion.
    frenzy = Destroy(RANDOM_ENEMY_MINION)


class BAR_072:
    """Burning Blade Acolyte"""

    # <b>Deathrattle:</b> Summon a 5/8 Demonspawn with <b>Taunt</b>.
    deathrattle = Summon(CONTROLLER, "BAR_072t")


class BAR_076:
    """Mor'shan Watch Post"""

    # [x]Can't attack. After your opponent plays a minion, _summon a 2/2 Grunt.
    events = Play(OPPONENT, MINION).after(Summon(CONTROLLER, "BAR_076t"))


class BAR_430:
    """Horde Operative"""

    # <b>Battlecry:</b> Copy your opponent's <b>Secrets</b> and put them into
    # play.
    play = Summon(CONTROLLER, Copy(ENEMY_SECRETS))


class BAR_745:
    """Hecklefang Hyena"""

    # <b>Battlecry:</b> Deal 3 damage to your hero.
    play = Hit(FRIENDLY_HERO, 3)
