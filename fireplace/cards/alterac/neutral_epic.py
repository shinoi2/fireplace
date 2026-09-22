from ..utils import *

##
# Minions


class AV_102:
    """Popsicooler"""

    # [x]<b>Deathrattle:</b> <b>Freeze</b> two random enemy minions.
    deathrattle = Freeze(RANDOM_ENEMY_MINION * 2)


class AV_222:
    """Spammy Arcanist"""

    # [x]<b>Battlecry:</b> Deal 1 damage to all other minions. If any die,
    # repeat this.
    def play(self):
        yield Hit(ALL_MINIONS - SELF, 1)
        for _ in range(13):
            if Dead(ALL_MINIONS - SELF).check(self):
                yield Deaths()
                yield Hit(ALL_MINIONS - SELF, 1)
            else:
                break


class AV_128:
    """Frozen Mammoth"""

    # This is <b>Frozen</b> until you cast a Fire spell.
    update = Find(APPLIED_BUFFS + ID("AV_128e")) | Refresh(SELF, {GameTag.FROZEN: True})
    events = Play(CONTROLLER, FIRE).after(Buff(SELF, "AV_128e"))


class AV_138:
    """Grimtotem Bounty Hunter"""

    # <b>Battlecry:</b> Destroy an enemy <b>Legendary</b> minion.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_LEGENDARY_TARGET: 0,
    }
    play = Destroy(TARGET)


class AV_139:
    """Abominable Lieutenant"""

    # At the end of your turn, eat a random enemy minion and gain its stats.
    events = OWN_TURN_END.after(
        Destroy(RANDOM_ENEMY_MINION).then(
            Buff(
                SELF,
                "AV_139e",
                atk=ATK(Destroy.TARGET),
                max_health=CURRENT_HEALTH(Destroy.TARGET),
            )
        )
    )


class ONY_003:
    """Whelp Bonker"""

    # <b>Frenzy and Honorable Kill:</b> Draw a card.
    frenzy = honorable_kill = Draw(CONTROLLER)
