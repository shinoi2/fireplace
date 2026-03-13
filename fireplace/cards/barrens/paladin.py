from ..utils import *

##
# Minions


class BAR_871:
    """Soldier's Caravan"""

    # [x]At the start of your turn, summon two 1/1 Silver Hand Recruits.
    events = OWN_TURN_BEGIN.on(SummonBothSides(CONTROLLER, "CS2_101t") * 2)


class BAR_873:
    """Knight of Anointment"""

    # <b>Battlecry:</b> Draw a Holy spell.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + HOLY))


class BAR_876:
    """Northwatch Commander"""

    # <b>Battlecry:</b> If you control a <b>Secret</b>, draw a minion.
    play = Find(FRIENDLY_SECRETS) & ForceDraw(RANDOM(FRIENDLY_DECK + MINION))


class BAR_878:
    """Veteran Warmedic"""

    # [x]After you cast a Holy spell, summon a 2/2 Medic with <b>Lifesteal</b>.
    events = Play(CONTROLLER, SPELL + HOLY).after(Summon(CONTROLLER, "BAR_878t"))


class BAR_879:
    """Cannonmaster Smythe"""

    # <b>Battlecry:</b> Transform your <b>Secrets</b> into 3/3 Soldiers. They
    # transform back when they die.
    def play(self):
        secrets = FRIENDLY_SECRETS.eval(self.game, self)
        player = self.controller
        for secret in secrets:
            if len(player.field) < 7:
                yield Destroy(secret)
                yield Summon(CONTROLLER, "BAR_878t").then(
                    StoringBuff(Summon.CARD, "BAR_878e", secret)
                )


class BAR_878t:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, STORE_CARD)


class BAR_902:
    """Cariel Roame"""

    # [x]<b>Rush</b>, <b>Divine Shield</b> Whenever this attacks, reduce the
    # Cost of Holy ______spells in your hand by (1).___
    events = Attack(SELF).on(Buff(FRIENDLY_HAND + SPELL + HOLY, "BAR_902e"))


class BAR_902e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


##
# Spells


class BAR_550:
    """Galloping Savior"""

    # [x]<b>Secret:</b> After your opponent plays three cards in a turn, summon
    # a 3/4 Steed with <b>Taunt</b>.
    secrets = Play(OPPONENT).after(
        (Count(CARDS_PLAYED_THIS_TURN) >= 3)
        & (Reveal(SELF), Summon(CONTROLLER, "BAR_550t"))
    )


class BAR_880:
    """Conviction (Rank 1)"""

    # [x]Give a random friendly minion +3 Attack. <i>(Upgrades when you have 5
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_880t")

    play = Buff(RANDOM(FRIENDLY_MINIONS), "BAR_880e")


class BAR_880t:
    """Conviction (Rank 2)"""

    # [x]Give two random friendly minions +3 Attack. <i>(Upgrades when you have
    # 10 Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_880t2")

    play = Buff(RANDOM(FRIENDLY_MINIONS, 2), "BAR_880e")


class BAR_880t2:
    """Conviction (Rank 3)"""

    # Give three random friendly minions +3_Attack.
    play = Buff(RANDOM(FRIENDLY_MINIONS, 3), "BAR_880e")


BAR_880e = buff(atk=3)


class BAR_881:
    """Invigorating Sermon"""

    # Give +1/+1 to all minions in your hand, deck, and battlefield.
    play = Buff(FRIENDLY + (IN_DECK | IN_HAND | IN_PLAY) + MINION - DORMANT, "BAR_881e")


BAR_881e = buff(+1, +1)


class WC_033:
    """Judgment of Justice"""

    # <b>Secret:</b> When an enemy minion attacks, set its Attack and Health to
    # 1.
    secret = Attack(ENEMY_MINIONS).on(Reveal(SELF), Buff(Attack.ATTACKER, "WC_033e"))


class WC_033e:
    atk = SET(1)
    max_health = SET(1)


class WC_034:
    """Party Up!"""

    # Summon five 2/2 Adventurers with random bonus effects.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    entourage = ADVENTURERS
    play = Summon(CONTROLLER, RandomEntourage()) * 5


##
# Weapons


class BAR_875:
    """Sword of the Fallen"""

    # [x]After your hero attacks, cast a <b>Secret</b> from your deck.
    events = Attack(FRIENDLY_HERO).after(
        Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))
    )


class WC_032:
    """Seedcloud Buckler"""

    # [x]<b>Deathrattle:</b> Give your _minions <b>Divine Shield</b>.
    deathrattle = GiveDivineShield(FRIENDLY_MINIONS)
