from ..utils import *

##
# Minions


class REV_352:
    """Stonebound Gargon"""

    # [x]<b>Rush</b> <b>Infuse (@):</b> Also damages the minions next to
    # __whomever this attacks.
    infuse_card = "REV_352t"


class REV_352t:
    """Stonebound Gargon"""

    # [x]<b>Infused</b> <b>Rush</b>. Also damages the minions next to
    # __whomever this attacks.
    events = Attack(SELF).on(CLEAVE)


class REV_353:
    """Huntsman Altimor"""

    # [x]<b>Battlecry:</b> Summon a Gargon Companion. <b>Infuse ({0}):</b>
    # Summon another. _<b>Infuse ({1}):</b> And another!
    infuse_card = "REV_353t"
    play = Summon(CONTROLLER, RandomID(*GARGON_COMPANION))


class REV_353t:
    """Huntsman Altimor"""

    # [x]<b>Infused</b> <b>Battlecry:</b> Summon 2 Gargon Companions.
    # _______<b>Infuse (@):</b> Summon all 3!___
    infuse_card = "REV_353t2"
    play = Summon(CONTROLLER, RandomID(*GARGON_COMPANION) * 2)


class REV_353t2:
    """Huntsman Altimor"""

    # [x]<b>Infused</b> <b>Battlecry:</b> Summon all 3 Gargon Companions.
    play = Summon(CONTROLLER, RandomID(*GARGON_COMPANION) * 3)


class REV_353t4:
    """Barghast"""

    # Your other minions have +1 Attack.
    update = Refresh(FRIENDLY_MINIONS - SELF, buff="REV_353t4e")


REV_353t4e = buff(atk=1)


class REV_356:
    """Batty Guest"""

    # <b>Deathrattle:</b> Summon a 2/1 Bat.
    deathrattle = Summon(CONTROLLER, "REV_350t")


class REV_360:
    """Spirit Poacher"""

    # <b>Battlecry:</b> Summon a random <b>Dormant</b> Wildseed.
    play = Summon(CONTROLLER, RandomID(*WILDSEED))


class REV_360t:
    """Fox Spirit Wildseed"""

    # <b>Dormant</b> for 1 turn. <b>Rush</b>
    tags = {GameTag.DORMANT: True}
    dormant_turns = 1


class REV_360t1:
    """Bear Spirit Wildseed"""

    # <b>Dormant</b> for 2 turns. <b>Taunt</b>
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2


class REV_360t2:
    """Stag Spirit Wildseed"""

    # <b>Dormant</b> for 3 turns. When this awakens, equip a 3/2 Greatbow.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 3
    awaken = Summon(CONTROLLER, "REV_360t4")


class REV_363:
    """Ara'lon"""

    # <b>Battlecry:</b> Summon one of each <b>Dormant</b> Wildseed.
    play = Summon(CONTROLLER, RandomID(*WILDSEED) * 3)


class MAW_009:
    """Shadehound"""

    infuse_race = Race.BEAST

    # [x]Whenever this attacks, give your other Beasts +2/+2. <b>Infuse (@
    # Beasts):</b> Gain <b>Rush</b>.
    infuse_card = "MAW_009t"
    events = Attack(SELF).on(Buff(FRIENDLY_MINIONS - SELF + BEAST, "MAW_009e"))


MAW_009e = buff(+2, +2)


class MAW_009t:
    """Shadehound"""

    # <b>Infused</b> <b>Rush</b>. Whenever this attacks, give your other Beasts
    # +2/+2.
    events = Attack(SELF).on(Buff(FRIENDLY_MINIONS - SELF + BEAST, "MAW_009e"))


class MAW_011:
    """Defense Attorney Nathanos"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a friendly <b>Deathrattle</b> minion
    # that died this game. Trigger and gain its <b>Deathrattle</b>.
    play = Choice(
        CONTROLLER, RANDOM(DeDuplicate(FRIENDLY + DEAD_MINIONS + DEATHRATTLE), 3)
    ).then(
        Deathrattle(Choice.CARD),
        CopyDeathrattleBuff(Choice.CARD, "MAW_011e"),
    )


##
# Spells


class REV_350:
    """Frenzied Fangs"""

    # Summon two 2/1 Bats. <b>Infuse (@):</b> Give them +1/+2.
    infuse_card = "REV_350t2"
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "REV_350t") * 2


class REV_350t2:
    """Frenzied Fangs"""

    # <b>Infused</b> Summon two 2/1 Bats. Give them +1/+2.
    play = Summon(CONTROLLER, "REV_350t").then(Buff(Summon.CARD, "REV_350e")) * 2


REV_350e = buff(+1, +2)


class REV_361:
    """Wild Spirits"""

    # [x]Summon two different <b>Dormant</b> Wildseeds. Make your Wildseeds
    # awaken 1 turn sooner.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, RandomID(*WILDSEED) * 2).then(
        AwakenSooner(FRIENDLY + IN_PLAY + MINION + DORMANT + IDS(WILDSEED), 1)
    )


class REV_364:
    """Stag Charge"""

    # Deal $3 damage. Summon a random <b>Dormant</b> Wildseed.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Summon(CONTROLLER, RandomID(*WILDSEED))


class MAW_010:
    """Motion Denied"""

    # [x]<b>Secret:</b> After your opponent plays three cards in a turn, deal
    # $6 damage to the enemy hero.
    secret = Play(OPPONENT).after(
        (Attr(OPPONENT, GameTag.NUM_CARDS_PLAYED_THIS_TURN) >= 2)
        & (Reveal(SELF), Hit(ENEMY_HERO, 6))
    )


class REV_369:
    """Collateral Damage"""

    # [x]Deal $6 damage to three random enemy minions. Excess damage hits the
    # enemy hero.
    def play(self):
        targets = RANDOM(ENEMY_MINIONS, 3).eval(self.game, self)
        excess = 0
        for target in targets:
            if target.zone != Zone.PLAY or target.dead:
                continue
            damage = self.controller.get_spell_damage(self, 6)
            if not target.divine_shield and not target.immune:
                excess += max(0, damage - target.health)
            if not target.immune:
                yield Predamage(target, damage)
        if excess and not self.controller.opponent.hero.immune:
            # Spell Damage has already been included in the excess.
            yield Predamage(ENEMY_HERO, excess)


##
# Locations


class REV_362:
    """Castle Kennels"""

    # [x]Give a friendly minion +2 Attack. If it's a Beast, give it
    # <b>Rush</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    activate = Buff(TARGET, "REV_362e"), Find(TARGET + BEAST) & GiveRush(TARGET)


REV_362e = buff(atk=2)
