from ..utils import *

##
# Minions


class RLK_650:
    """Lingering Zombie"""

    # [x]<b>Deathrattle:</b> Summon a 1/1 Disarmed Zombie with
    # "<b>Deathrattle:</b> Summon a 1/1 Zombie."
    deathrattle = Summon(CONTROLLER, "RLK_650t")


class RLK_651:
    """Crypt Keeper"""

    # <b>Taunt</b>. Costs (1) less for each Armor you have.
    cost_mod = -ARMOR(FRIENDLY_HERO)


class RLK_657:
    """Underking"""

    # [x]<b>Rush</b> <b>Battlecry and Deathrattle:</b> Gain 6 Armor.
    play = deathrattle = GainArmor(FRIENDLY_HERO, 6)


class RLK_658:
    """Elder Nadox"""

    # <b>Battlecry:</b> Destroy a friendly Undead. Your minions gain its
    # Attack.
    requirements = FRIENDLY_UNDEAD_BATTLECRY
    play = Destroy(TARGET), Buff(FRIENDLY_MINIONS - TARGET, "RLK_658e", atk=ATK(TARGET))


class RLK_659:
    """Anub'Rekhan"""

    # <b>Battlecry:</b> Gain 8 Armor. Your next 3 minions this turn cost Armor
    # instead of Mana.
    play = GainArmor(FRIENDLY_HERO, 8), Buff(CONTROLLER, "RLK_659e")


class RLK_956:
    """Nerubian Flyer"""

    # [x]<b>Battlecry:</b> If a friendly Undead died after your last turn,
    # summon a 2/2 Nerubian.
    play = FRIENDLY_UNDEAD_DIED & Summon(CONTROLLER, "RLK_956t")


class NX2_010:
    """Death Beetle"""

    # <b>Taunt</b> <b>Manathirst (@):</b> Gain +4/+4 and <b>Charge</b>.
    play = Manathirst(11) & Buff(SELF, "NX2_010e")


##
# Spells


class RLK_652:
    """Unending Swarm"""

    # Resurrect all friendly minions that cost (2) or less.
    play = Summon(
        CONTROLLER,
        Copy(FRIENDLY + DEAD_MINIONS + (COST <= 2)),
    )


class RLK_654:
    """Beetlemancy"""

    # [x]<b>Choose One</b> - Gain 12 Armor; or Summon two 3/3 Beetles with
    # <b>Taunt</b>.
    choose = ("RLK_654a", "RLK_654b")
    play = GainArmor(FRIENDLY_HERO, 12), Summon(CONTROLLER, "RLK_654t") * 2


class RLK_655:
    """Wither"""

    # [x]Choose a minion. Each friendly Undead steals 1 Attack and Health from
    # it.
    requirements = MINION_TARGET

    def play(self):
        for undead in (FRIENDLY_MINIONS + UNDEAD - TARGET).eval(self.game, self):
            victim = self.target
            if victim.zone != Zone.PLAY or victim.dead:
                break
            attack = min(1, victim.atk)
            yield Buff(victim, "RLK_655e", atk=-attack, max_health=-1)
            yield Buff(undead, "RLK_655e2", atk=attack, max_health=1)


class RLK_656:
    """Chitinous Plating"""

    # Gain 4 Armor. At the start of your next turn, gain 4 more.
    play = GainArmor(FRIENDLY_HERO, 4), Buff(CONTROLLER, "RLK_656e")


class NX2_011:
    """Life from Death"""

    # [x]Draw 3 cards. <b>Infuse (@):</b> This costs (1).
    infuse_card = "NX2_011t"
    play = Draw(CONTROLLER) * 3


class NX2_012:
    """Rake"""

    # [x]Give your hero +2 Attack this turn. Deal damage equal to your hero's
    # Attack to a minion.
    requirements = MINION_TARGET
    play = Buff(FRIENDLY_HERO, "NX2_012e"), Hit(TARGET, ATK(FRIENDLY_HERO))


class RLK_650t:
    deathrattle = Summon(CONTROLLER, "RLK_650t2")


class RLK_654a:
    play = GainArmor(FRIENDLY_HERO, 12)


class RLK_654b:
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "RLK_654t") * 2


class RLK_656e:
    events = OWN_TURN_BEGIN.on(GainArmor(FRIENDLY_HERO, 4), Destroy(SELF))


class RLK_659e:
    def apply(self, target):
        self.progress = 3

    def use(self, player, card, target):
        self.progress -= 1
        if not self.progress:
            return Destroy(SELF)

    update = Refresh(FRIENDLY_HAND + MINION, {GameTag.CARD_COSTS_ARMOR: True})
    events = OWN_MINION_PLAY.on(use), OWN_TURN_END.on(Destroy(SELF))


RLK_658e = RLK_655e = RLK_655e2 = buff()
NX2_010e = buff(4, 4, charge=True)
NX2_011t = NX2_011
NX2_012e = buff(atk=2, tag_one_turn_effect=True)
