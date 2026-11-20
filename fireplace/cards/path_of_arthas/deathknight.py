from ..utils import *


class RLK_042:
    """Horn of Winter"""

    # Refresh 2 Mana Crystals.
    play = FillMana(CONTROLLER, 2)


class RLK_038:
    """Icy Touch"""

    # Deal $2 damage to an enemy and <b>Freeze</b> it.
    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2), Freeze(TARGET)


class RLK_110:
    """Ymirjar Frostbreaker"""

    # <b>Battlecry:</b> Gain +1 Attack for each Frost spell in your hand.
    play = Buff(SELF, "RLK_110e") * Count(FRIENDLY_HAND + FROST + SPELL)


RLK_110e = buff(atk=1)


class RLK_516:
    """Bone Breaker"""

    # After your hero attacks a minion, deal 2 damage to the enemy hero.
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(Hit(ENEMY_HERO, 2))


class RLK_018:
    """Plague Strike"""

    # Deal $3 damage to a minion. If it dies, summon a 2/2 Zombie with
    # <b>Rush</b>. (The wiki: it checks whether the minion was dealt lethal
    # damage.)
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Dead(TARGET) & Summon(CONTROLLER, "RLK_018t")


class UnholyFrenzyAttack(TargetedAction):
    """Your minions attack TARGET, left to right, while it lives; then
    resummon (a new copy of) any of them that died."""

    TARGET = ActionArg()

    def do(self, source, target):
        game = source.game
        died = []
        for minion in list(source.controller.field):
            if target.dead or target.zone != Zone.PLAY:
                break
            if (
                minion.dead
                or minion.zone != Zone.PLAY
                or minion.dormant
                or not minion.atk
            ):
                continue
            game.queue_actions(source, [Attack(minion, target)])
            if minion.dead:
                died.append(minion.id)
            game.process_deaths()
        if died:
            for id in died:
                game.queue_actions(source, [Summon(CONTROLLER, id)])


class RLK_056:
    """Unholy Frenzy"""

    # Choose an enemy minion. Your minions attack it. Resummon any that die.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = UnholyFrenzyAttack(TARGET)


class RLK_057:
    """Dark Transformation"""

    # Transform an Undead into a 4/5 Undead Monstrosity with <b>Rush</b>.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_TARGET_WITH_RACE: Race.UNDEAD,
    }
    play = Morph(TARGET, "RLK_057t")


class RLK_066:
    """Hematurge"""

    # <b>Battlecry:</b> Spend a <b>Corpse</b> to <b>Discover</b> a Blood Rune
    # card.
    play = SpendCorpses(CONTROLLER, 1).then(
        DISCOVER(
            RandomCollectible(
                card_class=CardClass.DEATHKNIGHT,
                cost_blood=range(1, 3),
            )
        )
    )


class RLK_083:
    """Deathchiller"""

    # After you cast a spell, deal 1 damage to two random enemies.
    events = OWN_SPELL_PLAY.after(Hit(RANDOM(ENEMY_CHARACTERS - DEAD) * 2, 1))


class RLK_711:
    """Vicious Bloodworm"""

    # <b>Battlecry:</b> Give a minion in your hand Attack equal to this
    # minion's Attack. (A target of the hand, CAN_TARGET_CARDS_IN_HAND.)
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    tags = {GameTag.CAN_TARGET_CARDS_IN_HAND: True}
    play = Buff(TARGET, "RLK_711e", atk=ATK(SELF))


class RLK_712:
    """Blood Tap"""

    # Give all minions in your hand +1/+1. Spend 2 <b>Corpses</b> to give them
    # +1/+1 more.
    play = (
        Buff(FRIENDLY_HAND + MINION, "RLK_712e"),
        SpendCorpses(CONTROLLER, 2).then(Buff(FRIENDLY_HAND + MINION, "RLK_712e")),
    )


RLK_712e = buff(+1, +1)


class RLK_015:
    """Howling Blast"""

    # Deal $3 damage to an enemy and <b>Freeze</b> it. Deal $1 damage to all
    # other enemies.
    requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Freeze(TARGET), Hit(ENEMY_CHARACTERS - TARGET, 1)


class RLK_087:
    """Asphyxiate"""

    # Destroy the highest Attack enemy minion. (A tie: at random.)
    play = Destroy(HIGHEST_ATK(ENEMY_MINIONS))


class RLK_512:
    """Glacial Advance"""

    # Deal $4 damage. Your next spell this turn costs (1) less.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4), Buff(CONTROLLER, "RLK_025o")


class RLK_025o:
    # The next spell you cast this turn costs (1) less. (TAG_ONE_TURN_EFFECT)
    update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})
    events = OWN_SPELL_PLAY.on(Destroy(SELF)), OWN_TURN_END.on(Destroy(SELF))


class RLK_731:
    """Darkfallen Neophyte"""

    # <b>Battlecry:</b> Spend 2 <b>Corpses</b> to give all minions in your
    # hand +2 Attack.
    play = SpendCorpses(CONTROLLER, 2).then(Buff(FRIENDLY_HAND + MINION, "RLK_731e"))


RLK_731e = buff(atk=2)


class RLK_062:
    """Nerubian Swarmguard"""

    # <b>Taunt</b> <b>Battlecry:</b> Summon two copies of this minion.
    play = Summon(CONTROLLER, ExactCopy(SELF)) * 2


class TombGuardiansSummon(TargetedAction):
    """Summon two Menacing Zombies for TARGET (a player); spend 4 Corpses to
    give them Reborn."""

    TARGET = ActionArg()

    def do(self, source, target):
        game = source.game
        zombies = []
        for _ in range(2):
            for cards in game.queue_actions(source, [Summon(target, "RLK_118t3")])[0]:
                zombies += [c for c in cards if c.zone == Zone.PLAY]
        if not zombies:
            return
        spent = game.queue_actions(source, [SpendCorpses(target, 4)])[0]
        if spent and spent[0]:
            for zombie in zombies:
                if zombie.zone == Zone.PLAY:
                    game.queue_actions(source, [GiveReborn(zombie)])


class RLK_118:
    """Tomb Guardians"""

    # Summon two 2/2 Zombies with <b>Taunt</b>. Spend 4 <b>Corpses</b> to give
    # them <b>Reborn</b>.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = TombGuardiansSummon(CONTROLLER)


class RLK_713:
    """Lady Deathwhisper"""

    # <b>Deathrattle:</b> Copy all Frost spells in your hand.
    deathrattle = Give(CONTROLLER, ExactCopy(FRIENDLY_HAND + FROST + SPELL))


class RLK_740:
    """Might of Menethil"""

    # <b>Battlecry:</b> Spend up to 3 <b>Corpses</b>. <b>Freeze</b> that many
    # enemy minions. (At random: the wiki.)
    play = SpendCorpses(CONTROLLER, Min(3, CORPSES)).then(
        Freeze(RANDOM(ENEMY_MINIONS - DEAD, SpendCorpses.AMOUNT))
    )


class RLK_745:
    """Malignant Horror"""

    # <b>Reborn</b> At the end of your turn, spend 4 <b>Corpses</b> to summon a
    # copy of this minion.
    events = OWN_TURN_END.on(
        -FULL_BOARD
        & SpendCorpses(CONTROLLER, 4).then(Summon(CONTROLLER, ExactCopy(SELF)))
    )


class RLK_504:
    """Corpse Bride"""

    # <b>Battlecry:</b> Spend up to 10 <b>Corpses</b> to summon a Risen Groom
    # with <b>Taunt</b> and that much Attack and Health.
    play = SpendCorpses(CONTROLLER, Min(10, CORPSES)).then(
        SummonCustomMinion(
            CONTROLLER, "RLK_506t", 1, SpendCorpses.AMOUNT, SpendCorpses.AMOUNT
        )
    )


class RLK_506t:
    """Risen Groom"""

    # <i>Doesn't leave a <b>Corpse</b>.</i>
    tags = {enums.LEAVES_NO_CORPSE: True}


class RLK_730:
    """Blood Boil"""

    # <b>Lifesteal</b> Infect all enemy minions. At the end of your turns, they
    # take 2 damage.
    play = Buff(ENEMY_MINIONS, "RLK_730e")


class RLK_730e:
    # The infection: at the end of its caster's turns, 2 damage to the minion,
    # with the Lifesteal of Blood Boil (the CardDefs gives the enchantment
    # LIFESTEAL); the minion itself does not gain Lifesteal.
    tags = {GameTag.LIFESTEAL: False, enums.LIFESTEAL_DAMAGE: True}
    events = OWN_TURN_END.on(Hit(OWNER, 2))


class RememberKill(TargetedAction):
    """TARGET (a weapon) remembers CARD, a minion it killed."""

    TARGET = ActionArg()
    CARD = CardArg()

    def do(self, source, target, card):
        target.killed_minions = list(getattr(target, "killed_minions", ())) + [card.id]


class KilledByThisWeapon(LazyValue):
    """A new copy of every minion the weapon killed, in the order they died."""

    def evaluate(self, source):
        return [
            source.controller.card(id, source)
            for id in getattr(source, "killed_minions", ())
        ]


class RLK_086:
    """Frostmourne"""

    # <b>Deathrattle:</b> Summon every minion killed by this weapon.
    # The same effect as the Lich King's Frostmourne (ICC_314t1, the wiki),
    # held by the weapon itself: its Deathrattle is its own.
    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Find(
            Attack.DEFENDER
            + DEAD
            + FilterSelector(
                lambda card, source: getattr(card, "damaged_source", None)
                is source.controller.hero
            )
        )
        & RememberKill(SELF, Attack.DEFENDER)
    )
    deathrattle = Summon(CONTROLLER, KilledByThisWeapon())


class RLK_505:
    """Marrow Manipulator"""

    # <b>Battlecry:</b> Spend up to 5 <b>Corpses</b>. Deal 2 damage to a random
    # enemy for each.
    play = SpendCorpses(CONTROLLER, Min(5, CORPSES)).then(
        Hit(RANDOM_ENEMY_CHARACTER, 2) * SpendCorpses.AMOUNT
    )


class RLK_063:
    """Frostwyrm's Fury"""

    # Deal $5 damage. <b>Freeze</b> all enemy minions. Summon a 5/5 Frostwyrm.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 5), Freeze(ENEMY_MINIONS), Summon(CONTROLLER, "RLK_063t")


class RLK_122:
    """The Scourge"""

    # Fill your board with random Undead.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, RandomMinion(race=Race.UNDEAD)) * Attr(
        CONTROLLER, "minion_slots"
    )
