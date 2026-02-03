from ..utils import *

##
# Minions


class DMF_074:
    """Silas Darkmoon"""

    # <b>Battlecry:</b> Choose a direction to rotate all minions.
    # TODO: need to be tested
    play = Choice(CONTROLLER, ["DMF_074a", "DMF_074b"]).then(
        Battlecry(Choice.CARD, None)
    )


class DMF_074e:
    def play(self):
        # "This Way" rotates clockwise (your minions move left, your opponent's minions move right).
        left_my_minion = LEFTMOST(FRIENDLY_MINIONS).eval(self.game, self)
        right_op_minion = RIGHTMOST(ENEMY_MINIONS).eval(self.game, self)
        for minion in left_my_minion:
            minion._summon_index = 0
        for minion in right_op_minion:
            minion._summon_index = -1
        yield Steal(left_my_minion, self.controller.opponent)
        yield Steal(right_op_minion, self.controller)


class DMF_074b:
    def play(self):
        # "That Way" rotates counter-clockwise (your minions move right, your opponent's minions move left).
        right_my_minion = RIGHTMOST(FRIENDLY_MINIONS).eval(self.game, self)
        left_op_minion = LEFTMOST(ENEMY_MINIONS).eval(self.game, self)
        for minion in right_my_minion:
            minion._summon_index = -1
        for minion in left_op_minion:
            minion._summon_index = 0
        yield Steal(right_my_minion, self.controller.opponent)
        yield Steal(left_op_minion, self.controller)


class DMF_002:
    """N'Zoth, God of the Deep"""

    # <b>Battlecry:</b> Resurrect a friendly minion of each minion type.
    play = Summon(CONTROLLER, UniqueRace(FRIENDLY + KILLED + MINION))


class DMF_004(ThresholdUtils):
    """Yogg-Saron, Master of Fate"""

    # [x]<b>Battlecry:</b> If you've cast 10 spells this game, spin the Wheel
    # of Yogg-Saron.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
    entourage = [
        "DMF_004t1",
        "DMF_004t2",
        "DMF_004t3",
        "DMF_004t4",
        "DMF_004t5",
        "DMF_004t6",
    ]
    play = ThresholdUtils.powered_up & Battlecry(RandomEntourage(), None)


class DMF_004t1:
    """Mysterybox"""

    # Cast a random spell for every spell you've cast this game <i>(targets
    # chosen randomly)</i>.
    play = CastSpell(RandomSpell()) * TIMES_SPELL_PLAYED_THIS_GAME


class DMF_004t2:
    """Hand of Fate"""

    # Fill your hand with random spells. They cost (0) this turn.
    play = Give(CONTROLLER, RandomSpell()).then(Buff(Give.CARD, "DMF_004t1e")) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class DMF_004t1e:
    cost = SET(0)
    events = REMOVED_IN_PLAY


class DMF_004t3:
    """Curse of Flesh"""

    # Fill the board with random minions, then give yours <b>Rush</b>.
    play = Summon(CONTROLLER, RandomMinion()).then(
        GiveRush(Summon.CARD)
    ) * MINION_SLOTS(CONTROLLER)


class DMF_004t4:
    """Mindflayer Goggles"""

    # Take control of three random enemy minions.
    play = Steal(RANDOM_ENEMY_MINION * 3)


class DMF_004t5:
    """Devouring Hunger"""

    # Destroy all other minions. Gain their Attack and Health.
    play = (
        Buff(
            SELF,
            "DMF_004t5e",
            atk=ATK(ALL_MINIONS - SELF),
            max_health=CURRENT_HEALTH(ALL_MINIONS - SELF),
        ),
        Destroy(ALL_MINIONS - SELF),
    )


class DMF_004t6:
    """Rod of Roasting"""

    # Cast 'Pyroblast' randomly until a hero dies.
    def play(self):
        hero1 = self.controller.hero
        hero2 = self.controller.opponent.hero
        while not hero1.dead and not hero2.dead:
            yield CastSpell("EX1_279")


class DMF_188:
    """Y'Shaarj, the Defiler"""

    # [x]<b>Battlecry:</b> Add a copy of each <b>Corrupted</b> card you've
    # played this game to your hand. They cost (0) this turn.
    play = Give(
        CONTROLLER, SHUFFLE(FRIENDLY + CARDS_PLAYED_THIS_GAME + CORRUPTED_CARD)
    ).then(Buff(Give.CARD, "DMF_188e"))


class DMF_188e:
    cost = SET(0)
    events = REMOVED_IN_PLAY


class DMF_254:
    """C'Thun, the Shattered"""

    # [x]<b>Start of Game:</b> Break into pieces. <b>Battlecry:</b> Deal 30
    # damage randomly split among all enemies.
    class Deck:
        events = GameStart().on(
            Remove(SELF),
            Shuffle(CONTROLLER, ["DMF_254t3", "DMF_254t4", "DMF_254t5", "DMF_254t7"]),
        )

    progress_total = 4
    reward = Shuffle(CONTROLLER, SELF)
    play = Hit(RANDOM_ENEMY_CHARACTER, 1) * 30

    def progress(self):
        if not hasattr(self, "cthun_pieces"):
            self.cthun_pieces = set()
        return len(self.cthun_pieces)

    def add_progress(self, card):
        if not hasattr(self, "cthun_pieces"):
            self.cthun_pieces = set()
        self.cthun_pieces.add(card)


class DMF_254t3:
    """Eye of C'Thun"""

    # [x]<b>Piece_of_C'Thun_(@/4)</b> Deal $7 damage randomly split among all
    # enemies.
    play = (
        Hit(RANDOM_ENEMY_CHARACTER, 1) * 7,
        AddProgress(CREATOR, SELF),
    )


class DMF_254t4:
    """Heart of C'Thun"""

    # <b>Piece of C'Thun (@/4)</b> Deal $3 damage to all minions.
    play = (
        Hit(ALL_MINIONS, 1) * 7,
        AddProgress(CREATOR, SELF),
    )


class DMF_254t5:
    """Body of C'Thun"""

    # [x]<b>Piece of C'Thun (@/4)</b> Summon a 6/6 C'Thun's Body with
    # <b>Taunt</b>.
    play = (
        Summon(CONTROLLER, "DMF_254t5t"),
        AddProgress(CREATOR, SELF),
    )


class DMF_254t7:
    """Maw of C'Thun"""

    # <b>Piece of C'Thun (@/4)</b> Destroy a minion.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = (
        Destroy(TARGET),
        AddProgress(CREATOR, SELF),
    )


class YOP_035:
    """Moonfang"""

    # Can only take 1 damage at_a time.
    update = Refresh(SELF, {GameTag.HEAVILY_ARMORED: True})
