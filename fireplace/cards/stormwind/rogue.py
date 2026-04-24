from ..utils import *

##
# Minions


class SW_411:
    """SI:7 Informant"""

    # <b>Battlecry:</b> Gain +1/+1 for each SI:7 card you've played this game.
    play = Buff(
        SELF,
        "SW_411e",
        atk=Count(CARDS_PLAYED_THIS_GAME + SI_7),
        max_health=Count(CARDS_PLAYED_THIS_GAME + SI_7),
    )


class SW_413:
    """SI:7 Operative"""

    # <b>Rush</b> After this attacks a minion, gain <b>Stealth</b>.
    events = Attack(SELF, MINION).after(Stealth(SELF))


class SW_417:
    """SI:7 Assassin"""

    # [x]Costs (1) less for each SI:7 card you've played this game.
    # <b>Combo:</b> Destroy an enemy minion.
    requirements = {
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + SI_7)
    combo = Destroy(TARGET)


class SW_434:
    """Loan Shark"""

    # [x]<b>Battlecry:</b> Give your opponent a Coin. __<b>Deathrattle:</b> You
    # get two.
    play = Give(OPPONENT, THE_COIN)
    deathrattle = Give(CONTROLLER, THE_COIN) * 2


class SW_050:
    """Maestra of the Masquerade"""

    # You start the game as a different class until you play a Rogue card.
    class Hand:
        events = GameStart().on(Buff(CONTROLLER, "SW_050e"))

    class Deck:
        events = GameStart().on(Buff(CONTROLLER, "SW_050e"))


class SW_050e:
    events = Play(CONTROLLER, ROGUE).after(Summon(CONTROLLER, STARTING_HERO))


class DED_510:
    """Edwin, Defias Kingpin"""

    # [x]<b>Battlecry:</b> Draw a card. If you play it this turn, gain +2/+2
    # and repeat this effect.
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "DED_510e"))


class DED_510e:
    events = Play(CONTROLLER, OWNER).on(Buff(CREATOR, "DED_510e2"), Destroy(SELF))


DED_510e2 = buff(+2, +2)


##
# Spells


class SW_405:
    """Sketchy Information"""

    # [x]Draw a <b>Deathrattle</b> card that costs (4) or less. Trigger its
    # <b>Deathrattle.</b>
    play = ForceDraw(RANDOM(FRIENDLY_DECK + DEATHRATTLE + (COST <= 4))).then(
        Deathrattle(ForceDraw.TARGET)
    )


class SW_311:
    """Garrote"""

    # [x]Deal $2 damage to the enemy hero. Shuffle 2 Bleeds into your deck that
    # deal $2 more when drawn.
    play = Hit(ENEMY_HERO, 2), (Shuffle(CONTROLLER, "SW_311t") * 2)


class SW_311t:
    play = Hit(ENEMY_HERO, 2)


class SW_412:
    """SI:7 Extortion"""

    # <b>Tradeable</b> Deal $3 damage to an undamaged character.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_UNDAMAGED_TARGET: 0,
    }
    play = Hit(TARGET, 3)


class SW_052:
    """Find the Imposter"""

    # <b>Questline:</b> Play 2 SI:7 cards. <b>Reward:</b> Add a Spy Gizmo to
    # your hand.
    quest = Play(CONTROLLER, SI_7).on(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, RandomID(SPY_GIZMO)), Summon(CONTROLLER, "SW_052t")


class SW_052t:
    """Learn the Truth"""

    # <b>Questline:</b> Play 2 SI:7 cards. <b>Reward:</b> Add a Spy Gizmo to
    # your hand.
    quest = Play(CONTROLLER, SI_7).on(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, RandomID(SPY_GIZMO)), Summon(CONTROLLER, "SW_052t2")


class SW_052t2(QuestRewardProtect):
    """Marked a Traitor"""

    # <b>Questline:</b> Play 2 SI:7 cards. <b>Reward:</b> Spymaster Scabbs.
    quest = Play(CONTROLLER, SI_7).on(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "SW_052t3")


class SW_052t3:
    """Spymaster Scabbs"""

    # [x]<b>Battlecry:</b> Add one of each Spy Gizmo to your hand.
    play = Give(CONTROLLER, SPY_GIZMO)


class SW_052t4:
    """Fizzflash Distractor"""

    # [x]Return an enemy minion to its owner's hand. They can't play it next
    # turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Bounce(TARGET), Buff(TARGET, "SW_052t4e")


class SW_052t5:
    """Spy-o-matic"""

    # [x]<b>Battlecry:</b> Look at 3 cards in your opponent's deck. Pick one to
    # put on top.
    play = Choice(CONTROLLER, ENEMY_DECK[-3:]).then(PutOnTop(OPPONENT, Choice.CARD))


class SW_052t6:
    """Noggen-Fog Generator"""

    # Give a minion +2 Attack and <b>Stealth</b>.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "SW_052t6e"), Stealth(TARGET)


class SW_052t7:
    """Hidden Gyroblade"""

    # <b>Deathrattle:</b> Throw this at a random enemy minion.
    deathrattle = Hit(RANDOM_ENEMY_MINION, ATK(SELF))


class SW_052t4e:
    """Distracted"""

    # Can't be played.
    tags = {GameTag.CANT_PLAY: True}
    events = OWN_TURN_END.on(Destroy(SELF))


class SW_052t8_t:
    """Undercover Mole"""

    # [x]<b>Stealth</b>. After this attacks, add a random card to your hand
    # <i>(from your opponent's class).</i>
    events = Attack(SELF).after(
        Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))
    )


SW_052t6e = buff(atk=2)


class DED_005:
    """Parrrley"""

    # Swap this for a card in your opponent's deck.
    play = Swap(SELF, RANDOM(ENEMY_DECK + MINION))


##
# Weapons


class SW_310:
    """Counterfeit Blade"""

    # [x]<b>Battlecry:</b> Gain a random friendly <b>Deathrattle</b> that
    # _triggered this game.
    play = CopyDeathrattleBuff(
        RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE), "SW_310e"
    )


class DED_004:
    """Blackwater Cutlass"""

    # [x]<b>Tradeable</b> After you <b>Trade</b> this, reduce the cost of a
    # spell in your hand by (1).
    trade = Buff(RANDOM(FRIENDLY_HAND + SPELL), "DED_004e")


class DED_004e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY
