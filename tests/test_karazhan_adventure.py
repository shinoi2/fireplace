"""One Night in Karazhan as the official game plays it (Hearthstone WP-123):
the hero powers, the boss cards and the rules of each encounter, the chess
board excepted (WP-123b). What counts: the card's text, then
hearthstone.wiki.gg."""

import pytest
from utils import *
from utils import _empty_mulligan

from fireplace import enums
from fireplace.exceptions import GameOver, InvalidAction


class RealManaGame(CoinRules, BaseGame):
    """A game whose players start at 0 Mana Crystals, as in a real game."""


def _boss_game(hero1, hero2="HERO_08", deck=None, deck2=None, game_class=BaseTestGame):
    """A game where player1 (the first to play) is the boss `hero1`."""
    deck = deck if deck is not None else [WISP] * 20
    deck2 = deck2 if deck2 is not None else [WISP] * 20
    player1 = Player("Player1", list(deck), hero1)
    player2 = Player("Player2", list(deck2), hero2)
    game = game_class(players=(player1, player2))
    game.start()
    _empty_mulligan(game)
    if game.player1 is not player1:
        game.end_turn()
    return game, player1, player2


def db_passive(id):
    return fireplace.cards.db[id].tags.get(enums.PASSIVE_HERO_POWER)


##
# The prologue: An Uninvited Guest (Prince Malchezaar against Medivh)


def test_legion_summons_an_abyssal():
    # Legion: "Hero Power Summon a 6/6 Abyssal."
    for hero in ("KARA_00_01", "KARA_00_01H"):
        game, boss, other = _boss_game(hero)
        assert boss.hero.power.id in ("KARA_00_02", "KARA_00_02H")
        assert not db_passive(boss.hero.power.id)
        boss.hero.power.use()
        assert len(boss.field) == 1 and boss.field[0].id == "KARA_00_02a"
        assert boss.field[0].atk == 6 and boss.field[0].health == 6


def test_malchezaar_starts_with_five_mana_crystals():
    # An Uninvited Guest, Notes: "Prince Malchezaar starts with 5 Mana
    # Crystals." His opponent starts as usual.
    for hero in ("KARA_00_01", "KARA_00_01H"):
        player1 = Player("Player1", [WISP] * 20, hero)
        player2 = Player("Player2", [WISP] * 20, "KARA_00_03")
        game = RealManaGame(players=(player1, player2))
        game.start()
        _empty_mulligan(game)
        boss, other = player1, player2
        if game.current_player is boss:
            assert boss.max_mana == 6
            game.end_turn()
            assert other.max_mana == 1
        else:
            assert other.max_mana == 1
            game.end_turn()
            assert boss.max_mana == 6


def test_brilliance_draws_three():
    # Brilliance (Medivh): "Hero Power Draw 3 cards."
    for hero in ("KARA_00_03", "KARA_00_03H"):
        game, player, other = _boss_game(hero)
        hand = len(player.hand)
        player.hero.power.use()
        assert len(player.hand) == hand + 3


def test_archmages_insight():
    # "Your spells cost (0) this turn."
    game, player, other = _boss_game("KARA_00_03")
    fireball = player.give(FIREBALL)
    wisp = player.give(WISP)
    player.give("KARA_00_05").play()
    assert fireball.cost == 0
    player.give(PYROBLAST)
    assert player.hand[-1].cost == 0
    assert wisp.cost == 0 and player.give("CS2_182").cost == 4
    game.end_turn()
    game.end_turn()
    assert fireball.cost == 4


def test_arcane_power():
    # "You have Spell Damage +5 this turn."
    game, player, other = _boss_game("KARA_00_03")
    player.give("KARA_00_06").play()
    assert player.spellpower == 5
    player.give(MOONFIRE).play(target=other.hero)
    assert other.hero.health == 30 - 6
    game.end_turn()
    assert player.spellpower == 0


def test_astral_portal():
    # "Summon a random Legendary minion."
    game, player, other = _boss_game("KARA_00_03")
    player.give("KARA_00_07").play()
    assert len(player.field) == 1
    assert player.field[0].rarity == Rarity.LEGENDARY


def test_archmages_apprentice():
    # "Whenever you cast a spell, shuffle a copy of it into your deck."
    game, player, other = _boss_game("KARA_00_03")
    player.give("KARA_00_08").play()
    deck = len(player.deck)
    player.give(MOONFIRE).play(target=other.hero)
    assert len(player.deck) == deck + 1
    assert player.deck.filter(id=MOONFIRE)
    # Not the enemy's spells.
    game.end_turn()
    other.give(MOONFIRE).play(target=player.hero)
    assert len(player.deck) == deck + 1


def test_mage_armor():
    # "Gain 10 Armor."
    game, player, other = _boss_game("KARA_00_03")
    player.give("KARA_00_09").play()
    assert player.hero.armor == 10


def test_mysterious_rune():
    # "Put 5 random Mage Secrets into the battlefield."
    game, player, other = _boss_game("KARA_00_03")
    player.give("KARA_00_10").play()
    assert len(player.secrets) == 5
    assert len({s.id for s in player.secrets}) == 5
    for secret in player.secrets:
        assert secret.card_class == CardClass.MAGE


def test_guardians_evocation():
    # "Gain 5 Mana Crystals this turn only."
    player1 = Player("Player1", [WISP] * 20, "KARA_00_03")
    player2 = Player("Player2", [WISP] * 20, "HERO_08")
    game = RealManaGame(players=(player1, player2))
    game.start()
    _empty_mulligan(game)
    player = game.current_player
    player.give("KARA_00_11").play()
    assert player.mana == 1 + 5
    game.end_turn()
    game.end_turn()
    assert player.mana == 2


##
# The Parlor: Silverware Golem, Magic Mirror

PLATE = "KAR_A02_01"


def _plates(player):
    return player.field.filter(id=PLATE)


def test_be_our_guest():
    # "Hero Power Summon a 1/1 Plate." (heroic: "two 1/1 Plates")
    for hero, count in (("KAR_A02_12", 1), ("KAR_A02_12H", 2)):
        game, boss, other = _boss_game(hero)
        assert not db_passive(boss.hero.power.id)
        boss.hero.power.use()
        assert len(_plates(boss)) == count
        assert _plates(boss)[0].atk == 1 and _plates(boss)[0].health == 1


def test_silverware_auras():
    # Cup: "Plates have +1 Attack." (heroic +3) ; Fork: "Plates have
    # Charge." ; Knife: "Plates have Taunt."
    for cup, more in (("KAR_A02_05", 1), ("KAR_A02_05H", 3)):
        game, boss, other = _boss_game("KAR_A02_12")
        plate = boss.summon(PLATE)
        wisp = boss.summon(WISP)
        boss.summon(cup)
        assert plate.atk == 1 + more and wisp.atk == 1
        enemy_plate = other.summon(PLATE)
        assert enemy_plate.atk == 1
    for fork in ("KAR_A02_03", "KAR_A02_03H"):
        game, boss, other = _boss_game("KAR_A02_12")
        boss.summon(fork)
        plate = boss.summon(PLATE)
        assert plate.charge and plate.can_attack()
        assert not boss.field[0].charge
    for knife in ("KAR_A02_04", "KAR_A02_04H"):
        game, boss, other = _boss_game("KAR_A02_12")
        boss.summon(knife)
        plate = boss.summon(PLATE)
        assert plate.taunt and not boss.field[0].taunt


def test_pitcher():
    # Pitcher (heroic): "Battlecry: Give a minion +3/+3."
    game, boss, other = _boss_game("KAR_A02_12H")
    wisp = boss.summon(WISP)
    boss.give("KAR_A02_06H").play(target=wisp)
    assert wisp.atk == 4 and wisp.health == 4


def test_set_the_table_pour_a_round_tossing_plates():
    # Tossing Plates: "Summon five 1/1 Plates." ; Set the Table: "Give your
    # Plates +1/+1." (heroic +2/+2) ; Pour a Round: "Draw a card for each of
    # your Plates."
    game, boss, other = _boss_game("KAR_A02_12")
    boss.give("KAR_A02_11").play()
    assert len(_plates(boss)) == 5
    boss.give("KAR_A02_09").play()
    assert all(p.atk == 2 and p.health == 2 for p in _plates(boss))
    game.end_turn()
    game.end_turn()
    boss.give("KAR_A02_09H").play()
    assert all(p.atk == 4 and p.health == 4 for p in _plates(boss))
    for card in list(boss.hand):
        card.discard()
    boss.give("KAR_A02_10").play()
    assert len(boss.hand) == 5


def test_reflections_normal_copies_for_whoever_plays():
    # Magic Mirror: "Passive Hero Power Whenever a minion is played, summon a
    # 1/1 copy of it." In normal, each player gets the copy of the minion he
    # plays; in heroic, "Magic Mirror summons a 1/1 copy of it".
    game, boss, other = _boss_game("KAR_A01_01")
    assert db_passive("KAR_A01_02")
    with pytest.raises(InvalidAction):
        boss.hero.power.use()
    boss.give("CS2_182").play()
    assert len(boss.field) == 2
    copy = boss.field[1]
    assert copy.id == "CS2_182" and copy.atk == 1 and copy.health == 1
    game.end_turn()
    other.give("CS2_182").play()
    assert len(other.field) == 2 and len(boss.field) == 2
    assert other.field[1].atk == 1 and other.field[1].health == 1
    # A summoned minion is not played.
    other.summon(WISP)
    assert len(other.field) == 3 and len(boss.field) == 2


def test_reflections_heroic_copies_for_the_mirror():
    game, boss, other = _boss_game("KAR_A01_01H")
    assert db_passive("KAR_A01_02H")
    game.end_turn()
    other.give("CS2_182").play()
    assert len(other.field) == 1 and len(boss.field) == 1
    assert boss.field[0].id == "CS2_182" and boss.field[0].atk == 1
    game.end_turn()
    boss.give(WISP).play()
    assert len(boss.field) == 3


##
# The Parlor: Chess (the White King, the player, against the Black King)

WHITE_PAWN, WHITE_BISHOP, WHITE_ROOK, WHITE_KNIGHT, WHITE_QUEEN = (
    "KAR_A10_02",
    "KAR_A10_05",
    "KAR_A10_04",
    "KAR_A10_08",
    "KAR_A10_09",
)
BLACK_PAWN, BLACK_BISHOP, BLACK_ROOK, BLACK_KNIGHT, BLACK_QUEEN = (
    "KAR_A10_01",
    "KAR_A10_06",
    "KAR_A10_03",
    "KAR_A10_07",
    "KAR_A10_10",
)
WHITE_PIECES = (WHITE_PAWN, WHITE_BISHOP, WHITE_ROOK, WHITE_KNIGHT, WHITE_QUEEN)


def _chess(
    white="KAR_a10_Boss1",
    black="KAR_a10_Boss2",
    deck=None,
    deck2=None,
    game_class=BaseTestGame,
):
    """A chess game where the White King (`white`) plays first; the pieces
    stay in the decks (a side without any piece loses)."""
    deck = deck if deck is not None else [WHITE_PAWN] * 20
    deck2 = deck2 if deck2 is not None else [BLACK_PAWN] * 20
    return _boss_game(white, black, deck, deck2, game_class)


def _board(player, *ids):
    return [player.summon(id) for id in ids]


def test_chess_pieces_auto_attack_the_minion_opposite():
    # Pawn, Rook, Queen: "Auto-Attack: Deal 1 (2, 4) damage to the enemies
    # opposite this minion." The wiki (Auto-Attack, Notes): "Chess minions with
    # Auto-Attack cannot be commanded to attack. Instead, they deal damage
    # automatically at the end of the owner's turn to those of the opponent's
    # minions across from them" ; "Chess-related Auto-Attack is a positional
    # effect, and does not cause the minions to take retaliatory damage".
    for piece, amount in ((WHITE_PAWN, 1), (WHITE_ROOK, 2), (WHITE_QUEEN, 4)):
        game, white, black = _chess()
        (mine,) = _board(white, piece)
        (theirs,) = _board(black, BLACK_QUEEN)
        assert mine.cant_attack and not mine.can_attack()
        game.end_turn()
        assert theirs.damage == amount
        assert mine.damage == 0
        assert black.hero.damage == 0
        # The Black Queen, at the end of the Black King's turn.
        game.end_turn()
        assert mine.damage == 4
        assert white.hero.damage == 0


def test_chess_pieces_strike_both_enemies_across():
    # The wiki (Auto-Attack, Notes): "If one player has an odd number of
    # minions and the other player has an even number, chess Auto-Attack
    # minions will deal damage to both minions "diagonally" across from them. A
    # minion on the edge of the line may only have one minion diagonally across
    # from it." Moroes: "If a piece is in between two enemies, it will strike
    # them both!"
    game, white, black = _chess()
    (pawn,) = _board(white, WHITE_PAWN)
    left, right = _board(black, BLACK_ROOK, BLACK_ROOK)
    game.end_turn()
    assert (left.damage, right.damage) == (1, 1)
    assert black.hero.damage == 0
    # Three against two: the edges strike one, the middle strikes both.
    game, white, black = _chess()
    _board(white, WHITE_PAWN, WHITE_ROOK, WHITE_PAWN)
    left, right = _board(black, BLACK_ROOK, BLACK_ROOK)
    game.end_turn()
    assert left.damage == 1 + 2
    assert right.damage == 2 + 1
    assert black.hero.damage == 0


def test_chess_pieces_strike_the_hero_when_nothing_is_across():
    # The wiki (Auto-Attack, Notes): "If a chess Auto-Attack minion has no
    # minions directly or diagonally across from it, it will deal damage to the
    # enemy hero."
    game, white, black = _chess()
    _board(white, WHITE_PAWN, WHITE_ROOK, WHITE_QUEEN)
    (middle,) = _board(black, BLACK_ROOK)
    game.end_turn()
    assert middle.damage == 2
    assert black.hero.damage == 1 + 4
    game, white, black = _chess()
    _board(white, WHITE_QUEEN)
    game.end_turn()
    assert black.hero.damage == 4


def test_chess_auto_attacks_resolve_before_any_death():
    # The wiki (Auto-Attack, Notes): "minions which have taken fatal damage will
    # not be removed until all pieces have completed their auto-attacks." The
    # positions do not change in between: the middle Pawn strikes both Black
    # Pawns, the right Pawn the right one, and the Black King nothing.
    game, white, black = _chess()
    _board(white, WHITE_PAWN, WHITE_PAWN, WHITE_PAWN)
    dying, other = _board(black, BLACK_PAWN, BLACK_PAWN)
    dying.damage = 5
    game.end_turn()
    assert dying.dead or dying.zone == Zone.GRAVEYARD
    assert list(black.field) == [other]
    assert other.damage == 2
    assert black.hero.damage == 0


def test_chess_bishops_restore_adjacent_minions():
    # Bishop: "Auto-Attack: Restore #2 Health to adjacent minions." The wiki (A
    # Friendly Game of Chess, Notes): "[Bishops] do not attack at all, but
    # instead restore Health. They do not follow the usual Auto-Attack rules for
    # targeting, instead healing minions to their immediate left and right."
    # (Knights around it: they have no Auto-Attack.)
    for bishop, knight in ((WHITE_BISHOP, WHITE_KNIGHT), (BLACK_BISHOP, BLACK_KNIGHT)):
        game, white, black = _chess()
        side = white if bishop == WHITE_BISHOP else black
        if side is black:
            game.end_turn()
        left, middle, right, far = _board(side, knight, bishop, knight, knight)
        left.damage, right.damage, far.damage = 2, 1, 1
        game.end_turn()
        assert (left.damage, right.damage, far.damage) == (0, 0, 1)
        assert side.opponent.hero.damage == 0
        assert middle.cant_attack and not middle.can_attack()


def test_chess_black_pieces_auto_attack_too():
    game, white, black = _chess()
    game.end_turn()
    _board(black, BLACK_PAWN, BLACK_ROOK, BLACK_QUEEN)
    (middle,) = _board(white, WHITE_ROOK)
    game.end_turn()
    assert middle.damage == 2
    assert white.hero.damage == 1 + 4


def test_chess_knights_charge_but_never_at_a_hero():
    # Knight: "Charge. Can't Attack Heroes." No Auto-Attack: it attacks as any
    # minion, and not at the end of the turn.
    for knight in (WHITE_KNIGHT, BLACK_KNIGHT):
        game, white, black = _chess()
        side = white if knight == WHITE_KNIGHT else black
        if side is black:
            game.end_turn()
        side.give(knight).play()
        piece = side.field[0]
        assert piece.charge and not piece.cant_attack
        # Nothing to attack but the King: it cannot.
        assert not piece.can_attack() and not piece.can_attack(side.opponent.hero)
        (enemy,) = _board(side.opponent, WHITE_ROOK if side is black else BLACK_ROOK)
        assert piece.can_attack() and piece.can_attack(enemy)
        assert not piece.can_attack(side.opponent.hero)
        # It attacks the Rook, which strikes back; at the end of the turn, the
        # Knight does nothing more.
        piece.attack(enemy)
        assert enemy.damage == 4 and piece.damage == 2
        game.end_turn()
        assert enemy.damage == 4 and side.opponent.hero.damage == 0


def test_cheat_destroys_the_left_most_enemy_minion():
    # Cheat (the Black King, both modes): "Hero Power Destroy the left-most
    # enemy minion." Without an enemy minion, it cannot be used.
    for king in ("KAR_a10_Boss2", "KAR_a10_Boss2H"):
        game, white, black = _chess(black=king)
        game.end_turn()
        assert black.hero.power.id == "KAR_A10_33" and black.hero.power.cost == 2
        assert not black.hero.power.is_usable()
        left, right = _board(white, WHITE_ROOK, WHITE_QUEEN)
        assert black.hero.power.is_usable()
        black.hero.power.use()
        assert list(white.field) == [right]
        assert left.zone == Zone.GRAVEYARD
        assert not black.hero.power.is_usable()


def test_castle_discovers_a_chess_piece():
    # Castle (the White King, normal): "Hero Power Discover a chess piece." Three
    # of the five white pieces.
    game, white, black = _chess()
    power = white.hero.power
    assert power.id == "KAR_A10_22" and power.cost == 2
    hand = len(white.hand)
    power.use()
    choice = white.choice
    ids = [c.id for c in choice.cards]
    assert len(ids) == 3 and len(set(ids)) == 3
    assert set(ids) <= set(WHITE_PIECES)
    choice.choose(choice.cards[1])
    assert len(white.hand) == hand + 1 and white.hand[-1].id == ids[1]
    assert not power.is_usable()


def test_castle_heroic_moves_a_friendly_minion_left():
    # Castle (the White King, heroic): "Hero Power Move a friendly minion left.
    # Repeatable." (1 Mana each time)
    game, white, black = _chess(white="KAR_a10_Boss1H")
    power = white.hero.power
    assert power.id == "KAR_A10_22H" and power.cost == 1
    a, b, c = _board(white, WHITE_PAWN, WHITE_ROOK, WHITE_QUEEN)
    (enemy,) = _board(black, BLACK_PAWN)
    mana = white.mana
    assert enemy not in power.targets and white.hero not in power.targets
    power.use(target=c)
    assert list(white.field) == [a, c, b]
    power.use(target=c)
    assert list(white.field) == [c, a, b]
    # The left-most one stays where it is.
    power.use(target=c)
    assert list(white.field) == [c, a, b]
    assert white.mana == mana - 3
    assert power.is_usable()
    # Where they stand is where they strike: the Pawn faces the Black Pawn now,
    # the Queen and the Rook the Black King.
    game.end_turn()
    assert enemy.damage == 1
    assert black.hero.damage == 4 + 2


def test_chess_a_side_without_pieces_loses():
    # Moroes (Chess): "You don't have many pieces. If you run out, you will
    # lose." ; "You have run out of pieces. The game is forfeit." A piece is a
    # minion on the board, in the hand or in the deck.
    for king in ("KAR_a10_Boss1", "KAR_a10_Boss1H"):
        game, white, black = _chess(white=king, deck=[])
        game.end_turn()
        (last,) = _board(white, WHITE_ROOK)
        assert not white.deck and all(c.type != CardType.MINION for c in white.hand)
        with pytest.raises(GameOver):
            black.hero.power.use()
        assert white.playstate == PlayState.LOST
        assert black.playstate == PlayState.WON
    # One left in the hand: the game goes on.
    game, white, black = _chess(deck=[])
    game.end_turn()
    _board(white, WHITE_ROOK)
    white.give(WHITE_PAWN)
    black.hero.power.use()
    assert game.state != State.COMPLETE and white.playstate == PlayState.PLAYING
    # The Black King too, when his last piece falls to an Auto-Attack.
    for king in ("KAR_a10_Boss2", "KAR_a10_Boss2H"):
        game, white, black = _chess(black=king, deck2=[])
        _board(white, WHITE_QUEEN)
        (last,) = _board(black, BLACK_PAWN)
        last.damage = 2
        with pytest.raises(GameOver):
            game.end_turn()
        assert black.playstate == PlayState.LOST
        assert white.playstate == PlayState.WON


def test_chess_both_sides_without_pieces_no_draw():
    # The last White Knight and the last Black Pawn fall together: the deaths
    # are processed one by one, in the order they entered play, as fireplace
    # does for two heroes; the side of the first one loses.
    for first in ("white", "black"):
        game, white, black = _chess(deck=[], deck2=[])
        if first == "white":
            (knight,) = _board(white, WHITE_KNIGHT)
            (pawn,) = _board(black, BLACK_PAWN)
        else:
            (pawn,) = _board(black, BLACK_PAWN)
            (knight,) = _board(white, WHITE_KNIGHT)
        knight.damage, pawn.damage = 2, 2
        with pytest.raises(GameOver):
            knight.attack(pawn)
        loser, winner = (white, black) if first == "white" else (black, white)
        assert loser.playstate == PlayState.LOST
        assert winner.playstate == PlayState.WON


HEROIC_WHITE_DECK = (
    [WHITE_PAWN] * 8
    + [WHITE_BISHOP] * 2
    + [WHITE_ROOK] * 2
    + [WHITE_KNIGHT] * 2
    + [WHITE_QUEEN]
)
HEROIC_BLACK_DECK = (
    [BLACK_PAWN] * 8
    + [BLACK_BISHOP] * 2
    + [BLACK_ROOK] * 2
    + [BLACK_KNIGHT] * 2
    + [BLACK_QUEEN]
    + [BLACK_PAWN] * 15
)


def test_heroic_black_king_keeps_fifteen_pawns_at_the_bottom():
    # The wiki (Chess, Decks): "On Heroic the number of each card in the
    # player's deck is halved, resulting in a deck of just 15 cards. The Black
    # King's deck matches the player's deck, but has an additional 15 Pawns at
    # the bottom of the deck." They stay there through the mulligan and every
    # shuffle.
    for game_class in (Game, BaseTestGame):
        white = Player("White", list(HEROIC_WHITE_DECK), "KAR_a10_Boss1H")
        black = Player("Black", list(HEROIC_BLACK_DECK), "KAR_a10_Boss2H")
        game = game_class(players=(white, black))
        game.start()
        if black.choice:
            # The mulligan: the Black King sends every card back.
            black.choice.choose(*black.choice.cards)
            white.choice.choose()
        bottom = [c for c in black.deck if getattr(c, "stays_at_bottom", False)]
        assert len(bottom) == 15 and all(c.id == BLACK_PAWN for c in bottom)
        assert list(black.deck[: len(bottom)]) == bottom
        assert not any(getattr(c, "stays_at_bottom", False) for c in black.hand)
        black.shuffle_deck()
        assert set(black.deck[:15]) == set(bottom)
        # The other cards are drawn first.
        while len(black.deck) > 15:
            assert not getattr(black.draw(), "stays_at_bottom", False)
        assert black.draw() in bottom
    # Normal: no card is kept at the bottom.
    game, white, black = _chess(black="KAR_a10_Boss2", deck2=HEROIC_BLACK_DECK)
    assert not any(getattr(c, "stays_at_bottom", False) for c in black.deck)


def test_heroic_black_king_is_never_fatigued():
    # Black King (Heroic): CANT_BE_FATIGUED. The normal one is.
    for king, fatigued in (("KAR_a10_Boss2H", False), ("KAR_a10_Boss2", True)):
        game, white, black = _chess(black=king, deck2=[])
        before = black.hero.damage
        game.end_turn()
        assert game.current_player is black
        assert (black.hero.damage > before) == fatigued
        if not fatigued:
            assert black.hero.damage == 0


def test_chess_rules_are_the_kings_only():
    # Another hero whose last minion dies does not lose.
    game, white, black = _chess(black="HERO_08", deck2=[WISP] * 20)
    game.end_turn()
    (wisp,) = _board(black, WISP)
    game.end_turn()
    for card in list(black.hand) + list(black.deck):
        card.zone = Zone.SETASIDE
    white.give(WHITE_KNIGHT).play()
    white.field[-1].attack(wisp)
    assert game.state != State.COMPLETE


##
# The Opera: Romulo and Julianne, Big Bad Wolf, The Crone


def test_true_love_and_romulo():
    # True Love: "Hero Power If you don't have Romulo, summon him." ;
    # Romulo: "Julianne is Immune."
    for hero, romulo in (
        ("KARA_06_02", "KARA_06_01"),
        ("KARA_06_02heroic", "KARA_06_01heroic"),
    ):
        game, boss, other = _boss_game(hero)
        assert boss.hero.power.is_usable()
        boss.hero.power.use()
        assert len(boss.field) == 1 and boss.field[0].id == romulo
        assert boss.hero.immune
        game.end_turn()
        game.end_turn()
        # He is there: the Hero Power has nothing to do.
        assert not boss.hero.power.is_usable()
        game.end_turn()
        other.give(FIREBALL).play(target=boss.field[0])
        assert not boss.field
        assert not boss.hero.immune
        other.give(MOONFIRE).play(target=boss.hero)
        assert boss.hero.health == 14
        game.end_turn()
        assert boss.hero.power.is_usable()


def test_trembling():
    # Big Bad Wolf: "Passive Hero Power Enemy minions are 1/1 and cost (1)."
    # Heroic: "Minions cost (1). Enemy minions are 1/1."
    game, boss, other = _boss_game("KARA_05_01h")
    assert db_passive("KARA_05_01hp")
    with pytest.raises(InvalidAction):
        boss.hero.power.use()
    yeti = other.give("CS2_182")
    mine = boss.give("CS2_182")
    assert yeti.cost == 1 and mine.cost == 4
    game.end_turn()
    yeti.play()
    assert yeti.atk == 1 and yeti.health == 1
    assert other.give(FIREBALL).cost == 4
    game.end_turn()
    mine.play()
    assert mine.atk == 4 and mine.health == 5

    game, boss, other = _boss_game("KARA_05_01hheroic")
    assert db_passive("KARA_05_01hpheroic")
    mine = boss.give("CS2_182")
    yeti = other.give("CS2_182")
    assert mine.cost == 1 and yeti.cost == 1
    mine.play()
    assert mine.atk == 4 and mine.health == 5


def test_twister_and_dorothee():
    # Twister: "Hero Power Deal 100 damage. Can't be used if Dorothee is
    # alive." The wiki: "Twister always targets the player's hero, even if
    # they have Elusive." Dorothee: "Minions to the left have Charge. Minions
    # to the right have Taunt."
    for hero in ("KARA_04_01h", "KARA_04_01heroic"):
        game, boss, other = _boss_game(hero)
        dorothee = other.summon("KARA_04_01")
        assert not boss.hero.power.requires_target()
        assert not boss.hero.power.is_usable()
        game.end_turn()
        left = other.give("CS2_182")
        left.play(index=0)
        right = other.give("CS2_182")
        right.play(index=2)
        assert other.field == [left, dorothee, right]
        assert left.charge and not left.taunt
        assert right.taunt and not right.charge
        assert not dorothee.charge and not dorothee.taunt
        game.end_turn()
        boss.give(FIREBALL).play(target=dorothee)
        boss.give(FIREBALL).play(target=dorothee)
        assert dorothee.dead
        assert boss.hero.power.is_usable()
        with pytest.raises(GameOver):
            boss.hero.power.use()
        assert other.playstate == PlayState.LOST


##
# The Menagerie: Curator, Nightbane, Terestian Illhoof


def test_gallery_protection():
    # Curator: "Passive Hero Power Your hero has Taunt."
    for hero in ("KARA_07_01", "KARA_07_01heroic"):
        game, boss, other = _boss_game(hero)
        assert db_passive("KARA_07_02")
        assert boss.hero.taunt
        wisp = boss.summon(WISP)
        game.end_turn()
        yeti = other.summon("CS2_182")
        yeti.turns_in_play = 1
        assert boss.hero in yeti.attack_targets
        assert wisp not in yeti.attack_targets


def test_curator_escapes():
    # "Summon a random Murloc." (heroic: "two random Murlocs") ; Beast,
    # Demon, Mech, Dragon.
    for card, race, count in (
        ("KARA_07_03", Race.MURLOC, 1),
        ("KARA_07_03heroic", Race.MURLOC, 2),
        ("KARA_07_05", Race.BEAST, 1),
        ("KARA_07_05heroic", Race.BEAST, 1),
        ("KARA_07_06", Race.DEMON, 1),
        ("KARA_07_06heroic", Race.DEMON, 1),
        ("KARA_07_07", Race.MECHANICAL, 1),
        ("KARA_07_07heroic", Race.MECHANICAL, 1),
        ("KARA_07_08", Race.DRAGON, 1),
        ("KARA_07_08heroic", Race.DRAGON, 1),
    ):
        game, boss, other = _boss_game("KARA_07_01")
        boss.give(card).play()
        assert len(boss.field) == count, card
        for minion in boss.field:
            assert minion.race == race or race in getattr(minion, "races", ()), card


def test_manastorm():
    # Nightbane: "Passive Hero Power Players start with 10 Mana Crystals."
    for hero in ("KARA_11_01", "KARA_11_01heroic"):
        player1 = Player("Player1", [WISP] * 20, hero)
        player2 = Player("Player2", [WISP] * 20, "HERO_08")
        game = RealManaGame(players=(player1, player2))
        game.start()
        _empty_mulligan(game)
        assert db_passive("KARA_11_02")
        first = game.current_player
        assert first.max_mana == 10 and first.mana == 10
        game.end_turn()
        assert first.opponent.max_mana == 10 and first.opponent.mana == 10


def test_dark_pact_and_icky_imps():
    # Terestian Illhoof: "Passive Hero Power Only Icky Imps can damage
    # Illhoof!" ; Icky Imp: "Deathrattle: Resummon this minion and Illhoof
    # loses 2 Health." ; Many Imps!: "Summon 2 Icky Imps."
    for hero, many, imp in (
        ("KARA_09_01", "KARA_09_03", "KARA_09_03a"),
        ("KARA_09_01heroic", "KARA_09_03heroic", "KARA_09_03a_heroic"),
    ):
        game, boss, other = _boss_game(hero)
        assert db_passive("KARA_09_04")
        health = boss.hero.health
        boss.give(many).play()
        assert [m.id for m in boss.field] == [imp, imp]
        game.end_turn()
        other.give(FIREBALL).play(target=boss.hero)
        assert boss.hero.health == health
        other.give(FIREBALL).play(target=boss.field[0])
        assert boss.hero.health == health - 2
        assert [m.id for m in boss.field] == [imp, imp]
        assert other.hero.health == 30


def test_illhoofs_spells():
    # Summon Kil'rek ; Shadow Volley: "Deal $3 damage to all non-Demon
    # minions." ; Steal Life: "Deal $5 damage. Restore #5 Health to your
    # hero."
    for suffix, kilrek in (("", "KARA_09_08"), ("heroic", "KARA_09_08_heroic")):
        game, boss, other = _boss_game("KARA_09_01")
        boss.give("KARA_09_05" + suffix).play()
        assert boss.field[-1].id == kilrek
        yeti = other.summon("CS2_182")
        imp = other.summon(IMP)
        game.end_turn()
        game.end_turn()
        boss.give("KARA_09_06" + suffix).play()
        assert yeti.damage == 3 and imp.damage == 0 and boss.field[0].damage == 0
        game.end_turn()
        game.end_turn()
        boss.hero.set_current_health(20)
        boss.give("KARA_09_07" + suffix).play(target=other.hero)
        assert other.hero.health == 25
        assert boss.hero.health == 25


##
# The Spire: Shade of Aran, Netherspite


def test_ley_lines():
    # "Passive Hero Power Both players have Spell Damage +3." (heroic +5)
    for hero, more in (("KARA_12_01", 3), ("KARA_12_01H", 5)):
        game, boss, other = _boss_game(hero)
        assert db_passive(boss.hero.power.id)
        assert boss.spellpower == more and other.spellpower == more
        boss.give(MOONFIRE).play(target=other.hero)
        assert other.hero.health == 30 - 1 - more


def test_flame_wreath():
    # "Secret: When an enemy attacks, deal 5 damage to all other enemies."
    # (heroic 10) ; immune to Spell Damage (Ley Lines).
    for hero, secret, damage in (
        ("KARA_12_01", "KARA_12_03", 5),
        ("KARA_12_01H", "KARA_12_03H", 10),
    ):
        game, boss, other = _boss_game(hero)
        boss.give(secret).play()
        assert len(boss.secrets) == 1
        game.end_turn()
        attacker = other.summon("CS2_182")
        attacker.turns_in_play = 1
        bystander = other.summon("EX1_620")  # Molten Giant, 8/8
        attacker.attack(boss.hero)
        assert not boss.secrets
        assert bystander.dead if damage >= 8 else bystander.damage == damage
        assert other.hero.health == 30 - damage
        assert attacker.damage == 0


def test_nether_rage():
    # "Hero Power Give your hero +3 Attack this turn." (heroic +8, 1 mana)
    for hero, more in (("KARA_08_01", 3), ("KARA_08_01H", 8)):
        game, boss, other = _boss_game(hero)
        boss.hero.power.use()
        assert boss.hero.atk == more
        boss.hero.attack(other.hero)
        assert other.hero.health == 30 - more
        game.end_turn()
        assert boss.hero.atk == 0


def test_nether_breath_and_terrifying_roar():
    # Nether Breath: "Change the Health of all enemy minions to 1." ;
    # Terrifying Roar: "Return an enemy minion to your opponent's hand."
    for suffix in ("", "H"):
        game, boss, other = _boss_game("KARA_08_01")
        yeti = other.summon("CS2_182")
        giant = other.summon("EX1_620")
        mine = boss.summon("CS2_182")
        boss.give("KARA_08_03" + suffix).play()
        assert yeti.health == 1 and giant.health == 1 and mine.health == 5
        boss.give("KARA_08_05" + suffix).play(target=yeti)
        assert yeti.zone == Zone.HAND and yeti.controller is other


BLUE, RED = "KARA_08_06", "KARA_08_08"


def test_netherspites_portals():
    # Blue Portal: "The character in the blue beam only takes 1 damage at a
    # time." Red Portal: "The character in the red beam has Windfury." The
    # portals stand at the ends of the player's board, Blue on the left, Red
    # on the right; each beam runs from its portal across the board (the wiki:
    # a beam goes on "to the next non-dormant minion"), and hits Netherspite
    # when no minion is in its path.
    game, boss, other = _boss_game("KARA_08_01")
    blue = other.summon(BLUE)
    red = other.summon(RED)
    assert blue.dormant and red.dormant
    # No minion: both beams on Netherspite.
    assert boss.hero.heavily_armored and boss.hero.windfury
    boss.give(FIREBALL).play(target=other.hero)
    game.end_turn()
    other.give(FIREBALL).play(target=boss.hero)
    assert boss.hero.health == 29
    # A minion on the right of the Red Portal: the blue beam, not the red one.
    right = other.give("CS2_182")
    right.play(index=2)
    assert right.heavily_armored and not right.windfury
    assert not boss.hero.heavily_armored and boss.hero.windfury
    game.end_turn()
    game.end_turn()
    # A minion between them takes both beams.
    middle = other.give("CS2_182")
    middle.play(index=1)
    assert other.field == [blue, middle, red, right]
    assert middle.heavily_armored and middle.windfury
    assert not right.heavily_armored
    assert not boss.hero.heavily_armored and not boss.hero.windfury
    other.give(FIREBALL).play(target=middle)
    assert middle.damage == 1
    # The portals are permanent: no spell, no attack, no board clear.
    game.end_turn()
    boss.give("EX1_312").play()  # Twisting Nether
    assert other.field == [blue, red]


##
# The Spire: Free Medivh! (Nazra Wildaxe, then Prince Malchezaar)

TWISTING_NETHER = "EX1_312"
PHASE_DECK = [TWISTING_NETHER] + ["CS2_182"] * 29


def test_the_horde():
    # "Hero Power Summon a 3/2 Orc." (heroic: "a 3/3 Orc with Charge")
    for hero, orc in (("KARA_13_01", "KARA_13_03"), ("KARA_13_01H", "KARA_13_03H")):
        game, boss, other = _boss_game(hero)
        boss.hero.power.use()
        assert [m.id for m in boss.field] == [orc]
    assert not fireplace.cards.db["KARA_13_03"].tags.get(GameTag.CHARGE)
    assert fireplace.cards.db["KARA_13_03H"].tags.get(GameTag.CHARGE)


def test_malchezaars_cards():
    # Legion: "Summon a 6/6 Abyssal." (heroic: "two 6/6 Abyssals") ; Shadow
    # Bolt Volley: "Deal $4 damage to three random enemies." ; Demonic
    # Presence: "Draw 2 cards. Gain 10 Armor." (heroic: "Draw 3 cards.")
    for hero, count in (("KARA_13_06", 1), ("KARA_13_06H", 2)):
        game, boss, other = _boss_game(hero)
        # (The test game gives 10 crystals after his first turn has begun.)
        boss.used_mana = 0
        boss.hero.power.use()
        assert [m.id for m in boss.field] == ["KARA_00_02a"] * count
    game, boss, other = _boss_game("KARA_13_06")
    minions = [other.summon("EX1_620") for _ in range(3)]
    boss.give("KARA_13_11").play()
    hit = [m for m in minions if m.damage == 4] + (
        [other.hero] if other.hero.damage == 4 else []
    )
    assert len(hit) == 3
    for card, draws in (("KARA_13_12", 2), ("KARA_13_12H", 3)):
        game, boss, other = _boss_game("KARA_13_06")
        hand = len(boss.hand)
        boss.give(card).play()
        assert len(boss.hand) == hand + draws
        assert boss.hero.armor == 10


def test_nazra_falls_malchezaar_appears():
    # The wiki (Free Medivh!, Overview): "Destroying Nazra Wildaxe removes her
    # weapon and all minions from her side of the board, but does not
    # activate any of their Deathrattles." Prince Malchezaar appears "with
    # full Health [...], 8 mana (10 mana in Heroic mode), and a fresh deck and
    # hand of cards; notably, he always draws Twisting Nether at the start of
    # his turn." "When Prince Malchezaar appears, Medivh equips the player
    # with Atiesh."
    for nazra, prince, mana in (
        ("KARA_13_01", "KARA_13_06", 8),
        ("KARA_13_01H", "KARA_13_06H", 10),
    ):
        game, boss, other = _boss_game(nazra, game_class=RealManaGame)
        boss.next_phase_deck = list(PHASE_DECK)
        boss.summon(
            "FP1_001"
        )  # Zombie Chow: Deathrattle, restore 5 Health to the enemy hero
        boss.summon("CS2_106")  # Fiery War Axe
        old_hand = list(boss.hand)
        game.end_turn()
        other.max_mana, other.used_mana = 10, 0
        other.hero.set_current_health(20)
        boss.hero.set_current_health(3)
        other.give(FIREBALL).play(target=boss.hero)
        assert game.state != State.COMPLETE and boss.playstate == PlayState.PLAYING
        assert boss.hero.id == prince
        assert boss.hero.health == 30 and boss.hero.damage == 0
        assert boss.hero.power.id in ("KARA_13_13", "KARA_13_13H")
        assert not boss.field and boss.weapon is None
        assert other.hero.health == 20  # no Deathrattle
        assert not any(c in boss.hand for c in old_hand)
        assert len(boss.hand) == 3
        assert TWISTING_NETHER not in [c.id for c in boss.hand]
        assert all(c.id in PHASE_DECK for c in boss.hand)
        assert len(boss.deck) == len(PHASE_DECK) - 3
        assert other.weapon is not None and other.weapon.id == "KARA_13_26"
        # His turn: 8 mana (10 in heroic), and Twisting Nether drawn.
        game.end_turn()
        assert game.current_player is boss
        assert boss.mana == mana
        assert boss.hand[-1].id == TWISTING_NETHER
        # He falls: the boss is defeated.
        game.end_turn()
        other.max_mana, other.used_mana = 10, 0
        boss.hero.set_current_health(2)
        with pytest.raises(GameOver):
            other.give(MOONFIRE).play(target=boss.hero)
            other.give(MOONFIRE).play(target=boss.hero)
        assert other.playstate == PlayState.WON


def test_atiesh():
    # "After you cast a spell, summon a random minion of that Cost. Lose 1
    # Durability."
    game, boss, other = _boss_game("KARA_13_06")
    game.end_turn()
    other.summon("KARA_13_26")
    assert other.weapon.durability == 3
    other.give(FIREBALL).play(target=boss.hero)
    assert len(other.field) == 1 and other.field[0].cost == 4
    assert other.weapon.durability == 2
