# 暂停测试：阿尔萨斯之路（死亡骑士系列）；按要求保留原内容为注释。
# """The death knight: its base hero and Hero Power, the Corpses, the runes and
# the 26 cards of Path of Arthas (texts of HearthstoneJSON build 253216)."""
#
# from utils import *
#
# from fireplace import cards as cards_db
#
# PATH_OF_ARTHAS = [
#     "RLK_042",
#     "RLK_038",
#     "RLK_110",
#     "RLK_516",
#     "RLK_018",
#     "RLK_056",
#     "RLK_057",
#     "RLK_066",
#     "RLK_083",
#     "RLK_711",
#     "RLK_712",
#     "RLK_015",
#     "RLK_087",
#     "RLK_512",
#     "RLK_731",
#     "RLK_062",
#     "RLK_118",
#     "RLK_713",
#     "RLK_740",
#     "RLK_745",
#     "RLK_504",
#     "RLK_730",
#     "RLK_086",
#     "RLK_505",
#     "RLK_063",
#     "RLK_122",
# ]
#
#
# def dk_game(deck1=None, deck2=None, class2=CardClass.DEATHKNIGHT):
#     """An empty-deck game: player1 is a death knight, player2 of `class2`.
#     Not a Standard game: Path of Arthas is not in the fork's Standard sets
#     (a Standard game draws nothing of it at random)."""
#     player1 = Player(
#         "Player1", deck1 or [], CardClass.DEATHKNIGHT.default_hero, is_standard=False
#     )
#     player1.cant_fatigue = True
#     player2 = Player("Player2", deck2 or [], class2.default_hero, is_standard=False)
#     player2.cant_fatigue = True
#     game = BaseTestGame(players=(player1, player2))
#     game.start()
#     for player in game.players:
#         if player.choice:
#             player.choice.choose()
#     return game
#
#
# # --- the data -------------------------------------------------------------
#
#
# def test_path_of_arthas_in_carddefs():
#     db = cards_db.db
#     collectible = [
#         id
#         for id, card in db.items()
#         if card.card_set == CardSet.PATH_OF_ARTHAS and card.collectible
#     ]
#     assert sorted(collectible) == sorted(PATH_OF_ARTHAS)
#     for id in PATH_OF_ARTHAS:
#         assert db[id].card_class == CardClass.DEATHKNIGHT, id
#         assert db[id].tags.get(GameTag.CARDTEXT) or db[id].description, id
#
#
# def test_path_of_arthas_stats():
#     # (cost, attack, health or durability), build 253216
#     stats = {
#         "RLK_042": (0, 0, 0),
#         "RLK_038": (1, 0, 0),
#         "RLK_110": (1, 1, 2),
#         "RLK_516": (1, 2, 2),
#         "RLK_018": (2, 0, 0),
#         "RLK_056": (2, 0, 0),
#         "RLK_057": (2, 0, 0),
#         "RLK_066": (2, 2, 3),
#         "RLK_083": (2, 2, 3),
#         "RLK_711": (2, 3, 2),
#         "RLK_712": (2, 0, 0),
#         "RLK_015": (3, 0, 0),
#         "RLK_087": (3, 0, 0),
#         "RLK_512": (3, 0, 0),
#         "RLK_731": (3, 2, 5),
#         "RLK_062": (4, 1, 3),
#         "RLK_118": (4, 0, 0),
#         "RLK_713": (4, 4, 3),
#         "RLK_740": (4, 4, 2),
#         "RLK_745": (4, 2, 4),
#         "RLK_504": (5, 4, 4),
#         "RLK_730": (5, 0, 0),
#         "RLK_086": (6, 4, 3),
#         "RLK_505": (6, 5, 5),
#         "RLK_063": (7, 0, 0),
#         "RLK_122": (9, 0, 0),
#     }
#     db = cards_db.db
#     for id, (cost, atk, health) in stats.items():
#         card = db[id]
#         if card.type == CardType.WEAPON:
#             # A weapon of a recent CardDefs.xml gives its durability as
#             # HEALTH: the fork reads DURABILITY (patch 21.8)
#             assert (card.cost, card.atk, card.durability) == (cost, atk, health), id
#         else:
#             assert (card.cost, card.atk, card.health) == (cost, atk, health), id
#
#
# def test_texts_as_carddefs_gives_them():
#     # A text on several lines keeps its lines as they are (no stray tab)
#     db = cards_db.db
#     ids = [
#         id
#         for id, card in db.items()
#         if card.dbf_id
#         and (
#             card.card_set == CardSet.PATH_OF_ARTHAS
#             or id.startswith(("HERO_11", "RLK_"))
#         )
#     ]
#     assert len(ids) >= 43
#     for id in ids:
#         for tag in (GameTag.CARDNAME, GameTag.CARDTEXT, GameTag.FLAVORTEXT):
#             for text in db[id].strings.get(tag, {}).values():
#                 assert "\t" not in (text or ""), (id, tag, text)
#     assert db["RLK_730"].description == (
#         "<b>Lifesteal</b>\nInfect all enemy minions. At the end of your turns, "
#         "they take 2 damage."
#     )
#
#
# def test_death_knight_hero_and_hero_power():
#     db = cards_db.db
#     assert CardClass.DEATHKNIGHT.default_hero == "HERO_11"
#     hero = db["HERO_11"]
#     assert hero.type == CardType.HERO
#     assert hero.card_class == CardClass.DEATHKNIGHT
#     assert hero.health == 30
#     assert hero.hero_power == "HERO_11bp"
#     assert db["HERO_11bp"].name == "Ghoul Charge"
#     assert db["HERO_11bp"].cost == 2
#     assert db["HERO_11bpt"].name == "Frail Ghoul"
#     assert db["HERO_11bpt"].races == [Race.UNDEAD]
#
#
# def test_rune_tags():
#     db = cards_db.db
#     runes = lambda id: tuple(
#         db[id].tags.get(tag, 0)
#         for tag in (GameTag.COST_BLOOD, GameTag.COST_FROST, GameTag.COST_UNHOLY)
#     )
#     assert runes("RLK_730") == (2, 0, 0)  # Blood Boil
#     assert runes("RLK_063") == (0, 3, 0)  # Frostwyrm's Fury
#     assert runes("RLK_118") == (0, 0, 2)  # Tomb Guardians
#     assert runes("RLK_087") == (0, 0, 0)  # Asphyxiate
#     assert runes("RLK_042") == (0, 2, 0)  # Horn of Winter
#
#
# # --- the runes ------------------------------------------------------------
#
#
# def test_runes_of_a_card():
#     game = dk_game()
#     blood_boil = game.player1.give("RLK_730")
#     assert blood_boil.runes == (2, 0, 0)
#     assert blood_boil.runes.blood == 2
#     assert game.player1.give("RLK_063").runes == (0, 3, 0)
#     assert game.player1.give("RLK_118").runes == (0, 0, 2)
#     assert game.player1.give("RLK_087").runes == (0, 0, 0)
#     # Any other card has no rune
#     assert game.player1.give(FIREBALL).runes == (0, 0, 0)
#     assert game.player1.give(WISP).runes.frost == 0
#
#
# # --- the Corpses ----------------------------------------------------------
#
#
# def test_corpse_when_a_friendly_minion_dies():
#     game = dk_game(class2=CardClass.MAGE)
#     assert game.player1.corpses == 0
#     wisp = game.player1.give(WISP).play()
#     enemy_wisp = game.player2.summon(WISP)
#     game.player1.give(MOONFIRE).play(target=wisp)
#     assert game.player1.corpses == 1
#     # Every class tracks its Corpses (patch 25.4.0)
#     game.player1.give(MOONFIRE).play(target=enemy_wisp)
#     assert game.player1.corpses == 1
#     assert game.player2.corpses == 1
#
#
# def test_no_corpse_for_a_hero_or_a_weapon():
#     game = dk_game()
#     game.player1.give(LIGHTS_JUSTICE).play()
#     game.player1.give("RLK_516").play()  # Bone Breaker destroys the first weapon
#     assert game.player1.corpses == 0
#
#
# def test_corpse_before_the_deathrattle():
#     from fireplace.actions import Deathrattle
#
#     seen = []
#     do = Deathrattle.do
#
#     def spy(self, source, target):
#         seen.append(target.controller.corpses)
#         return do(self, source, target)
#
#     game = dk_game()
#     gnome = game.player1.give("EX1_029").play()  # Leper Gnome
#     Deathrattle.do = spy
#     try:
#         game.player1.give(MOONFIRE).play(target=gnome)
#     finally:
#         Deathrattle.do = do
#     assert seen == [1]
#
#
# def test_corpses_survive_a_deep_copy():
#     import copy
#
#     game = dk_game()
#     game.player1.give(MOONFIRE).play(target=game.player1.give(WISP).play())
#     other = copy.deepcopy(game)
#     assert other.player1.corpses == 1
#     other.player1.corpses = 5
#     assert game.player1.corpses == 1
#
#
# def test_spend_corpses():
#     from fireplace.actions import SpendCorpses
#
#     game = dk_game()
#     player = game.player1
#     hero = player.hero
#     player.corpses = 3
#     armor = GainArmor(FRIENDLY_HERO, SpendCorpses.AMOUNT)
#     # Not enough: nothing is spent, nothing happens
#     game.queue_actions(hero, [SpendCorpses(CONTROLLER, 4).then(armor)])
#     assert player.corpses == 3 and hero.armor == 0
#     game.queue_actions(hero, [SpendCorpses(CONTROLLER, 2).then(armor)])
#     assert player.corpses == 1 and hero.armor == 2
#     assert player.corpses_spent_this_game == 2
#     # Up to: as many as the player has
#     game.queue_actions(hero, [SpendCorpses(CONTROLLER, 5, up_to=True).then(armor)])
#     assert player.corpses == 0 and hero.armor == 3
#     game.queue_actions(hero, [SpendCorpses(CONTROLLER, 5, up_to=True).then(armor)])
#     assert player.corpses == 0 and hero.armor == 3
#     assert player.corpses_spent_this_game == 3
#
#
# # --- the hero and its Hero Power ------------------------------------------
#
#
# def test_ghoul_charge():
#     game = dk_game()
#     assert game.player1.hero.id == "HERO_11"
#     assert game.player1.hero.power.id == "HERO_11bp"
#     game.player1.hero.power.use()
#     ghoul = game.player1.field[0]
#     assert ghoul.id == "HERO_11bpt"
#     assert ghoul.atk == 1 and ghoul.health == 1
#     assert ghoul.charge and ghoul.can_attack()
#     assert Race.UNDEAD in ghoul.races
#     game.end_turn()
#     assert ghoul.zone == Zone.GRAVEYARD
#     assert not game.player1.field
#     assert game.player1.corpses == 1
#
#
# def test_frail_ghoul_dies_only_at_the_end_of_its_owners_turn():
#     game = dk_game()
#     game.end_turn()
#     ghoul = game.player1.summon("HERO_11bpt")
#     game.end_turn()
#     assert ghoul.zone == Zone.PLAY
#     game.end_turn()
#     assert ghoul.zone == Zone.GRAVEYARD
#
#
# def test_ghoul_frenzy_by_justicar_trueheart():
#     game = dk_game()
#     game.player1.give("AT_132").play()
#     assert game.player1.hero.power.id == "HERO_11bp2"
#     game.player1.hero.power.use()
#     ghoul = game.player1.field[-1]
#     assert ghoul.id == "HERO_11bp2t"
#     assert ghoul.atk == 2 and ghoul.health == 1 and ghoul.charge
#     game.end_turn()
#     assert ghoul.zone == Zone.GRAVEYARD
#
#
# # --- nothing leaks where the death knight is not --------------------------
#
#
# def test_no_death_knight_card_where_it_is_not_expected():
#     from fireplace.utils import random_class
#
#     dk = {
#         id
#         for id, card in cards_db.db.items()
#         if card.card_class == CardClass.DEATHKNIGHT
#     }
#     assert len(dk) > 26
#     # A random deck of another class
#     for card_class in (CardClass.MAGE, CardClass.WARRIOR, CardClass.DEMONHUNTER):
#         assert not dk & set(random_draft(card_class))
#     # A random class (Maestra, a random opponent...)
#     game = prepare_empty_game()
#     for _ in range(100):
#         assert random_class(game) != CardClass.DEATHKNIGHT
#     # A Standard game: Path of Arthas is not in the fork's Standard sets
#     assert game.is_standard
#     source = game.player1.hero
#     for picker in (RandomMinion(), RandomCollectible(), RandomSpell()):
#         pool = picker.find_cards(source)
#         assert pool and not dk & set(pool)
#     # The death knight's hero is never a random collectible
#     assert "HERO_11" not in RandomCollectible(type=CardType.HERO).find_cards(source)
#
#
# # --- the cards --------------------------------------------------------------
#
# CROCOLISK = "CS2_120"  # 2/3
# WAR_GOLEM = "CS2_186"  # 7/7
#
#
# # --- RLK_042
# def test_horn_of_winter():
#     game = dk_game()
#     game.player1.used_mana = 5
#     game.player1.give("RLK_042").play()
#     assert game.player1.used_mana == 3
#     assert game.player1.mana == 7
#     game.player1.give("RLK_042").play()
#     game.player1.give("RLK_042").play()
#     assert game.player1.used_mana == 0
#
#
# # --- RLK_038
# def test_icy_touch():
#     game = dk_game()
#     mine = game.player1.summon(CROCOLISK)
#     enemy = game.player2.summon(CROCOLISK)
#     icy_touch = game.player1.give("RLK_038")
#     assert mine not in icy_touch.targets
#     assert game.player2.hero in icy_touch.targets
#     icy_touch.play(target=enemy)
#     assert enemy.health == 1 and enemy.frozen
#
#
# # --- RLK_110
# def test_ymirjar_frostbreaker():
#     game = dk_game()
#     game.player1.give("RLK_038")  # Icy Touch, a Frost spell
#     game.player1.give("RLK_038")
#     game.player1.give(FIREBALL)  # a Fire spell
#     ymirjar = game.player1.give("RLK_110").play()
#     assert ymirjar.atk == 3 and ymirjar.health == 2
#     assert game.player1.give("RLK_110").play().atk == 3
#
#
# # --- RLK_516
# def test_bone_breaker():
#     game = dk_game()
#     enemy = game.player2.summon(WAR_GOLEM)
#     game.player1.give("RLK_516").play()
#     game.player1.hero.attack(enemy)
#     assert enemy.damage == 2
#     assert game.player2.hero.health == 28
#     game.end_turn()
#     game.end_turn()
#     game.player1.hero.attack(game.player2.hero)
#     assert game.player2.hero.health == 26  # the attack itself, no trigger
#     assert not game.player1.weapon
#
#
# # --- RLK_018
# def test_plague_strike():
#     game = dk_game()
#     wisp = game.player2.summon(WISP)
#     crocolisk = game.player2.summon(CROCOLISK)
#     game.player1.give("RLK_018").play(target=crocolisk)
#     assert crocolisk.health == 0 or crocolisk.dead
#     assert game.player1.field[-1].id == "RLK_018t"
#     zombie = game.player1.field[-1]
#     assert zombie.atk == 2 and zombie.health == 2 and zombie.rush
#     assert Race.UNDEAD in zombie.races
#     game.player2.summon(WAR_GOLEM)
#     golem = game.player2.field[-1]
#     game.player1.give("RLK_018").play(target=golem)
#     assert len(game.player1.field) == 1
#     assert wisp.zone == Zone.PLAY
#
#
# # --- RLK_056
# def test_unholy_frenzy():
#     game = dk_game()
#     wisp1 = game.player1.summon(WISP)
#     wisp2 = game.player1.summon(WISP)
#     crocolisk = game.player1.summon(CROCOLISK)
#     golem = game.player2.summon(WAR_GOLEM)
#     game.player1.give("RLK_056").play(target=golem)
#     assert golem.damage == 4
#     # All three died, and were resummoned: new ones
#     assert [m.id for m in game.player1.field] == [WISP, WISP, CROCOLISK]
#     for old in (wisp1, wisp2, crocolisk):
#         assert old.zone == Zone.GRAVEYARD
#     assert all(m.damage == 0 for m in game.player1.field)
#     assert game.player1.corpses == 3
#
#
# def test_unholy_frenzy_stops_when_the_target_dies():
#     game = dk_game()
#     crocolisk1 = game.player1.summon(CROCOLISK)
#     crocolisk2 = game.player1.summon(CROCOLISK)
#     wisp = game.player2.summon(WISP)
#     game.player1.give("RLK_056").play(target=wisp)
#     assert wisp.zone == Zone.GRAVEYARD
#     assert crocolisk1.damage == 1 and crocolisk2.damage == 0
#     assert game.player1.field == [crocolisk1, crocolisk2]
#     assert game.player1.corpses == 0
#
#
# # --- RLK_057
# def test_dark_transformation():
#     game = dk_game()
#     wisp = game.player1.summon(WISP)
#     ghoul = game.player1.summon("HERO_11bpt")
#     enemy_ghoul = game.player2.summon("HERO_11bpt")
#     dark = game.player1.give("RLK_057")
#     assert wisp not in dark.targets
#     assert ghoul in dark.targets and enemy_ghoul in dark.targets
#     dark.play(target=enemy_ghoul)
#     monstrosity = game.player2.field[0]
#     assert monstrosity.id == "RLK_057t"
#     assert monstrosity.atk == 4 and monstrosity.health == 5 and monstrosity.rush
#     assert Race.UNDEAD in monstrosity.races
#     assert ghoul.zone == Zone.PLAY and ghoul.id == "HERO_11bpt"
#
#
# def test_dark_transformation_needs_an_undead():
#     game = dk_game()
#     game.player1.summon(WISP)
#     assert not game.player1.give("RLK_057").is_playable()
#
#
# # --- RLK_066
# def test_hematurge():
#     game = dk_game()
#     game.player1.give("RLK_066").play()
#     assert not game.player1.choice
#     game.player1.corpses = 1
#     game.player1.give("RLK_066").play()
#     choice = game.player1.choice
#     assert choice and len(choice.cards) == 3
#     for card in choice.cards:
#         assert card.cost_blood > 0, card
#         assert sum(card.runes) < 3, card
#     picked = choice.cards[0]
#     choice.choose(picked)
#     assert game.player1.hand[-1].id == picked.id
#     assert game.player1.corpses == 0
#
#
# # --- RLK_083
# def test_deathchiller():
#     game = dk_game()
#     crocolisk1 = game.player2.summon(CROCOLISK)
#     crocolisk2 = game.player2.summon(CROCOLISK)
#     game.player1.give("RLK_083").play()
#     game.player1.give(THE_COIN).play()
#     enemies = [game.player2.hero, crocolisk1, crocolisk2]
#     assert sorted(e.damage for e in enemies) == [0, 1, 1]
#     game.player1.summon(WISP)
#     assert all(m.damage == 0 for m in game.player1.field)
#
#
# # --- RLK_711
# def test_vicious_bloodworm():
#     game = dk_game()
#     board = game.player1.summon(WISP)
#     wisp = game.player1.give(WISP)
#     fireball = game.player1.give(FIREBALL)
#     bloodworm = game.player1.give("RLK_711")
#     assert bloodworm.targets == [wisp]
#     assert bloodworm.requires_target()
#     bloodworm.play(target=wisp)
#     assert wisp.atk == 4 and wisp.health == 1
#     assert board.atk == 1 and fireball.zone == Zone.HAND
#     # Without a minion in hand, it is played without a target
#     game.player1.hand.filter(type=CardType.MINION)[0].discard()
#     lone = game.player1.give("RLK_711")
#     assert lone.targets == [] and not lone.requires_target()
#     lone.play()
#
#
# # --- RLK_712
# def test_blood_tap():
#     game = dk_game()
#     wisp = game.player1.give(WISP)
#     game.player1.give("RLK_712").play()
#     assert (wisp.atk, wisp.health) == (2, 2)
#     game.player1.corpses = 3
#     game.player1.give("RLK_712").play()
#     assert (wisp.atk, wisp.health) == (4, 4)
#     assert game.player1.corpses == 1
#
#
# # --- RLK_015
# def test_howling_blast():
#     game = dk_game()
#     mine = game.player1.summon(CROCOLISK)
#     crocolisk1 = game.player2.summon(CROCOLISK)
#     crocolisk2 = game.player2.summon(CROCOLISK)
#     game.player1.give("RLK_015").play(target=crocolisk1)
#     assert crocolisk1.zone == Zone.GRAVEYARD
#     assert crocolisk2.damage == 1 and not crocolisk2.frozen
#     assert game.player2.hero.damage == 1
#     assert mine.damage == 0 and game.player1.hero.damage == 0
#
#
# def test_howling_blast_freezes_its_target():
#     game = dk_game()
#     golem = game.player2.summon(WAR_GOLEM)
#     game.player1.give("RLK_015").play(target=golem)
#     assert golem.damage == 3 and golem.frozen
#
#
# # --- RLK_087
# def test_asphyxiate():
#     game = dk_game()
#     wisp = game.player2.summon(WISP)
#     golem = game.player2.summon(WAR_GOLEM)
#     mine = game.player1.summon(WAR_GOLEM)
#     game.player1.give("RLK_087").play()
#     assert golem.zone == Zone.GRAVEYARD
#     assert wisp.zone == Zone.PLAY and mine.zone == Zone.PLAY
#
#
# # --- RLK_512
# def test_glacial_advance():
#     game = dk_game()
#     fireball = game.player1.give(FIREBALL)
#     wisp = game.player1.give(WISP)
#     game.player1.give("RLK_512").play(target=game.player2.hero)
#     assert game.player2.hero.damage == 4
#     assert fireball.cost == 2 and wisp.cost == 0
#     game.player1.give(THE_COIN).play()
#     assert fireball.cost == 4
#
#
# def test_glacial_advance_lasts_this_turn():
#     game = dk_game()
#     fireball = game.player1.give(FIREBALL)
#     game.player1.give("RLK_512").play(target=game.player2.hero)
#     assert fireball.cost == 2
#     game.end_turn()
#     assert fireball.cost == 4
#
#
# # --- RLK_731
# def test_darkfallen_neophyte():
#     game = dk_game()
#     wisp = game.player1.give(WISP)
#     game.player1.corpses = 1
#     game.player1.give("RLK_731").play()
#     assert wisp.atk == 1 and game.player1.corpses == 1
#     game.player1.corpses = 2
#     neophyte = game.player1.give("RLK_731").play()
#     assert (wisp.atk, wisp.health) == (3, 1)
#     assert neophyte.atk == 2 and game.player1.corpses == 0
#
#
# def test_darkfallen_neophyte_with_brann_spends_twice():
#     game = dk_game()
#     game.player1.summon("LOE_077")  # Brann Bronzebeard
#     wisp = game.player1.give(WISP)
#     game.player1.corpses = 5
#     game.player1.give("RLK_731").play()
#     assert wisp.atk == 5 and game.player1.corpses == 1
#     game.player1.corpses = 3
#     game.player1.give("RLK_731").play()
#     assert wisp.atk == 7 and game.player1.corpses == 1
#
#
# # --- RLK_062
# def test_nerubian_swarmguard():
#     game = dk_game()
#     swarmguard = game.player1.give("RLK_062")
#     game.player1.give("RLK_712").play()  # Blood Tap: +1/+1 in hand
#     swarmguard.play()
#     assert len(game.player1.field) == 3
#     for minion in game.player1.field:
#         assert minion.id == "RLK_062"
#         assert (minion.atk, minion.health) == (2, 4) and minion.taunt
#
#
# # --- RLK_118
# def test_tomb_guardians():
#     game = dk_game()
#     game.player1.give("RLK_118").play()
#     assert [m.id for m in game.player1.field] == ["RLK_118t3", "RLK_118t3"]
#     for zombie in game.player1.field:
#         assert (zombie.atk, zombie.health) == (2, 2) and zombie.taunt
#         assert not zombie.reborn
#     game.player1.corpses = 4
#     game.player1.give("RLK_118").play()
#     assert len(game.player1.field) == 4
#     assert [m.reborn for m in game.player1.field] == [False, False, True, True]
#     assert game.player1.corpses == 0
#
#
# def test_tomb_guardians_needs_room():
#     game = dk_game()
#     for _ in range(7):
#         game.player1.summon(WISP)
#     assert not game.player1.give("RLK_118").is_playable()
#
#
# # --- RLK_713
# def test_lady_deathwhisper():
#     game = dk_game()
#     game.player1.give("RLK_038")
#     game.player1.give(FIREBALL)
#     game.player1.give("RLK_015")
#     lady = game.player1.give("RLK_713").play()
#     game.player1.give(MOONFIRE).play(target=lady)
#     game.player1.give(MOONFIRE).play(target=lady)
#     game.player1.give(MOONFIRE).play(target=lady)
#     assert lady.zone == Zone.GRAVEYARD
#     ids = [c.id for c in game.player1.hand]
#     assert sorted(ids) == sorted(["RLK_038", FIREBALL, "RLK_015", "RLK_038", "RLK_015"])
#
#
# # --- RLK_740
# def test_might_of_menethil():
#     game = dk_game()
#     minions = [game.player2.summon(CROCOLISK) for _ in range(4)]
#     game.player1.corpses = 2
#     game.player1.give("RLK_740").play()
#     assert sum(m.frozen for m in minions) == 2
#     assert game.player1.corpses == 0
#     assert game.player1.weapon.id == "RLK_740"
#     assert game.player1.weapon.durability == 2
#
#
# def test_might_of_menethil_up_to_three():
#     game = dk_game()
#     minions = [game.player2.summon(CROCOLISK) for _ in range(4)]
#     game.player1.corpses = 5
#     game.player1.give("RLK_740").play()
#     assert sum(m.frozen for m in minions) == 3
#     assert game.player1.corpses == 2
#
#
# # --- RLK_745
# def test_malignant_horror():
#     game = dk_game()
#     horror = game.player1.give("RLK_745").play()
#     assert horror.reborn
#     game.player1.corpses = 3
#     game.end_turn()
#     assert len(game.player1.field) == 1 and game.player1.corpses == 3
#     game.end_turn()
#     game.player1.corpses = 4
#     game.end_turn()
#     assert [m.id for m in game.player1.field] == ["RLK_745", "RLK_745"]
#     assert game.player1.corpses == 0
#
#
# # --- RLK_504
# def test_corpse_bride():
#     game = dk_game()
#     game.player1.corpses = 3
#     game.player1.give("RLK_504").play()
#     groom = game.player1.field[-1]
#     assert groom.id == "RLK_506t"
#     assert (groom.atk, groom.health) == (3, 3) and groom.taunt
#     assert game.player1.corpses == 0
#     # A Risen Groom doesn't leave a Corpse
#     game.player1.give(FIREBALL).play(target=groom)
#     assert groom.zone == Zone.GRAVEYARD
#     assert game.player1.corpses == 0
#
#
# def test_corpse_bride_up_to_ten():
#     game = dk_game()
#     game.player1.corpses = 12
#     game.player1.give("RLK_504").play()
#     groom = game.player1.field[-1]
#     assert (groom.atk, groom.health) == (10, 10)
#     assert game.player1.corpses == 2
#     game.player1.corpses = 0
#     game.player1.give("RLK_504").play()
#     assert len(game.player1.field) == 3  # two brides, one groom
#
#
# # --- RLK_730
# def test_blood_boil():
#     game = dk_game()
#     game.player1.hero.set_current_health(20)
#     crocolisk = game.player2.summon(CROCOLISK)
#     golem = game.player2.summon(WAR_GOLEM)
#     mine = game.player1.summon(WAR_GOLEM)
#     game.player1.give("RLK_730").play()
#     assert not crocolisk.lifesteal
#     game.end_turn()
#     assert crocolisk.damage == 2 and golem.damage == 2 and mine.damage == 0
#     assert game.player1.hero.health == 24
#     game.end_turn()
#     assert golem.damage == 2
#     game.end_turn()
#     assert crocolisk.zone == Zone.GRAVEYARD and golem.damage == 4
#     assert game.player1.hero.health == 28
#     # The infected minion does not heal its own hero when it attacks
#     game.player2.hero.set_current_health(20)
#     golem.attack(game.player1.hero)
#     assert game.player2.hero.health == 20
#
#
# # --- RLK_086
# def test_frostmourne():
#     game = dk_game()
#     wisp = game.player2.summon(WISP)
#     crocolisk = game.player2.summon(CROCOLISK)
#     game.player1.give("RLK_086").play()
#     game.player1.hero.attack(wisp)
#     game.end_turn()
#     game.end_turn()
#     game.player1.hero.attack(crocolisk)
#     game.end_turn()
#     game.end_turn()
#     assert game.player1.weapon.durability == 1
#     game.player1.hero.attack(game.player2.hero)
#     assert not game.player1.weapon
#     assert [m.id for m in game.player1.field] == [WISP, CROCOLISK]
#     assert all(m.damage == 0 for m in game.player1.field)
#
#
# def test_frostmourne_killed_nothing():
#     game = dk_game()
#     game.player1.give("RLK_086").play()
#     game.player1.weapon.destroy()
#     assert not game.player1.field
#
#
# def test_frostmourne_has_its_own_deathrattle():
#     assert cards_db.db["RLK_086"].scripts.deathrattle
#
#
# # --- RLK_505
# def test_marrow_manipulator():
#     game = dk_game()
#     game.player1.corpses = 3
#     game.player1.give("RLK_505").play()
#     assert game.player2.hero.damage == 6
#     assert game.player1.corpses == 0
#     game.player1.corpses = 7
#     game.player1.used_mana = 0
#     game.player1.give("RLK_505").play()
#     assert game.player2.hero.damage == 16
#     assert game.player1.corpses == 2
#
#
# # --- RLK_063
# def test_frostwyrms_fury():
#     game = dk_game()
#     crocolisk = game.player2.summon(CROCOLISK)
#     golem = game.player2.summon(WAR_GOLEM)
#     game.player1.give("RLK_063").play(target=game.player2.hero)
#     assert game.player2.hero.damage == 5
#     assert crocolisk.frozen and golem.frozen
#     wyrm = game.player1.field[-1]
#     assert wyrm.id == "RLK_063t" and (wyrm.atk, wyrm.health) == (5, 5)
#
#
# # --- RLK_122
# def test_the_scourge():
#     game = dk_game()
#     game.player1.summon(WISP)
#     game.player1.give("RLK_122").play()
#     assert len(game.player1.field) == 7
#     for minion in game.player1.field[1:]:
#         assert Race.UNDEAD in minion.races
#         assert minion.data.collectible
#     assert not game.player1.give("RLK_122").is_playable()
