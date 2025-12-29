from ..utils import *


##
# Minions


class DMF_074:
    """Silas Darkmoon"""

    # <b>Battlecry:</b> Choose a direction to rotate all minions.
    # TODO: need to be tested
    play = Choice(CONTROLLER, ["DMF_074a", "DMF_074b"]).then(Battlecry(Choice.CARD, None))


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
