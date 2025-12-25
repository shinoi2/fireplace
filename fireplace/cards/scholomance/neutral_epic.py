from ..utils import *


##
# Minions


class SCH_157:
    """Enchanted Cauldron"""

    # <b><b>Spellburst</b>:</b> Cast a random spell of the same Cost.

    # TODO: need to be tested
    spellburst = CastSpell(RandomSpell(cost=COST(SELF)))


class SCH_714:
    """Educated Elekk"""

    # [x]Whenever a spell is played, this minion remembers it.
    # <b>Deathrattle:</b> Shuffle the spells into your deck.
    events = OWN_SPELL_PLAY.on(StoringBuff(SELF, "SCH_714e", Play.CARD))


class SCH_714e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Shuffle(CONTROLLER, STORE_CARD)
