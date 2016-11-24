import unittest

import mwutils
import arbitrage


# ------------------------------------
# Eight88FootballMatchPage class tests
# ------------------------------------
class Eight88FootballMatchPageTestCase(unittest.TestCase):
    """Tests for Eight88FootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "EIGHT88")
        self.assertEqual(self.page.category, "FOOTBALL")
        self.assertEqual(self.page.sub_category, "League Two")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 36)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("FOOTBALL", "BLACKPOOL"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("FOOTBALL", "DONCASTER ROVERS"))
        self.assertEqual(win_odds, 2.5)
        self.assertEqual(draw_odds, 3.5)
        self.assertEqual(lose_odds, 2.65)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("FOOTBALL", "WYCOMBE WANDERERS"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("FOOTBALL", "BARNET"))
        self.assertEqual(win_odds, 2.1)
        self.assertEqual(draw_odds, 3.4)
        self.assertEqual(lose_odds, 3.4)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("888_Football_L2.txt")
        self.page = arbitrage.BettingPage(self.html_soup, "EIGHT88", "FOOTBALL")


# ------------------------------------
# PaddyPowerFootballMatchPage class tests
# ------------------------------------
class PaddyPowerFootballMatchPageTestCase(unittest.TestCase):
    """Tests for PaddyPowerFootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "PADDYPOWER")
        self.assertEqual(self.page.category, "FOOTBALL")
        self.assertEqual(self.page.sub_category, "English League 2")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 36)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("FOOTBALL", "BLACKPOOL"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("FOOTBALL", "DONCASTER"))
        self.assertEqual(win_odds, 2.625)
        self.assertEqual(draw_odds, 3.4)
        self.assertEqual(lose_odds, 2.5)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("FOOTBALL", "Wycombe"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("FOOTBALL", "BARNET"))
        self.assertEqual(win_odds, 2.1)
        self.assertEqual(draw_odds, 3.4)
        self.assertEqual(lose_odds, 3.4)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("Paddy_Football_L2.txt")
        self.page = arbitrage.BettingPage(self.html_soup, "PADDYPOWER", "FOOTBALL")


# ------------------------------------
# PaddyPowerFootballMatchPage class tests
# ------------------------------------
class PinnacleFootballMatchPageTestCase(unittest.TestCase):
    """Tests for PinnacleFootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "PINNACLE")
        self.assertEqual(self.page.category, "FOOTBALL")
        self.assertEqual(self.page.sub_category, "England-PremierLeague")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 33)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("FOOTBALL", "CHELSEA"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("FOOTBALL", "MANCHESTER UNITED"))
        self.assertEqual(win_odds, 2.190)
        self.assertEqual(draw_odds, 3.290)
        self.assertEqual(lose_odds, 3.850)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("FOOTBALL", "STOKE CITY"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("FOOTBALL", "SWANSEA CITY"))
        self.assertEqual(win_odds, 1.909)
        self.assertEqual(draw_odds, 3.640)
        self.assertEqual(lose_odds, 4.320)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("Pinnacle_Football_PL.txt")
        self.page = arbitrage.BettingPage(self.html_soup, "PINNACLE", "FOOTBALL")


# ------------------------------------
# WilliamHillFootballMatchPage class tests
# ------------------------------------
class WilliamHillFootballMatchPageTestCase(unittest.TestCase):
    """Tests for WilliamHillFootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "WILLIAMHILL")
        self.assertEqual(self.page.category, "FOOTBALL")
        self.assertEqual(self.page.sub_category, "English Premier League")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 27)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("FOOTBALL", "SUNDERLAND"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("FOOTBALL", "ARSENAL"))
        self.assertEqual(win_odds, 7)
        self.assertEqual(draw_odds, 4.4)
        self.assertEqual(lose_odds, 1.33333)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("FOOTBALL", "Southampton"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("FOOTBALL", "CHELSEA"))
        self.assertEqual(win_odds, 3.1)
        self.assertEqual(draw_odds, 3.1)
        self.assertEqual(lose_odds, 2.1)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("WilliamHill_Football_PL.txt")
        self.page = arbitrage.BettingPage(self.html_soup, "WILLIAMHILL", "FOOTBALL")


# ------------------------------------
# SportingBetFootballMatchPage class tests
# ------------------------------------
class SportingBetFootballMatchPageTestCase(unittest.TestCase):
    """Tests for SportingBetFootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "SPORTINGBET")
        self.assertEqual(self.page.category, "FOOTBALL")
        self.assertEqual(self.page.sub_category, "England - Premier League")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 60)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("FOOTBALL", "MANCHESTER UNITED"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("FOOTBALL", "ARSENAL"))
        self.assertEqual(win_odds, 2.7)
        self.assertEqual(draw_odds, 3.25)
        self.assertEqual(lose_odds, 2.818)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("FOOTBALL", "SOUTHAMPTON"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("FOOTBALL", "EVERTON"))
        self.assertEqual(win_odds, 2.15)
        self.assertEqual(draw_odds, 3.5)
        self.assertEqual(lose_odds, 3.4)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("SportingBet_Football_PL.txt")
        self.page = arbitrage.BettingPage(self.html_soup, "SPORTINGBET", "FOOTBALL")


# ------------------------------------
# MarathonBetFootballMatchPage class tests
# ------------------------------------
class MarathonBetFootballMatchPageTestCase(unittest.TestCase):
    """Tests for MarathonBetFootballMatchPage class in arbitrage.py."""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "MARATHONBET")
        self.assertEqual(self.page.category, "FOOTBALL")
        self.assertEqual(self.page.sub_category, "England. Premier League")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 90)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("FOOTBALL", "MANCHESTER UNITED"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("FOOTBALL", "ARSENAL"))
        self.assertEqual(win_odds, 2.75)
        self.assertEqual(draw_odds, 3.32)
        self.assertEqual(lose_odds, 2.85)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("FOOTBALL", "MIDDLESBROUGH"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("FOOTBALL", "HULL CITY"))
        self.assertEqual(win_odds, 1.83)
        self.assertEqual(draw_odds, 3.7)
        self.assertEqual(lose_odds, 5)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("MarathonBet_Football_PL.txt")
        self.page = arbitrage.BettingPage(self.html_soup, "MARATHONBET", "FOOTBALL")
