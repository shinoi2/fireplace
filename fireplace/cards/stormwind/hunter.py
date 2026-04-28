from ..utils import *

##
# Minions


class SW_455:
    """Rodent Nest"""

    # <b>Deathrattle:</b> Summon five 1/1 Rats.
    deathrattle = Summon(CONTROLLER, "SW_455t") * 5


class SW_459:
    """Stormwind Piper"""

    # After this minion attacks, give your Beasts +1/+1.
    events = Attack(SELF).after(Buff(FRIENDLY_MINIONS + BEAST, "SW_459e"))


SW_459e = buff(+1, +1)


class SW_323:
    """The Rat King"""

    # [x]<b>Rush</b>. <b>Deathrattle:</b> Go <b>Dormant</b>. Revive after 5
    # friendly minions die.
    deathrattle = Summon(CONTROLLER, "SW_323").then(
        SetTag(Buff(Summon.CARD, "SW_323e"), GameTag.DORMANT)
    )


class SW_323e:
    progress_total = 5
    dormant_events = Death(FRIENDLY_MINIONS).after(AddProgress(SELF, Death.ENTITY))
    reward = Awaken(OWNER), Destroy(SELF)


class SW_463:
    """Imported Tarantula"""

    # [x]<b>Tradeable</b> <b>Deathrattle:</b> Summon two 1/1 Spiders with
    # <b>Poisonous</b> and <b>Rush</b>.
    deathrattle = Summon(CONTROLLER, "SW_463t") * 2


class DED_007:
    """Defias Blastfisher"""

    # [x]<b>Battlecry:</b> Deal 2 damage to a random enemy. Repeat for each of
    # your Beasts.
    play = Hit(RANDOM_ENEMY_CHARACTER, 2) * (Count(FRIENDLY_MINIONS + BEAST) + 1)


class DED_008:
    """Monstrous Parrot"""

    # [x]<b>Battlecry:</b> Repeat the last friendly <b>Deathrattle</b> that
    # triggered.
    play = Deathrattle((FRIENDLY + KILLED + MINION + DEATHRATTLE)[-1:])


##
# Spells


class SW_320:
    """Rats of Extraordinary Size"""

    # [x]Summon seven 1/1 Rats. Any that can't fit on the battlefield go to
    # your hand with +4/+4.
    def play(self):
        minion_slots = self.controller.minion_slots
        yield Summon(CONTROLLER, "SW_455t") * minion_slots
        yield Give(CONTROLLER, "SW_455t").then(Buff(Give.CARD, "SW_320e")) * (
            7 - minion_slots
        )


SW_320e = buff(+4, +4)


class SW_321:
    """Aimed Shot"""

    # Deal $3 damage. Your next Hero Power deals 2 more damage.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Buff(CONTROLLER, "SW_321e")


class SW_321e:
    tags = {GameTag.HEROPOWER_DAMAGE: 2}
    events = Activate(FRIENDLY_HERO_POWER).after(Destroy(SELF))


class SW_322:
    """Defend the Dwarven District"""

    # <b>Questline:</b> Deal damage with 2 spells. <b>Reward:</b> Your Hero
    # Power can target minions.
    events = Damage(FRIENDLY + SPELL).after(AddProgress(SELF))
    reward = Buff(CONTROLLER, "SW_322e3")


class SW_322e3:
    """Crackshot"""

    # Your Hero Power Can Target Minions
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.STEADY_SHOT_CAN_TARGET: True})


class SW_322t:
    """Take the High Ground"""

    # [x]<b>Questline:</b> Deal damage with 2 spells. <b>Reward:</b> Set the
    # Cost of your Hero Power to (0).
    events = Damage(FRIENDLY + SPELL).after(AddProgress(SELF))
    reward = Buff(CONTROLLER, "SW_322e")


class SW_322e:
    update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})


class SW_322t2(QuestRewardProtect):
    """Knock 'Em Down"""

    # [x]<b>Questline:</b> Deal damage with 2 spells. <b>Reward:</b> Tavish,
    # Master Marksman.
    events = Damage(FRIENDLY + SPELL).after(AddProgress(SELF))
    reward = Give(CONTROLLER, "SW_322t4")


class SW_322t4:
    """Tavish, Master Marksman"""

    # [x]<b>Battlecry:</b> For the rest of the game, spells you cast refresh
    # your Hero Power.
    play = Buff(CONTROLLER, "SW_322e2")


class SW_322e2:
    """Tavish Stormpike Enchant"""

    # [x]<b>Battlecry:</b> For the rest of the game, your spells refresh your
    # Hero Power.
    events = Play(CONTROLLER, SPELL).after(RefreshHeroPower(FRIENDLY_HERO_POWER))


class SW_458:
    """Ramming Mount"""

    # [x]Give a minion +2/+2 and <b>Immune</b> while attacking. When it dies,
    # summon a Ram.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "SW_458e")


class SW_458e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.IMMUNE_WHILE_ATTACKING: True,
        GameTag.DEATHRATTLE: True,
    }
    deathrattle = Summon(CONTROLLER, "SW_458t")


class SW_460:
    """Devouring Swarm"""

    # [x]Choose an enemy minion. Your minions attack it, then return any that
    # die to your hand.
    requirements = {
        PlayReq.REQ_ENEMY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }

    def play(self):
        target = self.target
        minions = FRIENDLY_MINIONS.eval(self.game, self)
        for minion in minions:
            if target.dead:
                break
            yield Attack(minion, target)
            if minion.dead:
                yield Give(CONTROLLER, minion.id)


class DED_009:
    """Doggie Biscuit"""

    # [x]<b>Tradeable</b> Give a minion +2/+3. After you <b>Trade</b> this,
    # give a friendly minion <b>Rush</b>.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "DED_009e")
    trade = GiveRush(RANDOM_FRIENDLY_MINION)


DED_009e = buff(+2, +3)


##
# Weapons


class SW_457:
    """Leatherworking Kit"""

    # [x]After three friendly Beasts die, draw a Beast and give it +1/+1. Lose
    # 1 Durability.
    progress_total = 3
    events = Death(FRIENDLY_MINIONS + BEAST).after(AddProgress(SELF))
    reward = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
        Buff(ForceDraw.TARGET, "SW_457e"), Hit(SELF, 1)
    )


SW_457e = buff(+1, +1)
