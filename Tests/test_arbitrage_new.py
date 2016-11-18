import unittest

import arbitrage
import mwutils
import os
from config import *


# ------------------------
# Odds class tests
# ------------------------
class OddsFractionalOddsTestCase(unittest.TestCase):
    """Tests for Odds class in arbitrage.py."""

    def test_fractional_odds_no_space(self):
        """Are fractional odds translated correctly when no spacces?"""
        self.assertEqual(self.odds_one.odds, 3.5)

    def test_fractional_odds_with_space(self):
        """Are fractional odds translated correctly with spacces?"""
        self.assertEqual(self.odds_two.odds, 3.5)

    def test_fractional_odds_with_tabs(self):
        """Are fractional odds translated correctly with tabs and spacces?"""
        self.assertEqual(self.odds_three.odds, 3.5)

    def setUp(self):
        one = "5/2"
        two = "5 / 2"
        three = "5  \t / \t   2"
        self.odds_one = arbitrage.Odds(one)
        self.odds_two = arbitrage.Odds(two)
        self.odds_three = arbitrage.Odds(three)


class OddsDecimalOddsTestCase(unittest.TestCase):
    """Tests for Odds class in arbitrage.py."""

    def test_decimal_odds_long_decimal(self):
        """Are decimal odds with long decimals handled?"""
        self.assertEqual(self.odds_one.odds, 2.55515)

    def test_decimal_odds_integer(self):
        """Are integer odds handled?"""
        self.assertEqual(self.odds_two.odds, 1)

    def test_decimal_sub_one(self):
        """Are decimal odds below 1 handled?"""
        self.assertEqual(self.odds_three.odds, 0.15667)

    def setUp(self):
        one = 2.55515151
        two = 1
        three = "0.156666"
        self.odds_one = arbitrage.Odds(one)
        self.odds_two = arbitrage.Odds(two)
        self.odds_three = arbitrage.Odds(three)


class OddsEvensTestCase(unittest.TestCase):
    """Tests for Odds class in arbitrage.py."""

    def test_evens_odds(self):
        """Are "evens" odds handled?"""
        self.assertEqual(self.odds_one.odds, 1)

    def test_EVENS_odds(self):
        """Are "EVENS" odds handled?"""
        self.assertEqual(self.odds_two.odds, 1)

    def setUp(self):
        one = "evens"
        two = "EVENS"
        self.odds_one = arbitrage.Odds(one)
        self.odds_two = arbitrage.Odds(two)


class OddsComparisonTestCase(unittest.TestCase):
    def setUp(self):
        self.small = arbitrage.Odds(0.6)
        self.medium = arbitrage.Odds(0.65)
        self.large = arbitrage.Odds(2)
        self.v_large = arbitrage.Odds(2.3)

        self.v_large2 = arbitrage.Odds("13/10")

    def test_odds_less_than(self):
        self.assertLess(self.small, self.medium)
        self.assertLess(self.small, self.large)
        self.assertLess(self.medium, self.v_large)
        self.assertLess(self.large, self.v_large)

    def test_odds_greater_than(self):
        self.assertGreater(self.medium, self.small)
        self.assertGreater(self.large, self.small)
        self.assertGreater(self.v_large, self.medium)
        self.assertGreater(self.v_large, self.large)

    def test_odds_equal(self):
        self.assertEqual(self.v_large, self.v_large2)

    def test_less_equal_to(self):
        self.assertLessEqual(self.v_large, self.v_large2)

    def test_greater_equal_to(self):
        self.assertGreaterEqual(self.v_large, self.v_large2)


# ------------------------
# Participant class tests
# ------------------------
class ParticipantTestCase(unittest.TestCase):
    """Tests for Participant class in arbitrage.py."""

    def test_category_present(self):
        """Are categories found correctly?"""
        self.assertEqual(self.part_pres.cat_id, 1)

    def test_participant_present(self):
        """Are participants found correctly?"""
        self.assertEqual(self.part_pres.participant_id, 1)

    def test_category_not_present(self):
        """Are categories not found handled correctly"""
        self.assertRaises(KeyError, lambda: arbitrage.Participant("Rug", "Tib"))

    def test_participant_not_present(self):
        """Are participants not found handled correctly"""
        self.assertRaises(KeyError, lambda: arbitrage.Participant("Football", "Tib"))

    def setUp(self):
        cat_present = "Football"
        participant_present = "Arsenal"

        self.part_pres = arbitrage.Participant(cat_present, participant_present)


class ParticipantEqualityTestCase(unittest.TestCase):
    def setUp(self):
        self.bourn1 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH")
        self.bourn2 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH AFC")
        self.arsenal = arbitrage.Participant("FOOTBALL", "ARSENAL")

    def test_participant_equal(self):
        self.assertEqual(self.bourn1, self.bourn2)

    def test_participant_not_equal(self):
        self.assertNotEqual(self.bourn2, self.arsenal)


# ------------------------
# Event class tests
# ------------------------
class EventTestCase(unittest.TestCase):
    """Tests for Event class in arbitrage.py."""

    def test_basic_event(self):
        """Can basic events be created"""
        self.event = arbitrage.Event("sport", "cat", "name", "att", ["p1", "p2"])
        self.assertEqual(str(self.event), "sport-cat-name\natt:p1,p2")

    def test_event_equality(self):
        """Are the same events correctly identified"""
        self.event = arbitrage.Event("sport", "cat", "name", "att", ["p1", "p2"])
        self.event_same_diff_name = arbitrage.Event("sport", "cat", "namediff", "att", ["p1", "p2"])
        self.event_same_name_diff_participants = arbitrage.Event("sport", "cat", "name", "att", ["p3", "p2"])
        self.event_same_diff_order_diff_name = arbitrage.Event("sport", "cat", "namediff", "att", ["p2", "p1"])

        self.assertEqual(self.event, self.event_same_diff_name)
        self.assertNotEqual(self.event, self.event_same_name_diff_participants)
        self.assertEqual(self.event, self.event_same_diff_order_diff_name)

    def test_identity_dict(self):
        """Is the identity dictionary getting used"""
        self.event = arbitrage.Event("FOOTBALL", "cat", "name", "att", ["Arsenal", "Bournemouth"], identity_dict=FOOTBALL_DICT)
        self.assertEqual(self.event.participants_std[0], 1)
        self.assertEqual(self.event.participants_std[1], 2)

    def tearDown(self):
        self.event = None

    def setUp(self):
        pass


class EventEqualityTestCase(unittest.TestCase):
    def setUp(self):
        self.bourn1 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH")
        self.bourn2 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH AFC")
        self.arsenal = arbitrage.Participant("FOOTBALL", "ARSENAL")
        self.burn = arbitrage.Participant("FOOTBALL", "BURNLEY")

        self.event_one = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.bourn1, self.arsenal])
        self.event_one_dup = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.arsenal, self.bourn1])
        self.event_one_dup2 = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.arsenal, self.bourn2])

        self.event_two = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.burn, self.bourn1])

    def test_events_are_equal(self):
        self.assertEqual(self.event_one, self.event_one_dup)
        self.assertEqual(self.event_one, self.event_one_dup2)

    def test_events_are_not_equal(self):
        self.assertNotEqual(self.event_one, self.event_two)


# TODO: Start here
# --------------------------
# BettableOutcome class tests
# --------------------------
class BettableOutcomeTestCase(unittest.TestCase):
    def setUp(self):
        self.part_bourn1 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH")
        self.part_bourn2 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH AFC")
        self.part_arsenal = arbitrage.Participant("FOOTBALL", "ARSENAL")
        self.part_burn = arbitrage.Participant("FOOTBALL", "BURNLEY")

        self.event_one = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.part_bourn1, self.part_arsenal])
        self.event_one_dupe = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.part_burn, self.part_bourn1])
        self.event_two = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.part_bourn1, self.part_burn])

        self.odds_good = arbitrage.Odds("10/1")
        self.odds_bad = arbitrage.Odds("2/1")
        self.odds_bad_dec = arbitrage.Odds(3)
        self.odds_good_dec = arbitrage.Odds(11)

        self.bo_e1_p1_o1_good_other_odds = arbitrage.BettableOutcome(self.event_one,
                                                                     self.part_bourn1,
                                                                     "WIN",
                                                                     self.odds_good_dec,
                                                                     "B1")

        self.bo_e1_p1_o1_bad_other_odds = arbitrage.BettableOutcome(self.event_one,
                                                                    self.part_bourn1,
                                                                    "WIN",
                                                                    self.odds_bad_dec,
                                                                    "B1")

        self.bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_one, self.part_bourn1, "WIN", self.odds_good, "B1")
        self.bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_one, self.part_bourn1, "WIN", self.odds_bad, "B1")
        self.bo_e1_p1_o1_good_dupe = arbitrage.BettableOutcome(self.event_one, self.part_bourn1, "WIN", self.odds_good, "B1")

    def test_bettableoutcome_equality(self):
        self.assertEqual(self.bo_e1_p1_o1_good, self.bo_e1_p1_o1_good_dupe)

    def test_bettableoutcome_less_than(self):
        self.assertLess(self.bo_e1_p1_o1_bad, self.bo_e1_p1_o1_good)

    def test_bettableoutcome_greater_than(self):
        self.assertGreater(self.bo_e1_p1_o1_good, self.bo_e1_p1_o1_bad)

    def test_bettableoutcome_greater_equal(self):
        self.assertGreaterEqual(self.bo_e1_p1_o1_bad, self.bo_e1_p1_o1_bad_other_odds)
        self.assertGreater(self.bo_e1_p1_o1_good, self.bo_e1_p1_o1_bad)

    def test_bettableoutcome_less_equal(self):
        self.assertGreaterEqual(self.bo_e1_p1_o1_good, self.bo_e1_p1_o1_good_other_odds)
        self.assertLess(self.bo_e1_p1_o1_bad, self.bo_e1_p1_o1_good)



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
        self.assertEqual(t.events[1].p1_ind, FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[1].p2_ind, FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[1].win_odds, 5.82)
        self.assertEqual(t.events[1].lose_odds, 1.625)

        # Just to make sure
        self.assertEqual(t.events[0].p1, "Blackpool")
        self.assertEqual(t.events[0].p2, "Doncaster")
        self.assertEqual(t.events[0].p1_ind, FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[0].p2_ind, FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[0].win_odds, 2.1)
        self.assertEqual(t.events[0].lose_odds, 2.5)

    def test_non_ordered_third_exception(self):
        """Does the arb work when third event is not ordered?"""
        t = arbitrage.ArbitrageEvent([self.one, self.three, self.two])

        self.assertEqual(t.events[2].p1, "Blackpool")
        self.assertEqual(t.events[2].p2, "Doncaster")
        self.assertEqual(t.events[2].p1_ind, FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[2].p2_ind, FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[2].win_odds, 5.82)
        self.assertEqual(t.events[2].lose_odds, 1.625)

        # Confirm first two have not been reordered too
        self.assertEqual(t.events[0].p1, "Blackpool")
        self.assertEqual(t.events[0].p2, "Doncaster")
        self.assertEqual(t.events[0].p1_ind, FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[0].p2_ind, FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[0].win_odds, 2.1)
        self.assertEqual(t.events[0].lose_odds, 2.5)

        self.assertEqual(t.events[1].p1, "Blackpool")
        self.assertEqual(t.events[1].p2, "Doncaster")
        self.assertEqual(t.events[1].p1_ind, FOOTBALL_DICT['Blackpool'])
        self.assertEqual(t.events[1].p2_ind, FOOTBALL_DICT['Doncaster'])
        self.assertEqual(t.events[1].win_odds, 2.9)
        self.assertEqual(t.events[1].lose_odds, 2.5)

    def setUp(self):
        event1 = arbitrage.Event("FOOTBALL", "L2", "Blackpool v Doncaster", "win",
                                ["Blackpool", "Doncaster Rovers"], identity_dict=FOOTBALL_DICT)
        event2 = arbitrage.Event("FOOTBALL", "L2", "Blackpool v Doncaster", "win",
                                ["Doncaster", "Blackpool"], identity_dict=FOOTBALL_DICT)

        odds1 = arbitrage.Odds(true=2.1, false=2.5, null=1.65)
        odds2 = arbitrage.Odds(true=1.625, false=5.82, null=1.5)
        odds3 = arbitrage.Odds(true=2.9, false=2.5, null=1.25)

        self.one = arbitrage.BettingEvent(event1, odds1, "888")
        self.two = arbitrage.BettingEvent(event2, odds2, "PaddyPower")
        self.three = arbitrage.BettingEvent(event1, odds3, "AnotherOne")


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
                           2.1, 2.5, 1.65, IDENTITY_DICT=FOOTBALL_DICT)
        self.two = arbitrage.BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                           1.625, 5.82, 1.5, IDENTITY_DICT=FOOTBALL_DICT)
        self.three = arbitrage.BettingEvent("AnotherOne", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.9, 2.5, 1.25, IDENTITY_DICT=FOOTBALL_DICT)
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
                           2.1, 2.5, 1.65, IDENTITY_DICT=FOOTBALL_DICT)
        self.two = arbitrage.BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                           1.625, 5.82, 1.5, IDENTITY_DICT=FOOTBALL_DICT)
        self.three = arbitrage.BettingEvent("AnotherOne", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.9, 2.5, 1.25, IDENTITY_DICT=FOOTBALL_DICT)
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
                           2.1, 5.82, 1.65, IDENTITY_DICT=FOOTBALL_DICT)
        self.two = arbitrage.BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                           1.625, 5.82, 5.5, IDENTITY_DICT=FOOTBALL_DICT)
        self.three = arbitrage.BettingEvent("AnotherOne", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster",
                           2.9, 2.5, 1.25, IDENTITY_DICT=FOOTBALL_DICT)
        self.arb = arbitrage.ArbitrageEvent([self.one, self.two, self.three])


class ArbitrageEventArbBettingAmountsTestCase(unittest.TestCase):
    def setUp(self):
        self.event1 = arbitrage.BettingEvent("B1", "s", "c", "n", "1", "2", 4.3, 1, 2)
        self.event2 = arbitrage.BettingEvent("B2", "s", "c", "n", "1", "2", 3, 0.8, 3)
        self.event3 = arbitrage.BettingEvent("B3", "s", "c", "n", "1", "2", 4, 2.5, 1.7)
        self.event4 = arbitrage.BettingEvent("B3", "s", "c", "n", "1", "2", 4, 2.7, 1.7)

        self.arb = arbitrage.ArbitrageEvent([self.event1, self.event2, self.event3])
        self.arb2 = arbitrage.ArbitrageEvent([self.event1, self.event2, self.event3, self.event4])

    def test_get_arb_betting_amounts(self):
        self.assertEqual(self.arb.get_arb_betting_amounts(100, integer_round=False), (24.08, 34.51, 41.41))
        self.assertEqual(self.arb.get_arb_betting_amounts(100), (24, 34, 41))

        self.assertEqual(self.arb2.get_arb_betting_amounts(100, integer_round=False), (24.84, 35.60, 39.56))
        self.assertEqual(self.arb2.get_arb_betting_amounts(100), (25, 36, 40))

    def test_arb_event_string_output(self):
        self.assertTrue("1 to win:£48 at B1\nDraw:£69 at B2\n2 to win:£83 at B3" in str(self.arb))

# ------------------
# Market class tests
# ------------------
class MarketTestCase(unittest.TestCase):
    """Tests for Market class in arbitrage.py."""
    def setUp(self):
        self.event_list = []
        self.paddy = arbitrage.BettingPage(
            mwutils.get_page_source_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                      "Paddy_Football_L2.txt")),
        "PADDYPOWER", "FOOTBALL", IDENTITY_DICT=FOOTBALL_DICT)
        self.eee = arbitrage.BettingPage(
            mwutils.get_page_source_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                                      "888_Football_L2.txt")),
        "EIGHT88", "FOOTBALL", IDENTITY_DICT=FOOTBALL_DICT)

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




