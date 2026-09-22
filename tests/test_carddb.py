import utils
import pytest
from hearthstone.enums import CardType, GameTag, Rarity

CARDS = utils.fireplace.cards.db


# def test_all_tags_known():
#     """
#     Iterate through the card database and check that all specified GameTags
#     are known in hearthstone.enums.GameTag
#     """
#     unknown_tags = set()
#     known_tags = list(GameTag)
#     known_rarities = list(Rarity)
#
#     # Check the db loaded correctly
#     assert utils.fireplace.cards.db
#
#     for card in CARDS.values():
#         for tag in card.tags:
#             # We have fake tags in fireplace.enums which are always negative
#             if tag not in known_tags and tag > 0:
#                 unknown_tags.add(tag)
#
#         # Test rarities as well (cf. TB_BlingBrawl_Blade1e in 10956...)
#         assert card.rarity in known_rarities
#
#     assert not unknown_tags


def test_play_scripts():
    for card in CARDS.values():
        if card.scripts.activate:
            assert card.type in (CardType.HERO_POWER, CardType.SPELL, CardType.MINION)
        elif card.scripts.play:
            assert card.type not in (CardType.HERO_POWER, CardType.ENCHANTMENT)


def test_battlecry_scripts():
    for card in CARDS.values():
        if card.battlecry and card.collectible:
            if card.id in ["DRG_308", "GIL_614", "ULD_003"]:
                continue
            assert card.scripts.play


def test_deathrattle_scripts():
    for card in CARDS.values():
        if card.deathrattle and card.collectible:
            if card.id in [
                "BOT_558",
                "DRG_086",
                "ULD_163",
                "UNG_953",
                "BT_126",
                "SCH_714",
                "SW_069",
            ]:
                continue
            assert card.scripts.deathrattle


def test_card_docstrings():
    for card in CARDS.values():
        if card.locale != "enUS":
            continue
        c = utils.fireplace.cards.get_script_definition(card.id)
        name = c.__doc__
        if name is not None:
            if name.endswith(")"):
                continue
            if GameTag.DECK_RULE_COUNT_AS_COPY_OF_CARD_ID in card.tags:
                continue
            if name != card.name:
                assert name == card.name


def test_card_id():
    import os
    import re

    # 正则匹配 卡牌ID格式
    pattern = re.compile(r"\"[A-Z]{2,3}_[0-9]{3,4}[a-z0-9]*\"")
    # 匹配 cards 目录内所有文件, 找出所有的卡牌 ID
    card_ids = []  # 用于存储所有匹配的卡牌 ID
    for root, dirs, files in os.walk("fireplace/cards"):
        if root.endswith("debug"):
            continue
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        matches = pattern.findall(line)
                        for match in matches:
                            card_ids.append(match[1:-1])
    for card_id in card_ids:
        assert card_id in CARDS
