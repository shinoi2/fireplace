from ..utils import *

##
# Minions


class SW_444:
    """Twilight Deceptor"""

    # <b>Battlecry:</b> If any hero took damage this turn, draw a Shadow spell.
    powered_up = Find(ALL_HEROES + (DAMAGED_THIS_TURN > 0))
    play = powered_up & ForceDraw(RANDOM(FRIENDLY_DECK + SHADOW))


class SW_445:
    """Psyfiend"""

    # After you cast a Shadow spell, deal 2 damage to each hero.
    events = Play(CONTROLLER, SHADOW).after(Hit(ALL_HEROES, 2))


class SW_446:
    """Voidtouched Attendant"""

    # Both heroes take one extra damage from all sources.
    update = Refresh(ALL_HEROES, buff="SW_446e")


SW_446e = buff(incoming_damage_adjustment=1)


class SW_448:
    """Darkbishop Benedictus"""

    # <b>Start of Game:</b> If the spells in your deck are all Shadow, enter
    # Shadowform.
    class Deck:
        events = GameStart().on(
            Find(STARTING_DECK + SPELL - SHADOW) | Summon(CONTROLLER, "EX1_625t")
        )

    class Hand:
        events = GameStart().on(
            Find(STARTING_DECK + SPELL - SHADOW) | Summon(CONTROLLER, "EX1_625t")
        )


class DED_513:
    """Defias Leper"""

    # [x]<b>Battlecry:</b> If you're holding a Shadow spell, deal 2 damage.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_SHADOW_IN_HAND: 0}
    play = Hit(TARGET, 2)


class DED_514:
    """Copycat"""

    # <b>Battlecry:</b> Add a copy of the next card your opponent plays to your
    # hand.
    play = Buff(CONTROLLER, "DED_514e")


class DED_514e:
    events = Play(OPPONENT).after(Give(CONTROLLER, Copy(Play.CARD)), Destroy(SELF))


##
# Spells


class SW_433:
    """Seek Guidance"""

    # [x]<b>Questline:</b> Play a 2, 3, and 4-Cost card. <b>Reward:</b>
    # <b>Discover</b> a card from your deck.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        if card.cost not in self.entourage:
            self.entourage.append(card.cost)

    quest = Play(CONTROLLER, (COST >= 2) + (COST <= 4)).on(AddProgress(SELF, Play.CARD))
    reward = GenericChoice(CONTROLLER, RANDOM(FRIENDLY_DECK, 3)), Summon(
        CONTROLLER, "SW_433t"
    )


class SW_433t:
    """Discover the Void Shard"""

    # [x]<b>Questline:</b> Play a 5 and 6-Cost card. <b>Reward:</b>
    # <b>Discover</b> a card from your deck.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        if card.cost not in self.entourage:
            self.entourage.append(card.cost)

    quest = Play(CONTROLLER, (COST >= 5) + (COST <= 6)).on(AddProgress(SELF, Play.CARD))
    reward = GenericChoice(CONTROLLER, RANDOM(FRIENDLY_DECK, 3)), Summon(
        CONTROLLER, "SW_433t2"
    )


class SW_433t2(QuestRewardProtect):
    """Illuminate the Void"""

    # [x]<b>Questline:</b> Play a 7 and 8-Cost card. <b>Reward:</b> Xyrella,
    # the Sanctified.
    def progress(self):
        return len(self.entourage)

    def clear_progress(self):
        self.entourage = []

    def add_progress(self, card):
        if card.cost not in self.entourage:
            self.entourage.append(card.cost)

    quest = Play(CONTROLLER, (COST >= 7) + (COST <= 8)).on(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "SW_433t3")


class SW_433t3:
    """Xyrella, the Sanctified"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> Shuffle the Purified Shard into your
    # deck.
    play = Shuffle(CONTROLLER, "SW_433t3a")


class SW_433t3a:
    """Purified Shard"""

    # [x]Destroy the enemy hero.
    play = Destroy(ENEMY_HERO)


class SW_440:
    """Call of the Grave"""

    # [x]<b>Discover</b> a <b>Deathrattle</b> minion. If you have enough Mana
    # to play it, trigger its <b>Deathrattle</b>.
    play = DISCOVER(RandomMinion(deathrattle=True)).then(
        (CURRENT_MANA(CONTROLLER) >= COST(Discover.CARD)) & (Deathrattle(Discover.CARD))
    )


class SW_441:
    """Shard of the Naaru"""

    # <b>Tradeable</b> <b>Silence</b> all enemy minions.
    play = Silence(ALL_MINIONS)


class SW_442:
    """Void Shard"""

    # <b>Lifesteal</b> Deal $4 damage.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4)


class SW_443:
    """Elekk Mount"""

    # Give a minion +4/+7 and <b>Taunt</b>. When it dies, summon an Elekk.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "SW_443e")


class SW_443e:
    tags = {
        GameTag.ATK: 4,
        GameTag.HEALTH: 7,
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Summon(CONTROLLER, "SW_443t")


class DED_512:
    """Amulet of Undying"""

    # [x]<b>Tradeable</b> Resurrect @ friendly <b>Deathrattle</b> |4(minion,
    # minions). <i>(Upgrades when <b>Traded</b>!)</i>
    trade = AddProgress(SELF)
    play = Summon(
        CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE))
    ) * (CURRENT_PROGRESS(SELF) + 1)


##
# Weapons


class SW_012:
    """Shadowcloth Needle"""

    # [x]After you cast a Shadow spell, deal 1 damage to all enemies. Lose 1
    # Durability.
    events = Play(CONTROLLER, SHADOW).after(Hit(ENEMY_CHARACTERS, 1), Hit(SELF, 1))
