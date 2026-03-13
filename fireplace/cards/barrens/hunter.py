from ..utils import *

##
# Minions


class BAR_030:
    """Pack Kodo"""

    # <b>Battlecry:</b> <b>Discover</b> a Beast, <b>Secret</b>, or weapon.
    play = GenericChoice(
        CONTROLLER, [RandomBeast(), RandomSpell(secret=True), RandomWeapon()]
    )


class BAR_031:
    """Sunscale Raptor"""

    # <b>Frenzy:</b> Shuffle a Sunscale Raptor into your deck with permanent
    # +2/+1.
    def frenzy(self, amount):
        def create_custom_card(self):
            card = self.controller.card("BAR_031")
            card.custom_card = True
            if hasattr(self, "_buff_times"):
                card._buff_times = self._buff_times + 1
            else:
                card._buff_times = 1

            def create_custom_card(card):
                card.atk = card.atk + card._buff_times * 2
                card.max_health = card.max_health + card._buff_times

            card.create_custom_card = create_custom_card
            card.create_custom_card(card)
            return card

        yield Shuffle(CONTROLLER, create_custom_card(self))


class BAR_033:
    """Prospector's Caravan"""

    # At the start of your turn, give all minions in your hand +1/+1.
    events = OWN_TURN_BEGIN.on(Buff(FRIENDLY_HAND + MINION, "BAR_033e"))


BAR_031e = buff(+1, +1)


class BAR_035:
    """Kolkar Pack Runner"""

    # [x]After you cast a spell, summon a 1/1 Hyena with <b>Rush</b>.
    events = Play(CONTROLLER, SPELL).after(Summon(CONTROLLER, "BAR_035t"))


class BAR_037:
    """Warsong Wrangler"""

    # [x]<b>Battlecry:</b> <b>Discover</b> a Beast from your deck. Give all
    # copies of it +2/+1 <i>(wherever_they_are)</i>.
    play = GenericChoice(
        CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + BEAST)) * 3
    ).then(Buff(SameId(GenericChoice.CARD), "BAR_037e"))


BAR_037e = buff(+2, +1)


class BAR_038:
    """Tavish Stormpike"""

    # After a friendly Beast attacks, summon a Beast from your deck that costs
    # (1) less.
    events = Attack(FRIENDLY_MINIONS + BEAST).after(
        Summon(
            CONTROLLER,
            RANDOM(FRIENDLY_DECK + BEAST + (COST == (COST(Attack.ATTACKER) - 1))),
        )
    )


class BAR_551:
    """Barak Kodobane"""

    # [x]<b>Battlecry:</b> Draw a 1, 2, __and 3-Cost spell.
    play = (
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == 1))),
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == 2))),
        ForceDraw(RANDOM(FRIENDLY_DECK + SPELL + (COST == 3))),
    )


class WC_008:
    """Sin'dorei Scentfinder"""

    # <b>Frenzy:</b> Summon four 1/1 Hyenas with <b>Rush</b>.
    frenzy = SummonBothSides(CONTROLLER, "BAR_035t") * 4


##
# Spells


class BAR_032:
    """Piercing Shot"""

    # Deal $6 damage to a minion. Excess damage hits the enemy hero.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(ENEMY_HERO, HitExcessDamage(TARGET, SPELL_DAMAGE(6)))


class BAR_034:
    """Tame Beast (Rank 1)"""

    # Summon a 2/2 Beast with <b>Rush</b>. <i>(Upgrades when you have 5
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 5) & Morph(SELF, "BAR_034t")

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_034t3")


class BAR_034t:
    """Tame Beast (Rank 2)"""

    # Summon a 4/4 Beast with <b>Rush</b>. <i>(Upgrades when you have 10
    # Mana.)</i>
    class Hand:
        update = (MANA(CONTROLLER) >= 10) & Morph(SELF, "BAR_034t2")

    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_034t4")


class BAR_034t2:
    """Tame Beast (Rank 3)"""

    # Summon a 6/6 Beast with <b>Rush</b>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "BAR_034t5")


class BAR_801:
    """Wound Prey"""

    # Deal $1 damage. Summon a 1/1 Hyena with <b>Rush</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 1), Summon(CONTROLLER, "BAR_035t")


class WC_007:
    """Serpentbloom"""

    # Give a friendly Beast <b>Poisonous</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
    }
    play = Buff(TARGET, "WC_007e")


WC_007e = buff(poisonous=True)
