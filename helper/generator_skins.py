#!/usr/bin/env python
import argparse
import os
import sys
import textwrap

from hearthstone.enums import CardClass, CardSet, CardType, GameTag, Rarity
from fireplace.cards.utils import BASIC_HERO_POWERS
from hearthstone import cardxml
from utils import *

from fireplace import cards


def generate_basic_hero_power(hero: cardxml.CardXML, card: cardxml.CardXML):
    tab = " " * 4
    str = ""
    str += "\n\n"
    basic_hero = hero.card_class.default_hero
    str += f"class {card.id}({basic_hero}bp):\n"
    str += f'{tab}"""{card.name} ({hero.name})"""\n'
    str += "\n"
    str += f"{tab}pass\n"
    return str


def generate_upgraded_hero_power(hero: cardxml.CardXML, card: cardxml.CardXML):
    tab = " " * 4
    str = ""
    str += "\n\n"
    basic_hero = hero.card_class.default_hero
    str += f"class {card.id}({basic_hero}bp2):\n"
    str += f'{tab}"""{card.name} ({hero.name})"""\n'
    str += "\n"
    str += f"{tab}pass\n"
    return str


def main():
    output_dir = "./fireplace/cards/skins"
    card_set = CardSet.HERO_SKINS

    os.makedirs(output_dir, exist_ok=True)

    kws = [
        {"card_class": CardClass.DEMONHUNTER},
        {"card_class": CardClass.DRUID},
        {"card_class": CardClass.HUNTER},
        {"card_class": CardClass.MAGE},
        {"card_class": CardClass.PALADIN},
        {"card_class": CardClass.PRIEST},
        {"card_class": CardClass.ROGUE},
        {"card_class": CardClass.SHAMAN},
        {"card_class": CardClass.WARLOCK},
        {"card_class": CardClass.WARRIOR},
    ]
    for kw in kws:
        card_class = kw["card_class"]
        filename = output_dir + "/" + card_class.name.lower() + ".py"

        with open(filename, "w") as out:
            out.write("from .basic import *\n")
            ids = cards.filter(
                card_set=card_set,
                collectible=True,
                include_default_hero=True,
                **kw,
            )
            out.write("\n\n")
            out.write("##\n")
            out.write("# Hero Powers\n")
            for id in ids:
                if id != card_class.default_hero:
                    hero = cards.db[id]
                    hero_power_id = hero.hero_power
                    hero_power = cards.db[hero_power_id]
                    out.write(generate_basic_hero_power(hero, hero_power))
            out.write("\n\n")
            out.write("##\n")
            out.write("# Upgraded Hero Powers\n")
            for id in ids:
                if id != card_class.default_hero:
                    hero = cards.db[id]
                    hero_power_id = hero.hero_power
                    hero_power = cards.db[hero_power_id]
                    upgraded_hero_power_id = cards.db.dbf[
                        hero_power.tags[GameTag.UPGRADED_HERO_POWER]
                    ]
                    upgraded_hero_power = cards.db[upgraded_hero_power_id]
                    out.write(generate_upgraded_hero_power(hero, upgraded_hero_power))


if __name__ == "__main__":
    main()
