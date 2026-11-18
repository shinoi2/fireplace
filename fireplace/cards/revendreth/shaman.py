from ..utils import *

##
# Minions


class REV_921:
    """The Stonewright"""

    # <b>Battlecry:</b> For the rest of the game, your Totems have +2 Attack.
    play = Buff(CONTROLLER, "REV_921e")


class REV_925:
    """Baroness Vashj"""

    # [x]If this would transform into a minion, summon that minion instead.
    summon_instead_of_transform = True


class MAW_005:
    """Framester"""

    # [x]<b>Battlecry:</b> Shuffle 3 'Framed' cards into the opponent's deck.
    # When drawn, they <b>Overload</b> for (2).
    play = Shuffle(OPPONENT, "MAW_005t") * 3


class REV_935:
    """Party Favor Totem"""

    # [x]At the end of your turn, summon a random basic Totem. <b>Infuse
    # (@):</b> Summon two instead.
    infuse_card = "REV_935t"
    events = OWN_TURN_END.on(Summon(CONTROLLER, RandomBasicTotem()))


class REV_936:
    """Crud Caretaker"""

    # <b>Battlecry</b>: Summon a 3/5 Elemental with <b>Taunt</b>.
    play = Summon(CONTROLLER, "REV_936t")


class REV_838:
    """Gigantotem"""

    # Costs (1) less for each Totem you've summoned this game.
    cost_mod = -Attr(CONTROLLER, "times_totem_summoned_this_game")


class MAW_030:
    """Torghast Custodian"""

    # [x]<b>Battlecry:</b> For each enemy minion, randomly gain <b>Rush</b>,
    # <b>Divine Shield</b>, or <b>Windfury</b>.
    def play(self):
        yield from gain_keywords(
            self,
            len(ENEMY_MINIONS.eval(self.game, self)),
            [GameTag.RUSH, GameTag.DIVINE_SHIELD, GameTag.WINDFURY],
        )


##
# Spells


class REV_920:
    """Convincing Disguise"""

    # [x]Transform a friendly minion into one that costs (2) more. <b>Infuse
    # (@):</b> Transform all friendly minions instead.
    requirements = FRIENDLY_MINION_TARGET
    infuse_card = "REV_920t"
    play = Evolve(TARGET, 2)


class REV_924:
    """Primordial Wave"""

    # [x]Transform enemy minions into ones that cost (1) less and friendly
    # minions into ones that cost (1) more.
    play = Evolve(ENEMY_MINIONS, -1), Evolve(FRIENDLY_MINIONS, 1)


class REV_517:
    """Criminal Lineup"""

    # [x]Choose a friendly minion. Summon 3 copies of it. <b>Overload:</b> (2)
    requirements = FRIENDLY_MINION_TARGET
    play = Summon(CONTROLLER, ExactCopy(TARGET)) * 3


class MAW_003:
    """Totemic Evidence"""

    # Choose a basic Totem and summon it. <b>Infuse (@ Totems):</b> Summon all
    # 4 instead.
    infuse_card = "MAW_003t"
    infuse_race = Race.TOTEM
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Choice(CONTROLLER, BASIC_TOTEMS).then(Summon(CONTROLLER, Choice.CARD))


##
# Weapons


class REV_917:
    """Carving Chisel"""

    # After your hero attacks, summon a random basic Totem.
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, RandomBasicTotem()))


##
# Locations


class REV_923:
    """Muck Pools"""

    # Transform a friendly minion into one that costs (1) more.
    requirements = FRIENDLY_MINION_TARGET
    activate = Evolve(TARGET, 1)


class REV_921e:
    update = Refresh(FRIENDLY_MINIONS + TOTEM, {GameTag.ATK: 2})


class REV_935t:
    events = OWN_TURN_END.on(Summon(CONTROLLER, RandomBasicTotem()) * 2)


class REV_920t:
    requirements = {PlayReq.REQ_MINIMUM_TOTAL_MINIONS: 1}
    play = Evolve(FRIENDLY_MINIONS, 2)


class MAW_003t:
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, BASIC_TOTEMS)


class MAW_005t:
    # The Overload tag is handled by Battlecry when this is cast on draw.
    tags = {GameTag.CASTSWHENDRAWN: True}
