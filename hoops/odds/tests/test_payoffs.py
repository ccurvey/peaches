from django.test import TestCase

from games.models import Game
from odds.models import GameMoney, Wager, GameSide, GameTotal

class PayoffTests(TestCase):
    def test_money_line_win(self):
        game = Game(points_for=78, points_against=66)
        proposition = GameMoney(game=game, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 210)

    def test_money_line_loss(self):
        game = Game(points_for=66, points_against=78)
        proposition = GameMoney(game=game, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 0)

    def test_money_line_push(self):
        game = Game(points_for=66, points_against=66)
        proposition = GameMoney(game=game, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 110)

    def test_spread_win(self):
        game = Game(points_for=78, points_against=66)
        proposition = GameSide(game=game, value=+4.5, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 210)

    def test_spread_loss(self):
        game = Game(points_for=66, points_against=78)
        proposition = GameSide(game=game, value=+4.5, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 0)

    def test_spread_push(self):
        game = Game(points_for=66, points_against=70)
        proposition = GameSide(game=game, value=+4, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 110)

    def test_total_win(self):
        game = Game(points_for=80, points_against=70)
        proposition = GameTotal(game=game, value=140, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 210)

    def test_total_loss(self):
        game = Game(points_for=80, points_against=70)
        proposition = GameTotal(game=game, value=160.5, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 0)

    def test_total_push(self):
        game = Game(points_for=80, points_against=70)
        proposition = GameTotal(game=game, value=150, payoff=-110)
        wager = Wager(proposition=proposition, wager_amount=110)
        self.assertEqual(wager.payoff_amount, 110)

