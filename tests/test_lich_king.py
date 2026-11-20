import pytest

from fireplace import cards as cards_db
from test_path_of_arthas import dk_game
from utils import *


def test_sunwell_cost_tracks_other_cards_in_its_owners_hand():
    game = prepare_empty_game()
    game.player1.discard_hand()
    sunwell = game.player1.give("RLK_590")
    assert sunwell.cost == 9
    other = game.player1.give(WISP)
    assert sunwell.cost == 8
    game.player2.give(WISP)
    assert sunwell.cost == 8
    other.discard()
    assert sunwell.cost == 9
    second = game.player1.give("RLK_590")
    assert sunwell.cost == second.cost == 8


@pytest.mark.parametrize(
    "limit,other_cards", [(10, 0), (10, 4), (10, 9), (12, 0), (12, 11)]
)
def test_sunwell_fills_available_hand_slots_with_permanent_spells(limit, other_cards):
    game = prepare_empty_game()
    game.player1.discard_hand()
    if limit == 12:
        game.player1.give("DRG_208").play()
        game.player1.used_mana = 0
    original = [game.player1.give(WISP) for _ in range(other_cards)]
    sunwell = game.player1.give("RLK_590")
    assert sunwell.cost == max(0, 9 - other_cards)
    with mock(RandomSpell, lambda picker, source: [source.controller.card(FIREBALL)]):
        sunwell.play()
    assert len(game.player1.hand) == limit
    assert all(card in game.player1.hand for card in original)
    generated = game.player1.hand.filter(id=FIREBALL)
    assert len(generated) == limit - other_cards
    assert all(card.type == CardType.SPELL for card in generated)
    assert len({card.entity_id for card in generated}) == len(generated)
    assert sunwell.zone == Zone.GRAVEYARD
    game.end_turn()
    assert len(game.player1.hand) == limit


def empty_game(deck=()):
    game = dk_game(deck1=list(deck), deck2=list(deck))
    return game, game.current_player, game.current_player.opponent


def test_corpse_explosion_uses_corpses_from_earlier_waves():
    game, player, opponent = empty_game()
    friend = player.summon("CS2_231")
    enemy = opponent.summon("CS2_120")
    spell = player.give("RLK_035")
    assert not spell.is_playable()
    player.corpses = 2
    spell.play()
    assert friend.zone == enemy.zone == Zone.GRAVEYARD
    assert player.corpses == 0
    assert player.corpses_spent_this_game == 3
    assert opponent.corpses == 1


def test_arcane_spell_damage_and_vexallus():
    game, player, opponent = empty_game()
    bolt = player.give("RLK_843")
    player.summon("RLK_541")
    player.give("RLK_826").play()
    bolt.play(target=opponent.hero)
    assert opponent.hero.damage == 8


def test_anubrekhan_uses_armor_for_exactly_three_minions():
    game, player, _ = empty_game()
    player.give("RLK_659").play()
    assert player.hero.armor == 8
    assert player.mana == 2
    for _ in range(3):
        minion = player.give("CS2_120")
        assert minion.card_costs_armor
        minion.play()
    assert player.hero.armor == 2
    assert player.mana == 2
    assert not player.give("CS2_120").card_costs_armor


def test_astalor_adds_upgrade_below_manathirst():
    game, player, _ = empty_game()
    player.max_mana = 4
    astalor = player.give("RLK_222")
    assert not astalor.targets
    astalor.play()
    assert player.hand[-1].id == "RLK_222t1"


def test_haunted_spell_summons_its_soldier():
    game, player, _ = empty_game()
    player.give("GAME_005")
    player.summon("RLK_822").destroy()
    player.hand[-1].play()
    assert player.field[-1].id == "RLK_822t"


def test_sindragosa_destroys_a_frozen_enemy():
    game, player, opponent = empty_game()
    enemy = opponent.summon("CS2_186")
    player.give("NX2_037").play()
    assert [card.id for card in player.field] == ["NX2_037t", "NX2_037", "NX2_037t2"]
    player.give("RLK_038").play(target=enemy)
    assert enemy.zone == Zone.GRAVEYARD


def test_concoctions_mix_and_use_both_effects():
    game, player, opponent = empty_game()
    player.give("RLK_570t3")
    player.give("RLK_570t3")
    assert [card.id for card in player.hand] == ["RLK_570t3t"]
    player.hand[0].play(target=opponent.hero)
    assert opponent.hero.damage == 6


def test_spells_cannot_target_heroes_until_next_turn():
    game, player, opponent = empty_game()
    bolt = player.give("RLK_843")
    player.give("RLK_218").play()
    assert opponent.hero not in bolt.targets
    game.end_turn()
    game.end_turn()
    assert opponent.hero in bolt.targets


def test_mograine_persists_after_the_minion_dies():
    game, player, opponent = empty_game()
    player.give("RLK_706").play().destroy()
    game.end_turn()
    assert opponent.hero.damage == 3
    game.end_turn()
    assert opponent.hero.damage == 3
    game.end_turn()
    assert opponent.hero.damage == 6


def test_souleater_consumes_distinct_minions_and_replaces_them():
    deck = ["RLK_214", "CS2_231", "CS2_120", "CS2_186"] + ["GAME_005"] * 6
    game, player, opponent = empty_game(deck)
    for owner in game.players:
        souls = [card for card in owner.deck + owner.hand if card.id == "RLK_214t"]
        assert souls
        for soul in souls:
            consumed_ids = [card.id for card in soul.consumed_minions]
            assert len(set(consumed_ids)) == len(consumed_ids)
            assert all(card.id not in consumed_ids for card in owner.deck)
    soul = next(card for card in player.deck + player.hand if card.id == "RLK_214t")
    if soul.zone != Zone.HAND:
        soul.zone = Zone.HAND
    soul.play()
    choice = player.choice
    assert sorted(card.id for card in choice.cards) == sorted(
        card.id for card in soul.consumed_minions
    )
    selected = choice.cards[0]
    choice.choose(selected)
    assert selected in player.hand


CORE_DEATH_KNIGHT_CARDS = [
    "RLK_503",
    "RLK_958",
    "RLK_708",
    "RLK_082",
    "RLK_720",
    "RLK_025",
    "RLK_511",
    "RLK_710",
    "RLK_709",
    "RLK_223",
    "RLK_224",
    "RLK_039",
    "RLK_061",
    "RLK_705",
    "RLK_707",
    "RLK_085",
    "RLK_744",
    "RLK_048",
    "RLK_060",
    "RLK_071",
]

# Their tokens and enchantments (build 170126)
TOKENS = [
    "RLK_039t",  # Grain Crate
    "RLK_070t",  # Undead Peasant
    "RLK_061t",  # Risen Footman
    "RLK_008t",  # Risen Ghoul
    "RLK_085t",  # Risen Golem
    "RLK_705t",  # Shambling Zombie
]
ENCHANTMENTS = [
    "RLK_085e",
    "RLK_707e",
    "RLK_707e2",
    "RLK_710e",
    "RLK_958e",
    "RLK_048e",
]


# --- the data ---------------------------------------------------------------


def test_the_twenty_cards_are_in_carddefs():
    db = cards_db.db
    # (cost, attack, health or durability, runes blood/frost/unholy), build 170126
    stats = {
        "RLK_503": (1, 1, 3, (0, 0, 0)),
        "RLK_958": (1, 1, 2, (0, 0, 0)),
        "RLK_708": (3, 2, 2, (0, 0, 0)),
        "RLK_082": (5, 3, 5, (2, 0, 0)),
        "RLK_720": (6, 5, 6, (1, 0, 0)),
        "RLK_025": (2, 0, 0, (0, 2, 0)),
        "RLK_511": (2, 2, 2, (0, 2, 0)),
        "RLK_710": (3, 2, 3, (0, 2, 0)),
        "RLK_709": (4, 0, 0, (0, 1, 0)),
        "RLK_223": (4, 3, 3, (0, 1, 0)),
        "RLK_224": (6, 5, 6, (0, 2, 0)),
        "RLK_039": (1, 0, 0, (0, 0, 3)),
        "RLK_061": (2, 2, 3, (0, 0, 2)),
        "RLK_705": (3, 0, 0, (0, 0, 1)),
        "RLK_707": (4, 0, 0, (0, 0, 3)),
        "RLK_085": (8, 9, 7, (0, 0, 3)),
        "RLK_744": (9, 8, 8, (0, 0, 2)),
        "RLK_048": (3, 0, 0, (0, 0, 1)),
        "RLK_060": (5, 0, 0, (0, 0, 2)),
        "RLK_071": (7, 4, 6, (1, 0, 0)),
    }
    assert sorted(stats) == sorted(CORE_DEATH_KNIGHT_CARDS)
    for id, (cost, atk, health, runes) in stats.items():
        card = db[id]
        assert card.card_class == CardClass.DEATHKNIGHT, id
        assert card.tags.get(GameTag.CARDTEXT) or card.description, id
        assert (card.cost, card.atk) == (cost, atk), id
        if card.type == CardType.WEAPON:
            assert card.durability == health, id
        else:
            assert card.health == health, id
        assert (card.cost_blood, card.cost_frost, card.cost_unholy) == runes, id
    types = {
        "RLK_503": CardType.MINION,
        "RLK_710": CardType.WEAPON,
        "RLK_025": CardType.SPELL,
        "RLK_071": CardType.MINION,
    }
    for id, type in types.items():
        assert db[id].type == type, id


def test_their_tokens_and_enchantments_are_in_carddefs():
    db = cards_db.db
    for id in TOKENS:
        assert db[id].type in (CardType.MINION, CardType.SPELL), id
    for id in ENCHANTMENTS:
        assert db[id].type == CardType.ENCHANTMENT, id
    assert (db["RLK_061t"].atk, db["RLK_061t"].health) == (1, 3)
    assert (db["RLK_008t"].atk, db["RLK_008t"].health) == (2, 2)
    assert (db["RLK_085t"].atk, db["RLK_085t"].health) == (1, 1)
    assert (db["RLK_705t"].atk, db["RLK_705t"].health) == (1, 1)
    assert (db["RLK_070t"].atk, db["RLK_070t"].health) == (2, 2)
    assert db["RLK_039t"].type == CardType.SPELL


def test_core_death_knight_cards_are_collectible_and_standard():
    for card_id in CORE_DEATH_KNIGHT_CARDS:
        card = cards_db.db[card_id]
        assert card.collectible, card_id
        assert card.card_set == CardSet.CORE, card_id
        assert card.is_standard, card_id


# --- the cards ----------------------------------------------------------------

CROCOLISK = "CS2_120"  # 2/3
WAR_GOLEM = "CS2_186"  # 7/7
BRANN = "LOE_077"  # Brann Bronzebeard


# --- RLK_503
def test_body_bagger():
    game = dk_game()
    bagger = game.player1.give("RLK_503").play()
    assert (bagger.atk, bagger.health) == (1, 3)
    assert Race.UNDEAD in bagger.races
    assert game.player1.corpses == 1
    assert game.player2.corpses == 0
    game.player1.give("RLK_503").play()
    assert game.player1.corpses == 2


def test_body_bagger_with_brann():
    game = dk_game()
    game.player1.give(BRANN).play()
    game.player1.give("RLK_503").play()
    assert game.player1.corpses == 2


def test_gain_corpses_is_not_spending():
    game = dk_game()
    game.player1.give("RLK_503").play()
    assert game.player1.corpses_spent_this_game == 0


# --- RLK_958
def test_skeletal_sidekick():
    game = dk_game()
    undead = game.player1.summon("RLK_503")  # Body Bagger, an Undead
    crocolisk = game.player1.summon(CROCOLISK)
    enemy_undead = game.player2.summon("RLK_503")
    sidekick = game.player1.give("RLK_958")
    assert (sidekick.atk, sidekick.health) == (1, 2)
    assert Race.UNDEAD in sidekick.races
    assert sidekick.requires_target()
    # Only the friendly Undead is eligible.
    assert sidekick.targets == [undead]
    sidekick.play(target=undead)
    assert undead.atk == 3 and undead.health == 3
    assert crocolisk.atk == 2
    assert enemy_undead.atk == 1


def test_skeletal_sidekick_without_a_target():
    game = dk_game()
    game.player1.summon(CROCOLISK)
    sidekick = game.player1.give("RLK_958")
    assert not sidekick.requires_target()
    sidekick.play()
    assert game.player1.field[-1] is sidekick
    assert sidekick.atk == 1


# --- RLK_708
def test_chillfallen_baron():
    game = dk_game()
    for _ in range(4):
        game.player1.card(WISP, zone=Zone.DECK)
    baron = game.player1.give("RLK_708")
    # (Its second tribe, Draenei, is a tag of a newer build that the reader of
    # CardDefs.xml does not know: nothing here reacts to it.)
    assert Race.UNDEAD in baron.races
    hand = len(game.player1.hand)  # with the Baron
    baron.play()
    # The Baron leaves the hand, the Battlecry draws a card
    assert len(game.player1.hand) == hand
    assert len(game.player1.deck) == 3
    # The Deathrattle draws another
    game.player1.give(FIREBALL).play(target=baron)
    assert baron.zone == Zone.GRAVEYARD
    assert len(game.player1.hand) == hand + 1
    assert len(game.player1.deck) == 2


# --- RLK_082
def test_deathbringer_saurfang():
    game = dk_game()
    saurfang = game.player1.give("RLK_082").play()
    assert saurfang.taunt and (saurfang.atk, saurfang.health) == (3, 5)
    assert Race.UNDEAD in saurfang.races
    game.player1.give(FIREBALL).play(target=saurfang)
    # Returned to the hand, costing Health instead of Mana
    assert saurfang.zone == Zone.HAND
    back = game.player1.hand[-1]
    assert back is saurfang
    assert back.card_costs_health
    assert back.cost == 5
    game.player1.used_mana = 10
    health = game.player1.hero.health
    back.play()
    assert game.player1.hero.health == health - 5
    assert game.player1.used_mana == 10
    assert back.zone == Zone.PLAY


def test_deathbringer_saurfang_needs_the_health():
    game = dk_game()
    saurfang = game.player1.give("RLK_082").play()
    game.player1.give(FIREBALL).play(target=saurfang)
    back = game.player1.hand[-1]
    game.player1.used_mana = 0
    game.player1.hero.set_current_health(5)
    # 5 Health for a 5 cost: the hero would die
    assert not back.is_playable()
    game.player1.hero.set_current_health(6)
    assert back.is_playable()


def test_deathbringer_saurfang_comes_back_again():
    game = dk_game()
    saurfang = game.player1.give("RLK_082").play()
    game.player1.give(FIREBALL).play(target=saurfang)
    back = game.player1.hand[-1]
    back.play()
    assert back.zone == Zone.PLAY
    game.player1.used_mana = 0
    game.player1.give(FIREBALL).play(target=back)
    # Every death brings it back, costing Health again
    assert back.zone == Zone.HAND and back.card_costs_health
    assert game.player1.hand[-1] is back


# --- RLK_720
def test_gnome_muncher():
    game = dk_game(class2=CardClass.MAGE)
    muncher = game.player1.give("RLK_720").play()
    assert muncher.taunt and muncher.lifesteal
    assert (muncher.atk, muncher.health) == (5, 6)
    wisp = game.player2.summon(WISP)
    crocolisk = game.player2.summon(CROCOLISK)
    golem = game.player2.summon(WAR_GOLEM)
    game.player1.hero.set_current_health(20)
    game.end_turn()
    # It attacked the lowest Health enemy, the Wisp, and healed by its Lifesteal
    assert wisp.zone == Zone.GRAVEYARD
    assert crocolisk.damage == 0 and golem.damage == 0
    assert muncher.damage == 1
    assert game.player1.hero.health == 25
    # A forced attack does not use the Muncher's own attack
    assert muncher.num_attacks == 0


def test_gnome_muncher_attacks_the_hero_when_alone():
    game = dk_game()
    game.player1.give("RLK_720").play()
    game.end_turn()
    assert game.player2.hero.health == 25


def test_gnome_muncher_attacks_the_lowest_health_character_even_the_hero():
    game = dk_game()
    game.player1.give("RLK_720").play()
    game.player2.hero.set_current_health(6)
    golem = game.player2.summon(WAR_GOLEM)
    game.end_turn()
    assert game.player2.hero.health == 1
    assert golem.damage == 0


def test_gnome_muncher_only_at_the_end_of_its_owners_turn():
    game = dk_game()
    game.player1.give("RLK_720").play()
    game.end_turn()
    assert game.player2.hero.health == 25
    wisp = game.player2.summon(WISP)
    # The other player's turn ends: the Muncher does not attack
    game.end_turn()
    assert wisp.zone == Zone.PLAY and game.player2.hero.health == 25


def test_gnome_muncher_takes_one_of_two_equal_targets():
    game = dk_game()
    game.player1.give("RLK_720").play()
    wisps = [game.player2.summon(WISP), game.player2.summon(WISP)]
    game.end_turn()
    assert sorted(w.zone for w in wisps) == [Zone.PLAY, Zone.GRAVEYARD]


def test_gnome_muncher_ignores_taunt():
    game = dk_game()
    game.player1.give("RLK_720").play()
    footman = game.player2.summon(GOLDSHIRE_FOOTMAN)  # 1/2 Taunt
    wisp = game.player2.summon(WISP)
    game.end_turn()
    assert wisp.zone == Zone.GRAVEYARD
    assert footman.damage == 0


# --- RLK_025
def test_frost_strike():
    game = dk_game()
    enemy = game.player2.summon(CROCOLISK)
    frost_strike = game.player1.give("RLK_025")
    assert game.player2.hero not in frost_strike.targets
    frost_strike.play(target=enemy)
    assert enemy.zone == Zone.GRAVEYARD
    choice = game.player1.choice
    assert choice and len(choice.cards) == 3
    for card in choice.cards:
        assert card.card_class == CardClass.DEATHKNIGHT, card
        assert card.cost_frost > 0, card
        assert sum(card.runes) < 3, card
    picked = choice.cards[1]
    choice.choose(picked)
    assert game.player1.hand[-1].id == picked.id


def test_frost_strike_that_does_not_kill_discovers_nothing():
    game = dk_game()
    golem = game.player2.summon(WAR_GOLEM)
    game.player1.give("RLK_025").play(target=golem)
    assert golem.damage == 3
    assert not game.player1.choice


def test_frost_strike_on_a_friendly_minion():
    game = dk_game()
    wisp = game.player1.summon(WISP)
    game.player1.give("RLK_025").play(target=wisp)
    assert wisp.zone == Zone.GRAVEYARD
    assert game.player1.choice


# --- RLK_511
def test_harbinger_of_winter():
    game = dk_game()
    icy_touch = game.player1.card("RLK_038", zone=Zone.DECK)  # a Frost spell
    fireball = game.player1.card(FIREBALL, zone=Zone.DECK)  # a Fire spell
    wisp = game.player1.card(WISP, zone=Zone.DECK)
    harbinger = game.player1.give("RLK_511").play()
    assert (harbinger.atk, harbinger.health) == (2, 2)
    assert not game.player1.hand
    game.player1.give(FIREBALL).play(target=harbinger)
    assert harbinger.zone == Zone.GRAVEYARD
    assert icy_touch.zone == Zone.HAND
    assert fireball.zone == Zone.DECK and wisp.zone == Zone.DECK


def test_harbinger_of_winter_draws_one_of_the_frost_spells():
    game = dk_game()
    spells = [
        game.player1.card("RLK_038", zone=Zone.DECK),
        game.player1.card("RLK_015", zone=Zone.DECK),
    ]
    harbinger = game.player1.summon("RLK_511")
    game.player1.give(FIREBALL).play(target=harbinger)
    assert sorted(s.zone for s in spells) == [Zone.DECK, Zone.HAND]


def test_harbinger_of_winter_without_a_frost_spell():
    game = dk_game()
    fireball = game.player1.card(FIREBALL, zone=Zone.DECK)
    harbinger = game.player1.summon("RLK_511")
    game.player1.give(MOONFIRE).play(target=harbinger)
    game.player1.give(MOONFIRE).play(target=harbinger)
    assert harbinger.zone == Zone.GRAVEYARD
    assert fireball.zone == Zone.DECK


# --- RLK_710
def test_rimefang_sword():
    game = dk_game()
    game.player1.give("RLK_710").play()
    assert game.player1.weapon.atk == 2 and game.player1.weapon.durability == 3
    fireball = game.player1.give(FIREBALL)
    wisp = game.player1.give(WISP)
    game.player1.hero.attack(game.player2.hero)
    # The one spell of the hand costs (1) less; the minion does not
    assert fireball.cost == 3
    assert wisp.cost == 0
    game.end_turn()
    game.end_turn()
    game.player1.hero.attack(game.player2.hero)
    assert fireball.cost == 2


def test_rimefang_sword_reduces_one_of_two_spells():
    game = dk_game()
    game.player1.give("RLK_710").play()
    fireball = game.player1.give(FIREBALL)  # 4
    frostbolt = game.player1.give("CS2_024")  # 2
    game.player1.hero.attack(game.player2.summon(WAR_GOLEM))
    assert (fireball.cost, frostbolt.cost) in [(3, 2), (4, 1)]


def test_rimefang_sword_without_a_spell():
    game = dk_game()
    game.player1.give("RLK_710").play()
    wisp = game.player1.give(WISP)
    game.player1.hero.attack(game.player2.hero)
    assert wisp.cost == 0


def test_rimefang_sword_only_after_your_hero_attacks():
    game = dk_game()
    game.player1.give("RLK_710").play()
    fireball = game.player1.give(FIREBALL)
    wisp = game.player1.summon(WISP)
    game.end_turn()
    game.end_turn()
    wisp.attack(game.player2.hero)
    assert fireball.cost == 4


# --- RLK_709
def test_remorseless_winter():
    game = dk_game()
    for _ in range(2):
        game.player1.card(WISP, zone=Zone.DECK)
    mine = game.player1.summon(CROCOLISK)
    enemy1 = game.player2.summon(CROCOLISK)
    enemy2 = game.player2.summon(WISP)
    hand = len(game.player1.hand)
    game.player1.give("RLK_709").play()
    assert game.player2.hero.health == 28
    assert enemy1.damage == 2 and enemy2.zone == Zone.GRAVEYARD
    assert mine.damage == 0 and game.player1.hero.health == 30
    assert len(game.player1.hand) == hand + 1


def test_remorseless_winter_with_spell_power():
    game = dk_game()
    game.player1.summon(KOBOLD_GEOMANCER)
    enemy = game.player2.summon(CROCOLISK)
    game.player1.give("RLK_709").play()
    assert game.player2.hero.health == 27
    assert enemy.zone == Zone.GRAVEYARD


# --- RLK_223
def test_thassarian():
    game = dk_game()
    thassarian = game.player1.give("RLK_223").play()
    assert (thassarian.atk, thassarian.health) == (3, 3)
    assert thassarian.reborn and Race.UNDEAD in thassarian.races
    # Battlecry: 2 damage to a random enemy (here, only the hero)
    assert game.player2.hero.health == 28
    # Deathrattle: 2 more, then Reborn brings it back, and again
    game.player1.give(FIREBALL).play(target=thassarian)
    assert thassarian.zone == Zone.GRAVEYARD
    assert game.player2.hero.health == 26
    reborn = game.player1.field[0]
    assert reborn.id == "RLK_223" and reborn.health == 1 and not reborn.reborn
    game.player1.give(MOONFIRE).play(target=reborn)
    assert game.player2.hero.health == 24
    assert not game.player1.field


def test_thassarian_hits_one_random_enemy():
    game = dk_game()
    enemies = [game.player2.summon(WAR_GOLEM), game.player2.summon(WAR_GOLEM)]
    game.player1.give("RLK_223").play()
    damage = [game.player2.hero.damage] + [e.damage for e in enemies]
    assert sorted(damage) == [0, 0, 2]
    assert game.player1.hero.health == 30


def test_thassarian_never_hits_a_friend():
    game = dk_game()
    mine = game.player1.summon(WAR_GOLEM)
    game.player1.give("RLK_223").play()
    assert mine.damage == 0


# --- RLK_224
def test_overseer_frigidara_two_frost_spells():
    game = dk_game()
    frost = [
        game.player1.card("RLK_038", zone=Zone.DECK),
        game.player1.card("RLK_015", zone=Zone.DECK),
    ]
    wisp = game.player1.card(WISP, zone=Zone.DECK)
    enemy = game.player2.summon(CROCOLISK)
    mine = game.player1.summon(CROCOLISK)
    overseer = game.player1.give("RLK_224").play()
    assert (overseer.atk, overseer.health) == (5, 6)
    assert all(c.zone == Zone.HAND for c in frost)
    assert wisp.zone == Zone.DECK
    assert enemy.damage == 2 and game.player2.hero.health == 28
    assert mine.damage == 0 and game.player1.hero.health == 30


def test_overseer_frigidara_not_both_frost():
    game = dk_game()
    frost = game.player1.card("RLK_038", zone=Zone.DECK)
    fire = game.player1.card(FIREBALL, zone=Zone.DECK)
    wisp = game.player1.card(WISP, zone=Zone.DECK)
    game.player1.give("RLK_224").play()
    assert frost.zone == Zone.HAND and fire.zone == Zone.HAND
    assert wisp.zone == Zone.DECK
    assert game.player2.hero.health == 30


def test_overseer_frigidara_with_a_single_spell():
    game = dk_game()
    frost = game.player1.card("RLK_038", zone=Zone.DECK)
    game.player1.give("RLK_224").play()
    assert frost.zone == Zone.HAND
    assert game.player2.hero.health == 30  # they are not both Frost spells


# --- RLK_039 and its Crates
def test_plagued_grain():
    game = dk_game()
    game.player1.give("RLK_039").play()
    assert game.player1.corpses == 4
    crates = [c for c in game.player1.deck if c.id == "RLK_039t"]
    assert len(crates) == 4 and len(game.player1.deck) == 4
    assert game.player1.give("RLK_039").cost == 1


def test_plagued_grain_crates_summon_an_undead_peasant_when_drawn():
    game = dk_game()
    game.player1.card(WISP, zone=Zone.DECK)
    game.player1.card("RLK_039t", zone=Zone.DECK)
    hand = len(game.player1.hand)
    game.player1.draw()
    # Cast when drawn: a 2/2, no card in the hand (the next draw replaces it)
    peasant = game.player1.field[0]
    assert peasant.id == "RLK_070t" and (peasant.atk, peasant.health) == (2, 2)
    assert game.player1.hand[-1].id == WISP and len(game.player1.hand) == hand + 1
    assert game.player1.used_mana == 0


def test_plagued_grain_four_crates_in_a_row():
    game = dk_game()
    game.player1.give("RLK_039").play()
    game.player1.draw()
    # Each crate casts itself and draws the next one
    assert [m.id for m in game.player1.field] == ["RLK_070t"] * 4
    assert not game.player1.deck


# --- RLK_061 and the raising of Corpses
def test_battlefield_necromancer():
    game = dk_game()
    necromancer = game.player1.give("RLK_061").play()
    assert (necromancer.atk, necromancer.health) == (2, 3)
    game.player1.corpses = 2
    game.end_turn()
    footman = game.player1.field[-1]
    assert footman.id == "RLK_061t"
    assert (footman.atk, footman.health) == (1, 3) and footman.taunt
    assert game.player1.corpses == 1
    assert game.player1.corpses_spent_this_game == 1
    game.end_turn()
    game.end_turn()
    assert [m.id for m in game.player1.field] == ["RLK_061", "RLK_061t", "RLK_061t"]
    assert game.player1.corpses == 0


def test_battlefield_necromancer_without_a_corpse():
    game = dk_game()
    game.player1.give("RLK_061").play()
    game.end_turn()
    assert len(game.player1.field) == 1


def test_battlefield_necromancer_only_at_the_end_of_your_turn():
    game = dk_game()
    game.player1.give("RLK_061").play()
    game.player1.corpses = 3
    game.end_turn()
    assert game.player1.corpses == 2
    # The other player's turns raise nothing: 2 turns of yours, 2 Corpses spent
    game.end_turn()
    game.end_turn()
    game.end_turn()
    assert game.player1.corpses == 1
    assert len(game.player1.field) == 3


def test_battlefield_necromancer_with_a_full_board_spends_nothing():
    game = dk_game()
    game.player1.give("RLK_061").play()
    for _ in range(6):
        game.player1.summon(WISP)
    game.player1.corpses = 2
    game.end_turn()
    assert game.player1.corpses == 2


def test_a_risen_footman_leaves_no_corpse():
    game = dk_game()
    game.player1.give("RLK_061").play()
    game.player1.corpses = 1
    game.end_turn()
    game.end_turn()
    footman = game.player1.field[-1]
    game.player1.give(FIREBALL).play(target=footman)
    assert footman.zone == Zone.GRAVEYARD
    assert game.player1.corpses == 0


# --- RLK_705
def test_graveyard_shift():
    game = dk_game()
    game.player1.give("RLK_705").play()
    zombies = list(game.player1.field)
    assert [z.id for z in zombies] == ["RLK_705t", "RLK_705t"]
    assert all((z.atk, z.health) == (1, 1) and z.reborn for z in zombies)
    game.player1.give(MOONFIRE).play(target=zombies[0])
    assert zombies[0].zone == Zone.GRAVEYARD
    # Reborn: it comes back with 1 Health and no Reborn
    assert len(game.player1.field) == 2
    assert not game.player1.field[0].reborn


def test_graveyard_shift_needs_room():
    game = dk_game()
    for _ in range(7):
        game.player1.summon(WISP)
    assert not game.player1.give("RLK_705").is_playable()


def test_graveyard_shift_with_one_place_left():
    game = dk_game()
    for _ in range(6):
        game.player1.summon(WISP)
    game.player1.give("RLK_705").play()
    assert len(game.player1.field) == 7


# --- RLK_707
def test_grave_strength():
    game = dk_game()
    mine = [game.player1.summon(CROCOLISK), game.player1.summon(WISP)]
    enemy = game.player2.summon(CROCOLISK)
    game.player1.corpses = 4
    game.player1.give("RLK_707").play()
    # Not enough Corpses: +1 Attack, and nothing is spent
    assert [m.atk for m in mine] == [3, 2] and enemy.atk == 2
    assert game.player1.corpses == 4
    assert game.player1.corpses_spent_this_game == 0


def test_grave_strength_spending_five_corpses_gives_three_instead():
    game = dk_game()
    mine = [game.player1.summon(CROCOLISK), game.player1.summon(WISP)]
    enemy = game.player2.summon(CROCOLISK)
    game.player1.corpses = 7
    game.player1.give("RLK_707").play()
    # +3 instead of +1, not +4
    assert [m.atk for m in mine] == [5, 4] and enemy.atk == 2
    assert game.player1.corpses == 2
    assert game.player1.corpses_spent_this_game == 5


def test_grave_strength_with_no_minion_still_spends_the_corpses():
    game = dk_game()
    game.player1.corpses = 5
    game.player1.give("RLK_707").play()
    assert game.player1.corpses == 0


# --- RLK_085
def test_lord_marrowgar():
    game = dk_game()
    game.player1.corpses = 3
    marrowgar = game.player1.give("RLK_085").play()
    assert (marrowgar.atk, marrowgar.health) == (9, 7)
    assert Race.UNDEAD in marrowgar.races
    golems = game.player1.field[1:]
    assert [g.id for g in golems] == ["RLK_085t"] * 3
    assert all((g.atk, g.health) == (1, 1) and g.rush for g in golems)
    assert game.player1.corpses == 0
    assert game.player1.corpses_spent_this_game == 3


def test_lord_marrowgar_gives_one_bonus_per_corpse_that_cannot_fit():
    game = dk_game()
    game.player1.corpses = 9
    game.player1.give("RLK_085").play()
    golems = game.player1.field[1:]
    # Marrowgar and six Golems fill the board; the 3 other Corpses each give
    # one Golem +2/+2 (a Golem may get several)
    assert len(golems) == 6
    assert sum(g.atk for g in golems) == 6 + 3 * 2
    assert sum(g.health for g in golems) == 6 + 3 * 2
    assert game.player1.corpses == 0
    assert game.player1.corpses_spent_this_game == 9


def test_lord_marrowgar_without_a_corpse():
    game = dk_game()
    game.player1.give("RLK_085").play()
    assert len(game.player1.field) == 1


def test_lord_marrowgar_gives_all_the_bonuses_to_the_one_golem_that_fits():
    game = dk_game()
    for _ in range(5):
        game.player1.summon(WISP)
    game.player1.corpses = 4
    marrowgar = game.player1.give("RLK_085").play()
    golems = [m for m in game.player1.field if m.id == "RLK_085t"]
    assert len(golems) == 1 and (golems[0].atk, golems[0].health) == (
        1 + 3 * 2,
        1 + 3 * 2,
    )
    assert game.player1.corpses == 0
    assert marrowgar.zone == Zone.PLAY


def test_lord_marrowgar_on_a_full_board_still_spends_the_corpses():
    game = dk_game()
    for _ in range(6):
        game.player1.summon(WISP)
    game.player1.corpses = 4
    game.player1.give("RLK_085").play()
    assert len(game.player1.field) == 7
    assert not [m for m in game.player1.field if m.id == "RLK_085t"]
    assert game.player1.corpses == 0
    assert game.player1.corpses_spent_this_game == 4


def test_a_risen_golem_leaves_no_corpse():
    game = dk_game()
    game.player1.corpses = 1
    game.player1.give("RLK_085").play()
    golem = game.player1.field[-1]
    game.player1.used_mana = 0
    game.player1.give(FIREBALL).play(target=golem)
    assert golem.zone == Zone.GRAVEYARD
    assert game.player1.corpses == 0


# --- RLK_744
def test_stitched_giant():
    game = dk_game()
    giant = game.player1.give("RLK_744")
    assert (giant.atk, giant.health) == (8, 8) and Race.UNDEAD in giant.races
    assert giant.cost == 9
    # Gaining Corpses is not spending them
    game.player1.give("RLK_503").play()
    assert giant.cost == 9
    game.player1.corpses = 8
    game.player1.used_mana = 0
    game.player1.give("RLK_707").play()  # Grave Strength spends 5
    assert game.player1.corpses_spent_this_game == 5
    assert giant.cost == 4
    game.player1.corpses = 20
    game.player1.used_mana = 0
    game.player1.give("RLK_504").play()  # Corpse Bride spends up to 10
    assert game.player1.corpses_spent_this_game == 15
    # Never below 0
    assert giant.cost == 0
    game.player1.used_mana = 10
    giant.play()
    assert giant.zone == Zone.PLAY


def test_stitched_giant_counts_only_your_own_corpses():
    game = dk_game()
    giant = game.player1.give("RLK_744")
    game.player2.corpses = 5
    game.queue_actions(game.player2.hero, [SpendCorpses(game.player2, 5)])
    assert game.player2.corpses_spent_this_game == 5
    assert giant.cost == 9


def test_stitched_giant_after_the_corpses_of_a_raise():
    game = dk_game()
    giant = game.player1.give("RLK_744")
    game.player1.corpses = 3
    hero = game.player1.hero
    game.queue_actions(hero, [RaiseCorpses(CONTROLLER, 3, "RLK_008t")])  # raised: spent
    assert game.player1.corpses_spent_this_game == 3
    assert giant.cost == 6


# --- RLK_048
def test_anti_magic_shell():
    game = dk_game()
    mine = [game.player1.summon(CROCOLISK), game.player1.summon(WISP)]
    enemy = game.player2.summon(CROCOLISK)
    game.player1.give("RLK_048").play()
    assert [(m.atk, m.health) for m in mine] == [(3, 4), (2, 2)]
    assert (enemy.atk, enemy.health) == (2, 3)
    game.end_turn()
    # Elusive: no spell of the other player targets them
    fireball = game.player2.give(FIREBALL)
    assert fireball.targets
    assert mine[0] not in fireball.targets and mine[1] not in fireball.targets
    assert enemy in fireball.targets


def test_anti_magic_shell_minions_can_still_be_attacked():
    game = dk_game()
    mine = game.player1.summon(CROCOLISK)
    enemy = game.player2.summon(CROCOLISK)
    game.player1.give("RLK_048").play()
    game.end_turn()
    enemy.attack(mine)
    assert mine.damage == 2 and enemy.zone == Zone.GRAVEYARD


def test_anti_magic_shell_protects_from_your_own_spells_too():
    game = dk_game()
    wisp = game.player1.summon(WISP)
    game.player1.give("RLK_048").play()
    fireball = game.player1.give(FIREBALL)
    assert wisp not in fireball.targets
    newcomer = game.player1.summon(WISP)
    assert (newcomer.atk, newcomer.health) == (1, 1)
    assert newcomer in fireball.targets


def test_anti_magic_shell_protects_from_hero_powers():
    # Two mages (who plays first is drawn): Fireblast targets
    game = prepare_empty_game(CardClass.MAGE, CardClass.MAGE)
    wisp = game.player1.summon(WISP)
    game.player1.give("RLK_048").play()
    game.end_turn()
    power = game.player2.hero.power
    assert power.targets and wisp not in power.targets
    assert game.player1.hero in power.targets


# --- RLK_060
def test_army_of_the_dead():
    game = dk_game()
    game.player1.corpses = 3
    game.player1.give("RLK_060").play()
    ghouls = game.player1.field
    assert [g.id for g in ghouls] == ["RLK_008t"] * 3
    assert all((g.atk, g.health) == (2, 2) and g.rush for g in ghouls)
    assert game.player1.corpses == 0
    assert game.player1.corpses_spent_this_game == 3


def test_army_of_the_dead_up_to_five():
    game = dk_game()
    game.player1.corpses = 8
    game.player1.give("RLK_060").play()
    assert len(game.player1.field) == 5
    assert game.player1.corpses == 3


def test_army_of_the_dead_only_raises_what_fits():
    game = dk_game()
    for _ in range(5):
        game.player1.summon(WISP)
    game.player1.corpses = 8
    game.player1.give("RLK_060").play()
    assert len(game.player1.field) == 7
    assert game.player1.corpses == 6


def test_army_of_the_dead_without_a_corpse():
    game = dk_game()
    game.player1.give("RLK_060").play()
    assert not game.player1.field


def test_a_risen_ghoul_leaves_no_corpse():
    game = dk_game()
    game.player1.corpses = 1
    game.player1.give("RLK_060").play()
    ghoul = game.player1.field[0]
    game.player1.used_mana = 0
    game.player1.give(FIREBALL).play(target=ghoul)
    assert ghoul.zone == Zone.GRAVEYARD
    assert game.player1.corpses == 0


# --- RLK_071
def test_patchwerk():
    game = dk_game(class2=CardClass.MAGE)
    hand = [
        game.player2.give(WISP),
        game.player2.give(CROCOLISK),
        game.player2.give(FIREBALL),
    ]
    deck = [
        game.player2.card(WISP, zone=Zone.DECK),
        game.player2.card(WAR_GOLEM, zone=Zone.DECK),
        game.player2.card(FIREBALL, zone=Zone.DECK),
    ]
    board = [game.player2.summon(WISP), game.player2.summon(WAR_GOLEM)]
    mine = game.player1.summon(WISP)
    patchwerk = game.player1.give("RLK_071").play()
    assert (patchwerk.atk, patchwerk.health) == (4, 6)
    # One minion of each zone is destroyed; never a spell, never a friend
    assert sum(c.zone == Zone.GRAVEYARD for c in hand if c.type == CardType.MINION) == 1
    assert hand[2].zone == Zone.HAND
    assert sum(c.zone == Zone.GRAVEYARD for c in deck if c.type == CardType.MINION) == 1
    assert deck[2].zone == Zone.DECK
    assert sum(m.zone == Zone.GRAVEYARD for m in board) == 1
    assert mine.zone == Zone.PLAY and patchwerk.zone == Zone.PLAY
    assert game.player2.hero.health == 30


def test_patchwerk_with_only_one_zone():
    game = dk_game(class2=CardClass.MAGE)
    board = game.player2.summon(WAR_GOLEM)
    game.player1.give("RLK_071").play()
    assert board.zone == Zone.GRAVEYARD


def test_patchwerk_with_no_enemy_minion():
    game = dk_game()
    game.player2.give(FIREBALL)
    patchwerk = game.player1.give("RLK_071").play()
    assert patchwerk.zone == Zone.PLAY


def test_anachronos_returns_enemy_minions_to_their_original_board():
    game, player, opponent = empty_game()
    for card_id in (WISP, CROCOLISK, WAR_GOLEM):
        minion = opponent.card(card_id)
        minion._summon_index = 0
        opponent.summon(minion)
    minions = list(opponent.field)
    player.give("RLK_919").play()
    assert not opponent.field

    for _ in range(4):
        game.end_turn()

    assert opponent.field == minions
    assert player.field[0].id == "RLK_919"
    assert len(player.field) == 1


def test_thaddius_alternates_cost_polarity_on_its_owners_turns():
    game, player, _ = empty_game()
    odd = player.give("RLK_533")
    even = player.give(CROCOLISK)
    player.summon("NX2_033")
    assert (odd.cost, even.cost) == (1, 2)

    game.end_turn()
    game.end_turn()

    assert (odd.cost, even.cost) == (3, 1)


def test_energy_shaper_preserves_a_discounted_spells_cost():
    _, player, _ = empty_game()
    spell = player.give(FIREBALL)
    player.hero.buff(spell, "RLK_547e")
    assert spell.cost == 3

    player.give("RLK_545").play()

    (transformed,) = player.hand
    assert transformed is not spell
    assert transformed.data.cost == 5
    assert transformed.cost == 3


def test_scourge_supplies_only_offers_cards_drawn_by_the_spell():
    _, player, _ = empty_game()
    original = player.give(WISP)
    drawn = [
        player.card(card_id, zone=Zone.DECK)
        for card_id in (CROCOLISK, WAR_GOLEM, FIREBALL)
    ]

    player.give("RLK_533").play()

    assert player.choice.cards == drawn[::-1]
    player.choice.choose(drawn[0])
    assert original in player.hand
    assert drawn[0] not in player.hand


def test_scourge_supplies_with_no_cards_to_draw_skips_discard():
    _, player, _ = empty_game()
    original = player.give(WISP)

    player.give("RLK_533").play()

    assert player.choice is None
    assert player.hand == [original]
