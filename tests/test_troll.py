from utils import *


def test_griftah():
	game = prepare_empty_game()
	game.player1.give("TRL_096").play()
	card1 = game.player1.choice.cards[0]
	game.player1.choice.choose(card1)
	card2 = game.player1.choice.cards[0]
	game.player1.choice.choose(card2)
	if card1.id != card2.id:
		assert (
			game.player1.hand[0].id == card1.id and
			game.player2.hand[1].id == card2.id
		) ^ (
			game.player1.hand[0].id == card2.id and
			game.player2.hand[1].id == card1.id
		)
	else:
		assert game.player1.hand[0].id == card1.id
		assert game.player2.hand[1].id == card1.id
	assert not game.player1.choice


def test_hakkar():
	game = prepare_empty_game()
	hakkar = game.player1.give("TRL_541").play()
	hakkar.destroy()
	assert len(game.player1.deck) == 1
	assert game.player1.deck[0].id == "TRL_541t"
	assert len(game.player2.deck) == 1
	assert game.player2.deck[0].id == "TRL_541t"
	game.end_turn()
	assert len(game.player2.deck) == 2
	assert game.player2.deck[0].id == "TRL_541t"
	assert game.player2.deck[1].id == "TRL_541t"
	assert game.player2.hero.health == 27
	game.skip_turn()
	assert game.player2.hero.health == 21
	assert len(game.player2.deck) == 4


def test_hakkar_full():
	game = prepare_empty_game()
	game.player1.give("KAR_712").play()
	for _ in range(60):
		blood = game.player1.give("TRL_541t")
		blood.shuffle_into_deck()
	assert len(game.player1.deck) == 60
	game.skip_turn()
	assert len(game.player1.deck) == 60


def test_overkill():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	game.end_turn()
	direhorn = game.player2.give("TRL_232").play()
	game.skip_turn()
	direhorn.attack(wisp)
	assert len(game.player2.field) == 2


def test_overkill_spell():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	arrow = game.player1.give("TRL_347")
	arrow.play(target=wisp)
	assert len(game.player1.field) == 1


def test_snapjaw_shellfighter():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	shellfighter = game.player1.give("TRL_535").play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert wisp.damage == 0
	assert shellfighter.damage == 1


def test_two_snapjaw_shellfighters():
	game = prepare_game()
	shellfighter1 = game.player1.give("TRL_535").play()
	shellfighter2 = game.player1.give("TRL_535").play()
	game.player1.give(MOONFIRE).play(target=shellfighter1)
	assert shellfighter1.damage == 0
	assert shellfighter2.damage == 1


def test_treespeaker():
	game = prepare_game()
	game.player1.give("EX1_571").play()
	game.player1.give(WISP).play()
	game.player1.give("TRL_341").play()
	assert len(game.player1.field) == 5
	for i in range(3):
		assert game.player1.field[i].id == "TRL_341t"
	assert game.player1.field[3].id == WISP
	assert game.player1.field[4].id == "TRL_341"


def test_mass_hysteria():
	game = prepare_game()
	for _ in range(7):
		game.player1.give(WISP).play()
	game.player1.give("TRL_258").play()
	assert len(game.player1.field) == 1


def test_high_priest_thekal():
	game = prepare_game()
	game.player1.give("TRL_308").play()
	assert game.player1.hero.health == 1
	assert game.player1.hero.armor == 29


def test_spectral_cutlass():
	game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
	weapon = game.player1.give("GIL_672").play()
	durability = weapon.durability
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert weapon.durability == durability + 1


def test_stolen_steel():
	game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
	game.player1.give("TRL_156").play()
	assert game.player1.choice
	cards = game.player1.choice.cards
	for card in cards:
		assert card.card_class != CardClass.ROGUE
	game.player1.choice.choose(cards[0])


def test_masters_call():
	game = prepare_empty_game()
	beasts = ["NEW1_032", "NEW1_033", "NEW1_034"]
	for beast in beasts:
		game.player1.give(beast).shuffle_into_deck()
	game.player1.give("TRL_339").play()
	assert not game.player1.choice
	assert len(game.player1.hand) == 3

	game = prepare_empty_game()
	minions = [WISP, "NEW1_033", "NEW1_034"]
	for minion in minions:
		game.player1.give(minion).shuffle_into_deck()
	game.player1.give("TRL_339").play()
	assert game.player1.choice
	game.player1.choice.choose(game.player1.choice.cards[0])
	assert len(game.player1.hand) == 1


def test_pyromaniac():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	game.player1.give("TRL_315").play()
	wisp = game.player1.give(WISP).play()
	hand = len(game.player1.hand)
	game.player1.hero.power.use(target=wisp)
	assert len(game.player1.hand) == hand + 1


def test_janalai_the_dragonhawk():
	game = prepare_game(CardClass.HUNTER, CardClass.HUNTER)
	janalai = game.player1.give("TRL_316")
	assert not janalai.powered_up
	for _ in range(4):
		game.player1.hero.power.use()
		game.skip_turn()
	assert janalai.powered_up
	janalai.play()
	assert len(game.player1.field) == 2


def test_spirit_of_the_dragonhawk():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	game.player1.give("TRL_319").play()
	game.end_turn()
	for _ in range(3):
		game.player2.give(WISP).play()
	game.end_turn()
	assert len(game.player2.field) == 3
	game.player1.hero.power.use(target=game.player2.field[1])
	assert len(game.player2.field) == 0


def test_daring_fire_eater():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	game.player1.give("TRL_319").play()
	game.end_turn()
	for _ in range(3):
		game.player2.give(MECH).play()
	game.end_turn()
	game.player1.give("TRL_390").play()
	game.player1.hero.power.use(target=game.player2.field[1])
	for i in range(3):
		assert game.player2.field[i].damage == 3
	game.skip_turn()
	game.player1.hero.power.use(target=game.player2.field[1])
	for i in range(3):
		assert game.player2.field[i].damage == 4


def test_zuljin():
	game = prepare_game()
	game.player1.give(THE_COIN).play()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert game.player1.temp_mana == 0
	game.player1.give("TRL_065").play()
	assert game.player1.temp_mana == 1


def test_sulthraze():
	game = prepare_game()
	wisps = [game.player1.give(WISP).play() for _ in range(4)]
	game.end_turn()
	game.player2.give("TRL_325").play()
	for wisp in wisps:
		assert game.player2.hero.can_attack()
		game.player2.hero.attack(wisp)
	assert not game.player2.hero.can_attack()


def test_summon_tiger():
	game = prepare_game()
	game.player1.give("TRL_309").play()
	game.player1.give(FIREBALL).play(target=game.player2.hero)
	tiger = game.player1.field[1]
	assert tiger.cost == 4
	assert tiger.atk == 4
	assert tiger.health == 4
	game.player1.give(SILENCE).play(target=tiger)
	assert tiger.cost == 4
	assert tiger.atk == 4
	assert tiger.health == 4
	game.end_turn()

	game.player2.give("EX1_564").play(target=tiger)
	copy_tiger = game.player2.field[0]
	assert copy_tiger.cost == 4
	assert copy_tiger.atk == 4
	assert copy_tiger.health == 4


def test_mojomaster_zihi():
	game = prepare_game()
	zihi = game.player1.give("TRL_564").play()
	assert game.player1.max_mana == 5
	assert game.player2.max_mana == 5
	assert game.player1.mana == 10 - zihi.cost
	assert game.player2.mana == 5

	game2 = prepare_game(game_class=Game)
	for _ in range(5):
		game2.player1.give(THE_COIN).play()
	game2.player1.give("TRL_564").play()
	assert game2.player1.max_mana == 5
	assert game2.player2.max_mana == 5
	assert game2.player1.mana == 0
	assert game2.player2.mana == 0

	game3 = prepare_game(game_class=Game)
	for _ in range(10):
		game3.player1.give(THE_COIN).play()
	game3.player1.give("TRL_564").play()
	assert game3.player1.max_mana == 5
	assert game3.player2.max_mana == 5
	assert game3.player1.mana == 10 - zihi.cost
	assert game3.player2.mana == 0


def test_heavy_metal():
	game = prepare_game()
	game.player1.give("TRL_324").play()
	assert game.player1.field[0].cost == 0
	game.skip_turn()
	game.player1.give("LOOT_285t").play()
	game.skip_turn()
	assert game.player1.hero.armor == 15
	game.player1.give("TRL_324").play()
	assert game.player1.field[1].cost == 10


def test_wartbringer():
	game = prepare_game()
	wartbringer = game.player1.give("TRL_522")
	assert not wartbringer.powered_up
	assert not wartbringer.requires_target()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert not wartbringer.powered_up
	assert not wartbringer.requires_target()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert wartbringer.powered_up
	assert wartbringer.requires_target()


def test_kragwa_the_frog():
	game = prepare_empty_game()
	frog = game.player1.give("TRL_345")
	for _ in range(4):
		game.player1.give(MOONFIRE).play(target=game.player2.hero)
	game.skip_turn()
	assert game.player1.hand == [frog]
	frog.play()
	assert game.player1.hand == [MOONFIRE] * 4
