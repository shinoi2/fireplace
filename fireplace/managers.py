from hearthstone.enums import GameTag

from . import enums


class Manager(object):
    def __init__(self, obj):
        self.obj = obj
        self.observers = []

    def __getitem__(self, tag):
        if self.map.get(tag):
            return getattr(self.obj, self.map[tag], 0)
        raise KeyError

    def __setitem__(self, tag, value):
        setattr(self.obj, self.map[tag], value)

    def __iter__(self):
        for k in self.map:
            if self.map[k]:
                yield k

    def get(self, k, default=None):
        return self[k] if k in self.map else default

    def items(self):
        for k, v in self.map.items():
            if v is not None:
                yield k, self[k]

    def register(self, observer):
        self.observers.append(observer)

    def update(self, tags):
        for k, v in tags.items():
            if self.map.get(k) is not None:
                self[k] = v


class GameManager(Manager):
    map = {
        GameTag.CARDTYPE: "type",
        GameTag.NEXT_STEP: "next_step",
        GameTag.NUM_MINIONS_KILLED_THIS_TURN: "minions_killed_this_turn",
        GameTag.PROPOSED_ATTACKER: "proposed_attacker",
        GameTag.PROPOSED_DEFENDER: "proposed_defender",
        GameTag.STATE: "state",
        GameTag.STEP: "step",
        GameTag.TURN: "turn",
        GameTag.ZONE: "zone",
    }

    def __init__(self, obj):
        super().__init__(obj)
        self.counter = 1
        obj.entity_id = self.counter

    def action_start(self, type, source, index, target):
        for observer in self.observers:
            observer.action_start(type, source, index, target)

    def action_end(self, type, source):
        for observer in self.observers:
            observer.action_end(type, source)

    def new_entity(self, entity):
        self.counter += 1
        entity.entity_id = self.counter
        for observer in self.observers:
            observer.new_entity(entity)

    def start_game(self):
        for observer in self.observers:
            observer.start_game()

    def step(self, step, next_step=None):
        for observer in self.observers:
            observer.game_step(step, next_step)
        self.obj.step = step
        if next_step is not None:
            self.obj.next_step = next_step

    def turn(self, player):
        for observer in self.observers:
            observer.turn(player)

    def game_action(self, action, source, *args):
        for observer in self.observers:
            observer.game_action(action, source, *args)

    def targeted_action(self, action, source, target, *args):
        for observer in self.observers:
            observer.targeted_action(action, source, target, *args)


class BaseObserver:
    def action_start(self, type, source, index, target):
        pass

    def action_end(self, type, source):
        pass

    def game_step(self, step, next_step):
        pass

    def new_entity(self, entity):
        pass

    def start_game(self):
        pass

    def turn(self, player):
        pass

    def game_action(self, action, source, *args):
        pass

    def targeted_action(self, action, source, target, *args):
        pass


class PlayerManager(Manager):
    map = {
        GameTag.CANT_DRAW: "cant_draw",
        GameTag.CARDTYPE: "type",
        GameTag.COMBO_ACTIVE: "combo",
        GameTag.CONTROLLER: "controller",
        GameTag.CURRENT_PLAYER: "current_player",
        GameTag.CURRENT_SPELLPOWER: "spellpower",
        GameTag.CURRENT_HEROPOWER_DAMAGE_BONUS: "heropower_damage",
        GameTag.EMBRACE_THE_SHADOW: "healing_as_damage",
        GameTag.FATIGUE: "fatigue_counter",
        GameTag.FIRST_PLAYER: "first_player",
        GameTag.HEALING_DOUBLE: "healing_double",
        GameTag.HERO_ENTITY: "hero",
        GameTag.INVOKE_COUNTER: "invoke_counter",
        GameTag.LAST_CARD_PLAYED: "last_card_played",
        GameTag.MAXHANDSIZE: "max_hand_size",
        GameTag.MAXRESOURCES: "max_resources",
        GameTag.NUM_CARDS_DRAWN_THIS_TURN: "cards_drawn_this_turn",
        GameTag.NUM_CARDS_PLAYED_THIS_TURN: "cards_played_this_turn",
        GameTag.NUM_HERO_POWER_DAMAGE_THIS_GAME: "hero_power_damage_this_game",
        GameTag.AMOUNT_HEALED_THIS_GAME: "healed_this_game",
        GameTag.NUM_MINIONS_PLAYED_THIS_TURN: "minions_played_this_turn",
        GameTag.NUM_MINIONS_PLAYER_KILLED_THIS_TURN: "minions_killed_this_turn",
        GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME: "times_hero_power_used_this_game",
        GameTag.OVERLOAD_LOCKED: "overload_locked",
        GameTag.OVERLOAD_OWED: "overloaded",
        GameTag.OVERLOAD_THIS_GAME: "overloaded_this_game",
        GameTag.PLAYSTATE: "playstate",
        GameTag.RESOURCES: "max_mana",
        GameTag.RESOURCES_USED: "used_mana",
        GameTag.SPELLPOWER_DOUBLE: "spellpower_double",
        GameTag.STARTHANDSIZE: "start_hand_size",
        GameTag.HERO_POWER_DOUBLE: "hero_power_double",
        GameTag.TEMP_RESOURCES: "temp_mana",
        GameTag.TIMEOUT: "timeout",
        GameTag.TURN_START: "turn_start",
        enums.CANT_OVERLOAD: "cant_overload",
        enums.ELEMENTAL_PLAYED_LAST_TURN: "elemental_played_last_turn",
    }


CARD_ATTRIBUTE_MAP = {
    GameTag.ADJACENT_BUFF: "adjacent_buff",
    GameTag.ALL_TARGETS_RANDOM: "all_targets_random",
    GameTag.ARMOR: "armor",
    GameTag.ATK: "atk",
    GameTag.ATTACKING: "attacking",
    GameTag.ATTACHED: "owner",
    GameTag.AURA: "aura",
    GameTag.BATTLECRY: "has_battlecry",
    GameTag.CANNOT_ATTACK_HEROES: "cannot_attack_heroes",
    GameTag.CANT_ATTACK: "cant_attack",
    GameTag.CANT_BE_ATTACKED: "cant_be_attacked",
    GameTag.CANT_BE_DAMAGED: "cant_be_damaged",
    GameTag.CANT_BE_FROZEN: "cant_be_frozen",
    GameTag.CANT_BE_TARGETED_BY_ABILITIES: "cant_be_targeted_by_abilities",
    GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: "cant_be_targeted_by_hero_powers",
    GameTag.CANT_BE_TARGETED_BY_OPPONENTS: "cant_be_targeted_by_opponents",
    GameTag.CANT_PLAY: "cant_play",
    GameTag.CARD_ID: "id",
    GameTag.CARD_TARGET: "target",
    GameTag.CARDNAME: "name",
    GameTag.CARDRACE: "race",
    GameTag.CARDTYPE: "type",
    GameTag.CHARGE: "charge",
    GameTag.CHOOSE_ONE: "has_choose_one",
    GameTag.CHOOSE_BOTH: "choose_both",
    GameTag.CLASS: "card_class",
    GameTag.COMBO: "has_combo",
    GameTag.CONTROLLER: "controller",
    GameTag.COST: "cost",
    GameTag.CREATOR: "creator",
    GameTag.DAMAGE: "damage",
    GameTag.DEATHRATTLE: "has_deathrattle",
    GameTag.DEFENDING: "defending",
    GameTag.DISCOVER: "has_discover",
    GameTag.DIVINE_SHIELD: "divine_shield",
    GameTag.DORMANT: "dormant",
    GameTag.DURABILITY: "max_durability",
    GameTag.EMBRACE_THE_SHADOW: "healing_as_damage",
    GameTag.ENRAGED: "enrage",
    GameTag.EXHAUSTED: "exhausted",
    GameTag.EXTRA_DEATHRATTLES: "extra_deathrattles",
    GameTag.FORGETFUL: "forgetful",
    GameTag.FROZEN: "frozen",
    GameTag.GALAKROND_HERO_CARD: "galakrond_hero_card",
    GameTag.HEALING_DOUBLE: "healing_double",
    GameTag.HEALTH: "max_health",
    GameTag.HEALTH_MINIMUM: "min_health",
    GameTag.HEAVILY_ARMORED: "heavily_armored",
    GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: "additional_activations",
    GameTag.HEROPOWER_DAMAGE: "heropower_damage",
    enums.HEROPOWER_DISABLED: "heropower_disabled",
    GameTag.JADE_GOLEM: "jade_golem",
    GameTag.LIBRAM: "libram",
    GameTag.LIFESTEAL: "lifesteal",
    GameTag.IGNORE_TAUNT: "ignore_taunt",
    GameTag.INCOMING_DAMAGE_MULTIPLIER: "incoming_damage_multiplier",
    GameTag.ImmuneToSpellpower: "immune_to_spellpower",
    GameTag.IMMUNE_WHILE_ATTACKING: "immune_while_attacking",
    GameTag.INSPIRE: "has_inspire",
    GameTag.MAGNETIC: "has_magnetic",
    GameTag.MARK_OF_EVIL: "mark_of_evil",
    GameTag.MEGA_WINDFURY: "mega_windfury",
    GameTag.MULTI_CLASS_GROUP: "multi_class_group",
    GameTag.NUM_ATTACKS_THIS_TURN: "num_attacks",
    GameTag.NUM_TURNS_IN_PLAY: "turns_in_play",
    GameTag.TAG_ONE_TURN_EFFECT: "one_turn_effect",
    GameTag.TWINSPELL: "twinspell",
    GameTag.TWINSPELL_COPY: "twinspell_copy",
    GameTag.OVERLOAD: "overload",
    GameTag.OVERKILL: "has_overkill",
    GameTag.PARENT_CARD: "parent_card",
    GameTag.POISONOUS: "poisonous",
    GameTag.POWERED_UP: "powered_up",
    GameTag.QUEST: "quest",
    GameTag.QUEST_PROGRESS: "progress",
    GameTag.QUEST_PROGRESS_TOTAL: "progress_total",
    GameTag.RARITY: "rarity",
    GameTag.REBORN: "reborn",
    GameTag.RECEIVES_DOUBLE_SPELLDAMAGE_BONUS: "receives_double_spelldamage_bonus",
    GameTag.RUSH: "rush",
    GameTag.ECHO: "echo",
    GameTag.SECRET: "secret",
    GameTag.SECRET_DEATHRATTLE: "secret_deathrattle",
    GameTag.SHADOWFORM: "shadowform",
    GameTag.SHOULDEXITCOMBAT: "should_exit_combat",
    GameTag.STEADY_SHOT_CAN_TARGET: "steady_shot_can_target",
    GameTag.SILENCED: "silenced",
    GameTag.SPELLPOWER: "spellpower",
    GameTag.SPELLPOWER_DOUBLE: "spellpower_double",
    GameTag.SPELLS_COST_HEALTH: "spells_cost_health",
    GameTag.STEALTH: "stealthed",
    GameTag.HERO_POWER_DOUBLE: "hero_power_double",
    GameTag.TAUNT: "taunt",
    GameTag.UPGRADED_HERO_POWER: "upgraded_hero_power",
    GameTag.WINDFURY: "windfury",
    GameTag.ZONE: "zone",
    GameTag.ZONE_POSITION: "zone_position",
    enums.ALWAYS_WINS_BRAWLS: "always_wins_brawls",
    enums.CAST_ON_FRIENDLY_MINIONS: "cast_on_friendly_minions",
    enums.CAST_ON_FRIENDLY_CHARACTERS: "cast_on_friendly_characters",
    enums.EXTRA_BATTLECRIES: "extra_battlecries",
    enums.EXTRA_TRIGGER_SECRET: "extra_trigger_secret",
    enums.MINION_EXTRA_BATTLECRIES: "minio_extra_battlecries",
    enums.MINION_EXTRA_COMBOS: "minio_extra_combos",
    enums.KILLED_THIS_TURN: "killed_this_turn",
    enums.DISCARDED: "discarded",
    enums.MURLOCS_COST_HEALTH: "murlocs_cost_health",
    enums.UNLIMITED_ATTACKS: "unlimited_attacks",
    enums.EXTRA_END_TURN_EFFECT: "extra_end_turn_effect",
    enums.PASSIVE_HERO_POWER: "passive_hero_power",
    enums.KEEP_BUFF: "keep_buff",
    enums.DAMAGED_THIS_TURN: "damaged_this_turn",
    GameTag.CARDTEXT_ENTITY_0: "cardtext_entity_0",
    GameTag.CARDTEXT_ENTITY_1: "cardtext_entity_1",
    GameTag.CARDTEXT_ENTITY_2: "cardtext_entity_2",
    GameTag.CARDTEXT_ENTITY_3: "cardtext_entity_3",
    GameTag.CARDTEXT_ENTITY_4: "cardtext_entity_4",
    GameTag.CARDTEXT_ENTITY_5: "cardtext_entity_5",
    GameTag.CARDTEXT_ENTITY_6: "cardtext_entity_6",
    GameTag.CARDTEXT_ENTITY_7: "cardtext_entity_7",
    GameTag.CARDTEXT_ENTITY_8: "cardtext_entity_8",
    GameTag.CARDTEXT_ENTITY_9: "cardtext_entity_9",
    GameTag.AFFECTED_BY_SPELL_POWER: None,
    GameTag.ARTISTNAME: None,
    GameTag.AttackVisualType: None,
    GameTag.CARD_SET: None,
    GameTag.CARDTEXT_INHAND: "description",
    GameTag.CardTextInPlay: None,
    GameTag.COLLECTIBLE: None,
    GameTag.DevState: None,
    GameTag.ELITE: None,
    GameTag.ENCHANTMENT_IDLE_VISUAL: None,
    GameTag.ENCHANTMENT_BIRTH_VISUAL: None,
    GameTag.EVIL_GLOW: None,
    GameTag.FACTION: None,
    GameTag.FLAVORTEXT: None,
    GameTag.FREEZE: None,
    GameTag.HealTarget: None,
    GameTag.HIDE_COST: None,
    GameTag.HOW_TO_EARN: None,
    GameTag.HOW_TO_EARN_GOLDEN: None,
    GameTag.InvisibleDeathrattle: None,
    GameTag.MORPH: None,
    GameTag.SILENCE: None,
    GameTag.SUMMONED: None,
    GameTag.SPARE_PART: None,
    GameTag.SHOWN_HERO_POWER: None,
    GameTag.TARGETING_ARROW_TEXT: None,
    GameTag.TOPDECK: None,
    GameTag.TAG_AI_MUST_PLAY: None,
    GameTag.TRIGGER_VISUAL: None,
}


class CardManager(Manager):
    map = CARD_ATTRIBUTE_MAP
