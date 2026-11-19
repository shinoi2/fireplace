from utils import *
from utils import _random_class
from utils import _draft


def test_kindly_grandmother():
    game = prepare_game()
    grandma = game.player1.give("KAR_005")
    grandma.play()
    assert len(game.player1.field) == 1
    # Kill Grandma
    game.player1.give(MOONFIRE).play(target=grandma)
    assert len(game.player1.field) == 1
    assert game.player1.field[0].id == "KAR_005a"


def test_cloaked_huntress():
    game = prepare_game()
    huntress = game.player1.give("KAR_006")
    # Freezing Trap
    secret = game.player1.give("EX1_611")
    huntress.play()
    # Check cost of secret
    assert secret.cost == 0
    # Kill Huntress
    for i in range(4):
        game.player1.give(MOONFIRE).play(target=huntress)

    assert secret.cost == 2


def test_babbling_book():
    game = prepare_game()
    game.player1.discard_hand()
    book = game.player1.give("KAR_009")
    book.play()

    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].type == CardType.SPELL


def test_nightbane_templar():
    game = prepare_game()
    game.player1.discard_hand()
    nightbane1 = game.player1.give("KAR_010")
    assert not nightbane1.powered_up
    nightbane1.play()
    assert len(game.player1.field) == 1
    game.end_turn()

    game.player2.give(WHELP)
    nightbane2 = game.player2.give("KAR_010")
    assert nightbane2.powered_up
    nightbane2.play()
    assert len(game.player2.field) == 3


def test_wicked_witchdoctor():
    game = prepare_game(CardClass.SHAMAN, CardClass.SHAMAN)
    witchdoc = game.player1.give("KAR_021")
    witchdoc.play()
    game.player1.give(THE_COIN).play()

    assert len(game.player1.field) == 2
    assert game.player1.field[-1].id in BASIC_TOTEMS


def test_book_wyrm():
    game = prepare_game()
    game.player1.discard_hand()
    game.player1.give(WHELP)
    bookwyrm1 = game.player1.give("KAR_033")
    assert not bookwyrm1.powered_up
    bookwyrm1.play()
    assert len(game.player1.field) == 1
    game.end_turn()

    game.player2.discard_hand()
    game.player2.give(WHELP)
    bookwyrm2 = game.player2.give("KAR_033")
    assert bookwyrm2.powered_up
    bookwyrm2.play(target=bookwyrm1)
    assert len(game.player1.field) == 0
    assert len(game.player2.field) == 1
    game.end_turn()


def test_priest_of_the_feast():
    game = prepare_game()
    priest = game.player1.give("KAR_035")
    for _ in range(5):
        game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert game.player1.hero.health == 25
    priest.play()
    game.player1.give(THE_COIN).play()
    assert game.player1.hero.health == 28


def test_arcane_anomaly():
    game = prepare_game()
    anomaly = game.player1.give("KAR_036")
    anomaly.play()
    assert anomaly.health == 1
    game.player1.give(THE_COIN).play()
    assert anomaly.health == 2
    game.player1.give(THE_COIN).play()
    assert anomaly.health == 3


def test_avian_watcher():
    game = prepare_game()
    watcher1 = game.player1.give("KAR_037")
    assert not watcher1.powered_up
    watcher1.play()
    assert watcher1.health == 6
    assert watcher1.atk == 3
    game.end_turn()

    watcher2 = game.player2.give("KAR_037")
    secret = game.player2.give("EX1_611")
    assert not watcher2.powered_up
    secret.play()
    assert watcher2.powered_up
    watcher2.play()
    assert watcher2.health == 7
    assert watcher2.atk == 4


def test_moroes():
    game = prepare_game()
    moroes = game.player1.give("KAR_044")
    moroes.play()
    assert len(game.player1.field) == 1
    game.end_turn()

    assert len(game.player1.field) == 2


def test_the_curator():
    game = prepare_empty_game()
    murloc = game.player1.give(MURLOC)
    murloc.shuffle_into_deck()
    dragon = game.player1.give(WHELP)
    dragon.shuffle_into_deck()
    beast = game.player1.give(CHICKEN)
    beast.shuffle_into_deck()
    curator = game.player1.give("KAR_061")
    assert len(game.player1.hand) == 1
    curator.play()
    assert len(game.player1.hand) == 3
    game.end_turn()

    game.player2.discard_hand()  # Get rid of the coin
    murloc2 = game.player2.give(MURLOC)
    murloc2.shuffle_into_deck()
    curator2 = game.player2.give("KAR_061")
    assert len(game.player2.hand) == 1
    curator2.play()
    assert len(game.player2.hand) == 1


def test_netherspite_historian():
    game = prepare_game()
    game.player1.discard_hand()
    historian1 = game.player1.give("KAR_062")
    assert not historian1.powered_up
    historian1.play()
    assert not game.player1.choice

    game.player1.give(WHELP)
    historian2 = game.player1.give("KAR_062")
    assert historian2.powered_up
    historian2.play()
    assert len(game.player1.choice.cards) == 3
    for card in game.player1.choice.cards:
        assert card.type == CardType.MINION
        assert Race.DRAGON in card.races


def test_menagerie_warden():
    game = prepare_game()
    game.player1.discard_hand()
    warden1 = game.player1.give("KAR_065")
    dragon = game.player1.give(WHELP)
    dragon.play()
    assert not warden1.powered_up
    warden1.play()
    assert len(game.player1.field) == 2
    game.end_turn()

    game.player2.discard_hand()
    warden2 = game.player2.give("KAR_065")
    beast = game.player2.give(CHICKEN)
    beast.play()
    motw = game.player2.give("CS2_009")
    motw.play(target=beast)
    assert beast.atk == 1 + 2
    assert beast.health == 1 + 2
    assert beast.taunt
    game.player2.give(MOONFIRE).play(target=beast)
    assert beast.health == 1 + 2 - 1
    assert warden2.powered_up
    warden2.play(target=beast)
    clone = game.player2.field[-1]
    assert clone.id == CHICKEN
    assert clone.buffs
    assert beast.atk == clone.atk
    assert beast.health == clone.health
    assert beast.max_health == clone.max_health
    assert clone.buffs


def test_swashburglar():
    game = prepare_empty_game()
    burglar = game.player1.give("KAR_069")
    burglar.play()
    assert len(game.player1.hand) == 1
    # Patch 21.8: "from another class", not the opponent's class.
    assert any(
        card_class != game.player1.hero.card_class
        for card_class in game.player1.hand[0].classes
    )


def test_ethereal_peddler():
    game = prepare_empty_game(CardClass.ROGUE, CardClass.PRIEST)
    if CardClass.ROGUE in game.current_player.hero.classes:
        game.end_turn()

    game.current_player.discard_hand()
    mc = game.current_player.give(MIND_CONTROL)
    evis = game.current_player.give("EX1_124")  # Eviscerate
    assert mc.cost == 10
    assert evis.cost == 2
    game.current_player.give("KAR_070").play()
    assert mc.cost == 10
    assert evis.cost == 0
    game.end_turn()

    game.current_player.discard_hand()
    mc2 = game.current_player.give(MIND_CONTROL)
    evis2 = game.current_player.give("EX1_124")  # Eviscerate
    assert mc2.cost == 10
    assert evis2.cost == 2
    game.current_player.give("KAR_070").play()
    assert game.current_player.hero.card_class
    assert mc2.cost == 8
    assert evis2.cost == 2


def test_malchezaars_imp():
    game = prepare_game()
    imp = game.player1.give("KAR_089")
    imp.play()
    soulfire = game.player1.give(SOULFIRE)
    assert len(game.player1.hand) == 5
    soulfire.play(target=game.player2.hero)
    assert len(game.player1.hand) == 4

    game.end_turn()
    game.end_turn()

    imp.destroy()
    game.player1.discard_hand()
    imp = game.player1.give("KAR_089")
    imp.play()
    assert len(game.player1.hand) == 0
    game.player1.give(CHICKEN)
    assert len(game.player1.hand) == 1
    doomguard = game.player1.give("EX1_310")
    doomguard.play()
    assert len(game.player1.hand) == 1

    game.end_turn()
    game.end_turn()

    assert len(game.player1.hand) == 2
    doomguard2 = game.player1.give("EX1_310")
    doomguard2.play()
    assert len(game.player1.hand) == 2


def test_medivhs_valet():
    game = prepare_game()
    secret = game.player1.give("EX1_130")
    valet1 = game.player1.give("KAR_092")
    assert not valet1.powered_up
    assert not valet1.requires_target()
    valet1.play()
    valet2 = game.player1.give("KAR_092")
    secret.play()
    assert valet2.powered_up
    assert valet2.requires_target()
    valet2.play(target=game.player2.hero)
    assert game.player2.hero.health == 27


def test_deadly_fork():
    game = prepare_empty_game()
    fork = game.player1.give("KAR_094")
    fork.play()
    game.player1.give(MOONFIRE).play(target=fork)
    game.player1.give(MOONFIRE).play(target=fork)
    assert game.player1.hand[0].id == "KAR_094a"

    game.player1.hand[0].play()
    assert game.player1.hero.atk == 3


def test_zoobot():
    game = prepare_game()
    zoobot = game.player1.give("KAR_095")
    murloc = game.player1.give(MURLOC).play()
    beast = game.player1.give(CHICKEN).play()
    dragon = game.player1.give(WHELP).play()
    assert zoobot.powered_up
    zoobot.play()

    assert murloc.atk == 2
    assert murloc.health == 2
    assert murloc.buffs
    assert beast.atk == 2
    assert beast.health == 2
    assert beast.buffs
    assert dragon.atk == 2
    assert dragon.health == 2
    assert dragon.buffs


def test_medivh():
    game = prepare_game()
    game.player1.give("KAR_097").play()
    assert game.player1.weapon
    assert game.player1.weapon.durability == 3

    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert len(game.player1.field) == 2
    assert game.player1.field[-1].cost == 0
    assert game.player1.weapon.durability == 2

    game.end_turn()
    game.end_turn()

    # avoid 2-cost minions that may be Sorcerer's Apprentice
    game.player1.give(MOONFIRE).play(target=game.player1.hero)
    assert len(game.player1.field) == 3
    assert game.player1.field[-1].cost == 0
    assert game.player1.weapon.durability == 1

    game.player1.give("EX1_295").play()
    assert len(game.player1.field) == 4
    assert game.player1.field[-1].cost == 3
    assert not game.player1.weapon

    game.player1.give(INNERVATE).play()
    assert len(game.player1.field) == 4


def test_barnes():
    game = prepare_empty_game()
    kobold = game.player1.give(KOBOLD_GEOMANCER)
    kobold.shuffle_into_deck()
    barnes = game.player1.give("KAR_114")
    assert len(game.player1.hand) == 1
    assert len(game.player1.deck) == 1

    barnes.play()

    assert len(game.player1.deck) == 1
    assert len(game.player1.field) == 2
    summon = game.player1.field[-1]
    assert summon.id == kobold.id
    assert summon.atk == 1
    assert summon.health == 1


def test_onyx_bishop():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    game.player1.give("CS2_009").play(target=wisp)
    assert wisp.atk == 3
    game.player1.give(SOULFIRE).play(target=wisp)
    assert len(game.player1.field) == 0
    game.player1.give("KAR_204").play()

    assert len(game.player1.field) == 2
    assert game.player1.field[-1].atk == 1


def test_menagerie_magician():
    game = prepare_game()
    zoobot = game.player1.give("KAR_702")
    murloc = game.player1.give(MURLOC).play()
    beast = game.player1.give(CHICKEN).play()
    dragon = game.player1.give(WHELP).play()
    assert zoobot.powered_up
    zoobot.play()

    assert murloc.atk == 3
    assert murloc.health == 3
    assert murloc.buffs
    assert beast.atk == 3
    assert beast.health == 3
    assert beast.buffs
    assert dragon.atk == 3
    assert dragon.health == 3
    assert dragon.buffs


def test_arcanosmith():
    game = prepare_game()
    game.player1.give("KAR_710").play()
    assert len(game.player1.field) == 2
    assert game.player1.field[-1].id == "KAR_710m"
    assert game.player1.field[-1].taunt


def test_violet_illusionist():
    game = prepare_game()
    game.player1.give("KAR_712").play()
    assert game.player1.hero.immune
    game.player1.give("CS2_064").play()  # Dread Infernal
    assert game.player1.hero.health == 30
    assert game.player2.hero.health == 29

    game.end_turn()

    assert not game.player1.hero.immune
    game.player2.give("CS2_064").play()  # Dread Infernal
    assert game.player1.hero.health == 29
    assert game.player2.hero.health == 28


def test_cat_trick():
    game = prepare_game()
    cattrick = game.player1.give("KAR_004").play()
    assert cattrick in game.player1.secrets
    game.end_turn()

    game.player2.give("CS2_032").play()
    assert len(game.player1.field) == 1
    assert game.player1.field[-1].id == "KAR_004a"


def test_purify():
    game = prepare_game()
    game.player1.discard_hand()
    purify = game.player1.give("KAR_013")
    assert not purify.is_playable()
    game.end_turn()

    acolyte1 = game.player2.give("EX1_007")
    acolyte1.play()
    game.end_turn()

    assert not purify.is_playable()
    acolyte2 = game.player1.give("EX1_007").play()
    assert purify.is_playable()
    purify.play(target=acolyte2)
    handsize = len(game.player1.hand)
    game.player1.give(MOONFIRE).play(target=acolyte2)
    assert len(game.player1.hand) == handsize


def test_kara_kazham():
    game = prepare_game()
    game.player1.give("KAR_025").play()
    assert len(game.player1.field) == 3
    game.player1.give("KAR_025").play()
    assert len(game.player1.field) == 6
    game.end_turn()
    game.end_turn()
    game.player1.give("KAR_025").play()
    assert len(game.player1.field) == 7
    assert game.player1.field[-1].id == "KAR_025a"


def test_protect_the_king():
    game = prepare_game()
    ptk = game.player1.give("KAR_026")
    assert not ptk.is_playable()
    game.end_turn()

    game.player2.give(WISP).play()
    game.player2.give(WHELP).play()
    game.end_turn()
    assert ptk.is_playable()
    ptk.play()
    assert len(game.player1.field) == 2


def test_maelstrom_portal():
    game = prepare_empty_game()
    game.player2.is_standard = False
    game.player1.give(WISP).play()
    game.end_turn()
    assert len(game.player1.field) == 1
    assert len(game.player2.field) == 0

    def pick_minion(picker, source):
        pool = picker.find_cards(source)
        assert GOLDSHIRE_FOOTMAN in pool and WISP not in pool
        return [GOLDSHIRE_FOOTMAN]

    with mock(RandomMinion, pick_minion):
        game.player2.give("KAR_073").play()
    assert len(game.player1.field) == 0
    assert len(game.player2.field) == 1
    assert game.player2.field[0].id == GOLDSHIRE_FOOTMAN


def test_moonglade_portal():
    game = prepare_game()
    game.player1.hero.set_current_health(20)
    assert len(game.player1.field) == 0
    assert game.player1.hero.health == 20

    game.player1.give("KAR_075").play(target=game.player1.hero)
    assert len(game.player1.field) == 1
    assert game.player1.hero.health == 26


def test_firelands_portal():
    game = prepare_game()
    assert len(game.player1.field) == 0
    assert game.player2.hero.health == 30

    game.player1.give("KAR_076").play(target=game.player2.hero)
    assert len(game.player1.field) == 1
    assert game.player1.field[0].cost == 5
    assert game.player2.hero.health == 25


def test_silvermoon_portal():
    game = prepare_game()
    portal = game.player1.give("KAR_077")
    assert not portal.is_playable()
    whelp = game.player1.give(WHELP).play()
    assert len(game.player1.field) == 1
    assert whelp.atk == 1
    assert whelp.health == 1

    portal.play(target=whelp)
    assert len(game.player1.field) == 2
    assert game.player1.field[-1].cost == 2
    game.player1.field[-1].bounce()
    assert whelp.atk == 3
    assert whelp.max_health == 3  # random summon Wild Pyromancer will hit 1
    assert whelp.buff


def test_ironforge_portal():
    game = prepare_game()
    assert game.player1.hero.armor == 0
    assert len(game.player1.field) == 0

    portal = game.player1.give("KAR_091")
    portal.play()
    assert game.player1.hero.armor == 4
    assert len(game.player1.field) == 1
    assert game.player1.field[0].cost == 4


def test_arcane_giant():
    game = prepare_game()
    giant = game.player1.give("KAR_711")
    giant_cost = giant.cost
    assert giant_cost == 12
    game.player1.give(THE_COIN).play()
    assert giant.cost == giant_cost - 1
    game.player1.give(THE_COIN).play()
    assert giant.cost == giant_cost - 2


def test_fools_bane():
    game = prepare_game()
    game.player1.give("KAR_028").play()
    assert game.player1.hero.atk == 3
    assert not game.player1.hero.can_attack()
    game.end_turn()
    for _ in range(7):
        game.player2.give(WISP).play()
    game.end_turn()
    assert game.player1.hero.atk == 3
    assert game.player1.hero.can_attack()
    assert game.player2.hero not in game.player1.hero.attack_targets
    for _ in range(4):
        assert game.player1.hero.can_attack()
        game.player1.hero.attack(game.player2.field[0])
    assert game.player1.weapon is None
    assert not game.player1.hero.can_attack()


def test_spirit_claws():
    game = prepare_game()
    game.player1.give("KAR_063").play()
    assert game.player1.hero.atk == 1
    kobold = game.player1.give(KOBOLD_GEOMANCER).play()
    assert game.player1.hero.atk == 3
    game.player1.give(MOONFIRE).play(target=kobold)
    assert game.player1.hero.atk == 1


def test_moat_lurker():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    lurker = game.player1.give("KAR_041").play(target=wisp)
    game.player1.give(FIREBALL).play(target=lurker)
    wisp = game.player1.field[0]
    assert wisp.id == WISP
    game.end_turn()
    lurker2 = game.player2.give("KAR_041").play(target=wisp)
    assert len(game.player1.field) == 0
    game.player2.give(FIREBALL).play(target=lurker2)
    wisp = game.player1.field[0]
    assert wisp.id == WISP

    game = prepare_game()
    lurker = game.player1.give("KAR_041").play()
    game.player1.give(FIREBALL).play(target=lurker)


def test_ivory_knight():
    game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
    game.player1.hero.set_current_health(1)
    game.player1.give("KAR_057").play()
    for card in game.player1.choice.cards:
        assert (
            CardClass.NEUTRAL in fireplace.cards.db[card].classes
            or CardClass.PALADIN in fireplace.cards.db[card].classes
        )
        assert fireplace.cards.db[card].type == CardType.SPELL

    choice = random.choice(game.player1.choice.cards)
    game.player1.choice.choose(choice)
    assert game.player1.choice is None
    assert len(game.player1.hand) == 1
    assert game.player1.hero.health == min(30, 1 + choice.cost)


def test_prince_malchezaar():
    game = prepare_game(include=("KAR_096",))
    assert len(game.player1.deck) + len(game.player1.hand) == 35
    assert len(game.player2.deck) + len(game.player2.hand) == 36  # The Coin


def test_silverware_golem():
    game = prepare_empty_game()
    game.player1.give("KAR_205")
    game.player1.give(SOULFIRE).play(target=game.player2.hero)
    assert game.player1.field[0].id == "KAR_205"


def test_cat_trick_reveals_once():
    # A secret triggers once, then is gone: a second spell summons nothing.
    game = prepare_game()
    game.player1.give("KAR_004").play()
    game.end_turn()

    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert [m.id for m in game.player1.field] == ["KAR_004a"]
    assert not game.player1.secrets
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert [m.id for m in game.player1.field] == ["KAR_004a"]


def test_cat_trick_full_board():
    game = prepare_game()
    for _ in range(7):
        game.player1.give(WISP).play()
    game.player1.give("KAR_004").play()
    game.end_turn()

    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    assert len(game.player1.field) == 7
    assert [s.id for s in game.player1.secrets] == ["KAR_004"]


def test_babbling_book_mage_spell():
    for _ in range(20):
        game = prepare_empty_game(CardClass.WARRIOR, CardClass.WARRIOR)
        game.player1.give("KAR_009").play()
        spell = game.player1.hand[0]
        assert spell.type == CardType.SPELL
        assert CardClass.MAGE in spell.classes


def test_swashburglar_another_class():
    for _ in range(20):
        game = prepare_empty_game(CardClass.ROGUE, CardClass.MAGE)
        # player1 is whoever goes first, Rogue or Mage.
        game.player1.give("KAR_069").play()
        card = game.player1.hand[0]
        assert any(
            card_class != game.player1.hero.card_class for card_class in card.classes
        )
        assert CardClass.NEUTRAL not in card.classes


def test_arcane_anomaly_after_the_spell():
    # "After you cast a spell": Moonfire kills the 2/1 before the +1 Health.
    game = prepare_game()
    anomaly = game.player1.give("KAR_036")
    anomaly.play()
    game.player1.give(MOONFIRE).play(target=anomaly)
    assert anomaly.dead


def test_atiesh_after_the_spell():
    # "After you cast a spell": Twisting Nether resolves first, the summon survives.
    game = prepare_game()
    game.player1.give("KAR_097").play()
    game.end_turn()
    game.end_turn()
    game.player1.give("EX1_312").play()
    assert len(game.player1.field) == 1
    assert game.player1.field[0].cost == 8
    assert game.player1.weapon.durability == 2


def test_atiesh_final_cost():
    # The final Cost of the spell, Sorcerer's Apprentice included.
    game = prepare_empty_game()
    game.player1.is_standard = False
    game.player1.give("KAR_097").play()
    game.end_turn()
    game.end_turn()
    game.player1.give("EX1_608").play()
    frostbolt = game.player1.give("CS2_024")
    assert frostbolt.cost == 1

    def pick_minion(picker, source):
        pool = picker.find_cards(source)
        assert GOLDSHIRE_FOOTMAN in pool and WISP not in pool
        return [GOLDSHIRE_FOOTMAN]

    with mock(RandomMinion, pick_minion):
        frostbolt.play(target=game.player2.hero)
    assert game.player1.field[-1].id == GOLDSHIRE_FOOTMAN
    assert game.player1.weapon.durability == 2


def test_atiesh_full_board():
    # No room to summon: Atiesh keeps its Durability.
    game = prepare_game()
    game.player1.give("KAR_097").play()
    for _ in range(6):
        game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert len(game.player1.field) == 7
    assert game.player1.weapon.durability == 3


def test_prince_malchezaar_five_different_legendaries_of_his_class():
    starting = ["KAR_096", "EX1_016", "EX1_562"] + [WISP] * 27
    for _ in range(10):
        player1 = Player("Player1", list(starting), CardClass.MAGE.default_hero)
        player2 = Player("Player2", [WISP] * 30, CardClass.WARRIOR.default_hero)
        game = BaseTestGame(players=(player1, player2))
        game.start()
        for player in game.players:
            if player.choice:
                player.choice.choose()
        mage = player1
        added = [c for c in list(mage.deck) + list(mage.hand) if c.id not in starting]
        added = [c for c in added if c.id != THE_COIN]
        assert len(added) == 5
        assert len({c.id for c in added}) == 5
        for card in added:
            assert card.type == CardType.MINION
            assert card.rarity == Rarity.LEGENDARY
            assert CardClass.MAGE in card.classes or CardClass.NEUTRAL in card.classes


def test_barnes_keeps_the_enchantments_of_the_deck_card():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP)
    wisp.shuffle_into_deck()
    game.queue_actions(game.player1, [Buff(wisp, "CS2_009e")])
    assert wisp.taunt
    game.player1.give("KAR_114").play()
    summoned = game.player1.field[-1]
    assert summoned.id == WISP
    assert summoned.taunt
    assert summoned.atk == 1
    assert summoned.health == 1


def test_moat_lurker_resummons_at_the_far_right():
    # hearthstone.wiki.gg: "summons the minion to the far right of the
    # controlling player's board", not where Moat Lurker stood.
    game = prepare_game()
    game.end_turn()
    wisp = game.player2.give(WISP).play()
    game.player2.give("CS2_182").play()
    game.player2.give(CHICKEN).play()
    game.end_turn()
    lurker = game.player1.give("KAR_041")
    lurker.play(target=wisp)
    game.player1.give(FIREBALL).play(target=lurker)
    assert [m.id for m in game.player2.field] == ["CS2_182", CHICKEN, WISP]


def test_moat_lurker_own_minion_far_right():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    game.player1.give("CS2_182").play()
    lurker = game.player1.give("KAR_041")
    lurker.play(target=wisp, index=0)
    game.end_turn()
    game.end_turn()
    game.player1.give(KOBOLD_GEOMANCER).play()
    game.player1.give(FIREBALL).play(target=lurker)
    assert [m.id for m in game.player1.field] == [
        "CS2_182",
        KOBOLD_GEOMANCER,
        WISP,
    ]


def test_ivory_knight_heals_the_base_cost():
    # Under the enemy's Loatheb, the discovered spell costs 5 more: the heal is its base Cost.
    game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
    game.end_turn()
    game.player2.give("FP1_030").play()  # Loatheb
    game.end_turn()
    game.player1.hero.set_current_health(1)
    with mock(RandomSpell, [game.player1.card("CS2_093")]):
        game.player1.give("KAR_057").play()
    choice = game.player1.choice.cards[0]
    base = fireplace.cards.db[choice.id].cost
    game.player1.choice.choose(choice)
    assert choice.cost == base + 5
    assert game.player1.hero.health == 1 + base


def test_arcane_giant_countered_spell_does_not_count():
    game = prepare_game()
    giant = game.player1.give("KAR_711")
    game.end_turn()
    game.player2.give("EX1_287").play()  # Counterspell
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player2.hero.health == 30
    assert giant.cost == 12
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert giant.cost == 11


def test_spirit_claws_enemy_jungle_moonkin():
    # "While you have Spell Damage": the enemy's Jungle Moonkin gives it to both players.
    game = prepare_game()
    game.player1.give("KAR_063").play()
    claws = game.player1.weapon
    assert claws.atk == 1
    game.end_turn()
    moonkin = game.player2.give("LOE_051")
    moonkin.play()
    assert game.player1.spellpower == 2
    assert claws.atk == 3
    game.player2.give(FIREBALL).play(target=moonkin)
    assert moonkin.dead
    assert claws.atk == 1
