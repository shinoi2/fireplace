from ..utils import *

##
# Minions


class REV_960:
    """Ashen Elemental"""

    # [x]<b>Battlecry:</b> Whenever your opponent draws a card next turn, they
    # take 2 damage.
    play = Buff(OPPONENT, "REV_960e")


class REV_960e:
    events = (
        Draw(OPPONENT).on(Find(CURRENT_PLAYER + OPPONENT) & Hit(ENEMY_HERO, 2)),
        EndTurn(OPPONENT).on(Destroy(SELF)),
    )


class REV_370:
    """Party Crasher"""

    # [x]<b>Battlecry:</b> Choose an enemy minion. Throw a random minion from
    # your hand at it.
    requirements = ENEMY_MINION_BATTLECRY
    play = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION)).then(
        Attack(Summon.CARD, TARGET)
    )


class REV_017:
    """Insatiable Devourer"""

    # [x]<b>Battlecry:</b> Devour an enemy minion and gain its stats.
    # _<b>Infuse (@):</b> And its neighbors.
    requirements = ENEMY_MINION_BATTLECRY
    infuse_card = "REV_017t"

    def play(self):
        if self.target:
            yield Buff(
                SELF, "REV_017e", atk=self.target.atk, max_health=self.target.health
            )
            yield Destroy(TARGET)


class MAW_032:
    """Tight-Lipped Witness"""

    # <b>Secrets</b> can't be revealed.
    update = Refresh(ALL_PLAYERS, {enums.CANT_REVEAL_SECRETS: True})


class REV_843:
    """Sinfueled Golem"""

    # <b>Infuse (@):</b> Gain stats equal to the Attack of the minions that
    # <b>Infused</b> this.
    infuse_card = "REV_843t"

    def on_infuse(self, minion):
        self.data_num_2 += minion.atk
        if self.infuse >= self.data_num_1:
            yield Buff(
                SELF, "REV_843e", atk=self.data_num_2, max_health=self.data_num_2
            )


class REV_023:
    """Demolition Renovator"""

    # <b>Battlecry:</b> Destroy an enemy location.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_LOCATION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Destroy(TARGET)


REV_017e = buff()
REV_843e = buff()


class REV_017t:
    requirements = ENEMY_MINION_BATTLECRY

    def play(self):
        if self.target:
            targets = (TARGET | ADJACENT(TARGET)).eval(self.game, self)
            yield Buff(
                SELF,
                "REV_017e",
                atk=sum(c.atk for c in targets),
                max_health=sum(c.health for c in targets),
            )
            yield Destroy(targets)
