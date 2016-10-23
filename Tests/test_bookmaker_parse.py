import unittest

import arbitrage


# ------------------------------------
# Eight88FootballMatchPage class tests
# ------------------------------------
class Eight88FootballMatchPageTestCase(unittest.TestCase):
    """Tests for Eight88FootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "888")
        self.assertEqual(self.page.sport, "FOOTBALL")
        self.assertEqual(self.page.category, "League Two")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.betting_events), 12)

    def test_betting_event_correct_first(self):
        self.assertEqual(self.page.betting_events[0].p1, "Blackpool")
        self.assertEqual(self.page.betting_events[0].p2, "Doncaster Rovers")
        self.assertEqual(self.page.betting_events[0].win_odds, 2.5)
        self.assertEqual(self.page.betting_events[0].draw_odds, 3.5)
        self.assertEqual(self.page.betting_events[0].lose_odds, 2.65)

    def test_betting_event_correct_last(self):
        self.assertEqual(self.page.betting_events[11].p1, "Wycombe Wanderers")
        self.assertEqual(self.page.betting_events[11].p2, "Barnet")
        self.assertEqual(self.page.betting_events[11].win_odds, 2.1)
        self.assertEqual(self.page.betting_events[11].draw_odds, 3.4)
        self.assertEqual(self.page.betting_events[11].lose_odds, 3.4)

    def setUp(self):
        self.html_soup = arbitrage.get_page_source_file("888_Football_L2.txt")
        self.page = arbitrage.Eight88FootballMatchPage(self.html_soup)


# ------------------------------------
# PaddyPowerFootballMatchPage class tests
# ------------------------------------
class PaddyPowerFootballMatchPageTestCase(unittest.TestCase):
    """Tests for PaddyPowerFootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "PADDYPOWER")
        self.assertEqual(self.page.sport, "FOOTBALL")
        self.assertEqual(self.page.category, "English League 2")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.betting_events), 12)

    def test_betting_event_correct_first(self):
        self.assertEqual(self.page.betting_events[0].p1, "Blackpool")
        self.assertEqual(self.page.betting_events[0].p2, "Doncaster")
        self.assertEqual(self.page.betting_events[0].win_odds, 2.625)
        self.assertEqual(self.page.betting_events[0].draw_odds, 3.4)
        self.assertEqual(self.page.betting_events[0].lose_odds, 2.5)

    def test_betting_event_correct_last(self):
        self.assertEqual(self.page.betting_events[11].p1, "Wycombe")
        self.assertEqual(self.page.betting_events[11].p2, "Barnet")
        self.assertEqual(self.page.betting_events[11].win_odds, 2.1)
        self.assertEqual(self.page.betting_events[11].draw_odds, 3.4)
        self.assertEqual(self.page.betting_events[11].lose_odds, 3.4)

    def setUp(self):
        self.html_soup = arbitrage.get_page_source_file("Paddy_Football_L2.txt")
        self.page = arbitrage.PaddyPowerFootballMatchPage(self.html_soup)


# ------------------------------------
# PaddyPowerFootballMatchPage class tests
# ------------------------------------
class PinnacleFootballMatchPageTestCase(unittest.TestCase):
    """Tests for PinnacleFootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "PINNACLE")
        self.assertEqual(self.page.sport, "FOOTBALL")
        self.assertEqual(self.page.category, "England-PremierLeague")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.betting_events), 11)

    def test_betting_event_correct_first(self):
        self.assertEqual(self.page.betting_events[0].p1, "Chelsea")
        self.assertEqual(self.page.betting_events[0].p2, "Manchester United")
        self.assertEqual(self.page.betting_events[0].win_odds, 2.190)
        self.assertEqual(self.page.betting_events[0].draw_odds, 3.290)
        self.assertEqual(self.page.betting_events[0].lose_odds, 3.850)

    def test_betting_event_correct_last(self):
        self.assertEqual(self.page.betting_events[10].p1, "Stoke City")
        self.assertEqual(self.page.betting_events[10].p2, "Swansea City")
        self.assertEqual(self.page.betting_events[10].win_odds, 1.909)
        self.assertEqual(self.page.betting_events[10].draw_odds, 3.640)
        self.assertEqual(self.page.betting_events[10].lose_odds, 4.320)

    def setUp(self):
        self.html_soup = arbitrage.get_page_source_file("Pinnacle_Football_PL.txt")
        self.page = arbitrage.PinnacleFootballMatchPage(self.html_soup)
