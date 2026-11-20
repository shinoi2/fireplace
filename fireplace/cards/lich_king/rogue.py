from ..utils import *

CONCOCTIONS = ("RLK_570t1", "RLK_570t2", "RLK_570t3", "RLK_570t4", "RLK_570t5")
MIXED_CONCOCTIONS = dict(
    zip(
        (
            (left, right)
            for i, left in enumerate(CONCOCTIONS)
            for right in CONCOCTIONS[i:]
        ),
        (
            "RLK_570t1t4",
            "RLK_570t1t2",
            "RLK_570t1t3",
            "RLK_570t1t1",
            "RLK_570tt1",
            "RLK_570t2t2",
            "RLK_570t2t1",
            "RLK_570t4t1",
            "RLK_570tt3",
            "RLK_570t3t",
            "RLK_570t4t2",
            "RLK_570tt2",
            "RLK_570t4t3",
            "RLK_570tt4",
            "RLK_570tt5",
        ),
    )
)
CONCOCTION_IDS = CONCOCTIONS + tuple(MIXED_CONCOCTIONS.values())

##
# Minions


class RLK_529:
    """Noxious Infiltrator"""

    # [x]<b>Poisonous</b> <b>Battlecry:</b> If a friendly Undead died after
    # your last turn, deal 1 damage to a minion.
    requirements = {
        enums.REQ_TARGET_IF_AVAILABLE_AND_FRIENDLY_UNDEAD_DIED: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    powered_up = FRIENDLY_UNDEAD_DIED
    play = powered_up & Hit(TARGET, 1)


class RLK_216:
    """Rotten Rodent"""

    # <b>Battlecry:</b> Reduce the Cost of all <b>Deathrattle</b> cards in your
    # deck by (1).
    play = Buff(FRIENDLY_DECK + DEATHRATTLE, "RLK_216e")


class RLK_217:
    """Scourge Illusionist"""

    # [x]<b>Deathrattle:</b> Add a 4/4 copy of another <b>Deathrattle</b>
    # minion in your deck to your hand. It costs (4) less.
    deathrattle = Give(
        CONTROLLER,
        ExactCopy(RANDOM(FRIENDLY_DECK + MINION + DEATHRATTLE - ID("RLK_217"))),
    ).then(Buff(Give.CARD, "RLK_217e"), Buff(Give.CARD, "RLK_217e2"))


class RLK_570:
    """Ghoulish Alchemist"""

    # <b>Battlecry</b>: Your next Concoction costs (0).
    play = Buff(CONTROLLER, "RLK_570e4")


class RLK_568:
    """Concoctor"""

    # <b>Battlecry:</b> Add a random Concoction to your hand.
    play = Give(CONTROLLER, RandomID(*CONCOCTIONS))


class RLK_571:
    """Vile Apothecary"""

    # At the end of your turn, add a random Concoction to your hand.
    events = OWN_TURN_END.on(Give(CONTROLLER, RandomID(*CONCOCTIONS)))


class RLK_572:
    """Potionmaster Putricide"""

    # After a minion dies, add a Concoction to your hand.
    events = Death(MINION).after(Give(CONTROLLER, RandomID(*CONCOCTIONS)))


class NX2_005:
    """Stitched Creation"""

    # <b>Combo:</b> Gain +2/+2. <b>Infuse ({0}):</b> Gain +3/+3. <b>Manathirst
    # ({1}):</b> Gain +4/+4.
    infuse_card = "NX2_005t"
    play = Manathirst(8) & Buff(SELF, "NX2_005e2")
    combo = Buff(SELF, "NX2_005e"), play


class NX2_006:
    """Jolly Roger"""

    # After your hero attacks, summon a 1/1 Undead Pirate.
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "NX2_006t"))


##
# Spells


class RLK_567:
    """Shadow of Demise"""

    # Each time you cast a spell, transform this into a copy of it.
    def draw(self):
        for spell in reversed(self.controller.cards_played_this_game):
            if spell.type == CardType.SPELL:
                yield Morph(SELF, Copy(spell)).then(Buff(Morph.CARD, "RLK_567e"))
                break

    class Hand:
        events = OWN_SPELL_PLAY.after(
            Morph(SELF, Copy(Play.CARD)).then(Buff(Morph.CARD, "RLK_567e"))
        )


class RLK_569:
    """Potion Belt"""

    # [x]<b>Discover</b> 2 Concoctions.
    play = (
        Choice(CONTROLLER, RandomID(*CONCOCTIONS) * 3).then(
            Give(CONTROLLER, Choice.CARD)
        )
        * 2
    )


class RLK_573:
    """Ghostly Strike"""

    # Deal $1 damage. <b>Combo:</b> Draw a card.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 1)
    combo = play, Draw(CONTROLLER)


class NX2_004:
    """Ransack"""

    # Deal $1 damage to a minion. If you've played a card from another class
    # this turn, deal $4 instead.
    requirements = MINION_TARGET
    play = Find(
        CARDS_PLAYED_THIS_GAME + CARDS_PLAYED_THIS_TURN + OTHER_CLASS_CHARACTER
    ) & Hit(TARGET, 4) | Hit(TARGET, 1)


RLK_216e = buff(cost=-1)
RLK_217e2 = buff(cost=-4)
NX2_005e = buff(2, 2)
NX2_005e2 = buff(4, 4)
NX2_005t = NX2_005


class RLK_217e:
    atk = max_health = SET(4)


class RLK_567e:
    class Hand:
        events = OWN_SPELL_PLAY.after(Morph(OWNER, Copy(Play.CARD)))


class RLK_570e4:
    update = Refresh(FRIENDLY_HAND + IDS(CONCOCTION_IDS), {GameTag.COST: SET(0)})
    events = Play(CONTROLLER, IDS(CONCOCTION_IDS)).on(Destroy(SELF))


def mix_concoctions(source, player, added):
    if (
        source is added
        or added.id not in CONCOCTIONS
        or source.zone != Zone.HAND
        or added.zone != Zone.HAND
    ):
        return
    mixed = MIXED_CONCOCTIONS[tuple(sorted((source.id, added.id)))]
    yield Remove(added)
    yield Morph(source, mixed)


class Concoction:
    class Hand:
        events = Give(CONTROLLER, IDS(CONCOCTIONS)).after(mix_concoctions)
        events = (
            events,
            Draw(CONTROLLER, IDS(CONCOCTIONS)).on(
                lambda source, player, card, _: mix_concoctions(source, player, card)
            ),
        )


class RLK_570t1(Concoction):
    play = Summon(CONTROLLER, RandomMinion(cost=3))


class RLK_570t2(Concoction):
    play = Destroy(RANDOM_ENEMY_MINION)


class RLK_570t3(Concoction):
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3)


class RLK_570t4(Concoction):
    play = Give(
        CONTROLLER, Buff(RandomCollectible(card_class=ANOTHER_CLASS), "RLK_570e3")
    )


class RLK_570t5(Concoction):
    play = Draw(CONTROLLER) * 2


RLK_570e3 = buff(cost=-3)

_concoction_scripts = (RLK_570t1, RLK_570t2, RLK_570t3, RLK_570t4, RLK_570t5)
for (first, second), card_id in MIXED_CONCOCTIONS.items():
    effects = [_concoction_scripts[CONCOCTIONS.index(card)] for card in (first, second)]
    globals()[card_id] = type(
        card_id,
        (),
        {
            "play": tuple(effect.play for effect in effects),
            "requirements": next(
                (
                    effect.requirements
                    for effect in effects
                    if hasattr(effect, "requirements")
                ),
                {},
            ),
        },
    )
