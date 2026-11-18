from ...dsl.copy import copy_buffs
from ..utils import *


def remornia_form(source, card_id):
    card = source.controller.card(card_id, source)
    copy_buffs(source, source, card)
    # Preserve granted keywords in both directions, including minion-only
    # keywords while the blade is equipped as a weapon.
    card.silenceable_attributes = source.silenceable_attributes
    for attribute in card.silenceable_attributes:
        setattr(card, attribute, getattr(source, attribute))
    card.additional_deathrattles = source.additional_deathrattles[:]
    return card


##
# Minions


class REV_006:
    """Suspicious Pirate"""

    # <b>Battlecry:</b> <b>Discover</b> a weapon. If your opponent guesses your
    # choice, they get a copy.
    play = suspicious_discover(RandomWeapon())


class REV_930:
    """Crazed Wretch"""

    # Has +2 Attack and <b>Charge</b> while damaged.
    enrage = Refresh(SELF, {GameTag.ATK: 2, GameTag.CHARGE: True})


class REV_934:
    """Decimator Olgra"""

    # [x]<b>Battlecry:</b> Gain +1/+1 for each damaged minion, _then attack all
    # enemies.
    def play(self):
        count = len((ALL_MINIONS + DAMAGED).eval(self.game, self))
        yield Buff(SELF, "REV_934e", atk=count, max_health=count)
        targets = ENEMY_CHARACTERS.eval(self.game, self)
        for target in self.game.random.sample(targets, len(targets)):
            if self.zone != Zone.PLAY or self.dead:
                break
            yield Attack(SELF, target)
            yield Deaths()


class REV_316:
    """Remornia, Living Blade"""

    # <b>Rush</b> After this attacks, equip it.
    def equip(self, attacker, defender):
        if self.dead or self.zone != Zone.PLAY:
            return
        weapon = remornia_form(self, "REV_316t")
        yield SetStats(weapon, "REV_316e", self.atk, self.max_health)
        yield SetCurrentHealth(weapon, self.health)
        yield Remove(SELF)
        yield Summon(CONTROLLER, weapon)

    events = Attack(SELF).after(equip)


class REV_332:
    """Anima Extractor"""

    # [x]Whenever a friendly minion takes damage, give a random minion in your
    # hand +1/+1.
    events = Damage(FRIENDLY_MINIONS).on(
        Buff(RANDOM(FRIENDLY_HAND + MINION), "REV_332e")
    )


class MAW_028:
    """Mawsworn Bailiff"""

    # <b><b>Taunt</b>.</b> <b>Battlecry:</b> If you have 4 or more Armor, gain
    # +4/+4.
    play = (ARMOR(FRIENDLY_HERO) >= 4) & Buff(SELF, "MAW_028e2")


class MAW_029:
    """Weapons Expert"""

    # <b>Battlecry:</b> If you have a weapon equipped, give it +1/+1.
    # Otherwise, draw a weapon.
    play = Find(FRIENDLY_WEAPON) & Buff(FRIENDLY_WEAPON, "MAW_029e2") | FORCE_DRAW(
        WEAPON
    )


##
# Spells


class REV_931:
    """Conqueror's Banner"""

    # Reveal a card from each player's deck, three times. Draw any of yours
    # that cost more.
    def play(self):
        for _ in range(3):
            yield JoustHelper(RANDOM(FRIENDLY_DECK), RANDOM(ENEMY_DECK)) & ForceDraw(
                Joust.CHALLENGER
            )


class REV_334:
    """Burden of Pride"""

    # [x]Summon three 1/3 Jailers with <b>Taunt</b>. If you have 20 or less
    # Health, give them +1/+1.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = (
        Summon(CONTROLLER, "REV_334t").then(
            (CURRENT_HEALTH(FRIENDLY_HERO) <= 20) & Buff(Summon.CARD, "REV_334e")
        )
        * 3
    )


class REV_337:
    """Riot!"""

    # [x]Your minions can't be reduced below 1 Health this turn. They each
    # attack a random enemy minion.
    def play(self):
        yield Buff(CONTROLLER, "REV_337e2")
        yield Buff(FRIENDLY_MINIONS, "REV_337e")
        for minion in FRIENDLY_MINIONS.eval(self.game, self):
            yield Attack(minion, RANDOM_ENEMY_MINION)
            yield Deaths()


class MAW_027:
    """Call to the Stand"""

    # Your opponent summons a random minion from their hand.
    play = Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION))


##
# Weapons


class REV_933:
    """Imbued Axe"""

    # [x]After your hero attacks, give your damaged minions +1/+2. <b>Infuse
    # (@):</b> +2/+2 instead.
    infuse_card = "REV_933t"
    events = Attack(FRIENDLY_HERO).after(Buff(FRIENDLY_MINIONS + DAMAGED, "REV_933e"))


##
# Locations


class REV_990:
    """Sanguine Depths"""

    # [x]Deal 1 damage to a minion and give it +2 Attack.
    requirements = MINION_TARGET
    activate = Hit(TARGET, 1), Buff(TARGET, "REV_990e")


REV_316e = FixedStats
REV_332e = buff(+1, +1)
REV_934e = buff()
REV_334e = buff(+1, +1)
REV_990e = buff(atk=2)
REV_933e = buff(+1, +2)
REV_933e2 = buff(+2, +2)
MAW_028e2 = buff(+4, +4)
MAW_029e2 = buff(+1, +1)
REV_337e = buff(health_minimum=1)


class REV_337e2:
    events = Summon(CONTROLLER, MINION).on(Buff(Summon.CARD, "REV_337e"))


class REV_933t:
    events = Attack(FRIENDLY_HERO).after(Buff(FRIENDLY_MINIONS + DAMAGED, "REV_933e2"))


class REV_316t:
    def return_to_board(self, attacker, defender):
        if self.durability <= 0 or self.zone != Zone.PLAY:
            return
        minion = remornia_form(self, "REV_316")
        yield SetStats(minion, "REV_316e", self.atk, self.max_durability)
        yield SetCurrentHealth(minion, self.durability)
        yield Remove(SELF)
        yield Summon(CONTROLLER, minion)

    events = Attack(FRIENDLY_HERO).after(return_to_board)
