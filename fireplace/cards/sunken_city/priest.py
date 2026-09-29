from ..utils import *

##
# Minions


class TSC_828:
    """Priestess Valishj"""

    # [x]<b>Battlecry:</b> Refresh an empty Mana Crystal for each spell
    # ___you've cast this turn.@ <i>(@)</i>
    play = FillMana(CONTROLLER, Count(CARDS_PLAYED_THIS_TURN + SPELL))


class TSC_212(HoldingSpellThresholdUtils):
    """Handmaiden"""

    # [x]<b>Battlecry:</b> If you've cast three spells while holding this, draw
    # 3 cards.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    play = Draw(CONTROLLER) * 3


class TSC_213:
    """Queensguard"""

    # <b>Battlecry:</b> Gain +1/+1 for each spell you've cast this turn.
    play = Buff(SELF, "TSC_213e") * Count(CARDS_PLAYED_THIS_TURN + SPELL)


TSC_213e = buff(+1, +1)


class TSC_216:
    """Blackwater Behemoth"""

    # <b>Colossal +1</b> <b>Lifesteal</b>
    colossal = Summon(CONTROLLER, "TSC_216t")


class TSC_216t:
    """Behemoth's Lure"""

    # [x]At the end of your turn, force a random enemy minion to attack the
    # __Blackwater Behemoth.
    events = OWN_TURN_END.on(
        Find(FRIENDLY_MINIONS + CREATOR) & Attack(RANDOM(ENEMY_MINIONS), CREATOR)
    )


class TID_700:
    """Disarming Elemental"""

    # [x]<b>Battlecry:</b> <b>Dredge</b> for your opponent. Set its Cost to
    # (6).
    play = DredgeOpponent(OPPONENT).then(Buff(DredgeOpponent.CARD, "TID_700e"))


TID_700e = buff(cost=SET(6))


class TID_085:
    """Herald of Light"""

    # [x]<b>Battlecry:</b> If you've cast a Holy spell while holding this,
    # restore #6 Health to all friendly characters.
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + HOLY)
    play = powered_up & Heal(FRIENDLY_CHARACTERS, 6)


##
# Spells


class TSC_209:
    """Whirlpool"""

    # Destroy all minions and all copies of them <i>(wherever they are)</i>.
    def play(self):
        minions = ALL_MINIONS.eval(self.game, self)
        for minion in minions:
            yield Destroy(ID(minion.id))


class TSC_210:
    """Illuminate"""

    # <b>Dredge</b>. If it's a spell, reduce its Cost by (3).
    play = Dredge(CONTROLLER).then(
        Find(Dredge.CARD + SPELL) & (Buff(Dredge.CARD, "TSC_210e"))
    )


@custom_card
class TSC_210e:
    tags = {
        GameTag.CARDNAME: "Illuminate Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -3,
    }
    events = REMOVED_IN_PLAY


class TSC_211:
    """Whispers of the Deep"""

    # [x]<b>Silence</b> a friendly minion, then deal damage equal to its Attack
    # randomly split among all enemy minions.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Silence(TARGET), (Hit(RANDOM_ENEMY_MINION, 1) * SPELL_DAMAGE(ATK(TARGET)))


class TSC_215:
    """Serpent Wig"""

    # [x]Give a minion +1/+2. If you played a Naga while holding this, add a
    # Serpent Wig to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    powered_up = Find(CARDS_PLAYED_WHEN_HOLDING + NAGA)
    play = Buff(TARGET, "TSC_215e"), powered_up & Give(CONTROLLER, "TSC_215")


TSC_215e = buff(+1, +2)


class TSC_775:
    """Azsharan Ritual"""

    # <b>Silence</b> a minion and summon a copy of it. Put a 'Sunken Ritual' on
    # the bottom of your deck.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Silence(TARGET),
        Summon(CONTROLLER, ExactCopy(TARGET)),
        PutOnBottom(CONTROLLER, "TSC_775t"),
    )


class TSC_775t:
    """Sunken Ritual"""

    # <b>Silence</b> a minion and summon 2 copies of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (Silence(TARGET), Summon(CONTROLLER, ExactCopy(TARGET)) * 2)


class TSC_702:
    """Switcheroo"""

    # Draw 2 minions. Swap their Health.
    play = SwapStateBuff(FORCE_DRAW(MINION), FORCE_DRAW(MINION), "TSC_702e")


class TSC_702e:
    max_health = lambda self, i: self._xhealth


class TID_920:
    """Drown"""

    # Put an enemy minion on the bottom of your deck.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = PutOnBottom(CONTROLLER, TARGET)
