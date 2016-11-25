import unittest

import mwutils
import arbitrage


# ------------------------------------
# Eight88FootballMatchPage class tests
# ------------------------------------
class Eight88FootballMatchPageTestCase(unittest.TestCase):
    """Tests for Eight88FootballMatchPage"""

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

    def test_betting_event_correct_date_time(self):
        self.assertEqual(self.page_pl.bettable_outcomes[0].event.date, "26/11")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("888_Football_L2.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "EIGHT88", "FOOTBALL")

        self.html_soup_pl = mwutils.get_page_source_file("888_Football_PL.txt")
        self.page_pl = arbitrage.OddsPageParser(self.html_soup_pl, "EIGHT88", "FOOTBALL")


class Eight88SnookerPageTestCase(unittest.TestCase):
    """Tests for Eight88SnookerPage"""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "EIGHT88")
        self.assertEqual(self.page.category, "SNOOKER")
        self.assertEqual(self.page.sub_category, "UK Championship")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 64)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("SNOOKER", "BRECEL, LUCA"))
        self.assertEqual(self.page.bettable_outcomes[1].participant,
                         arbitrage.Participant("SNOOKER", "CRAIGIE, SAM"))
        self.assertEqual(win_odds, 1.33)
        self.assertEqual(lose_odds, 3.30)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[-2].participant,
                         arbitrage.Participant("SNOOKER", "ZHANG ANDA"))
        self.assertEqual(self.page.bettable_outcomes[-1].participant, arbitrage.Participant("SNOOKER", "MCGILL, ANTHONY"))
        self.assertEqual(win_odds, 2.65)
        self.assertEqual(lose_odds, 1.46)

    def test_betting_event_correct_date_time(self):
        self.assertEqual(self.page.bettable_outcomes[0].event.date, "26/11")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("888_Snooker_UKChamps.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "EIGHT88", "SNOOKER")


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
        self.page = arbitrage.OddsPageParser(self.html_soup, "PADDYPOWER", "FOOTBALL")


class PaddyPowerSnookerPageTestCase(unittest.TestCase):
    """Tests for PaddyPowerSnookerPage"""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "PADDYPOWER")
        self.assertEqual(self.page.category, "SNOOKER")
        self.assertEqual(self.page.sub_category, "UK Championship")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 64)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("SNOOKER", "JOHN HIGGINS"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("SNOOKER", "NOPPON SAENGKHAM"))
        self.assertEqual(win_odds, 1.083)
        self.assertEqual(lose_odds, 7.5)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("SNOOKER", "JIMMY ROBERTSON"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("SNOOKER", "MARK DAVIS"))
        self.assertEqual(win_odds, 2.2)
        self.assertEqual(lose_odds, 1.67)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("Paddy_Snooker_UKChamps.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "PADDYPOWER", "SNOOKER")


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
        self.page = arbitrage.OddsPageParser(self.html_soup, "PINNACLE", "FOOTBALL")


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

    def test_betting_event_correct_date(self):
        self.assertEqual(self.page.bettable_outcomes[0].event.date, "29 Oct")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("WilliamHill_Football_PL.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "WILLIAMHILL", "FOOTBALL")


class WilliamHillSnookerPageTestCase(unittest.TestCase):
    """Tests for WilliamHillSnookerPage"""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "WILLIAMHILL")
        self.assertEqual(self.page.category, "SNOOKER")
        self.assertEqual(self.page.sub_category, "UK Championship")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 64)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant,
                         arbitrage.Participant("SNOOKER", "JOHN HIGGINS"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("SNOOKER", "NOPPON SAENGKHAM"))
        self.assertEqual(win_odds, 1.08333)
        self.assertEqual(lose_odds, 7.5)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[-2].participant,
                         arbitrage.Participant("SNOOKER", "XIAO GUODONG"))
        self.assertEqual(self.page.bettable_outcomes[-1].participant, arbitrage.Participant("SNOOKER", "JOE PERRY"))
        self.assertEqual(win_odds, 2.9)
        self.assertEqual(lose_odds, 1.4)

    def test_betting_event_correct_date(self):
        self.assertEqual(self.page.bettable_outcomes[0].event.date, "26 Nov")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("WilliamHill_Snooker.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "WILLIAMHILL", "SNOOKER")


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

    def test_betting_event_correct_date(self):
        self.assertEqual(self.page.bettable_outcomes[0].event.date, "19/11/2016 12:30 GMT")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("SportingBet_Football_PL.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "SPORTINGBET", "FOOTBALL")


class SportingBetSnookerPageTestCase(unittest.TestCase):
    """Tests for SportingBetSnookerPage"""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "SPORTINGBET")
        self.assertEqual(self.page.category, "SNOOKER")
        self.assertEqual(self.page.sub_category, "UK Championships")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 64)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant,
                         arbitrage.Participant("SNOOKER", "DANIEL WELLS"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("SNOOKER", "MARK SELBY"))
        self.assertEqual(win_odds, 7)
        self.assertEqual(lose_odds, 1.1)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[-2].participant,
                         arbitrage.Participant("SNOOKER", "RORY MCLEOD"))
        self.assertEqual(self.page.bettable_outcomes[-1].participant, arbitrage.Participant("SNOOKER", "MARCO FU"))
        self.assertEqual(win_odds, 5.5)
        self.assertEqual(lose_odds, 1.142)

    def test_betting_event_correct_date(self):
        self.assertEqual(self.page.bettable_outcomes[0].event.date, "26/11/2016 13:00 GMT")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("SportingBet_Snooker.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "SPORTINGBET", "SNOOKER")


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

    def test_betting_event_correct_date(self):
        self.assertEqual(self.page.bettable_outcomes[0].event.date, "19 Nov 12:30")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("MarathonBet_Football_PL.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "MARATHONBET", "FOOTBALL")


class MarathonBetSnookerPageTestCase(unittest.TestCase):
    """Tests for MarathonBetSnookerPage"""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "MARATHONBET")
        self.assertEqual(self.page.category, "SNOOKER")
        self.assertEqual(self.page.sub_category, "UK Championships")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 64)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:2] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("SNOOKER", "BRECEL, LUCA"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("SNOOKER", "CRAIGIE, SAM"))
        self.assertEqual(win_odds, 1.4)
        self.assertEqual(lose_odds, 3.22)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-2:] if x.outcome == "LOSE"][0]

        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("SNOOKER", "WALDEN, RICKY"))
        self.assertEqual(self.page.bettable_outcomes[-1].participant, arbitrage.Participant("SNOOKER", "DONALDSON, SCOTT"))
        self.assertEqual(win_odds, 1.34)
        self.assertEqual(lose_odds, 3.58)

    def test_betting_event_correct_date(self):
        self.assertEqual(self.page.bettable_outcomes[0].event.date, "26 Nov 13:00")

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("MarathonBet_Snooker.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "MARATHONBET", "SNOOKER")


# ------------------------------------
# Eight88FootballMatchPage class tests
# ------------------------------------
class LadbrokesFootballMatchPageTestCase(unittest.TestCase):
    """Tests for LadbrokesFootballMatchPage"""

    def test_constants(self):
        self.assertEqual(self.page.bookmaker, "LADBROKES")
        self.assertEqual(self.page.category, "FOOTBALL")
        self.assertEqual(self.page.sub_category, "Premier League")

    def test_all_betting_events_found(self):
        self.assertEqual(len(self.page.bettable_outcomes), 51)

    def test_betting_event_correct_first(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[0:3] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[0].participant, arbitrage.Participant("FOOTBALL", "BURNLEY"))
        self.assertEqual(self.page.bettable_outcomes[1].participant, arbitrage.Participant("FOOTBALL", "MANCHESTER CITY"))
        self.assertEqual(win_odds, 10)
        self.assertEqual(draw_odds, 6)
        self.assertEqual(lose_odds, 1.3)

    def test_betting_event_correct_last(self):
        win_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "WIN"][0]
        lose_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "LOSE"][0]
        draw_odds = [x.odds.odds for x in self.page.bettable_outcomes[-3:] if x.outcome == "DRAW"][0]

        self.assertEqual(self.page.bettable_outcomes[-3].participant, arbitrage.Participant("FOOTBALL", "WEST HAM"))
        self.assertEqual(self.page.bettable_outcomes[-2].participant, arbitrage.Participant("FOOTBALL", "ARSENAL"))
        self.assertEqual(win_odds, 4.33333)
        self.assertEqual(draw_odds, 3.8)
        self.assertEqual(lose_odds, 1.75)

    def setUp(self):
        self.html_soup = mwutils.get_page_source_file("LadBrokes_Football_PL.txt")
        self.page = arbitrage.OddsPageParser(self.html_soup, "LADBROKES", "FOOTBALL")
