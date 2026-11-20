from ..utils import *

random_outcast = RandomCollectible(outcast=True)

##
# Minions


class RLK_207:
    """Fierce Outsider"""

    # <b>Rush</b> <b>Outcast:</b> Your next <b>Outcast</b> card costs (1) less.
    outcast = Buff(CONTROLLER, "RLK_207e")


class RLK_210:
    """Wretched Exile"""

    # [x]After you play an <b>Outcast</b> card, add a random <b>Outcast</b>
    # card to your hand.
    events = Play(CONTROLLER, OUTCAST).after(Give(CONTROLLER, random_outcast))


class RLK_212:
    """Brutal Annihilan"""

    # [x]<b>Taunt</b>, <b>Rush</b> After this minion survives damage, deal that
    # amount to the enemy hero.
    events = SELF_DAMAGE.after(Find(SELF - DEAD) & Hit(ENEMY_HERO, Damage.AMOUNT))


class RLK_213:
    """Vengeful Walloper"""

    # <b>Rush</b>. Costs (1) less for each <b>Outcast</b> card you've played
    # this game.
    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + OUTCAST)


class RLK_215:
    """Felerin, the Forgotten"""

    # [x]<b>Battlecry:</b> Add a random <b>Outcast</b> card to the left and
    # right sides of your hand. They cost (2) less.
    def play(self):
        for left in (True, False):
            player = self.controller
            ids = random_outcast.evaluate(self)
            if ids and len(player.hand) < player.max_hand_size:
                card = player.card(ids[0], self)
                yield Buff(card, "RLK_834e")
                if left:
                    # Put the first card at the left edge before Give listeners resolve.
                    card._summon_index = 0
                yield Give(player, card)


class NX2_024:
    """Shambling Chow"""

    # <b>Rush</b> <b>Deathrattle:</b> Deal 4 damage to your hero.
    deathrattle = Hit(FRIENDLY_HERO, 4)


class NX2_026:
    """Felscale Evoker"""

    # [x]<b>Battlecry:</b> If you've cast three spells while holding this,
    # summon a different Demon from your deck.@ <i>({0} left!)</i>@
    # <i>(Ready!)</i>
    powered_up = Count(CARDS_PLAYED_WHEN_HOLDING + SPELL) >= 3
    play = powered_up & Summon(
        CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + DEMON - ID("NX2_026"))
    )


##
# Spells


class RLK_206:
    """Mark of Scorn"""

    # [x]Draw a card. If it's not a minion, deal $3 damage to the lowest Health
    # enemy.
    play = Draw(CONTROLLER).then(
        Find(Draw.CARD - MINION) & Hit(LOWEST_HEALTH(ENEMY_CHARACTERS - DEAD), 3)
    )


class RLK_208:
    """Fel'dorei Warband"""

    # Deal $4 damage. If your deck has no minions, summon four 1/1 Illidari
    # with <b>Rush</b>.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 4), -Find(FRIENDLY_DECK + MINION) & (
        Summon(CONTROLLER, "BT_036t") * 4
    )


class RLK_209:
    """Unleash Fel"""

    # Deal $1 damage to all enemies. <b>Manathirst_(6):</b> With
    # <b>Lifesteal</b>.
    play = Manathirst(6) & GiveLifesteal(SELF), Hit(ENEMY_CHARACTERS, 1)


class RLK_211:
    """Deal with a Devil"""

    # Summon two 3/3 Felfiends with <b>Lifesteal</b>. If your deck has no
    # minions, summon another.
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "RLK_211t") * 2, -Find(FRIENDLY_DECK + MINION) & Summon(
        CONTROLLER, "RLK_211t"
    )


##
# Weapons


class RLK_214:
    """Souleater's Scythe"""

    # [x]<b>Start of Game:</b> Consume 3 different minions in your deck. Leave
    # behind Souls that <b>Discover</b> them.
    class Deck:
        events = GameStart().on(lambda source: RLK_214.consume(source))

    Hand = Deck

    def consume(self):
        player = self.controller
        minions = RANDOM(DeDuplicate(FRIENDLY_DECK + MINION), 3).eval(self.game, self)
        if minions and not getattr(player, "souleater_used", False):
            player.souleater_used = True
            for minion in minions:
                yield Remove(minion)
                soul = player.card("RLK_214t", self)
                soul.consumed_minions = minions
                yield Shuffle(player, soul)


class NX2_025:
    """Calamity's Grasp"""

    # <b>Deathrattle:</b> Add a random <b>Outcast</b> card to your hand.
    deathrattle = Give(CONTROLLER, random_outcast)


class RLK_207e:
    update = Refresh(FRIENDLY_HAND + OUTCAST, {GameTag.COST: -1})
    events = Play(CONTROLLER, OUTCAST).on(Destroy(SELF))


class RLK_214t:
    def play(self):
        cards = getattr(self, "consumed_minions", ())
        if cards:
            yield Choice(
                CONTROLLER, [self.controller.card(card.id, self) for card in cards]
            ).then(Give(CONTROLLER, Choice.CARD))
