from ..utils import *


##
# Minions

class AT_038:
	"""Darnassus Aspirant"""
	play = GainEmptyMana(CONTROLLER, 1)
	deathrattle = GainMana(CONTROLLER, -1)


class AT_039:
	"""Savage Combatant"""
	inspire = Buff(FRIENDLY_HERO, "AT_039e")


AT_039e = buff(atk=2)


class AT_040:
	"""Wildwalker"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 20}
	play = Buff(TARGET, "AT_040e")


AT_040e = buff(health=3)


class AT_041:
	"""Knight of the Wild"""
	class Hand:
		events = Summon(CONTROLLER, BEAST).on(Buff(SELF, "AT_041e"))


class AT_041e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -1}


class AT_042:
	"""Druid of the Saber"""
	choose = ("AT_042a", "AT_042b")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "OG_044c")


class AT_042a:
	play = Morph(SELF, "AT_042t")


class AT_042b:
	play = Morph(SELF, "AT_042t2")


class AT_045:
	"""Aviana"""
	update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: SET(1)})


##
# Spells

class AT_037:
	"""Living Roots"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	choose = ("AT_037a", "AT_037b")
	play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Summon(CONTROLLER, "AT_037t") * 2)


class AT_037a:
	play = Hit(TARGET, 2)
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}


class AT_037b:
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	play = Summon(CONTROLLER, "AT_037t") * 2


class AT_043:
	"""Astral Communion"""
	play = Discard(FRIENDLY_HAND), (
		AT_MAX_MANA(CONTROLLER) &
		Give(CONTROLLER, "CS2_013t") |
		GainMana(CONTROLLER, 10)
	)


class AT_044:
	"""Mulch"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Destroy(TARGET), Give(OPPONENT, RandomMinion())
