import unittest

import arbitrage


# ------------------------
# BettingEvent class tests
# ------------------------
class BettingEventFractionalOddsTestCase(unittest.TestCase):
    """Tests for BettingEvent class in arbitrage.py."""

    def test_fractional_odds_no_space(self):
        """Are fractional odds translated correctly when no spacces?"""
        self.assertEqual(self.event.win_odds, 3.5)

    def test_fractional_odds_with_space(self):
        """Are fractional odds translated correctly with spacces?"""
        self.assertEqual(self.event.lose_odds, 3.5)

    def test_fractional_odds_with_tabs(self):
        """Are fractional odds translated correctly with tabs and spacces?"""
        self.assertEqual(self.event.draw_odds, 3.5)

    def setUp(self):
        bookmaker = "Dummy bookmaker"
        sport = "dummy sport"
        category = "dummy category"
        name = "dummy name"
        p1 = "dummy p1"
        p2 = "dummy p2"

        win_odds = "5/2"
        lose_odds = "5 / 2"
        draw_odds = "5  \t / \t   2"
        self.event = arbitrage.BettingEvent(bookmaker, sport, category,
                                            name, p1, p2, win_odds, lose_odds,
                                            draw_odds)


class BettingEventDecimalOddsTestCase(unittest.TestCase):
    """Tests for BettingEvent class in arbitrage.py."""

    def test_decimal_odds_long_decimal(self):
        """Are decimal odds with long decimals handled?"""
        self.assertEqual(self.event.win_odds, 2.55515)

    def test_decimal_odds_integer(self):
        """Are integer odds handled?"""
        self.assertEqual(self.event.lose_odds, 1)

    def test_decimal_sub_one(self):
        """Are decimal odds below 1 handled?"""
        self.assertEqual(self.event.draw_odds, 0.15667)

    def setUp(self):
        bookmaker = "Dummy bookmaker"
        sport = "dummy sport"
        category = "dummy category"
        name = "dummy name"
        p1 = "dummy p1"
        p2 = "dummy p2"

        win_odds = 2.55515151
        lose_odds = 1
        draw_odds = "0.156666"
        self.event = arbitrage.BettingEvent(bookmaker, sport, category,
                                            name, p1, p2, win_odds, lose_odds,
                                            draw_odds)


class BettingEventEvensTestCase(unittest.TestCase):
    """Tests for BettingEvent class in arbitrage.py."""

    def test_evens_odds(self):
        """Are "evens" odds handled?"""
        self.assertEqual(self.event.win_odds, 1)

    def test_EVENS_odds(self):
        """Are "EVENS" odds handled?"""
        self.assertEqual(self.event.lose_odds, 1)

    def setUp(self):
        bookmaker = "Dummy bookmaker"
        sport = "dummy sport"
        category = "dummy category"
        name = "dummy name"
        p1 = "dummy p1"
        p2 = "dummy p2"

        win_odds = "evens"
        lose_odds = "EVENS"
        self.event = arbitrage.BettingEvent(bookmaker, sport, category,
                                            name, p1, p2, win_odds, lose_odds)



    """Tests for BettingEvent class in arbitrage.py."""

    def test_evens_odds(self):
        """Are "evens" odds handled?"""
        self.assertEqual(self.event.win_odds, 1)

    def test_EVENS_odds(self):
        """Are "EVENS" odds handled?"""
        self.assertEqual(self.event.lose_odds, 1)

    def setUp(self):
        bookmaker = "Dummy bookmaker"
        sport = "dummy sport"
        category = "dummy category"
        name = "dummy name"
        p1 = "dummy p1"
        p2 = "dummy p2"

        win_odds = "evens"
        lose_odds = "EVENS"
        self.event = arbitrage.BettingEvent(bookmaker, sport, category,
                                            name, p1, p2, win_odds, lose_odds)


class BettingEventPlayerIndTestCase(unittest.TestCase):
    """Tests for BettingEvent class in arbitrage.py."""

    def test_player_ind_in_dictionary(self):
        """Are teams in the dictionary found correctly?"""
        self.p2 = "Luton"
        self.event = arbitrage.BettingEvent(self.bookmaker, self.sport, self.category,
                                            self.name, self.p1, self.p2, self.win_odds, self.lose_odds)
        self.assertEqual(self.event.p1_ind, arbitrage.FOOTBALL_DICT['Barnet'])

    def test_player_ind_not_in_dictionary(self):
        """Are teams not in the dictionary raised?"""
        self.p2 = "This aint in no dictionary"
        self.assertRaises(KeyError, lambda: arbitrage.BettingEvent(self.bookmaker, self.sport, self.category,
                                            self.name, self.p1, self.p2, self.win_odds, self.lose_odds))

    def setUp(self):
        self.bookmaker = "Dummy bookmaker"
        self.sport = "FOOTBALL"
        self.category = "dummy category"
        self.name = "dummy name"
        self.p1 = "Barnet"
        self.p2 = "Luton"

        self.win_odds = "evens"
        self.lose_odds = "EVENS"


# --------------------------
# ArbitrageEvent class tests
# --------------------------
class ArbitrageEventNonOrderedPlayersTestCase(unittest.TestCase):
    """Tests for ArbitrageEvent class in arbitrage.py."""

    def test_non_ordered_exception(self):
        """Does the arb fail when players are not ordered?"""
        arb = arbitrage.ArbitrageEvent([self.one, self.two])

    def test_non_ordered(self):
        """Does the arb work when players are not ordered?"""
        t = arbitrage.ArbitrageEvent([self.one, self.two])

        self.assertEqual(t.events[1].p1, "Blackpool")
        self.assertEqual(t.events[1].p2, "Doncaster")
        self.assertEqual(t.events[1].p1_ind, arbitrage.FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[1].p2_ind, arbitrage.FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[1].win_odds, 5.82)
        self.assertEqual(t.events[1].lose_odds, 1.625)

        # Just to make sure
        self.assertEqual(t.events[0].p1, "Blackpool")
        self.assertEqual(t.events[0].p2, "Doncaster")
        self.assertEqual(t.events[0].p1_ind, arbitrage.FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[0].p2_ind, arbitrage.FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[0].win_odds, 2.1)
        self.assertEqual(t.events[0].lose_odds, 2.5)

    def test_non_ordered_third_exception(self):
        """Does the arb work when third event is not ordered?"""
        t = arbitrage.ArbitrageEvent([self.one, self.three, self.two])

        self.assertEqual(t.events[2].p1, "Blackpool")
        self.assertEqual(t.events[2].p2, "Doncaster")
        self.assertEqual(t.events[2].p1_ind, arbitrage.FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[2].p2_ind, arbitrage.FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[2].win_odds, 5.82)
        self.assertEqual(t.events[2].lose_odds, 1.625)

        # Confirm first two have not been reordered too
        self.assertEqual(t.events[0].p1, "Blackpool")
        self.assertEqual(t.events[0].p2, "Doncaster")
        self.assertEqual(t.events[0].p1_ind, arbitrage.FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[0].p2_ind, arbitrage.FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[0].win_odds, 2.1)
        self.assertEqual(t.events[0].lose_odds, 2.5)

        self.assertEqual(t.events[1].p1, "Blackpool")
        self.assertEqual(t.events[1].p2, "Doncaster")
        self.assertEqual(t.events[1].p1_ind, arbitrage.FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[1].p2_ind, arbitrage.FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[1].win_odds, 2.9)
        self.assertEqual(t.events[1].lose_odds, 2.5)

    def setUp(self):
        self.one = arbitrage.BettingEvent("888", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.1, 2.5, 1.65)
        self.two = arbitrage.BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Doncaster", "Blackpool",
                           1.625, 5.82, 1.5)
        self.three = arbitrage.BettingEvent("AnotherOne", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.9, 2.5, 1.25)


class ArbitrageEventBestOddsTestCase(unittest.TestCase):
    """Tests for ArbitrageEvent class in arbitrage.py."""

    def test_best_odds(self):
        """Does the arb select the best odds?"""
        self.assertEqual(self.arb.win_odds, 2.9)

    def test_best_odds_bookmaker(self):
        """Does the arb select the best bookmaker?"""
        self.assertEqual(self.arb.win_bookmaker, 2)

    def setUp(self):
        self.one = arbitrage.BettingEvent("888", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.1, 2.5, 1.65)
        self.two = arbitrage.BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                           1.625, 5.82, 1.5)
        self.three = arbitrage.BettingEvent("AnotherOne", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.9, 2.5, 1.25)
        self.arb = arbitrage.ArbitrageEvent([self.one, self.two, self.three])


class ArbitrageEventArbPercentageNoArbTestCase(unittest.TestCase):
    """Tests for ArbitrageEvent class in arbitrage.py."""

    def test_win_odds_arb(self):
        """Are arb win odds calculated correctly?"""
        self.assertEqual(self.arb.win_odds_arb, round(1/2.9, 5))

    def test_arb_percent(self):
        """Are arbitrage percentages calculated correctly?"""
        self.assertEqual(self.arb.arb_perc, 1.12271)

    def test_arb_percent_profit(self):
        """Are arb profits calculated correctly?"""
        self.assertEqual(self.arb.arb_perc_profit, -0.10930)

    def test_arb_present(self):
        """Is the arb present?"""
        self.assertEqual(self.arb.arb_present, False)

    def setUp(self):
        self.one = arbitrage.BettingEvent("888", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.1, 2.5, 1.65)
        self.two = arbitrage.BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                           1.625, 5.82, 1.5)
        self.three = arbitrage.BettingEvent("AnotherOne", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.9, 2.5, 1.25)
        self.arb = arbitrage.ArbitrageEvent([self.one, self.two, self.three])


class ArbitrageEventArbPercentageArbTestCase(unittest.TestCase):
    """Tests for ArbitrageEvent class in arbitrage.py."""

    def test_win_odds_arb(self):
        """Are arb win odds calculated correctly?"""
        self.assertEqual(self.arb.win_odds_arb, round(1/2.9, 5))

    def test_arb_percent(self):
        """Are arbitrage percentages calculated correctly?"""
        self.assertEqual(self.arb.arb_perc, 0.69847)

    def test_arb_percent_profit(self):
        """Are arb profits calculated correctly?"""
        self.assertEqual(self.arb.arb_perc_profit, 0.4317)

    def test_arb_present(self):
        """Is the arb present?"""
        self.assertEqual(self.arb.arb_present, True)

    def setUp(self):
        self.one = arbitrage.BettingEvent("888", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.1, 5.82, 1.65)
        self.two = arbitrage.BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                           1.625, 5.82, 5.5)
        self.three = arbitrage.BettingEvent("AnotherOne", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.9, 2.5, 1.25)
        self.arb = arbitrage.ArbitrageEvent([self.one, self.two, self.three])


# ------------------
# Market class tests
# ------------------
class MarketTestCase(unittest.TestCase):
    """Tests for Market class in arbitrage.py."""
    def setUp(self):
        self.event_list = []
        self.paddy = arbitrage.BettingPage(
            arbitrage.get_page_source_file("F:\Coding\PycharmProjects\Arbitrage\Tests\Paddy_Football_L2.txt"),
        "PADDYPOWER", "FOOTBALL")
        self.eee = arbitrage.BettingPage(
            arbitrage.get_page_source_file("F:\Coding\PycharmProjects\Arbitrage\Tests\888_Football_L2.txt"),
        "888", "FOOTBALL")

        self.event_list.append(self.paddy.betting_events)
        self.event_list.append(self.eee.betting_events)

    def test_correct_number_of_arbs_full_pairing(self):
        """Are all pairs of arbs created when full pairings are present?"""
        market = arbitrage.Market(self.event_list)
        self.assertEqual(len(market.arbitrage_events), 12)
        self.assertEqual(len(market.orphan_events), 0)

    def test_correct_number_of_arbs_partial_pairing_1(self):
        """Are all pairs of arbs created when there are partial pairings present?"""
        del self.event_list[0][5]
        market = arbitrage.Market(self.event_list)
        self.assertEqual(len(market.arbitrage_events), 11)
        self.assertEqual(len(market.orphan_events), 1)

    def test_correct_number_of_arbs_partial_pairing_2(self):
        """Are all pairs of arbs created when there are partial pairings present?"""
        del self.event_list[0][5]
        del self.event_list[1][6]
        market = arbitrage.Market(self.event_list)
        self.assertEqual(len(market.arbitrage_events), 10)
        self.assertEqual(len(market.orphan_events), 2)

    def test_correct_number_of_possible_arbs_full_pairing(self):
        """Are arbs correctly identified?"""
        market = arbitrage.Market(self.event_list)
        self.assertEqual(len(market.possible_arb_list), 0)

        self.event_list[0][2].win_odds = 20
        self.event_list[1][2].lose_odds = 20
        market2 = arbitrage.Market(self.event_list)
        self.assertEqual(len(market2.possible_arb_list), 1)




