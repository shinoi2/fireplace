from ..utils import *

##
# Minions


class REV_947:
    """Muckborn Servant"""

    # <b>Taunt</b> <b>Battlecry:</b> <b>Discover</b> a Paladin card.
    play = DISCOVER(RandomCollectible(card_class=CardClass.PALADIN))


class REV_951:
    """The Countess"""

    # [x]<b>Battlecry:</b> If your deck has no Neutral cards, add 3
    # <b>Legendary </b>Invitations to your hand.
    play = Find(FRIENDLY_DECK + NEUTRAL) | (Give(CONTROLLER, "REV_951t") * 3)


class REV_952:
    """Sinful Sous Chef"""

    # <b>Deathrattle:</b> Add 2 Silver Hand Recruits to your hand.
    deathrattle = Give(CONTROLLER, "CS2_101t") * 2


class REV_955:
    """Stewart the Steward"""

    # [x]<b>Deathrattle:</b> Give the next Silver Hand Recruit you summon +3/+3
    # and this <b>Deathrattle</b>.
    deathrattle = Buff(CONTROLLER, "REV_955e")


class REV_958:
    """Buffet Biggun"""

    # [x]<b>Battlecry:</b> Summon two Silver Hand Recruits. <b>Infuse (@):</b>
    # Give them +2 Attack and <b>Divine Shield</b>.
    infuse_card = "REV_958t"
    play = Summon(CONTROLLER, "CS2_101t") * 2


class REV_961:
    """Elitist Snob"""

    # [x]<b>Battlecry:</b> For each Paladin card in your hand, randomly gain
    # <b>Divine Shield</b>, <b>Lifesteal</b>, <b>Rush</b>, or <b>Taunt</b>.
    def play(self):
        yield from gain_keywords(
            self,
            len([c for c in self.controller.hand if CardClass.PALADIN in c.classes]),
            [GameTag.DIVINE_SHIELD, GameTag.LIFESTEAL, GameTag.RUSH, GameTag.TAUNT],
        )


class MAW_017:
    """Class Action Lawyer"""

    # [x]<b>Battlecry:</b> If your deck has no Neutral cards, set _a minion's
    # stats to 1/1.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_MINION_TARGET: 0}
    powered_up = -Find(FRIENDLY_DECK + NEUTRAL)
    play = powered_up & SetStats(TARGET, "MAW_017e", 1, 1)


##
# Spells


class REV_948:
    """Service Bell"""

    # <b>Discover</b> a Class card from your deck and draw all copies of it.
    play = Choice(CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK - NEUTRAL), 3)).then(
        ForceDraw(FRIENDLY_DECK + SameId(Choice.CARD))
    )


class REV_950:
    """Divine Toll"""

    # [x]Shoot 5 rays at random minions. They give friendly minions +2/+2, and
    # deal $2 damage to enemy minions.
    def play(self):
        for _ in range(5):
            targets = ALL_MINIONS.eval(self.game, self)
            if targets:
                target = self.game.random.choice(targets)
                if target.controller is self.controller:
                    yield Buff(target, "REV_950e")
                else:
                    yield Hit(target, 2)
                yield Deaths()


class MAW_016:
    """Order in the Court"""

    # [x]Reorder your deck from highest Cost to lowest Cost. Draw a card.
    def play(self):
        # The top of a deck is the last element.
        self.controller.deck.sort(key=lambda card: card.cost)
        yield Draw(CONTROLLER)


class MAW_015:
    """Jury Duty"""

    # [x]Summon two Silver Hand Recruits. Give your Silver Hand Recruits +1/+1.
    play = Summon(CONTROLLER, "CS2_101t") * 2, Buff(
        FRIENDLY_MINIONS + ID("CS2_101t"), "MAW_015e"
    )


class REV_842:
    """Promotion"""

    # [x]Give a Silver Hand Recruit +3/+3 and <b>Taunt</b>.
    requirements = dict(FRIENDLY_MINION_TARGET)
    requirements[PlayReq.REQ_TARGET_SILVER_HAND_RECRUIT] = 0
    play = Buff(TARGET, "REV_842e")


##
# Locations


class REV_983:
    """Great Hall"""

    # Set a minion's Attack and Health to 3.
    requirements = MINION_TARGET
    activate = SetStats(TARGET, "REV_983e", 3, 3)


def own_class_cards(entities, source):
    own_class = source.controller.hero.card_class
    result = []
    for id, card in db.items():
        group = card.tags.get(GameTag.MULTI_CLASS_GROUP, MultiClassGroup.INVALID)
        classes = MultiClassGroup(group).card_classes if group else [card.card_class]
        if own_class in classes:
            result.append(id)
    return result


OWN_CLASS_CARDS = FuncSelector(own_class_cards)


class REV_951t:
    play = Discover(
        CONTROLLER,
        RandomMinion(
            rarity=Rarity.LEGENDARY, card_class=ANOTHER_CLASS, exclude=OWN_CLASS_CARDS
        ),
    ).then(Give(CONTROLLER, Discover.CARD), Buff(Discover.CARD, "REV_951e"))


class REV_951e:
    cost = SET(0)
    events = REMOVED_IN_PLAY


class REV_955e:
    events = Summon(CONTROLLER, ID("CS2_101t")).after(
        Buff(Summon.CARD, "REV_955e2"), Destroy(SELF)
    )


class REV_955e2:
    tags = {GameTag.ATK: 3, GameTag.HEALTH: 3, GameTag.DEATHRATTLE: True}
    deathrattle = Buff(CONTROLLER, "REV_955e")


class REV_958t:
    play = Summon(CONTROLLER, "CS2_101t").then(Buff(Summon.CARD, "REV_958e")) * 2


REV_958e = buff(atk=2, divine_shield=True)
REV_950e = buff(+2, +2)
MAW_015e = buff(+1, +1)
REV_842e = buff(+3, +3, taunt=True)
MAW_017e = FixedStats
REV_983e = FixedStats
