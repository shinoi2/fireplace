from hearthstone.deckstrings import Deck
from hearthstone.enums import (
    CardClass,
    CardSet,
    CardType,
    GameTag,
    MultiClassGroup,
    Race,
    Rarity,
)

from ..actions import *
from ..aura import Refresh
from ..cards import db
from ..dsl import *
from ..enums import PlayReq, BoardEnum
from ..events import *

# For buffs which are removed when the card is moved to play (eg. cost buffs)
# This needs to be Summon, because of Summon from the hand
REMOVED_IN_PLAY = Summon(ALL_PLAYERS, OWNER).after(Destroy(SELF))

ENEMY_CLASS = Attr(ENEMY_HERO, GameTag.CLASS)
FRIENDLY_CLASS = Attr(FRIENDLY_HERO, GameTag.CLASS)


SetTag = lambda target, tag: SetTags(target, (tag,))
UnsetTag = lambda target, tag: UnsetTags(target, (tag,))

Freeze = lambda target: SetTag(target, GameTag.FROZEN)
Stealth = lambda target: SetTag(target, GameTag.STEALTH)
Unstealth = lambda target: UnsetTag(target, GameTag.STEALTH)
Taunt = lambda target: SetTag(target, GameTag.TAUNT)
GiveCharge = lambda target: SetTag(target, GameTag.CHARGE)
GiveDivineShield = lambda target: SetTag(target, GameTag.DIVINE_SHIELD)
GiveWindfury = lambda target: SetTag(target, GameTag.WINDFURY)
GivePoisonous = lambda target: SetTag(target, GameTag.POISONOUS)
GiveLifesteal = lambda target: SetTag(target, GameTag.LIFESTEAL)
GiveRush = lambda target: SetTag(target, GameTag.RUSH)
GiveReborn = lambda target: SetTag(target, GameTag.REBORN)
GiveTemporary = lambda target: SetTag(target, enums.TEMPORARY)


CLEAVE = Hit(TARGET_ADJACENT, ATK(SELF))
COINFLIP = RandomNumber(0, 1) == 1
EMPTY_BOARD = Count(FRIENDLY_MINIONS) == 0
EMPTY_HAND = Count(FRIENDLY_HAND) == 0
FULL_BOARD = Count(FRIENDLY_MINIONS) == 7
FULL_HAND = Count(FRIENDLY_HAND) == Attr(CONTROLLER, GameTag.MAXHANDSIZE)
HOLDING_DRAGON = Find(FRIENDLY_HAND + DRAGON - SELF)
ELEMENTAL_PLAYED_LAST_TURN = Attr(CONTROLLER, enums.ELEMENTAL_PLAYED_LAST_TURN) > 0
TIMES_SPELL_PLAYED_THIS_GAME = Attr(CONTROLLER, GameTag.NUM_SPELLS_PLAYED_THIS_GAME)
TIMES_SECRETS_PLAYED_THIS_GAME = Count(CARDS_PLAYED_THIS_GAME + SECRET)

DISCOVER = lambda *args: Discover(CONTROLLER, *args).then(
    Give(CONTROLLER, Discover.CARD)
)
FORCE_DRAW = lambda args: ForceDraw(CONTROLLER, RANDOM(FRIENDLY_DECK + args))

BASIC_HERO_POWERS = [
    "HERO_01bp",
    "HERO_02bp",
    "HERO_03bp",
    "HERO_04bp",
    "HERO_05bp",
    "HERO_06bp",
    "HERO_07bp",
    "HERO_08bp",
    "HERO_09bp",
    "HERO_10bp",
]

UPGRADED_HERO_POWERS = [
    "HERO_01bp",
    "HERO_02bp",
    "HERO_03bp",
    "HERO_04bp",
    "HERO_05bp",
    "HERO_06bp",
    "HERO_07bp",
    "HERO_08bp",
    "HERO_09bp",
    "HERO_10bp2",
]

UPGRADE_HERO_POWER = Summon(CONTROLLER, UPGRADED_HERO_POWER)

BASIC_TOTEMS = ["CS2_050", "CS2_051", "CS2_058", "NEW1_009"]

POTIONS = [
    "CFM_021",  # Freezing Potion
    "CFM_065",  # Volcanic Potion
    "CFM_620",  # Potion of Polymorph
    "CFM_603",  # Potion of Madness
    "CFM_604",  # Greater Healing Potion
    "CFM_661",  # Pint-Size Potion
    "CFM_662",  # Dragonfire Potion
    "CFM_094",  # Felfire Potion
    "CFM_608",  # Blastcrystal Potion
    "CFM_611",  # Bloodfury Potion
]

LICH_KING_CARDS = [
    "ICC_314t1",
    "ICC_314t2",
    "ICC_314t3",
    "ICC_314t4",
    "ICC_314t5",
    "ICC_314t6",
    "ICC_314t7",
    "ICC_314t8",
]

THE_COIN = "GAME_005"

LACKEY_CARDS = [
    "DAL_613",
    "DAL_614",
    "DAL_615",
    "DAL_739",
    "DAL_741",
    "ULD_616",
    "DRG_052",
]

ADVENTURERS = [
    "WC_034t",
    "WC_034t2",
    "WC_034t3",
    "WC_034t4",
    "WC_034t5",
    "WC_034t6",
    "WC_034t7",
    "WC_034t8",
]


WATCH_POSTS = [
    "BAR_074",
    "BAR_075",
    "BAR_076",
]

POISONS = [
    "CS2_074",
    "ICC_221",
    "YOP_015",
    "BAR_318",
    "BAR_321",
]

SOUL_FRAGMENT = "SCH_307t"

SPY_GIZMO = ["SW_052t4", "SW_052t5", "SW_052t6", "SW_052t7", "SW_052t8_t"]

RandomBasicTotem = lambda *args, **kw: RandomID(*BASIC_TOTEMS, **kw)
RandomBasicHeroPower = lambda *args, **kw: RandomID(*BASIC_HERO_POWERS, **kw)
RandomUpgradedHeroPower = lambda *args, **kw: RandomID(*UPGRADED_HERO_POWERS, **kw)
RandomPotion = lambda *args, **kw: RandomID(*POTIONS, **kw)
RandomLackey = lambda *args, **kw: RandomID(*LACKEY_CARDS, **kw)

# 50% chance to attack the wrong enemy.
FORGETFUL = Attack(SELF).on(
    COINFLIP
    & Retarget(SELF, RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(SELF)))
)

AT_MAX_MANA = lambda s: MANA(s) == MAX_MANA(s)
OVERLOADED = lambda s: (OVERLOAD_LOCKED(s) > 0) or (OVERLOAD_OWED(s) > 0)
CHECK_CTHUN = ATK(HIGHEST_ATK(CTHUN)) >= 10
INVOKED_TWICE = Attr(CONTROLLER, GameTag.INVOKE_COUNTER) >= 2

ZEPHRYS_POOL = [
    # 0 Cost
    "CS2_008",  # 月火术
    "CS2_041",  # 先祖治疗
    "CS2_072",  # 背刺
    "EX1_332",  # 沉默
    "EX1_607",  # 怒火中烧
    "EX1_621",  # 治疗之环
    "NEW1_003",  # 牺牲契约
    # 1 Cost
    "CS1_129",  # 心灵之火
    "CS2_004",  # 真言术：盾
    "CS2_005",  # 爪击
    "CS2_027",  # 镜像
    "CS2_037",  # 冰霜震击
    "CS2_065",  # 虚空行者
    "CS2_074",  # 致命药膏
    "CS2_075",  # 影袭
    "CS2_087",  # 力量祝福
    "CS2_146",  # 南海船工
    "DS1_185",  # 奥术射击
    "EX1_192",  # 圣光闪耀
    "EX1_238",  # 闪电箭
    "EX1_245",  # 大地震击
    "EX1_251",  # 叉状闪电
    "EX1_277",  # 奥术飞弹
    "EX1_302",  # 死亡缠绕
    "EX1_308",  # 灵魂之火
    "EX1_319",  # 烈焰小鬼
    "EX1_360",  # 谦逊
    "EX1_400",  # 旋风斩
    "EX1_410",  # 盾牌猛击
    "EX1_578",  # 野蛮之击
    "NEW1_017",  # 鱼人杀手蟹
    "NEW1_025",  # 血帆海盗
    # 2 Cost
    "CS2_009",  # 野性印记
    "CS2_024",  # 寒冰箭
    "CS2_025",  # 魔爆术
    "CS2_039",  # 风怒
    "CS2_045",  # 石化武器
    "CS2_073",  # 冷血
    "CS2_084",  # 猎人印记
    "CS2_089",  # 圣光术
    "CS2_104",  # 狂暴
    "CS2_105",  # 英勇打击
    "CS2_108",  # 斩杀
    "CS2_114",  # 顺劈斩
    "CS2_234",  # 暗言术：痛
    "EX1_059",  # 疯狂的炼金师
    "EX1_066",  # 酸性沼泽软泥怪
    "EX1_124",  # 刺骨
    "EX1_126",  # 背叛
    "EX1_154",  # 愤怒
    "EX1_160",  # 野性之力
    "EX1_392",  # 战斗怒火
    "EX1_544",  # 照明弹
    "EX1_581",  # 闷棍
    "EX1_608",  # 巫师学徒
    # 3 Cost
    "CS2_007",  # 治疗之触
    "CS2_011",  # 野蛮咆哮
    "CS2_013",  # 野性成长
    "CS2_023",  # 奥术智慧
    "CS2_026",  # 冰霜新星
    "CS2_057",  # 暗影箭
    "CS2_203",  # 铁喙猫头鹰
    "EX1_014",  # 穆克拉
    "EX1_085",  # 精神控制技师
    "EX1_129",  # 刀扇
    "EX1_134",  # 军情七处特工
    "EX1_155",  # 自然印记
    "EX1_189",  # 光明之翼
    "EX1_241",  # 熔岩爆裂
    "EX1_248",  # 野性狼魂
    "EX1_259",  # 闪电风暴
    "EX1_507",  # 鱼人领军
    "EX1_536",  # 鹰角弓
    "EX1_538",  # 关门放狗
    "EX1_539",  # 杀戮命令
    "EX1_590",  # 血骑士
    "EX1_606",  # 盾牌格挡
    "EX1_613",  # 艾德温·范克里夫
    "EX1_617",  # 致命射击
    "EX1_622",  # 暗言术：灭
    "NEW1_027",  # 南海船长
    "NEW1_031",  # 动物伙伴
    # 4 Cost
    "CS2_012",  # 横扫
    "CS2_022",  # 变形术
    "CS2_029",  # 火球术
    "CS2_033",  # 水元素
    "CS2_062",  # 地狱烈焰
    "CS2_092",  # 王者祝福
    "CS2_093",  # 奉献
    "CS2_094",  # 愤怒之锤
    "CS2_097",  # 真银圣剑
    "CS2_233",  # 剑刃乱舞
    "DS1_070",  # 驯兽师
    "DS1_183",  # 多重射击
    "EX1_043",  # 暮光幼龙
    "EX1_048",  # 破法者
    "EX1_093",  # 阿古斯防御者
    "EX1_158",  # 丛林之魂
    "EX1_186",  # 军情七处渗透者
    "EX1_246",  # 妖术
    "EX1_275",  # 冰锥术
    "EX1_303",  # 暗影烈焰
    "EX1_334",  # 暗影狂乱
    "EX1_570",  # 撕咬
    "EX1_587",  # 风语者
    "EX1_619",  # 生而平等
    "EX1_626",  # 群体驱散
    "NEW1_022",  # 恐怖海盗
    # 5 Cost
    "CS1_112",  # 神圣新星
    "CS2_046",  # 嗜血
    "CS2_076",  # 刺杀
    "CS2_080",  # 刺客之刃
    "CS2_112",  # 奥金斧
    "DS1_178",  # 苔原犀牛
    "EX1_005",  # 王牌猎人
    "EX1_165",  # 利爪德鲁伊
    "EX1_250",  # 土元素
    "EX1_355",  # 受祝福的勇士
    "EX1_407",  # 绝命乱斗
    "EX1_537",  # 爆炸射击
    "EX1_558",  # 哈里森·琼斯
    "EX1_564",  # 无面操纵者
    "EX1_567",  # 毁灭之锤
    "NEW1_041",  # 狂奔科多兽
    # 6 Cost
    "CS2_028",  # 暴风雪
    "CS2_042",  # 火元素
    "CS2_064",  # 恐惧地狱火
    "EX1_002",  # 黑骑士
    "EX1_091",  # 秘教暗影祭司
    "EX1_164",  # 滋养
    "EX1_309",  # 灵魂虹吸
    "EX1_384",  # 复仇之怒
    "EX1_534",  # 长鬃草原狮
    "EX1_624",  # 神圣之火
    # 7 Cost
    "CS2_032",  # 烈焰风暴
    "CS2_077",  # 疾跑
    "CS2_088",  # 列王守卫
    "DS1_188",  # 角斗士的长弓
    "EX1_178",  # 战争古树
    "EX1_190",  # 大检察官怀特迈恩
    "EX1_249",  # 迦顿男爵
    "EX1_411",  # 血吼
    # 8 Cost
    "EX1_183",  # 野性赐福
    "EX1_312",  # 扭曲虚空
    "EX1_354",  # 圣疗术
    "EX1_383",  # 提里奥·弗丁
    # 9 Cost
    "EX1_323",  # 加拉克苏斯大王
    "EX1_543",  # 暴龙王克鲁什
    "EX1_561",  # 阿莱克丝塔萨
    "EX1_572",  # 伊瑟拉
    # 10+ Cost
    "CS1_113",  # 精神控制
    "EX1_279",  # 炎爆术
    "EX1_586",  # 海巨人
    "NEW1_030",  # 死亡之翼
    "EX1_105",  # 山岭巨人
]


SPELL_SCHOOLS = [
    SpellSchool.ARCANE,
    SpellSchool.FIRE,
    SpellSchool.FROST,
    SpellSchool.NATURE,
    SpellSchool.HOLY,
    SpellSchool.SHADOW,
    SpellSchool.FEL,
]


class JoustHelper(Evaluator):
    """
    A helper evaluator class for jousts to allow JOUST & ... syntax.
    """

    def __init__(self, challenger, defender):
        self.challenger = challenger
        self.defender = defender
        super().__init__()

    def trigger(self, source):
        action = Joust(self.challenger, self.defender).then(
            JoustEvaluator(Joust.CHALLENGER, Joust.DEFENDER) & self._if | self._else
        )

        return action.trigger(source)


JOUST = JoustHelper(RANDOM(FRIENDLY_DECK + MINION), RANDOM(ENEMY_DECK + MINION))

JOUST_SPELL = JoustHelper(RANDOM(FRIENDLY_DECK + SPELL), RANDOM(ENEMY_DECK + SPELL))

RECRUIT = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
Recruit = lambda selector: Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + selector))

MAGNETIC = lambda buff: Find(RIGHT_OF(SELF) + MECH) & (
    Buff(RIGHT_OF(SELF), buff, atk=ATK(SELF), max_health=CURRENT_HEALTH(SELF)),
    Remove(SELF),
)

INVOKE = Invoke(MAIN_GALAKROND)


def SET(amt):
    return lambda self, i: amt


# Buff helper
def buff(atk=0, health=0, **kwargs):
    buff_tags = {}
    if atk:
        buff_tags[GameTag.ATK] = atk
    if health:
        buff_tags[GameTag.HEALTH] = health

    for tag in GameTag:
        if tag.name.lower() in kwargs.copy():
            buff_tags[tag] = kwargs.pop(tag.name.lower())

    if "immune" in kwargs:
        value = kwargs.pop("immune")
        buff_tags[GameTag.CANT_BE_DAMAGED] = value
        buff_tags[GameTag.CANT_BE_TARGETED_BY_OPPONENTS] = value

    if kwargs:
        raise NotImplementedError(kwargs)

    class Buff:
        tags = buff_tags

    return Buff


def AttackHealthSwapBuff():
    def apply(self, target):
        self._xatk = target.health
        self._xhealth = target.atk
        target.damage = 0

    cls = buff()
    cls.atk = lambda self, i: self._xatk
    cls.max_health = lambda self, i: self._xhealth
    cls.apply = apply

    return cls


def GainEmptyMana(selector, amount):
    """
    Helper to gain an empty mana crystal (gains mana, then spends it)
    """
    return GainMana(selector, amount).then(SpendMana(selector, GainMana.AMOUNT))


def custom_card(cls):
    from . import CardDB, db

    id = cls.__name__
    if GameTag.CARDNAME not in cls.tags:
        raise ValueError("No name provided for custom card %r" % (cls))
    db[id] = CardDB.merge(id, None, cls)
    # Give the card its fake name
    db[id].strings = {
        GameTag.CARDNAME: {"enUS": cls.tags[GameTag.CARDNAME]},
        GameTag.CARDTEXT_INHAND: {"enUS": ""},
    }
    return cls


def decode_deckstring(deckstring: str):
    deck = Deck.from_deckstring(deckstring)
    hero_id = deck.heroes[0]
    hero_id = db.dbf[hero_id]
    cards = []
    for card_id, num in deck.cards:
        card_id: str = db.dbf[card_id]
        card_id = card_id.removeprefix("CORE_")
        cards += [card_id] * num
    return hero_id, cards


class JadeGolemUtils:
    def custom_cardtext(self):
        return self.data.description.split("@")[0]

    def cardtext_entity_0(self):
        jade_golem = self.controller.jade_golem
        return f"{jade_golem}/{jade_golem}"

    def cardtext_entity_1(self):
        if self.data.locale == "enUS":
            jade_golem = self.controller.jade_golem
            if jade_golem == 8 or jade_golem == 18:
                return "n"
        return ""

    tags = {
        enums.CUSTOM_CARDTEXT: custom_cardtext,
        GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
        GameTag.CARDTEXT_ENTITY_1: cardtext_entity_1,
    }


class SchemeUtils:
    def custom_cardtext(self):
        return self.data.description.replace("@", "{0}")

    def cardtext_entity_0(self):
        return self.progress

    tags = {
        enums.CUSTOM_CARDTEXT: custom_cardtext,
        GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
    }

    class Hand:
        events = OWN_TURN_BEGIN.on(AddProgress(SELF, SELF))


class GalakrondUtils:
    def custom_cardtext(self):
        if self.zone == Zone.PLAY:
            return self.data.description.replace("(@)", "").replace("（@）", "")
        locale_map = {
            "deDE": "Noch {0}-mal",
            "enUS": "{0} left!",
            "esES": "Faltan: {0}",
            "esMX": "¡Faltan {0}!",
            "frFR": "Encore {0} !",
            "itIT": "{0} restante!",
            "jaJP": "あと{0}回！",
            "koKR": "{0}회 남음",
            "plPL": "Jeszcze {0}!",
            "ptBR": "{0} restando",
            "ruRU": "Еще {0} раз.",
            "thTH": "เหลืออีก {0} ครั้ง!",
            "zhCN": "还剩{0}次",
            "zhTW": "還剩{0}次",
        }
        return self.data.description.replace("@", locale_map[self.data.locale])

    def cardtext_entity_0(self):
        return self.progress_total - self.progress

    def finished(self):
        return (
            self.progress_total > 0
            and self.progress >= self.progress_total
            and self.zone != Zone.PLAY
        )

    tags = {
        enums.CUSTOM_CARDTEXT: custom_cardtext,
        GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
    }


class ThresholdUtils(type):
    def __new__(cls, name, bases, namespace):
        def custom_cardtext(self):
            splited = self.data.description.split("@")
            if self.powered_up:
                return splited[0] + splited[2]
            return splited[0] + splited[1]

        def cardtext_entity_0(self):
            return self.player_tag_threshold_value - getattr(
                self.controller, self.map[self.player_tag_threshold_tag_id], 0
            )

        tags = {
            enums.CUSTOM_CARDTEXT: custom_cardtext,
            GameTag.CARDTEXT_ENTITY_0: cardtext_entity_0,
        }

        cardscript = db[name]
        player_tag_threshold_tag_id = cardscript.tags[
            GameTag.PLAYER_TAG_THRESHOLD_TAG_ID
        ]
        player_tag_threshold_value = cardscript.tags[GameTag.PLAYER_TAG_THRESHOLD_VALUE]
        powered_up = (
            Attr(CONTROLLER, player_tag_threshold_tag_id) >= player_tag_threshold_value
        )

        namespace["custom_cardtext"] = custom_cardtext
        namespace["cardtext_entity_0"] = cardtext_entity_0
        namespace["tags"] = tags
        namespace["powered_up"] = powered_up
        if "play" in namespace:
            namespace["play"] = powered_up & namespace["play"]
        return super().__new__(cls, name, bases, namespace)


class QuestRewardProtect:
    def finished(self):
        return (
            self.progress_total > 0
            and self.progress >= self.progress_total
            and len(self.controller.hand) < self.controller.max_hand_size
        )
