from ..utils import *

##
# Minions


class AV_100:
    """Drek'Thar"""

    # [x]<b>Battlecry</b>: If this costs more than every minion in your deck,
    # summon 2 of them.
    powered_up = -Find(FRIENDLY_DECK + MINION + (COST <= COST(SELF)))
    play = powered_up & Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION, 2))


class AV_223:
    """Vanndar Stormpike"""

    # [x]<b>Battlecry</b>: If this costs less than every minion in your deck,
    # reduce their Cost by (3).
    powered_up = -Find(FRIENDLY_DECK + MINION + (COST >= COST(SELF)))
    play = powered_up & Buff(FRIENDLY_DECK + MINION, "AV_223e")


class AV_223e:
    tags = {GameTag.COST: -3}
    events = REMOVED_IN_PLAY


class AV_141t:
    """Lokholar the Ice Lord"""

    # <b>Rush</b>, <b>Windfury</b> Costs (5) less if you have 15 Health or
    # less.
    cost_mod = (CURRENT_HEALTH(FRIENDLY_HERO) <= 15) & -3


class AV_142t:
    """Ivus, the Forest Lord"""

    # [x]<b>Battlecry:</b> Spend the rest of your Mana and gain +2/+2,
    # <b>Rush</b>, <b>Divine Shield</b>, or <b>Taunt</b> at random for each.
    def play(self):
        count = self.controller.mana
        yield SpendMana(CONTROLLER, count)
        buffs = ["AV_142e", "AV_142e2", "AV_142e3", "AV_142e4"]
        for _ in range(count):
            buff = self.game.random.choice(buffs)
            if buff != "AV_142e":
                buffs.remove(buff)
            yield Buff(SELF, buff)


AV_142e = buff(+2, +2)
AV_142e2 = buff(rush=True)


class AV_142e3:
    """Forestguard"""

    # <b>Divine Shield</b>.
    def apply(self, target):
        self.game.trigger(self, (GiveDivineShield(target),), None)


AV_142e4 = buff(taunt=True)


class AV_143:
    """Korrak the Bloodrager"""

    # [x]<b>Deathrattle:</b> If this wasn't <b>Honorably Killed</b>, resummon
    # Korrak.
    deathrattle = (CURRENT_HEALTH(SELF) < 0) & Summon(CONTROLLER, "AV_143")


class ONY_004:
    """Raid Boss Onyxia"""

    # [x]<b>Rush</b>. <b>Immune</b> while you control a Whelp.
    # <b>Battlecry:</b> Summon six _2/1 Whelps with <b>Rush</b>.
    play = SummonBothSides(CONTROLLER, "ONY_001t") * 6
    update = Find(FRIENDLY_MINIONS + ID("ONY_001t")) & Refresh(
        SELF, {GameTag.IMMUNE: True}
    )


class ONY_005:
    """Kazakusan"""

    # [x]<b>Battlecry:</b> If all minions in your deck are Dragons, craft a
    # custom deck of Treasures.
    entourage = [
        "ONY_005ta1",
        "ONY_005ta2",
        "ONY_005ta3",
        "ONY_005ta4",
        "ONY_005ta5",
        "ONY_005ta6",
        "ONY_005ta7",
        "ONY_005ta8",
        "ONY_005ta9",
        "ONY_005ta10",
        "ONY_005ta11",
        "ONY_005ta12",
        "ONY_005ta13",
        "ONY_005tb1",
        "ONY_005tb2",
        "ONY_005tb3",
        "ONY_005tb4",
        "ONY_005tb5",
        "ONY_005tb6",
        "ONY_005tb7",
        "ONY_005tb8",
        "ONY_005tb9",
        "ONY_005tb12",
        "ONY_005tb13",
        "ONY_005tb14",
        "ONY_005tc1",
        "ONY_005tc2",
        "ONY_005tc3",
        "ONY_005tc4",
        "ONY_005tc5",
        "ONY_005tc6",
        "ONY_005tc7",
    ]
    powered_up = -Find(FRIENDLY_DECK + DRAGON)
    play = powered_up & (
        Destroy(FRIENDLY_DECK),
        Discover(CONTROLLER, RandomEntourage() * 3).then(
            Shuffle(CONTROLLER, Copy(Discover.CARD)) * 2
        )
        * 5,
    )


##
# Kazakusan generator cards


class ONY_005ta1:
    """Necrotic Poison"""

    # Destroy a minion.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY,
        PlayReq.REQ_MINION_TARGET,
    }
    play = Destroy(TARGET)


class ONY_005ta2:
    """Mutating Injection"""

    # Give a minion +4/+4 and <b>Taunt</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY,
        PlayReq.REQ_MINION_TARGET,
    }
    play = Buff(TARGET, "ONY_005ta2e")


ONY_005ta2e = buff(+4, +4, taunt=True)


class ONY_005ta3:
    """The Exorcisor"""

    # <b>Silence</b> any minion attacked by this weapon.
    events = Attack(FRIENDLY_HERO).on(Silence(Attack.DEFENDER))


class ONY_005ta4:
    """Pure Cold"""

    # Deal $8 damage to the enemy hero, and <b>Freeze</b> it.
    play = Hit(ENEMY_HERO, 8), Freeze(ENEMY_HERO)


class ONY_005ta5:
    """Bubba"""

    # [x]<b>Battlecry</b>: Summon six 1/1 Bloodhounds with <b>Rush</b> to
    # attack an enemy minion.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE,
        PlayReq.REQ_MINION_TARGET,
    }
    play = (
        SummonBothSides(CONTROLLER, "ONY_005ta5t").then(
            Dead(TARGET) | Attack(SummonBothSides.CARD, TARGET)
        )
        * 6
    )


class ONY_005ta6:
    """Holy Book"""

    # <b>Silence</b> and destroy a minion. Summon a 10/10 copy of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY,
        PlayReq.REQ_MINION_TARGET,
    }
    play = (
        Silence(TARGET),
        Destroy(TARGET),
        Summon(CONTROLLER, Copy(TARGET)).then(Buff(Summon.CARD, "ONY_005ta6e")),
    )


@custom_card
class ONY_005ta6e:
    tags = {
        GameTag.CARDNAME: "Holy Book Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    atk = SET(10)
    max_health = SET(10)


class ONY_005ta7:
    """Crusty the Crustacean"""

    # [x]<b>Battlecry:</b> Destroy a minion. Gain its Attack and Health.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE,
        PlayReq.REQ_MINION_TARGET,
    }
    play = (
        Buff(SELF, "ONY_005ta7e", atk=ATK(TARGET), max_health=CURRENT_HEALTH(TARGET)),
        Destroy(TARGET),
    )


class ONY_005ta8:
    """Looming Presence"""

    # Draw 2 cards. Gain 4 Armor.
    play = (Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4))


class ONY_005ta9:
    """Beastly Beauty"""

    # [x]<b>Rush</b> After this attacks a minion and survives, transform this
    # into an 8/8.
    events = Attack(SELF, ALL_MINIONS).after(Dead(SELF) | Morph(SELF, "ONY_005ta9t"))


class ONY_005ta10:
    """Spyglass"""

    # Put a copy of a random card in your opponent's hand into yours. It costs
    # (3) less.
    play = Give(CONTROLLER, Copy(RANDOM(ENEMY_HAND))).then(
        Buff(Give.CARD, "ONY_005ta10e")
    )


@custom_card
class ONY_005ta10e:
    tags = {
        GameTag.CARDNAME: "Spyglass Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.COST: -3,
    }
    events = REMOVED_IN_PLAY


class ONY_005ta11:
    """Clockwork Assistant"""

    # Has +1/+1 for each spell you've cast this game.
    update = Refresh(
        SELF,
        {
            GameTag.ATK: Count(CARDS_PLAYED_THIS_GAME + SPELL),
            GameTag.HEALTH: Count(CARDS_PLAYED_THIS_GAME + SPELL),
        },
    )


class ONY_005ta12:
    """Grimmer Patron"""

    # At the end of your turn, summon a copy of this minion.
    events = OWN_TURN_END.on(Summon(CONTROLLER, ExactCopy(SELF)))


class ONY_005ta13:
    """Puzzle Box"""

    # Transform all minions into random ones that cost (3) more.
    play = Evolve(ALL_MINIONS, 3)


class ONY_005tb1:
    """Hyperblaster"""

    # <b>Poisonous</b>. Your hero is <b>Immune</b> while attacking.
    update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class ONY_005tb2:
    """Gnomish Army Knife"""

    # [x]Give a minion <b>Rush</b>, <b>Windfury</b>, <b>Divine Shield</b>,
    # <b>Lifesteal</b>, <b>Poisonous</b>, <b>Taunt</b>, and <b>Stealth</b>.
    play = Buff(TARGET, "ONY_005tb2e"), GiveDivineShield(TARGET)


ONY_005tb2e = buff(
    rush=True,
    windfury=True,
    lifesteal=True,
    poisonous=True,
    taunt=True,
    stealth=True,
)


class ONY_005tb3:
    """LOCUUUUSTS!!!"""

    # <b>Twinspell</b> Choose an enemy. Fill your board with 2/2 Locusts that
    # attack it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = (
        Summon(CONTROLLER, "ONY_005tb3t2").then(
            Dead(TARGET) | Attack(Summon.CARD, TARGET)
        )
        * 7
    )


class ONY_005tb3t(ONY_005tb3):
    """LOCUUUUSTS!!!"""

    # Choose an enemy. Fill your board with 2/2 Locusts that attack it.
    pass


class ONY_005tb4:
    """Wand of Disintegration"""

    # <b>Silence</b> and destroy all enemy minions.
    play = Silence(ENEMY_MINIONS), Destroy(ENEMY_MINIONS)


class ONY_005tb5:
    """Staff of Scales"""

    # Summon three 1/1 Snakes with <b>Rush</b>, <b>Poisonous</b> and
    # <b>Reborn</b>.
    play = Summon(CONTROLLER, "ONY_005tb5t") * 3


class ONY_005tb6:
    """Phaoris' Blade"""

    # <b>Windfury</b>. After your hero attacks and kills a minion, this gains
    # +2/+1.
    events = Attack(FRIENDLY_HERO, MINION).after(
        Dead(Attack.DEFENDER) & Buff(SELF, "ONY_005tb6e")
    )


ONY_005tb6e = buff(+2, +1)


class ONY_005tb7:
    """Canopic Jars"""

    # [x]Give your minions "<b>Deathrattle:</b> Summon a random
    # <b>Legendary</b> minion."
    play = Buff(FRIENDLY_MINIONS, "ONY_005tb7e")


class ONY_005tb7e:
    """Canopic Jars"""

    # <b>Deathrattle:</b> Summon a random <b>Legendary</b> minion.
    deathrattle = Summon(CONTROLLER, RandomLegendaryMinion())


class ONY_005tb8:
    """Ancient Reflections"""

    # Choose a minion. Fill your board with 1/1 copies of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, Copy(TARGET)).then(Buff(Summon.CARD, "ONY_005tb8e")) * 7


class ONY_005tb8e:
    atk = SET(1)
    max_health = SET(1)


class ONY_005tb9:
    """Banana Split"""

    # Give a friendly minion +2/+2. Summon two copies of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ONY_005tb9e").then(Summon(CONTROLLER, ExactCopy(TARGET)) * 2)


ONY_005tb9e = buff(+2, +2)


class ONY_005tb610:
    """Zephrys's Lamp"""

    # Wish for the perfect card.
    play = GenericChoice(CONTROLLER, ZEPHRYS_POOL)


class ONY_005tb12:
    """Dr. Boom's Boombox"""

    # [x]Summon 7 'Boom Bots'.
    play = Summon(CONTROLLER, "GVG_110t") * 7


class ONY_005tb13:
    """Wax Rager"""

    # <b>Deathrattle:</b> Resummon this minion.
    deathrattle = Summon(CONTROLLER, "ONY_005tb13")


class ONY_005tb14:
    """Vampiric Fangs"""

    # Destroy a minion. Restore its Health to your hero.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Heal(FRIENDLY_HERO, CURRENT_HEALTH(TARGET)), Destroy(TARGET)


class ONY_005tc1:
    """Embers of Ragnaros"""

    # Shoot three fireballs at random enemies that deal $8 damage each.
    play = Hit(RANDOM_ENEMY_CHARACTER, 8) * 3


class ONY_005tc2:
    """Book of the Dead"""

    # Deal $7 damage to all enemies. Costs (1) less for each minion that's died
    # this game.
    cost_mod = -Count(KILLED + MINION)
    play = Hit(ENEMY_CHARACTERS, 7)


class ONY_005tc3:
    """Annoy-o Horn"""

    # Fill your board with annoying minions.
    entourage = [
        "GVG_085",
        "BOT_911",
        "OG_145",
    ]
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, RandomEntourage()) * 7


class ONY_005tc4:
    """Flex-plosion"""

    # Blow up half your opponent's stuff.
    def play(self):
        minion_count = Count(ENEMY_MINIONS).evaluate(self)
        yield Destroy(RANDOM(ENEMY_MINIONS) * ((minion_count + 1) / 2))
        hand_count = Count(ENEMY_HAND).evaluate(self)
        yield Destroy(RANDOM(ENEMY_HAND) * ((hand_count + 1) / 2))
        deck_count = Count(ENEMY_DECK).evaluate(self)
        yield Destroy(RANDOM(ENEMY_DECK) * ((deck_count + 1) / 2))
        health = CURRENT_HEALTH(ENEMY_HERO).evaluate(self)
        yield SetCurrentHealth(ENEMY_HERO, health / 2)
        mana = CURRENT_MANA(OPPONENT).evaluate(self)
        yield SetMana(OPPONENT, mana / 2)


class ONY_005tc5:
    """Blade of Quel'Delar"""

    pass


class ONY_005tc6:
    """Hilt of Quel'Delar"""

    # Give a minion +3/+3.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY,
        PlayReq.REQ_MINION_TARGET,
    }
    play = Buff(TARGET, "ONY_005tc6e")


ONY_005tc6e = buff(+3, +3)


class ONY_005tc7:
    """Quel'Delar"""

    # After your hero attacks, deal 4 damage to all_enemies.
    events = Attack(FRIENDLY_HERO).after(Hit(ENEMY_CHARACTERS, 4))
