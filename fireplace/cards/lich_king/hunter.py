from ..utils import *
from ..icecrown.hunter import ICC_828p

##
# Minions


class RLK_820:
    """Halduron Brightwing"""

    # <b>Battlecry:</b> Give all Arcane spells in your deck <b>Spell Damage
    # +1</b>.
    play = Buff(FRIENDLY_DECK + SPELL + ARCANE, "RLK_826e")


class RLK_821:
    """Scourge Tamer"""

    # <b>Battlecry:</b> Craft a custom Zombeast.
    play = ICC_828p.CreateZombeast(CONTROLLER)


class RLK_825:
    """Shockspitter"""

    # <b>Battlecry:</b> Deal @ damage. <i>(Improved by your hero attacks this
    # game!)</i>
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, Attr(CONTROLLER, enums.NUM_HERO_ATTACKS_THIS_GAME) + 1)


class RLK_826:
    """Silvermoon Farstrider"""

    # <b>Battlecry:</b> Give all Arcane spells in your hand <b>Spell Damage
    # +1</b>.
    play = Buff(FRIENDLY_HAND + SPELL + ARCANE, "RLK_826e")


class RLK_827:
    """Keeneye Spotter"""

    # [x]Whenever your hero attacks a minion, set its Health to 1.
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).on(Buff(Attack.DEFENDER, "RLK_827e"))


class NX2_014:
    """Trinket Tracker"""

    # <b>Battlecry:</b> Draw a 1-Cost spell.
    play = FORCE_DRAW(SPELL + (COST == 1))


##
# Spells


class RLK_804:
    """Conjured Arrow"""

    # Deal $2 damage to a minion. <b>Manathirst (6):</b> Draw that many cards.
    requirements = MINION_TARGET

    def play(self):
        damage = self.game.queue_actions(self, [Hit(TARGET, 2)])[0][0]
        if self.controller.max_mana >= 6 and damage:
            yield Draw(CONTROLLER) * damage


class RLK_817:
    """Arcane Quiver"""

    # [x]<b>Discover</b> a spell from your deck. If it's Arcane, give it
    # <b>Spell Damage +1</b>.
    play = Choice(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + SPELL), 3)).then(
        Find(Choice.CARD + ARCANE) & Buff(Choice.CARD, "RLK_826e"),
        ForceDraw(Choice.CARD),
    )


class RLK_818:
    """Ricochet Shot"""

    # Deal $1 damage to three random enemies.
    play = Hit(RANDOM(ENEMY_CHARACTERS - DEAD, 3), 1)


class RLK_819:
    """Eversong Portal"""

    # [x]Summon $1 4/4 |4(Lynx, Lynxes) with <b>Rush</b> <i>(improved by
    # <b>Spell Damage</b>)</i>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "RLK_819t") * SPELL_DAMAGE(1)


def zombees(token):
    def trigger(secret, opponent, target, _):
        if (
            target not in opponent.field
            or target.dead
            or target.dormant
            or not secret.controller.minion_slots
        ):
            return []

        def attack(source, player, bees):
            (bee,) = bees
            if bee.zone == Zone.PLAY and target.zone == Zone.PLAY and not target.dead:
                return [Attack(bee, target), Deaths()]
            return []

        return [Reveal(SELF), Summon(CONTROLLER, token).then(attack) * 4]

    return Play(OPPONENT, MINION).after(trigger)


class NX2_013:
    """ZOMBEEEES!!!"""

    # <b>Secret:</b> After your opponent plays a minion, summon four 1/1
    # Zombees to attack it.
    secret = zombees("NX2_013t")


class NX2_015:
    """Faithful Companions"""

    # [x]<b>Discover</b> a Beast from your deck and summon it. <b>Manathirst
    # (@):</b> Also summon a copy of it.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Choice(
        CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + MINION + BEAST), 3)
    ).then(
        Summon(CONTROLLER, Choice.CARD),
        Manathirst(10) & Summon(CONTROLLER, ExactCopy(Choice.CARD)),
    )


##
# Weapons


class RLK_828:
    """Hope of Quel'Thalas"""

    # [x]After your hero attacks, give your minions +1/+1 <i>(wherever they
    # are).</i>
    events = Attack(FRIENDLY_HERO).after(
        Buff((FRIENDLY_HAND | FRIENDLY_DECK | FRIENDLY_MINIONS) + MINION, "RLK_828e")
    )


class NX2_013t2:
    secret = zombees("NX2_013t3")


class RLK_827e:
    max_health = SET(1)


RLK_826e = buff(spellpower=1)
RLK_828e = buff(1, 1)
