from ..utils import *


##
# Minions

class OG_096:
	"""Twilight Darkmender"""
	play = CHECK_CTHUN & Heal(FRIENDLY_HERO, 10)


class OG_334:
	"""Hooded Acolyte"""
	events = Heal(ALL_CHARACTERS).on(Buff(CTHUN, "OG_281e", atk=1, max_health=1))


class OG_234:
	"""Darkshire Alchemist"""
	requirements = {PlayReq.REQ_NONSELF_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Heal(TARGET, 5)


class OG_335:
	"""Shifting Shade"""
	deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


class OG_316:
	"""Herald Volazj"""
	play = Summon(CONTROLLER, ExactCopy(FRIENDLY_MINIONS - SELF)).then(
		Buff(Summon.CARD, "OG_316k"))


class OG_316k:
	atk = SET(1)
	max_health = SET(1)


##
# Spells

class OG_104:
	"""Embrace the Shadow"""
	play = Buff(CONTROLLER, "OG_104e")


class OG_104e:
	update = Refresh(CONTROLLER, {
		GameTag.EMBRACE_THE_SHADOW: True,
	})


class OG_094:
	"""Power Word: Tentacles"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "OG_094e")


OG_094e = buff(+2, +6)


class OG_100:
	"""Shadow Word: Horror"""
	play = Destroy(ALL_MINIONS + (ATK <= 2))


class OG_101:
	"""Forbidden Shaping"""
	play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)).then(
		Summon(CONTROLLER, RandomMinion(cost=SpendMana.AMOUNT))
	)
