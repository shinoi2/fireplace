from itertools import chain
from typing import TYPE_CHECKING

from collections import defaultdict
from hearthstone.enums import (
    CardClass,
    CardSet,
    CardType,
    GameTag,
    PlayState,
    Rarity,
    SpellSchool,
    Zone,
)

from .actions import (
    Concede,
    Discard,
    Draw,
    Fatigue,
    Give,
    Hit,
    LoseArmor,
    SpendMana,
    Steal,
    Summon,
)
from .aura import TargetableByAuras
from .card import Card
from .cards import db
from .deck import Deck
from .entity import Entity, slot_property
from .managers import PlayerManager
from .utils import CardList

if TYPE_CHECKING:
    from .card import (
        Character,
        Hero,
        Minion,
        Location,
        PlayableCard,
        Spell,
        Quest,
        Secret,
        SideQuest,
        HeroPower,
    )
    from .game import Game


class Player(Entity, TargetableByAuras):
    Manager = PlayerManager
    arcane_spells_cast_twice = slot_property("arcane_spells_cast_twice")
    spells_cant_target_heroes = slot_property("spells_cant_target_heroes")
    all_targets_random = slot_property("all_targets_random")
    cant_overload = slot_property("cant_overload")
    choose_both = slot_property("choose_both")
    extra_battlecries = slot_property("extra_battlecries")
    extra_trigger_secret = slot_property("extra_trigger_secret")
    minion_extra_battlecries = slot_property("minion_extra_battlecries")
    minion_extra_combos = slot_property("minion_extra_combos")
    extra_deathrattles = slot_property("extra_deathrattles")
    extra_end_turn_effect = slot_property("extra_end_turn_effect")
    healing_double = slot_property("healing_double", sum)
    hero_power_double = slot_property("hero_power_double", sum)
    healing_as_damage = slot_property("healing_as_damage")
    shadowform = slot_property("shadowform")
    spellpower_double = slot_property("spellpower_double", sum)
    spellpower_adjustment = slot_property("spellpower", sum)
    spellpower_arcane_adjustment = slot_property("spellpower_arcane", sum)
    spellpower_fire_adjustment = slot_property("spellpower_fire", sum)
    spellpower_frost_adjustment = slot_property("spellpower_frost", sum)
    spellpower_nature_adjustment = slot_property("spellpower_nature", sum)
    spellpower_holy_adjustment = slot_property("spellpower_holy", sum)
    spellpower_shadow_adjustment = slot_property("spellpower_shadow", sum)
    spellpower_fel_adjustment = slot_property("spellpower_fel", sum)
    spellpower_physical_adjustment = slot_property("spellpower_physical", sum)
    heropower_damage_adjustment = slot_property("heropower_damage", sum)
    spells_cost_health = slot_property("spells_cost_health")
    lifesteal_damages_opposing_hero = slot_property("lifesteal_damages_opposing_hero")
    cant_trigger_deathrattle = slot_property("cant_trigger_deathrattle")
    infuse_in_deck = slot_property("infuse_in_deck")
    cant_reveal_secrets = slot_property("cant_reveal_secrets")
    type = CardType.PLAYER

    def __init__(
        self,
        name,
        deck: list[str],
        hero: str,
        is_standard=True,
        *,
        sideboards: dict[str, list[str]] | None = None,
    ):
        self.game: Game = None
        self.opponent: Player = None
        self.first_player: bool = False
        self.starting_deck = deck
        if sideboards is None:
            sideboards = getattr(deck, "sideboards", {})
        self.starting_sideboards = {
            owner: tuple(cards) for owner, cards in sideboards.items()
        }
        self.starting_hero = hero
        self.data = None
        self.name = name
        self.hero: Hero = None
        self.hero_power: HeroPower = None
        self.is_standard = is_standard
        super().__init__()
        self.deck = Deck()
        self.sideboards = {
            owner: list(cards) for owner, cards in self.starting_sideboards.items()
        }
        self.hand = CardList["PlayableCard"]()
        self.field = CardList["Minion | Location"]()
        self.graveyard = CardList["PlayableCard"]()
        self.secrets = CardList["Secret | Quest | SideQuest"]()
        self.removed = CardList()
        self.choice = None
        self.max_hand_size = 10
        self.max_resources = 10
        self.max_deck_size = 60
        self.cant_draw = False
        self.cant_fatigue = False
        self.corpses = 0
        self.corpses_spent_this_game = 0
        self.combo = False
        self.fatigue_counter = 0
        self.last_card_played = None
        self.overloaded = 0
        self.overload_locked = 0
        self.overloaded_this_game = 0
        self._max_mana = 0
        self._start_hand_size = 3
        self.playstate = PlayState.INVALID
        self.temp_mana = 0
        self.timeout = 75
        self.times_hero_power_used_this_game = 0
        self.used_mana = 0
        self.minions_killed_this_turn = 0
        self.minions_played_this_turn = 0
        self.weapon = None
        self.zone = Zone.INVALID
        self.turn = None
        self.last_turn = None
        self.turns = []
        self.jade_golem = 1
        self.times_abyssal_curse = 0
        self.times_totem_summoned_this_game = 0
        self.times_beast_summoned_this_game = 0
        self.times_pirate_summoned_this_game = 0
        self.elemental_played_this_turn = 0
        self.elemental_played_last_turn = 0
        self.cards_drawn_this_turn = 0
        self.damage_dealt_to_enemy_hero_this_turn = 0
        self.cards_played_this_turn = 0
        self.cards_played_this_game = CardList()
        self.hero_power_damage_this_game = 0
        self.hero_attacks_this_game = 0
        self.spent_mana_on_spells_this_game = 0
        self.healed_this_game = 0
        self.armor_gained_this_game = 0
        self.healed_this_turn = 0
        self.hero_health_changed_this_turn = 0
        self.hero_health_changed_on_own_turn = 0
        self.cthun = None
        self.invoke_counter = 0
        self.spells_played_this_game = 0
        self.holy_spells_spent_this_game = 0
        self.other_choice_from_the_last_choose_one_spell = None
        self.relic_level = 1

    def is_legal(self):
        # The hero must be a collectible hero skin; its class determines deck rules.
        hero_id = (
            self.starting_hero
            if isinstance(self.starting_hero, str)
            else self.starting_hero.id
        )
        if hero_id not in db:
            return False
        heroxml = db[hero_id]
        if not heroxml.collectible:
            return False
        if heroxml.card_set != CardSet.HERO_SKINS:
            return False
        hero_classes = heroxml.card_class

        # Most decks contain 30 cards, but cards such as Prince Renathal can change this.
        deck_size = 30
        card_count = defaultdict(int)
        cost_blood = 0
        cost_frost = 0
        cost_unholy = 0
        deck_ids = [
            card if isinstance(card, str) else card.id for card in self.starting_deck
        ]
        if any(card_id not in db for card_id in deck_ids):
            return False
        sideboard_owners = {
            card_id: db[card_id]
            for card_id in deck_ids
            if db[card_id].tags.get(GameTag.MAX_SIDEBOARD_CARDS)
        }
        if self.starting_sideboards.keys() != sideboard_owners.keys():
            return False
        for owner, cards in self.starting_sideboards.items():
            tags = sideboard_owners[owner].tags
            maximum = tags[GameTag.MAX_SIDEBOARD_CARDS]
            minimum = tags.get(GameTag.MIN_SIDEBOARD_CARDS, maximum)
            if not minimum <= len(cards) <= maximum:
                return False
        sideboard_ids = chain.from_iterable(self.starting_sideboards.values())
        for card_id, in_sideboard in chain(
            ((card_id, False) for card_id in deck_ids),
            ((card_id, True) for card_id in sideboard_ids),
        ):
            if card_id not in db:
                return False
            cardxml = db[card_id]

            # Some cards count as copies of another card for the copy limit.
            if GameTag.DECK_RULE_COUNT_AS_COPY_OF_CARD_ID in cardxml.tags:
                dbf_id = cardxml.tags[GameTag.DECK_RULE_COUNT_AS_COPY_OF_CARD_ID]
                if dbf_id < cardxml.dbf_id and dbf_id in db.dbf:
                    card_id = db.dbf[dbf_id]
            if not cardxml.collectible:
                return False
            if in_sideboard and (
                (self.is_standard and not cardxml.is_standard)
                or cardxml.type
                not in (
                    CardType.MINION,
                    CardType.SPELL,
                    CardType.WEAPON,
                    CardType.HERO,
                    CardType.LOCATION,
                )
                or cardxml.card_set == CardSet.HERO_SKINS
                or cardxml.tags.get(GameTag.START_OF_GAME)
                or cardxml.tags.get(GameTag.GALAKROND_HERO_CARD)
                or card_id in ("SW_050", "BOT_914", "DAL_800")
            ):
                return False

            # A normal card may appear twice; legendary cards may appear only once.
            card_count[card_id] += 1
            if card_count[card_id] > 2:
                return False
            if cardxml.rarity == Rarity.LEGENDARY and card_count[card_id] > 1:
                return False
            # Multi-class cards accept any one of their listed classes.
            if cardxml.multiple_classes:
                if hero_classes not in cardxml.classes:
                    return False
            else:
                if cardxml.card_class not in [hero_classes, CardClass.NEUTRAL]:
                    return False

            # Deathknight three runes
            cost_blood = max(cost_blood, cardxml.cost_blood)
            cost_frost = max(cost_frost, cardxml.cost_frost)
            cost_unholy = max(cost_unholy, cardxml.cost_unholy)

            # Only one card may change the deck size, and all such cards must agree.
            if not in_sideboard and GameTag.DECK_RULE_MOD_DECK_SIZE in cardxml.tags:
                new_deck_size = cardxml.tags[GameTag.DECK_RULE_MOD_DECK_SIZE]
                if deck_size != new_deck_size:
                    if deck_size != 30:
                        return False
                    deck_size = new_deck_size

        if cost_blood + cost_frost + cost_unholy > 3:
            return False

        if len(self.starting_deck) != deck_size:
            return False

        return True

    def dump(self):
        data = super().dump()
        # data["name"], data["avatar"] = self.name
        if self.hero:
            data["hero"] = self.hero.dump()
            if self.hero.power:
                data["heropower"] = self.hero.power.dump()
        if self.weapon:
            data["weapon"] = self.weapon.dump()
        data["deck"] = len(self.deck)
        data["fatigue_counter"] = self.fatigue_counter
        data["hand"] = [card.dump() for card in self.hand]
        data["field"] = [card.dump() for card in self.field]
        data["secrets"] = [card.dump() for card in self.secrets]
        if self.choice:
            choice = data["choice"] = {}
            choice["cards"] = [card.dump() for card in self.choice.cards]
            choice["max_count"] = self.choice.max_count
            choice["min_count"] = self.choice.min_count
        data["max_mana"] = self.max_mana
        data["mana"] = self.mana
        data["timeout"] = self.timeout
        data["playstate"] = int(self.playstate)
        return data

    def dump_hidden(self):
        data = super().dump()
        # data["name"], data["avatar"] = self.name
        if self.hero:
            data["hero"] = self.hero.dump()
            if self.hero.power:
                data["heropower"] = self.hero.power.dump()
        if self.weapon:
            data["weapon"] = self.weapon.dump()
        data["deck"] = len(self.deck)
        data["fatigue_counter"] = self.fatigue_counter
        data["hand"] = [card.dump_hidden() for card in self.hand]
        data["field"] = [card.dump() for card in self.field]
        data["secrets"] = [card.dump_hidden() for card in self.secrets]
        if self.choice:
            choice = data["choice"] = {}
            choice["cards"] = [card.dump_hidden() for card in self.choice.cards]
            choice["max_count"] = self.choice.max_count
            choice["min_count"] = self.choice.min_count
        data["max_mana"] = self.max_mana
        data["mana"] = self.mana
        data["timeout"] = self.timeout
        data["playstate"] = int(self.playstate)
        return data

    def __str__(self):
        return self.name

    def __repr__(self):
        return "%s(name=%r, hero=%r)" % (self.__class__.__name__, self.name, self.hero)

    @property
    def current_player(self):
        return self.game.current_player is self

    @property
    def controller(self):
        return self

    @property
    def mana(self):
        mana = (
            max(0, self.max_mana - self.used_mana - self.overload_locked)
            + self.temp_mana
        )
        return mana

    @property
    def max_mana(self):
        return self._max_mana

    @max_mana.setter
    def max_mana(self, amount):
        self._max_mana = min(self.max_resources, max(0, amount))
        self.log("%s is now at %i mana crystals", self, self._max_mana)

    @property
    def heropower_damage(self):
        aura_power = self.controller.heropower_damage_adjustment
        minion_power = sum(
            minion.heropower_damage
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_arcane(self):
        aura_power = self.controller.spellpower_arcane_adjustment
        minion_power = sum(
            minion.spellpower_arcane
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_fire(self):
        aura_power = self.controller.spellpower_fire_adjustment
        minion_power = sum(
            minion.spellpower_fire
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_frost(self):
        aura_power = self.controller.spellpower_frost_adjustment
        minion_power = sum(
            minion.spellpower_frost
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_nature(self):
        aura_power = self.controller.spellpower_nature_adjustment
        minion_power = sum(
            minion.spellpower_nature
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_holy(self):
        aura_power = self.controller.spellpower_holy_adjustment
        minion_power = sum(
            minion.spellpower_holy
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_shadow(self):
        aura_power = self.controller.spellpower_shadow_adjustment
        minion_power = sum(
            minion.spellpower_shadow
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_fel(self):
        aura_power = self.controller.spellpower_fel_adjustment
        minion_power = sum(
            minion.spellpower_fel
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower_physical(self):
        aura_power = self.controller.spellpower_physic_adjustment
        minion_power = sum(
            minion.spellpower_physic
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def spellpower(self):
        aura_power = self.controller.spellpower_adjustment
        minion_power = sum(
            minion.spellpower
            for minion in self.field.filter(dormant=False, type=CardType.MINION)
        )
        return aura_power + minion_power

    @property
    def start_hand_size(self):
        if not self.first_player:
            # Give the second player an extra card
            return self._start_hand_size + 1
        return self._start_hand_size

    @property
    def characters(self):
        return CardList(
            chain(
                [self.hero] if self.hero else [],
                self.field.filter(type=CardType.MINION),
            )
        )

    @property
    def entities(self):
        for entity in self.field:
            yield from entity.entities
        for secret in self.secrets:
            yield from secret.entities
        yield from self.buffs
        if self.hero:
            yield from self.hero.entities
        yield self

    @property
    def live_entities(self):
        yield from self.field.filter(dormant=False, type=CardType.MINION)
        if self.hero:
            yield self.hero
        if self.weapon:
            yield self.weapon

    @property
    def actionable_entities(self):
        yield from self.characters
        yield from self.field.filter(type=CardType.LOCATION)
        yield from self.hand
        if self.hero.power:
            yield self.hero.power

    @property
    def minion_slots(self):
        return max(0, self.game.MAX_MINIONS_ON_FIELD - len(self.field))

    def copy_cthun_buff(self, card):
        for buff in self.cthun.buffs:
            buff.source.buff(
                card,
                buff.id,
                atk=buff.atk,
                max_health=buff.max_health,
                taunt=getattr(buff, "taunt", False),
            )

    def card(self, id, source=None, parent=None, zone=Zone.SETASIDE):
        card = Card(id)
        card.controller = self
        card.zone = zone
        if source is not None:
            card.creator = source
        if parent is not None:
            card.parent_card = parent
        # C'THUN
        if self.cthun and id == self.cthun.id:
            self.copy_cthun_buff(card)
        self.game.manager.new_entity(card)
        return card

    def prepare_for_game(self):
        # Whizbang
        if self.starting_hero == "BOT_914h" or self.starting_deck == ["BOT_914"]:
            from .cards.boomsday.whizbang_decks import WHIZBANG_DECKS

            self.starting_hero, self.starting_deck = self.game.random.choice(
                WHIZBANG_DECKS
            )

        if self.starting_hero == "DAL_800h" or self.starting_deck == ["DAL_800"]:
            from .cards.dalaran.zayle_decks import ZAYLE_DECKS

            self.starting_hero, self.starting_deck = self.game.random.choice(
                ZAYLE_DECKS
            )

        self.starting_hero = self.card(self.starting_hero)

        if "SW_050" in self.starting_deck:
            # Maestra of the Masquerad
            # You start the game as a different class until you play a Rogue card.
            classes = [
                # CardClass.DEATHKNIGHT,
                CardClass.DRUID,
                CardClass.HUNTER,
                CardClass.MAGE,
                CardClass.PALADIN,
                CardClass.PRIEST,
                # CardClass.ROGUE,
                CardClass.SHAMAN,
                CardClass.WARLOCK,
                CardClass.WARRIOR,
                CardClass.DEMONHUNTER,
            ]
            hero = self.game.random.choice(classes).default_hero
            self.summon(hero)
        else:
            self.summon(self.starting_hero)
        # self.game.trigger(self, [Summon(self, self.starting_hero)], event_args=None)
        for id in self.starting_deck:
            card = self.card(id, zone=Zone.DECK)
            if self.is_standard and not card.is_standard:
                self.is_standard = False
        if self.is_standard and any(
            not db[card_id].is_standard
            for cards in self.starting_sideboards.values()
            for card_id in cards
        ):
            self.is_standard = False
        self.starting_deck = CardList(self.deck[:])
        self.mulligan_shuffle_deck()
        self.cthun = self.card("OG_280")
        self.playstate = PlayState.PLAYING

        # Draw initial hand (but not any more than what we have in the deck)
        hand_size = min(len(self.deck), self.start_hand_size)
        # It's faster to move cards directly to the hand instead of drawing
        for _ in range(hand_size):
            self.deck[-1].zone = Zone.HAND

    def get_spell_damage(self, spell: "Spell", amount: int) -> int:
        """
        Returns the amount of damage \a amount will do, taking
        SPELLPOWER and SPELLPOWER_DOUBLE into account.
        """
        spell_school_power_map = {
            SpellSchool.ARCANE: self.spellpower_arcane,
            SpellSchool.FIRE: self.spellpower_fire,
            SpellSchool.FROST: self.spellpower_frost,
            SpellSchool.NATURE: self.spellpower_nature,
            SpellSchool.HOLY: self.spellpower_holy,
            SpellSchool.SHADOW: self.spellpower_shadow,
            SpellSchool.FEL: self.spellpower_fel,
        }
        if getattr(spell, "spell_school", SpellSchool.NONE) in spell_school_power_map:
            amount += spell_school_power_map[spell.spell_school]
        amount += self.spellpower + getattr(spell, "spellpower", 0)
        amount <<= self.controller.spellpower_double
        return amount

    def get_spell_heal(self, spell: "Spell", amount: int) -> int:
        """
        Returns the amount of heal \a amount will do, taking
        SPELLPOWER and SPELLPOWER_DOUBLE into account.
        """
        amount <<= self.controller.healing_double
        return amount

    def get_heropower_damage(self, heropower: "HeroPower", amount: int) -> int:
        amount += self.heropower_damage
        amount <<= self.controller.hero_power_double
        return amount

    def get_heropower_heal(self, heropower: "HeroPower", amount: int) -> int:
        amount <<= self.controller.hero_power_double
        return amount

    def discard_hand(self):
        self.log("%r discards their entire hand!", self)
        # iterate the list in reverse so we don't skip over cards in the process
        # yes it's stupid.
        self.game.refresh_auras()
        for card in self.hand[::-1]:
            card.discard()

    def can_pay_cost(self, card):
        """
        Returns whether the player can pay the resource cost of a card.
        """
        if self.spells_cost_health and card.type == CardType.SPELL:
            return self.hero.health > card.cost
        if card.card_costs_armor:
            return self.hero.armor >= card.cost
        if card.card_costs_health:
            return self.hero.health > card.cost
        return self.mana >= card.cost

    def pay_cost(self, source: Entity, amount: int) -> int:
        """
        Make player pay \a amount mana.
        Returns how much mana is spent, after temporary mana adjustments.
        """
        if self.spells_cost_health and source.type == CardType.SPELL:
            self.log("%s spells cost %i health", self, amount)
            self.game.queue_actions(self, [Hit(self.hero, amount)])
            return amount
        if getattr(source, "card_costs_armor", False):
            self.game.queue_actions(source, [LoseArmor(self.hero, amount)])
            return amount
        if getattr(source, "card_costs_health", False):
            self.log("%s cards cost %i health", source, amount)
            self.game.queue_actions(self, [Hit(self.hero, amount)])
            return amount
        if source.type == CardType.SPELL:
            self.spent_mana_on_spells_this_game += amount
            if source.spell_school == SpellSchool.HOLY:
                self.holy_spells_spent_this_game += amount
        self.game.queue_actions(source, [SpendMana(self, amount)])
        return amount

    def mulligan_shuffle_deck(self):
        """
        Quest cards are automatically included in the player's mulligan as the left-most card
        CANT_DRAW_DURING_MULLIGAN cards never included in the player's mulligan card
        """

        def key_func(card):
            if card.tags.get(GameTag.QUEST) or card.tags.get(GameTag.QUESTLINE):
                return 1, self.game.random.random()
            if card.tags.get(GameTag.CANT_DRAW_DURING_MULLIGAN):
                return -1, self.game.random.random()
            return 0, self.game.random.random()

        self.deck.sort(key=key_func)

    def shuffle_deck(self):
        self.log("%r shuffles their deck", self)
        self.game.random.shuffle(self.deck)

    def draw(self, count=1):
        if self.cant_draw:
            self.log("%s tries to draw %i cards, but can't draw", self, count)
            return None

        ret = self.game.cheat_action(self, [Draw(self) * count])[0]
        if count == 1:
            if not ret[0]:  # fatigue
                return None
            return ret[0][0]
        return ret

    def give(self, id: str) -> "PlayableCard":
        cards = self.game.cheat_action(self, [Give(self, id)])[0][0]
        if len(cards) > 0:
            return cards[0]

    def concede(self):
        ret = self.game.cheat_action(self, [Concede(self)])
        return ret

    def fatigue(self):
        return self.game.cheat_action(self, [Fatigue(self)])[0]

    def steal(self, card):
        return self.game.cheat_action(self, [Steal(card)])

    def summon(self, card) -> "PlayableCard":
        """
        Puts \a card in the PLAY zone
        """
        if isinstance(card, str):
            card = self.card(card)
        self.game.cheat_action(self, [Summon(self, card)])
        return card
