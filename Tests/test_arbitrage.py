import unittest

import arbitrage
import mwutils
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
        self.assertEqual(self.part_pres.category_id, 1)

    def test_participant_present(self):
        """Are participants found correctly?"""
        self.assertEqual(self.part_pres.participant_id, 1)

    def test_category_not_present(self):
        """Are categories not found handled correctly"""
        self.assertRaises(KeyError, lambda: arbitrage.Participant("Rug", "Tib"))

    def test_participant_not_present(self):
        """Are participants not found handled correctly"""
        self.assertRaises(KeyError, lambda: arbitrage.Participant("Football", "Tib"))

    def test_participant_numeric_id(self):
        """Can participants be created by passing in the raw id"""
        participant_id = arbitrage.Participant("FOOTBALL", 15)
        self.assertEqual(participant_id.participant_id, 15)
        self.assertEqual(participant_id.participant, "SUNDERLAND")

    def test_participant_numeric_id_non_unique(self):
        """Can participants be created by passing in the raw id"""
        participant_id = arbitrage.Participant("FOOTBALL", 19)
        self.assertEqual(participant_id.participant_id, 19)
        self.assertIn(participant_id.participant, ["WEST BROM", "WEST BROMWICH", "WEST BROMWICH ALBION", "W.B.A"])

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

    def test_basic_event_full_definition(self):
        """Can basic events be created"""
        self.event = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [arbitrage.Participant("FOOTBALL", "ARSENAL"),
                                                                    arbitrage.Participant("FOOTBALL", "LIVERPOOL")])
        self.assertEqual(str(self.event), "FOOTBALL-PREMIER LEAGUE-ARSENAL(1),LIVERPOOL(9)")

    def test_basic_event_short_definition_name(self):
        """Can basic events be created"""
        self.event = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["ARSENAL", "LIVERPOOL"])
        self.assertEqual(str(self.event), "FOOTBALL-PREMIER LEAGUE-ARSENAL(1),LIVERPOOL(9)")

    def test_event_equality(self):
        """Are the same events correctly identified"""
        self.event = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["ARSENAL", "MAN UTD"])
        self.event_same_name_diff_participants = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["LIVERPOOL", "MAN UTD"])
        self.event_same_diff_order_diff_name = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["MAN UTD", "ARSENAL"])

        self.assertNotEqual(self.event, self.event_same_name_diff_participants)
        self.assertEqual(self.event, self.event_same_diff_order_diff_name)

    def test_identity_dict(self):
        """Is the identity dictionary getting used"""
        self.event = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["Arsenal", "Bournemouth"])
        self.assertEqual(self.event.participant_ids[0], 1)
        self.assertEqual(self.event.participant_ids[1], 2)


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


# --------------------------
# BettableOutcome class tests
# --------------------------
class BettableOutcomeTestCase(unittest.TestCase):
    def setUp(self):
        self.part_bourn1 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH")
        self.part_bournafc = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH AFC")
        self.part_arsenal = arbitrage.Participant("FOOTBALL", "ARSENAL")
        self.part_burn = arbitrage.Participant("FOOTBALL", "BURNLEY")

        self.event_bourn_arsenal = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.part_bourn1, self.part_arsenal])
        self.event_burn_bourn = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.part_burn, self.part_bourn1])
        self.event_bourn_burn = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.part_bourn1, self.part_burn])

        self.odds_good = arbitrage.Odds("10/1")
        self.odds_bad = arbitrage.Odds("2/1")
        self.odds_bad_dec = arbitrage.Odds(3)
        self.odds_good_dec = arbitrage.Odds(11)

    def test_bettableoutcome_equality(self):
        bo_bourn_arsenal_bourn_good = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                self.part_bourn1,
                                                                "WIN",
                                                                "WIN",
                                                                self.odds_good,
                                                                "B")
        bo_bourn_arsenal_bournafc_good = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                   self.part_bournafc,
                                                                   "WIN",
                                                                   "WIN",
                                                                   self.odds_good,
                                                                   "B")
        bo_bourn_arsenal_bourn_good_dec = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                    self.part_bourn1,
                                                                    "WIN",
                                                                    "WIN",
                                                                    self.odds_good_dec,
                                                                    "B")
        bo_bourn_arsenal_bourn_good_dec_B2 = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                    self.part_bourn1,
                                                                    "WIN",
                                                                    "WIN",
                                                                    self.odds_good_dec,
                                                                    "B2")
        # Test decimal vs text odds
        self.assertEqual(bo_bourn_arsenal_bourn_good_dec, bo_bourn_arsenal_bourn_good)
        # Test different version of same participant
        self.assertEqual(bo_bourn_arsenal_bourn_good, bo_bourn_arsenal_bournafc_good)
        # Test diff bookies
        self.assertEqual(bo_bourn_arsenal_bourn_good_dec, bo_bourn_arsenal_bourn_good_dec_B2)

    def test_bettableoutcome_not_equality(self):
        bo_bourn_arsenal_bourn_good = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                self.part_bourn1,
                                                                "WIN",
                                                                "WIN",
                                                                self.odds_good,
                                                                "B")
        bo_bourn_arsenal_bourn_bad = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                               self.part_bourn1,
                                                               "WIN",
                                                               "WIN",
                                                               self.odds_bad,
                                                               "B")
        bo_bourn_burn_bourn_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                            self.part_bourn1,
                                                            "WIN",
                                                            "WIN",
                                                            self.odds_good,
                                                            "B")
        bo_bourn_burn_bourn_bad_lose = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                 self.part_bourn1,
                                                                 "LOSE",
                                                                 "WIN",
                                                                 self.odds_good,
                                                                 "B")
        bo_bourn_burn_burn_bad_lose = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                 self.part_burn,
                                                                 "LOSE",
                                                                 "WIN",
                                                                 self.odds_good,
                                                                 "B")

        # Test odds are different
        self.assertNotEqual(bo_bourn_arsenal_bourn_good, bo_bourn_arsenal_bourn_bad)
        # Test events are different
        self.assertNotEqual(bo_bourn_arsenal_bourn_bad, bo_bourn_burn_bourn_bad)
        # Test outcome type different
        self.assertNotEqual(bo_bourn_burn_bourn_bad, bo_bourn_burn_bourn_bad_lose)
        # Test outcome participant is different
        self.assertNotEqual(bo_bourn_burn_bourn_bad_lose, bo_bourn_burn_burn_bad_lose)

    def test_bettableoutcome_less_than(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    self.part_bourn1,
                                                    "WIN",
                                                    "WIN",
                                                    self.odds_bad,
                                                    "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    self.part_bourn1,
                                                    "WIN",
                                                    "WIN",
                                                    self.odds_good,
                                                    "B")
        self.assertLess(bo_e1_p1_o1_bad, bo_e1_p1_o1_good)

    def test_bettableoutcome_greater_than(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    self.part_bourn1,
                                                    "WIN",
                                                    "WIN",
                                                    self.odds_bad,
                                                    "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    self.part_bourn1,
                                                    "WIN",
                                                    "WIN",
                                                    self.odds_good,
                                                    "B")
        self.assertGreater(bo_e1_p1_o1_good, bo_e1_p1_o1_bad)

    def test_bettableoutcome_greater_equal(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    self.part_bourn1,
                                                    "WIN",
                                                    "WIN",
                                                    self.odds_bad,
                                                    "B")
        bo_e1_p1_o1_bad_other_odds = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                               self.part_bourn1,
                                                               "WIN",
                                                               "WIN",
                                                               self.odds_bad_dec,
                                                               "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                     self.part_bourn1,
                                                     "WIN",
                                                     "WIN",
                                                     self.odds_good,
                                                     "B")
        self.assertGreaterEqual(bo_e1_p1_o1_bad, bo_e1_p1_o1_bad_other_odds)
        self.assertGreater(bo_e1_p1_o1_good, bo_e1_p1_o1_bad)

    def test_bettableoutcome_less_equal(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    self.part_bourn1,
                                                    "WIN",
                                                    "WIN",
                                                    self.odds_bad,
                                                    "B")
        bo_e1_p1_o1_good_other_odds = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                self.part_bourn1,
                                                                "WIN",
                                                                "WIN",
                                                                self.odds_good_dec,
                                                                "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    self.part_bourn1,
                                                    "WIN",
                                                    "WIN",
                                                    self.odds_good,
                                                    "B")
        self.assertGreaterEqual(bo_e1_p1_o1_good, bo_e1_p1_o1_good_other_odds)
        self.assertLess(bo_e1_p1_o1_bad, bo_e1_p1_o1_good)

    def test_bettableoutcome_participant_validation(self):
        self.assertRaises(ValueError, lambda :arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                        self.part_arsenal,
                                                                        "WIN",
                                                                        "WIN",
                                                                        self.odds_good,
                                                                        "B"))


class BettableOutcomeShorthandTestCase(unittest.TestCase):
    def setUp(self):
        self.event_bourn_arsenal = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["BOURNEMOUTH", "ARSENAL"])
        self.event_burn_bourn = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["BURNLEY", "BOURNEMOUTH"])
        self.event_bourn_burn = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["BOURNEMOUTH", "BURNLEY"])

    def test_bettableoutcome_equality(self):
        bo_bourn_arsenal_bourn_good = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                "BOURNEMOUTH",
                                                                "WIN",
                                                                "WIN",
                                                                "10/1",
                                                                "B")
        bo_bourn_arsenal_bournafc_good = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                   "BOURNEMOUTH AFC",
                                                                   "WIN",
                                                                   "WIN",
                                                                   "10/1",
                                                                   "B")
        bo_bourn_arsenal_bourn_good_dec = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                    "BOURNEMOUTH",
                                                                    "WIN",
                                                                    "WIN",
                                                                    11,
                                                                    "B")
        bo_bourn_arsenal_bourn_good_dec_B2 = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                       "BOURNEMOUTH",
                                                                       "WIN",
                                                                       "WIN",
                                                                       11,
                                                                       "B2")
        # Test decimal vs text odds
        self.assertEqual(bo_bourn_arsenal_bourn_good_dec, bo_bourn_arsenal_bourn_good)
        # Test different version of same participant
        self.assertEqual(bo_bourn_arsenal_bourn_good, bo_bourn_arsenal_bournafc_good)
        # Test diff bookies
        self.assertEqual(bo_bourn_arsenal_bourn_good_dec, bo_bourn_arsenal_bourn_good_dec_B2)

    def test_bettableoutcome_not_equality(self):
        bo_bourn_arsenal_bourn_good = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                                "BOURNEMOUTH",
                                                                "WIN",
                                                                "WIN",
                                                                "10/1",
                                                                "B")
        bo_bourn_arsenal_bourn_bad = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                               "BOURNEMOUTH",
                                                               "WIN",
                                                               "WIN",
                                                               "2/1",
                                                               "B")
        bo_bourn_burn_bourn_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                            "BOURNEMOUTH",
                                                            "WIN",
                                                            "WIN",
                                                            "10/1",
                                                            "B")
        bo_bourn_burn_bourn_bad_lose = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                 "BOURNEMOUTH",
                                                                 "LOSE",
                                                                 "WIN",
                                                                 "10/1",
                                                                 "B")
        bo_bourn_burn_burn_bad_lose = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                "BURNLEY",
                                                                "LOSE",
                                                                "WIN",
                                                                "10/1",
                                                                "B")

        # Test odds are different
        self.assertNotEqual(bo_bourn_arsenal_bourn_good, bo_bourn_arsenal_bourn_bad)
        # Test events are different
        self.assertNotEqual(bo_bourn_arsenal_bourn_bad, bo_bourn_burn_bourn_bad)
        # Test outcome type different
        self.assertNotEqual(bo_bourn_burn_bourn_bad, bo_bourn_burn_bourn_bad_lose)
        # Test outcome participant is different
        self.assertNotEqual(bo_bourn_burn_bourn_bad_lose, bo_bourn_burn_burn_bad_lose)

    def test_bettableoutcome_less_than(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    "BOURNEMOUTH",
                                                    "WIN",
                                                    "WIN",
                                                    "2/1",
                                                    "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                     "BOURNEMOUTH",
                                                     "WIN",
                                                     "WIN",
                                                     "10/1",
                                                     "B")
        self.assertLess(bo_e1_p1_o1_bad, bo_e1_p1_o1_good)

    def test_bettableoutcome_greater_than(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    "BOURNEMOUTH",
                                                    "WIN",
                                                    "WIN",
                                                    "2/1",
                                                    "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                     "BOURNEMOUTH",
                                                     "WIN",
                                                     "WIN",
                                                     "10/1",
                                                     "B")
        self.assertGreater(bo_e1_p1_o1_good, bo_e1_p1_o1_bad)

    def test_bettableoutcome_greater_equal(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    "BOURNEMOUTH",
                                                    "WIN",
                                                    "WIN",
                                                    "2/1",
                                                    "B")
        bo_e1_p1_o1_bad_other_odds = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                               "BOURNEMOUTH",
                                                               "WIN",
                                                               "WIN",
                                                               3,
                                                               "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                     "BOURNEMOUTH",
                                                     "WIN",
                                                     "WIN",
                                                     "10/1",
                                                     "B")
        self.assertGreaterEqual(bo_e1_p1_o1_bad, bo_e1_p1_o1_bad_other_odds)
        self.assertGreater(bo_e1_p1_o1_good, bo_e1_p1_o1_bad)

    def test_bettableoutcome_less_equal(self):
        bo_e1_p1_o1_bad = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                    "BOURNEMOUTH",
                                                    "WIN",
                                                    "WIN",
                                                    "2/1",
                                                    "B")
        bo_e1_p1_o1_good_other_odds = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                "BOURNEMOUTH",
                                                                "WIN",
                                                                "WIN",
                                                                11,
                                                                "B")
        bo_e1_p1_o1_good = arbitrage.BettableOutcome(self.event_bourn_burn,
                                                     "BOURNEMOUTH",
                                                     "WIN",
                                                     "WIN",
                                                     "10/1",
                                                     "B")
        self.assertGreaterEqual(bo_e1_p1_o1_good, bo_e1_p1_o1_good_other_odds)
        self.assertLess(bo_e1_p1_o1_bad, bo_e1_p1_o1_good)

    def test_bettableoutcome_participant_validation(self):
        self.assertRaises(ValueError, lambda :arbitrage.BettableOutcome(self.event_bourn_burn,
                                                                        "ARSENAL",
                                                                        "WIN",
                                                                        "WIN",
                                                                        "10/1",
                                                                        "B"))


# --------------------------
# Bet class tests
# --------------------------
class BetTestCase(unittest.TestCase):
    def setUp(self):
        self.part_bourn1 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH")
        self.part_arsenal = arbitrage.Participant("FOOTBALL", "ARSENAL")
        self.event_bourn_arsenal = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE",
                                                   [self.part_bourn1, self.part_arsenal])
        self.odds_good = arbitrage.Odds("10/1")
        self.odds_good_two = arbitrage.Odds("10/3")

        self.bettable_outcome = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                          self.part_bourn1,
                                                          "WIN",
                                                          "WIN",
                                                          self.odds_good,
                                                          "B")
        self.bettable_outcome_two = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                              self.part_bourn1,
                                                              "WIN",
                                                              "WIN",
                                                              self.odds_good_two,
                                                              "B")

    def test_bet_amounts(self):
        bet = arbitrage.Bet(self.bettable_outcome, 100)

        self.assertEqual(bet.bet_amount, 100)
        self.assertEqual(bet.return_amount, 1100)
        self.assertEqual(bet.profit_amount, 1000)

    def test_bet_amounts_complicated(self):
        bet = arbitrage.Bet(self.bettable_outcome_two, 52)

        self.assertEqual(bet.bet_amount, 52)
        self.assertEqual(bet.return_amount, 225.33)
        self.assertEqual(bet.profit_amount, 173.33)


class BetShortHandTestCase(unittest.TestCase):
    def setUp(self):
        self.event_bourn_arsenal = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE",
                                                   ["BOURNEMOUTH", "ARSENAL"])

        self.bettable_outcome = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                          "BOURNEMOUTH",
                                                          "WIN",
                                                          "WIN",
                                                          "10/1",
                                                          "B")
        self.bettable_outcome_two = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                              "BOURNEMOUTH",
                                                              "WIN",
                                                              "WIN",
                                                              "10/3",
                                                              "B")

    def test_bet_amounts(self):
        bet = arbitrage.Bet(self.bettable_outcome, 100)

        self.assertEqual(bet.bet_amount, 100)
        self.assertEqual(bet.return_amount, 1100)
        self.assertEqual(bet.profit_amount, 1000)

    def test_bet_amounts_complicated(self):
        bet = arbitrage.Bet(self.bettable_outcome_two, 52)

        self.assertEqual(bet.bet_amount, 52)
        self.assertEqual(bet.return_amount, 225.33)
        self.assertEqual(bet.profit_amount, 173.33)


# --------------------------
# ArbitrageBet class tests
# --------------------------
class ArbitrageBetTestCase(unittest.TestCase):
    """Tests for ArbitrageBet class in arbitrage.py."""

    def test_validations_same_event(self):
        """Does the arb bet fail when events are different?"""
        event2 = arbitrage.Event("FOOTBALL", "FA CUP", [self.part_bourn1, self.part_arsenal])
        bo_draw = arbitrage.BettableOutcome(event2, self.part_arsenal, "LOSE", "LOSE",
                                            arbitrage.Odds(5.1), "B2")

        self.assertRaises(ValueError, lambda: arbitrage.ArbitrageBet([bo_draw, self.bo_arse]))

    def test_validations_same_outcometype(self):
        """Does the arb bet fail when outcome type is different?"""
        bo_goals = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                             self.part_bourn1,
                                             "GOALS",
                                             "More than 1",
                                             arbitrage.Odds(1),
                                             "B2")

        self.assertRaises(ValueError, lambda : arbitrage.ArbitrageBet([self.bo_arse, bo_goals]))

    def test_validations_incomplete_outcome_type(self):
        """Does the arb bet fail when outcome type is incomplete?"""
        self.assertRaises(ValueError, lambda : arbitrage.ArbitrageBet([self.bo_bourn, self.bo_arse]))

    def test_no_total_investment_change(self):
        """Is profit calculated correctly when total_investment is not changed?"""
        arb_bet = arbitrage.ArbitrageBet([self.bo_bourn, self.bo_arse, self.bo_draw], total_investment=199)

        self.assertEqual(arb_bet.arb_perc, 96.59)
        self.assertEqual(arb_bet.profit, 7.01)
        self.assertEqual(arb_bet.return_perc, 3.52)
        self.assertEqual(arb_bet.total_investment, 199)

    def test_total_investment_change(self):
        """Is profit calculated correctly when total_investment is changed?"""
        arb_bet = arbitrage.ArbitrageBet([self.bo_bourn, self.bo_arse, self.bo_draw], total_investment=1990)

        self.assertEqual(arb_bet.arb_perc, 96.59)
        self.assertEqual(arb_bet.profit, 70.27)
        self.assertEqual(arb_bet.return_perc, 3.53)
        self.assertAlmostEqual(arb_bet.total_investment, 1990, places=1)

    def test_set_betting_amounts_integer_round(self):
        # TODO: Betting amount integer rounding test
        """Does the arbitrageBet integer rounding work correctly?"""
        arb_bet = arbitrage.ArbitrageBet([self.bo_bourn, self.bo_arse, self.bo_draw], total_investment=1990)

        self.assertEqual(arb_bet.arb_perc, 96.59)
        self.assertEqual(arb_bet.profit, 70.27)
        self.assertEqual(arb_bet.return_perc, 3.53)
        self.assertAlmostEqual(arb_bet.total_investment, 1990, places=1)
        pass

    def setUp(self):
        self.part_bourn1 = arbitrage.Participant("FOOTBALL", "BOURNEMOUTH")
        self.part_arsenal = arbitrage.Participant("FOOTBALL", "ARSENAL")
        self.event_bourn_arsenal = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE",
                                                   [self.part_bourn1, self.part_arsenal])
        self.odds_bourn = arbitrage.Odds(4.3)
        self.odds_arsenal = arbitrage.Odds(3)
        self.odds_draw = arbitrage.Odds(2.5)

        self.bo_bourn = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                  self.part_bourn1,
                                                  "FULLTIME_RESULT",
                                                  "WIN",
                                                  self.odds_bourn,
                                                  "B")
        self.bo_arse = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                    self.part_arsenal,
                                                    "FULLTIME_RESULT",
                                                    "WIN",
                                                    self.odds_arsenal,
                                                    "B")
        self.bo_draw = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                 self.part_bourn1,
                                                 "FULLTIME_RESULT",
                                                 "DRAW",
                                                 self.odds_draw,
                                                 "B")


class ArbitrageBetShortHandTestCase(unittest.TestCase):
    """Tests for ArbitrageBet class in arbitrage.py."""

    def test_validations_same_event(self):
        """Does the arb bet fail when events are different?"""
        event2 = arbitrage.Event("FOOTBALL", "FA CUP", ["BOURNEMOUTH", "ARSENAL"])
        bo_draw = arbitrage.BettableOutcome(event2, "ARSENAL", "LOSE", "LOSE",
                                            5.1, "B2")

        self.assertRaises(ValueError, lambda: arbitrage.ArbitrageBet([bo_draw, self.bo_arse]))

    def test_validations_same_outcometype(self):
        """Does the arb bet fail when outcome type is different?"""
        bo_goals = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                             "BOURNEMOUTH",
                                             "GOALS",
                                             "More than 1",
                                             1,
                                             "B2")

        self.assertRaises(ValueError, lambda: arbitrage.ArbitrageBet([self.bo_arse, bo_goals]))

    def test_validations_incomplete_outcome_type(self):
        """Does the arb bet fail when outcome type is incomplete?"""
        self.assertRaises(ValueError, lambda: arbitrage.ArbitrageBet([self.bo_bourn, self.bo_arse]))

    def test_no_total_investment_change(self):
        """Is profit calculated correctly when total_investment is not changed?"""
        arb_bet = arbitrage.ArbitrageBet([self.bo_bourn, self.bo_arse, self.bo_draw], total_investment=199)

        self.assertEqual(arb_bet.arb_perc, 96.59)
        self.assertEqual(arb_bet.profit, 7.01)
        self.assertEqual(arb_bet.return_perc, 3.52)
        self.assertEqual(arb_bet.total_investment, 199)

    def test_total_investment_change(self):
        """Is profit calculated correctly when total_investment is changed?"""
        arb_bet = arbitrage.ArbitrageBet([self.bo_bourn, self.bo_arse, self.bo_draw], total_investment=1990)

        self.assertEqual(arb_bet.arb_perc, 96.59)
        self.assertEqual(arb_bet.profit, 70.27)
        self.assertEqual(arb_bet.return_perc, 3.53)
        self.assertAlmostEqual(arb_bet.total_investment, 1990, places=1)

    def setUp(self):
        self.event_bourn_arsenal = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE",
                                                   ["BOURNEMOUTH", "ARSENAL"])

        self.bo_bourn = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                  "BOURNEMOUTH",
                                                  "FULLTIME_RESULT",
                                                  "WIN",
                                                  4.3,
                                                  "B")
        self.bo_arse = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                 "ARSENAL",
                                                 "FULLTIME_RESULT",
                                                 "WIN",
                                                 3,
                                                 "B")
        self.bo_draw = arbitrage.BettableOutcome(self.event_bourn_arsenal,
                                                 "BOURNEMOUTH",
                                                 "FULLTIME_RESULT",
                                                 "DRAW",
                                                 2.5,
                                                 "B")


# ------------------------------
# ArbitrageBetParser class tests
# ------------------------------
class ArbitrageBetParserArbBettingAmountsTestCase(unittest.TestCase):
    def setUp(self):

        self.participant_1 = arbitrage.Participant("FOOTBALL", "ARSENAL")
        self.participant_2 = arbitrage.Participant("FOOTBALL", "LIVERPOOL")
        self.event = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", [self.participant_1, self.participant_2])

        self.bo_B1_1_win = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "WIN",
                                               arbitrage.Odds(4.3), "B1")
        self.bo_B1_2_win = arbitrage.BettableOutcome(self.event, self.participant_2, "FULLTIME RESULT", "LOSE",
                                               arbitrage.Odds(2), "B1")
        self.bo_B1_draw = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "DRAW",
                                               arbitrage.Odds(1), "B1")

        self.bo_B2_1_win = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "WIN",
                                               arbitrage.Odds(3), "B2")
        self.bo_B2_2_win = arbitrage.BettableOutcome(self.event, self.participant_2, "FULLTIME RESULT", "LOSE",
                                               arbitrage.Odds(3), "B2")
        self.bo_B2_draw = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "DRAW",
                                               arbitrage.Odds(0.8), "B2")

        self.bo_B3_1_win = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "WIN",
                                               arbitrage.Odds(4), "B3")
        self.bo_B3_2_win = arbitrage.BettableOutcome(self.event, self.participant_2, "FULLTIME RESULT", "LOSE",
                                               arbitrage.Odds(1.7), "B3")
        self.bo_B3_draw = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "DRAW",
                                               arbitrage.Odds(2.5), "B3")

        self.bo_B4_1_win = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "WIN",
                                               arbitrage.Odds(4), "B4")
        self.bo_B4_2_win = arbitrage.BettableOutcome(self.event, self.participant_2, "FULLTIME RESULT", "LOSE",
                                               arbitrage.Odds(1.7), "B4")
        self.bo_B4_draw = arbitrage.BettableOutcome(self.event, self.participant_1, "FULLTIME RESULT", "DRAW",
                                               arbitrage.Odds(2.7), "B4")

        self.arb = arbitrage.ArbitrageBetParser([self.bo_B1_1_win, self.bo_B1_2_win, self.bo_B1_draw,
                                                 self.bo_B2_1_win, self.bo_B2_2_win, self.bo_B2_draw,
                                                 self.bo_B3_1_win, self.bo_B3_2_win, self.bo_B3_draw])

        self.arb2 = arbitrage.ArbitrageBetParser([self.bo_B1_1_win, self.bo_B1_2_win, self.bo_B1_draw,
                                                  self.bo_B2_1_win, self.bo_B2_2_win, self.bo_B2_draw,
                                                  self.bo_B3_1_win, self.bo_B3_2_win, self.bo_B3_draw,
                                                  self.bo_B4_1_win, self.bo_B4_2_win, self.bo_B4_draw])

    def test_get_arb_betting_amounts(self):
        win_bet = [x.bet_amount for x in self.arb.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "WIN"][0]
        lose_bet = [x.bet_amount for x in self.arb.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "LOSE"][0]
        draw_bet = [x.bet_amount for x in self.arb.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "DRAW"][0]

        self.assertEqual(win_bet, 24.08)
        self.assertEqual(lose_bet, 34.51)
        self.assertEqual(draw_bet, 41.41)

        win_bet = [x.bet_amount for x in self.arb2.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "WIN"][0]
        lose_bet = [x.bet_amount for x in self.arb2.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "LOSE"][0]
        draw_bet = [x.bet_amount for x in self.arb2.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "DRAW"][0]

        self.assertEqual(win_bet, 24.84)
        self.assertEqual(lose_bet, 35.60)
        self.assertEqual(draw_bet, 39.56)

    def test_arb_event_string_output(self):
        self.assertTrue("B1:ARSENAL(1)-FULLTIME RESULT-WIN: 24.08[103.54]" in str(self.arb))
        self.assertTrue("B3:ARSENAL(1)-FULLTIME RESULT-DRAW: 41.41[103.52]" in str(self.arb))
        self.assertTrue("B2:LIVERPOOL(9)-FULLTIME RESULT-LOSE: 34.51[103.53]" in str(self.arb))


class ArbitrageBetParserArbBettingAmountsShortHandTestCase(unittest.TestCase):
    def setUp(self):
        self.event = arbitrage.Event("FOOTBALL", "PREMIER LEAGUE", ["ARSENAL", "LIVERPOOL"])

        self.bo_B1_1_win = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "WIN", 4.3, "B1")
        self.bo_B1_2_win = arbitrage.BettableOutcome(self.event, "LIVERPOOL", "FULLTIME RESULT", "LOSE", 2, "B1")
        self.bo_B1_draw = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "DRAW", 1, "B1")

        self.bo_B2_1_win = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "WIN", 3, "B2")
        self.bo_B2_2_win = arbitrage.BettableOutcome(self.event, "LIVERPOOL", "FULLTIME RESULT", "LOSE", 3, "B2")
        self.bo_B2_draw = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "DRAW", 0.8, "B2")

        self.bo_B3_1_win = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "WIN", 4, "B3")
        self.bo_B3_2_win = arbitrage.BettableOutcome(self.event, "LIVERPOOL", "FULLTIME RESULT", "LOSE", 1.7, "B3")
        self.bo_B3_draw = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "DRAW", 2.5, "B3")

        self.bo_B4_1_win = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "WIN", 4, "B4")
        self.bo_B4_2_win = arbitrage.BettableOutcome(self.event, "LIVERPOOL", "FULLTIME RESULT", "LOSE", 1.7, "B4")
        self.bo_B4_draw = arbitrage.BettableOutcome(self.event, "ARSENAL", "FULLTIME RESULT", "DRAW", 2.7, "B4")

        self.arb = arbitrage.ArbitrageBetParser([self.bo_B1_1_win, self.bo_B1_2_win, self.bo_B1_draw,
                                                 self.bo_B2_1_win, self.bo_B2_2_win, self.bo_B2_draw,
                                                 self.bo_B3_1_win, self.bo_B3_2_win, self.bo_B3_draw])

        self.arb2 = arbitrage.ArbitrageBetParser([self.bo_B1_1_win, self.bo_B1_2_win, self.bo_B1_draw,
                                                  self.bo_B2_1_win, self.bo_B2_2_win, self.bo_B2_draw,
                                                  self.bo_B3_1_win, self.bo_B3_2_win, self.bo_B3_draw,
                                                  self.bo_B4_1_win, self.bo_B4_2_win, self.bo_B4_draw])

    def test_get_arb_betting_amounts(self):
        win_bet = [x.bet_amount for x in self.arb.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "WIN"][0]
        lose_bet = [x.bet_amount for x in self.arb.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "LOSE"][0]
        draw_bet = [x.bet_amount for x in self.arb.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "DRAW"][0]

        self.assertEqual(win_bet, 24.08)
        self.assertEqual(lose_bet, 34.51)
        self.assertEqual(draw_bet, 41.41)

        win_bet = [x.bet_amount for x in self.arb2.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "WIN"][0]
        lose_bet = [x.bet_amount for x in self.arb2.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "LOSE"][0]
        draw_bet = [x.bet_amount for x in self.arb2.arbitrage_bets[0].bets if x.bettable_outcome.outcome == "DRAW"][0]

        self.assertEqual(win_bet, 24.84)
        self.assertEqual(lose_bet, 35.60)
        self.assertEqual(draw_bet, 39.56)

    def test_arb_event_string_output(self):
        self.assertTrue("B1:ARSENAL(1)-FULLTIME RESULT-WIN: 24.08[103.54]" in str(self.arb))
        self.assertTrue("B3:ARSENAL(1)-FULLTIME RESULT-DRAW: 41.41[103.52]" in str(self.arb))
        self.assertTrue("B2:LIVERPOOL(9)-FULLTIME RESULT-LOSE: 34.51[103.53]" in str(self.arb))


class ArbitrageBetParserFromRealFilesTestCase(unittest.TestCase):
    """Tests for ArbitrageBetParser from real files"""
    def setUp(self):
        self.bettable_outcome_list = []
        self.paddy = arbitrage.OddsPageParser(mwutils.get_page_source_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                           "Paddy_Football_L2.txt")), "PADDYPOWER", "FOOTBALL")
        self.eee = arbitrage.OddsPageParser(mwutils.get_page_source_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
                                         "888_Football_L2.txt")), "EIGHT88", "FOOTBALL")

        self.bettable_outcome_list += self.paddy.bettable_outcomes
        self.bettable_outcome_list += self.eee.bettable_outcomes

    def test_correct_number_of_arbs_full_pairing(self):
        """Are all pairs of arbs created when full pairings are present?"""
        arb_parser = arbitrage.ArbitrageBetParser(self.bettable_outcome_list)
        self.assertEqual(len(arb_parser.possible_arbitrage_events), 12)
        self.assertEqual(len(arb_parser.singleton_events), 0)

    def test_correct_number_of_arbs_partial_pairing_1(self):
        """Are all pairs of arbs created when there are partial pairings present?"""
        del self.bettable_outcome_list[3:6]
        arb_parser = arbitrage.ArbitrageBetParser(self.bettable_outcome_list)
        self.assertEqual(len(arb_parser.possible_arbitrage_events), 11)
        self.assertEqual(len(arb_parser.singleton_events), 1)

    def test_correct_number_of_arbs_partial_pairing_2(self):
        """Are all pairs of arbs created when there are partial pairings present?"""
        del self.bettable_outcome_list[3:6]
        del self.bettable_outcome_list[42:45]
        arb_parser = arbitrage.ArbitrageBetParser(self.bettable_outcome_list)
        self.assertEqual(len(arb_parser.possible_arbitrage_events), 10)
        self.assertEqual(len(arb_parser.singleton_events), 2)

    def test_correct_number_of_possible_arbs_full_pairing(self):
        """Are arbs correctly identified?"""
        arb_parser = arbitrage.ArbitrageBetParser(self.bettable_outcome_list)
        self.assertEqual(len(arb_parser.arbitrage_bets), 0)

        self.bettable_outcome_list[1].odds.odds = 20
        self.bettable_outcome_list[1].odds.odds_arb = 0.05
        self.bettable_outcome_list[36].odds.odds_arb = 20
        self.bettable_outcome_list[36].odds.odds_arb = 0.05
        arb_parser2 = arbitrage.ArbitrageBetParser(self.bettable_outcome_list)
        self.assertEqual(len(arb_parser2.arbitrage_bets), 1)