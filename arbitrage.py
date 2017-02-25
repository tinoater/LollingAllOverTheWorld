import warnings
import copy
from config import *
import time


class Odds:
    """
    Odds, fractional or decimal
    """
    def __init__(self, odds):
        self.odds = self.fractional_to_decimal_odds(odds)
        self.odds_arb = 1/self.odds

    def __str__(self):
        output = str(self.odds) + " (" + str(self.odds_arb) + ")"

        return output

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.odds < other.odds:
                return True

        return False

    def __le__(self, other):
        if isinstance(other, self.__class__):
            if self.odds <= other.odds:
                return True

        return False

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            if self.odds > other.odds:
                return True

        return False

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            if self.odds >= other.odds:
                return True

        return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.odds == other.odds:
                return True

        return False

    def __hash__(self):
        return hash(self.odds)

    def fractional_to_decimal_odds(self, odds):
        """
        Convert odds from fractional to decimal
        :param odds:
        :return:
        """
        if odds is None:
            return None

        try:
            if odds.lower() in ("evens", "evs"):
                return 1
        except AttributeError:
            pass

        try:
            odds = float(odds)
            return round(odds, 5)
        except ValueError:
            num, den = odds.replace(" ", "").split("/")
            return round((float(num) + float(den))/float(den), 5)


class Participant:
    """
    Participant

    identifier: Either name of participant or their id
    """
    def __init__(self, category, identifier):
        self.category = category.upper()
        try:
            self.category_id = CATEGORY_DICT[self.category]
        except KeyError:
            raise KeyError("Category " + category + " not in CATEGORY_DICT")

        if isinstance(identifier, str):
            self.participant = identifier.upper()
            try:
                self.participant_id = PARTICIPANT_DICT[self.category][self.participant]
            except KeyError:
                raise KeyError("Participant " + identifier + " not in PARTICIPANT_DICT for category " + category)
        elif isinstance(identifier, int):
            self.participant = list(PARTICIPANT_DICT[self.category].keys())\
                [list(PARTICIPANT_DICT[self.category].values()).index(identifier)]
            self.participant_id = identifier

    def __str__(self):
        return self.participant + "(" + str(self.participant_id) + ")"

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.category_id == other.category_id:
                if self.participant_id == other.participant_id:
                    return True

        return False

    def __hash__(self):
        return hash((self.category_id, self.participant_id))


class Event:
    """
    Real-world event
    """
    def __init__(self, category, sub_category, participant_list, date=None, time=None):
        self.category = category.upper()
        self.sub_category = sub_category.upper()
        # TODO: Make it handle this date as a datetime object, for now it is a string
        self.date = date
        self.time = time

        # Read participants. Can either be participant class, the name or the id
        self.participants = []
        for participant in participant_list:
            if isinstance(participant, Participant):
                self.participants.append(participant)
            elif isinstance(participant, str):
                try:
                    self.participants.append(Participant(self.category, participant))
                except KeyError:
                    raise KeyError(participant + " not in participant dictionary for " + self.category)
            elif isinstance(participant, int):
                self.participants.append(Participant(self.category, participant))
        self.participant_ids = [x.participant_id for x in self.participants]

        try:
            self.category_id = CATEGORY_DICT[self.category]
        except IndexError:
            raise IndexError("Category " + self.category + " not in CATEGORY_DICT")

        try:
            self.sub_category_id = SUBCATEGORY_DICT[self.category][self.sub_category]
        except KeyError:
            raise KeyError("Subcategory " + self.sub_category + " not in SUBCATEGORY_DICT")

    def __str__(self):
        output = ""
        if self.date is not None:
            output += str(self.date) + "-"

        output += self.category + "-" + self.sub_category + "-"

        for participant in self.participants:
            output += str(participant) + ","

        output = output[:-1]

        return output

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.category_id == other.category_id and self.sub_category_id == other.sub_category_id:
                if set(self.participant_ids) == set(other.participant_ids):
                    return True

        return False

    def __hash__(self):
        self.participants.sort(key=lambda x: x.participant_id)
        participants_tup = tuple(self.participants)
        properties_tup = (self.category_id, self.sub_category_id, participants_tup)

        return hash(properties_tup)


class BettableOutcome:
    """
    Bookmaker, event, participant, outcome_type, outcome and odds

    Supported outcome_types and outcomes:
    FULLTIME_RESULT: HOME_WIN, AWAY_WIN, DRAW     (Paticipant does nothing)
    """
    # TODO: Either remove participant from this or utilise it
    def __init__(self, event, participant, outcome_type, outcome, odds, bookmaker):
        self.outcome_type = outcome_type
        self.outcome = outcome
        self.bookmaker = bookmaker
        self.event = event

        # Participant
        if isinstance(participant, Participant):
            self.participant = participant
        elif isinstance(participant, str):
            try:
                self.participant = Participant(self.event.category, participant)
            except KeyError:
                raise KeyError(participant + " not in participant dictionary for " + self.event.category)
        elif isinstance(participant, id):
            self.participant = Participant(self.event.category, participant)
        else:
            raise ValueError("Participant type incorrect. Needs to be Participant, str or int not "
                             + str(type(participant)))

        # Odds
        if isinstance(odds, Odds):
            self.odds = odds
        elif isinstance(odds, str):
            self.odds = Odds(odds)
        elif isinstance(odds, float) or isinstance(odds, int):
            self.odds = Odds(odds)
        else:
            raise ValueError("Odds type inccorect. Needs to be Odds, float or int not " + str(type(odds)))

        # Validations
        if self.participant not in self.event.participants:
            raise ValueError("Participant not in the Event")

    def __str__(self):
        outcome = self.bookmaker + "-" + \
                  str(self.event) + "-" + \
                  self.participant.participant + \
                  "-" + self.outcome_type + ":" + str(self.odds)

        return outcome

    def __lt__(self, other):
        if isinstance(other, self.__class__):
            if self.participant == other.participant and self.event == other.event and \
               self.outcome_type == other.outcome_type:
                if self.odds.odds < other.odds.odds:
                    return True

        return False

    def __le__(self, other):
        if isinstance(other, self.__class__):
            if self.participant == other.participant and self.event == other.event and \
               self.outcome_type == other.outcome_type:
                if self.odds.odds <= other.odds.odds:
                    return True

        return False

    def __gt__(self, other):
        if isinstance(other, self.__class__):
            if self.participant == other.participant and self.event == other.event and \
               self.outcome_type == other.outcome_type:
                if self.odds.odds > other.odds.odds:
                    return True

        return False

    def __ge__(self, other):
        if isinstance(other, self.__class__):
            if self.participant == other.participant and self.event == other.event and \
               self.outcome_type == other.outcome_type:
                if self.odds.odds >= other.odds.odds:
                    return True

        return False

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.participant == other.participant and self.event == other.event and \
               self.outcome_type == other.outcome_type:
                if self.odds.odds == other.odds.odds:
                    return True

        return False

    def __hash__(self):
        properties_tup = (self.event, self.participant, self.outcome_type, self.outcome, self.odds, self.bookmaker)

        return hash(properties_tup)


class Bet:
    def __init__(self, BettableOutcome, bet_amount):
        self.bettable_outcome = BettableOutcome
        self.event = self.bettable_outcome.event
        self.odds = self.bettable_outcome.odds

        self.bet_amount = 0
        self.return_amount = 0
        self.profit_amount = 0

        self.set_bet_amount(bet_amount)

    def __str__(self):
        output = self.bettable_outcome.bookmaker + ":" + str(self.bettable_outcome.participant) + "-" + \
                 self.bettable_outcome.outcome_type + "-" + str(self.bettable_outcome.outcome) + "[" + \
                 str(round(self.bettable_outcome.odds.odds, 2)) + "] " + \
                 "Bet: " + str(self.bet_amount) + " Return: " + str(self.return_amount)

        return output

    def __hash__(self):
        return hash((self.bettable_outcome, self.bet_amount))

    def set_bet_amount(self, amount):
        self.bet_amount = amount
        self.return_amount = round(self.bet_amount * self.bettable_outcome.odds.odds, 2)
        self.profit_amount = self.return_amount - self.bet_amount


class ArbitrageBet:
    """
    Combination of BettableOutcomes to try to form an arbitrage
    """
    def __init__(self, bettable_outcomes, total_investment=100, integer_round=False):
        self.bettable_outcomes = copy.deepcopy(bettable_outcomes)

        # First check that all bets are for the same event
        if len(set([x.event for x in self.bettable_outcomes])) != 1:
            raise ValueError("Multiple events in ArbitrageBet")
        # Check that all bets are for the same outcome type
        if len(set([x.outcome_type for x in self.bettable_outcomes])) != 1:
            raise ValueError("Multiple outcome_types in ArbitrageBet")
        else:
            self.outcome_type = self.bettable_outcomes[0].outcome_type
        # Check that we have the full set of outcomes for this outcome_type
        # TODO: Make the outcome_type check generic
        self.outcomes = set([x.outcome for x in self.bettable_outcomes])
        if self.outcome_type == "FULLTIME_RESULT":
            if "DRAW" not in self.outcomes:
                raise ValueError("Not all outcomes present for FULLTIME_RESULT. Only have :" + str(self.outcomes))
        elif self.outcome_type == "FULLTIME_RESULT_NO_DRAW":
            if "WIN" not in self.outcomes or "LOSE" not in self.outcomes:
                raise ValueError("Not all outcomes present for FULLTIME_RESULT_NO_DRAW. Only have :" + str(self.outcomes))

        self.arb_perc = round(sum([x.odds.odds_arb for x in self.bettable_outcomes]), 4) * 100

        # Check if this is actually an arbitrage
        if self.arb_perc >= 100:
            self.arbitrage_present = False
        else:
            self.arbitrage_present = True

        # Get the date of the arb - this may be set on at least one or none of the events
        event_dates = [x.event.date for x in self.bettable_outcomes if x.event.date is not None]
        if len(event_dates) > 0:
            self.event_date = event_dates[0]
        else:
            self.event_date = None

        # Create the associated bets
        self.bets = []
        for bo in self.bettable_outcomes:
            self.bets.append(Bet(bo, 0))

        # Scale them to the desired cost
        self.set_arb_betting_amounts(total_investment, integer_round=integer_round)
        self.total_investment = sum([x.bet_amount for x in self.bets])

        # Set the profit values
        self.profit = round(min(x.return_amount - self.total_investment for x in self.bets), 2)
        self.return_perc = round(self.profit / self.total_investment * 100, 2)

    def __str__(self):
        output = "Return percentage: " + str(self.return_perc)
        if self.event_date is not None:
            output += " (" + self.event_date + ")"

        output += "\n" + str(self.bettable_outcomes[0].event)

        for bet in self.bets:
            output += "\n" + str(bet)

        return output

    def set_arb_betting_amounts(self, total_investment, integer_round):
        """
        Calculate required betting amounts for arb
        :param total_investment:
        :return:
        """
        for bet in self.bets:
            bet.set_bet_amount(round(bet.odds.odds_arb * 100 * total_investment / self.arb_perc, 2))

        if integer_round:
            pass
            # TODO: Finish the integer rounding function
        #    approx_betting = []
        #    # Test each possible bet and pick the one with the best rate of return
        #    for win_approx in (math.floor(win_bet), math.ceil(win_bet)):
        #        for draw_approx in (math.floor(draw_bet), math.ceil(draw_bet)):
        #            for lose_approx in (math.floor(lose_bet), math.ceil(lose_bet)):
        #                bets = (win_approx, draw_approx, lose_approx)
        #                bet_return = min(win_approx * self.win_odds,
        #                                 draw_approx * self.draw_odds,
        #                                 lose_approx * self.lose_odds)
        #                bet_return -= win_approx + draw_approx + lose_approx
        #                bet_return /= (win_approx + draw_approx + lose_approx)
        #                approx_betting.append([bet_return, bets])
        #    # Pick the best return
        #    t = max(approx_betting, key=lambda x: x[0])
        #    return t[1]

        self.arb_profit = min([x.profit_amount for x in self.bets])


class ArbitrageBetParser:
    """
    Parses a collection of BettingOutcomes for all ArbitrageBets
    """
    def __init__(self, bettable_outcome_list):
        self.bettable_outcomes = copy.deepcopy(bettable_outcome_list)
        self.possible_arbitrage_events = []
        self.singleton_events = []

        # Set a False matched flag against each bettable_outcome in the list
        for each in self.bettable_outcomes:
            each.match = False

        # TODO: This outcome logic needs to be rethunk to deal with p1 LOSE == p2 WIN
        # First check that we have multiple bookmakers
        all_bookmakers = set([x.bookmaker for x in self.bettable_outcomes])
        if len(all_bookmakers) == 1:
            warnings.warn("Only one bookmaker passed in")
        else:
            # For each (event, outcome_type)
            event_outcomes = set([(x.event, x.outcome_type) for x in self.bettable_outcomes])
            for event_outcome in event_outcomes:
                # Find all similar
                event_outcome_bos = [x for x in self.bettable_outcomes if x.event == event_outcome[0]
                           and x.outcome_type == event_outcome[1]]
                # Get the best odds for each outcome
                outcomes = set([x.outcome for x in event_outcome_bos])
                # Check for singleton event_outcomes
                if len(outcomes) == len([x.outcome for x in event_outcome_bos]):
                    arb = ArbitrageBet(event_outcome_bos)
                    self.singleton_events.append(arb)
                else:
                    event_outcome_arb_candidate = []
                    for outcome in outcomes:
                        event_outcome_arb_candidate.append(max([x for x in event_outcome_bos if x.outcome == outcome],
                                                               key=lambda y: y.odds))
                    # Create an ArbitrageBet
                    arb = ArbitrageBet(event_outcome_arb_candidate)
                    self.possible_arbitrage_events.append(arb)

        # All bettable_outcomes now parsed into ArbitrageBets
        self.arbitrage_bets = [x for x in self.possible_arbitrage_events if x.arbitrage_present]
        # Sort by arb percentage
        self.arbitrage_bets.sort(key=lambda x: x.arb_perc)

    def __str__(self):
        """
        Multiple Odds for Events: 21
        Orphaned Odds for Evens: 3
        Arb possibilities: 1
        :return:
        """
        output = "Multiple Odds for Events: " + str(len(self.possible_arbitrage_events)) + "\n"
        output += "Singleton Odds for Events: " + str(len(self.singleton_events)) + "\n"
        output += "Arb possibilities: " + str(len(self.arbitrage_bets)) + "\n"

        for each in self.arbitrage_bets:
            output += str(each) + "\n"

        return output

    def get_full_output(self, to_screen=True, out_file_path=None):
        output = "------ SUMMARY -----" + "\n"
        output += str(self) + "\n\n"

        if len(self.arbitrage_bets) > 0:
            output += "------ All Possible Arbs -----" + "\n"
            for arb in self.arbitrage_bets:
                output += str(arb) + "\n"
        else:
            output += "------ No Possible Arbs -----" + "\n"

        if len(self.singleton_events) > 0:
            output += "------ All Singleton Events -----" + "\n"
            for orphan in self.singleton_events:
                output += str(orphan) + "\n"
        else:
            output += "------ No Singleton Events -----" + "\n"

        output += "------ All Bet Collections -----" + "\n"
        for arb in self.possible_arbitrage_events:
            output += str(arb) + "\n\n"

        if out_file_path is not None:
            if not os.path.exists(os.path.dirname(out_file_path)):
                os.makedirs(os.path.dirname(out_file_path))
            out_file = open(out_file_path, "w")
            out_file.write(output)
            out_file.close()

        if to_screen:
            print(output)


class OddsPageParser:
    """
    Parses html_soup into list of BettableOutcomes
    """
    def __init__(self, html_soup, bookmaker, category):
        self.bookmaker = bookmaker
        self.category = category
        self.sub_category = None
        self.html_soup = html_soup
        self.bettable_outcomes = []
        self.parsing_error = False
        self.parsing_error_reason = ""
        self.parsing_row_error_reason = []

        # If redirected to an outrights page then no odds so exit
        if self.html_soup.url != self.html_soup.final_url:
            self.parsing_error = True
            self.parsing_error_reason = "URL redirect:" + self.html_soup.requested_url + \
                                        "\n URL landed" + self.html_soup.final_url
            return

        try:
            if bookmaker == "PINNACLE":
                self.parse_pinnacle()
            elif bookmaker == "EIGHT88":
                self.parse_eight88()
            elif bookmaker == "PADDYPOWER":
                self.parse_paddypower()
            elif bookmaker == "WILLIAMHILL":
                self.parse_williamhill()
            elif bookmaker == "SPORTINGBET":
                self.parse_sportingbet()
            elif bookmaker == "MARATHONBET":
                self.parse_marathonbet()
            elif bookmaker == "LADBROKES":
                self.parse_ladbrokes()
        except IndexError:
            self.parsing_error = True
            self.parsing_error_reason = "IndexError"
        except KeyError:
            self.parsing_error = True
            self.parsing_error_reason = "KeyError"

        # Now parse the individual odds rows
        if not self.parsing_error:
            for each in self.rows:
                parsed_row = OddsPageOddsRowParser(each, self.bookmaker, self.category, self.sub_category)
                self.bettable_outcomes += parsed_row.bettable_outcomes
                if parsed_row.row_parse_error:
                    self.parsing_row_error_reason.append(parsed_row.row_parse_error_reason)


    def __str__(self):
        output = ""
        for outcome in self.bettable_outcomes:
            output += str(outcome) + "\n"
        return output

    def parse_pinnacle(self):
        identifier = self.html_soup.findAll("div", {"ng-click": "triggerCollapse(league.league, date.date)"})
        self.sub_category = identifier[0].text.replace("\t", "").replace("\n", "").replace(" ", "")

        # Note that some of these are empty
        self.rows = self.html_soup.findAll("tbody", {"class": "ng-scope"})

    def parse_eight88(self):
        identifier = self.html_soup.findAll("span", {"class": "KambiBC-modularized-event-path__fragment"})
        identifier = [x for x in identifier if x.text.upper() != self.category]
        # Remove the spain identifier from the european leagues
        identifier = [x for x in identifier if x.text.upper() != "SPAIN"
                      and x.text.upper() != "GERMANY"
                      and x.text.upper() != "ENGLAND"]
        try:
            self.sub_category = identifier[-1].text
        except:
            self.parsing_error = True
            self.parsing_error_reason += "No subcategory found. "
            return

        self.rows = self.html_soup.findAll("div", {"class": "KambiBC-event-item__event-wrapper"})

    def parse_paddypower(self):
        self.sub_category = self.html_soup.findAll('div', {"class": "fb-market-filters"})[0].\
            findAll('span', {"class": "tooltip"})[0].text.replace("\n", "")

        if self.category == "FOOTBALL":
            # Get the rows from the page
            self.rows = self.html_soup.findAll('div', {"class": "pp_fb_event"})
        elif self.category == "SNOOKER":
            pass

    def parse_williamhill(self):
        # Extract information from page
        self.sub_category = self.html_soup.findAll('h1')[1].text

        try:
            self.rows = self.html_soup.findAll('tbody')[0].findAll('tr', {"class": "rowOdd"})
        except IndexError:
            self.parsing_error = True
            self.parsing_error_reason += "No odds found. "
            # No odds table so exit the evaluation here
            return

    def parse_sportingbet(self):
        banner = self.html_soup.findAll('div', {"id": "content"})[0].findAll('div', {"class": "breadcrumb"})[0]
        if self.category == "FOOTBALL":
            self.sub_category = banner.findAll("strong")[0].text
            self.outcome_type = "FULLTIME_RESULT"
        elif self.category == "SNOOKER":
            self.sub_category = "UK Championships"
            self.outcome_type = "FULLTIME_RESULT_NO_DRAW"

        # Get the rows from the page
        self.rows = self.html_soup.findAll('div', {"class": "event active"})

    def parse_marathonbet(self):
        if self.category == "FOOTBALL":
            try:
                self.sub_category = self.html_soup.findAll("h1", {"class": "category-label"})[0].\
                    text.replace("\n", "").replace("\t", "")
            except IndexError:
                self.parsing_error = True
                self.parsing_error_reason += "Category label not found. "
                return
        elif self.category == "SNOOKER":
            self.sub_category = "UK Championships"

        # Get the rows from the page
        self.rows = self.html_soup.findAll("table", {"class": "foot-market"})[0].findAll("tbody", recursive=False)[1:]

    def parse_ladbrokes(self):
        if self.category == "FOOTBALL":
            # Extract information from page
            self.sub_category = self.html_soup.findAll("h1", {"data-bind": "text: headerViewModel.title()"})[0].text

        if self.sub_category.upper() == "ENGLISH":
            # Probably no odds for this sub category
            self.parsing_error = True
            self.parsing_error_reason += "Sub category is ENGLISH"
            return

        # Get the rows from the page
        self.rows = self.html_soup.findAll("div", {"class": "event-list pre"})


class OddsPageOddsRowParser:
    """
    Takes html of an odds row and returns the BettableOutcomes
    """
    def __init__(self, html_row, bookmaker, category, sub_category):
        self.html_row = html_row
        self.bookmaker = bookmaker
        self.category = category
        self.sub_category = sub_category
        self.bettable_outcomes = []

        self.player_list = []
        self.win = None
        self.lose = None
        self.draw = None
        self.date = None
        self.outcome_type = None

        self.row_parse_error = False
        self.row_parse_error_reason = ""

        try:
            if bookmaker == "PINNACLE":
                self.parse_row_pinnacle()
            elif bookmaker == "EIGHT88":
                self.parse_row_eight88()
            elif bookmaker == "PADDYPOWER":
                self.parse_row_paddypower()
            elif bookmaker == "WILLIAMHILL":
                self.parse_row_williamhill()
            elif bookmaker == "SPORTINGBET":
                self.parse_row_sportingbet()
            elif bookmaker == "MARATHONBET":
                self.parse_row_marathonbet()
            elif bookmaker == "LADBROKES":
                self.parse_row_ladbrokes()
        except KeyError:
            self.row_parse_error = True
            self.row_parse_error_reason = "KeyError"
        except IndexError:
            self.row_parse_error = True
            self.row_parse_error_reason = "IndexError"

        # Now create the bettable outcomes
        if not self.row_parse_error:
            self.event = Event(self.category, self.sub_category, [self.player_list[0], self.player_list[1]], date=self.date)
            self.bettable_outcomes.append(BettableOutcome(self.event, self.player_list[0],
                                                          "FULLTIME_RESULT", "WIN", self.win, self.bookmaker))
            self.bettable_outcomes.append(BettableOutcome(self.event, self.player_list[1],
                                                          "FULLTIME_RESULT", "LOSE", self.lose, self.bookmaker))
            self.bettable_outcomes.append(BettableOutcome(self.event, self.player_list[0],
                                                          "FULLTIME_RESULT", "DRAW", self.draw, self.bookmaker))

    def parse_row_pinnacle(self):
        tr_rows = self.html_row.findAll("tr")
        # First tr is the home team
        try:
            self.player_list.append(tr_rows[0].findAll("td", {"class": "game-name name"})[0].text \
                               .replace("\n", "").replace("\t", ""))
        except IndexError:
            self.row_parse_error = True
            self.row_parse_error_reason += "Failed to find first player\n"
            return

        self.win = tr_rows[0].findAll("td", {"class": "oddTip game-moneyline"})[0].text \
            .replace("\n", "").replace("\t", "")

        if self.win == "":
            self.row_parse_error = True
            self.row_parse_error_reason = "No odds found\n"
            return

        # Second tr is the away team
        self.player_list.append(tr_rows[1].findAll("td", {"class": "game-name name"})[0].text \
                           .replace("\n", "").replace("\t", ""))
        self.lose = tr_rows[1].findAll("td", {"class": "oddTip game-moneyline"})[0].text \
            .replace("\n", "").replace("\t", "")

        # Third tr is the draw
        self.player_list.append(tr_rows[2].findAll("td", {"class": "game-name name"})[0].text \
                           .replace("\n", "").replace("\t", ""))

        if self.player_list[2] == "Draw":
            self.draw = tr_rows[2].findAll("td", {"class": "oddTip game-moneyline"})[0].text \
                .replace("\n", "").replace("\t", "")
        else:
            self.row_parse_error = True
            self.row_parse_error_reason += "Draw odds not found\n"

    def parse_row_eight88(self):

        date_list = self.html_row.findAll('span', {"class": "KambiBC-event-item__start-time--date"})
        try:
            self.date = date_list[0].text
        except IndexError:
            # If no date shown then match is currently playing
            self.date = time.strftime("%Y_%m_%d")

        players = self.html_row.findAll('div', {"class": "KambiBC-event-participants__name"})
        if len(players) != 2:
            self.row_parse_error = True
            self.row_parse_error_reason += "Cannot find players on row. "
            return
        else:
            self.player_list = [x.text.replace("\n", "").replace("\t", "") for x in players]

        odds_list = self.html_row.findAll('span', {"class": "KambiBC-mod-outcome__odds"})
        if (self.category == "FOOTBALL" and len(odds_list) < 3) or (self.category == "SNOOKER" and len(odds_list) < 2):
            self.row_parse_error = True
            self.row_parse_error_reason += "Incorrect numbers of odds on row. "
            return
        else:
            if self.category == "FOOTBALL":
                self.win = odds_list[0].text
                self.draw = odds_list[1].text
                self.lose = odds_list[2].text
                self.outcome_type = "FULLTIME_RESULT"
            elif self.category == "SNOOKER":
                self.win = odds_list[0].text
                self.lose = odds_list[1].text
                self.outcome_type = "FULLTIME_RESULT_NO_DRAW"

    def parse_row_paddypower(self):
        time_list = self.html_row.findAll('div', {"class": "fb_event_time"})
        try:
            self.date = time_list[0].text
        except IndexError:
            self.row_parse_error = True
            self.row_parse_error_reason += "Time not found. "
            self.date = ""

        name_list = self.html_row.findAll('div', {"class": "fb_event_name"})
        if len(name_list) == 1:
            name = name_list[0].text.replace("\t", "")
        else:
            self.row_parse_error = True
            self.row_parse_error_reason += "Cannot find players on row. "
            return

        self.player_list = name.replace("\t", "").replace("\n", "").split(' v ')

        odds_list = self.html_row.findAll('div', {"class": "fb_odds item"})
        if len(odds_list) == 1:
            odds = odds_list[0].findAll('div')
        else:
            self.row_parse_error = True
            self.row_parse_error_reason += "Cannot find any odds on row. "
            return

        if len(odds) != 3:
            self.row_parse_error = True
            self.row_parse_error_reason += "Cannot find all odds on row. "
            return
        else:
            self.win = odds[0].text.replace("\t", "").replace("\n", "")
            self.draw = odds[1].text.replace("\t", "").replace("\n", "")
            self.lose = odds[2].text.replace("\t", "").replace("\n", "")

    def parse_row_williamhill(self):
        if self.category == "FOOTBALL":
            # td list:
            # 0) Date 1) Time 2) Teams 4) Home 5) Draw 6) Away
            tr_rows = self.html_row.findAll('td')

            date = tr_rows[0].text.replace("\t", "").replace("\n", "")
            time = tr_rows[1].text.replace("\t", "").replace("\n", "")
            self.date = date + " " + time
            name = tr_rows[2].text.replace("\t", "").replace("\n", "")
            p1, p2 = name.split(" v ")
            p1 = p1.strip()
            p2 = p2.strip()
            self.player_list = [p1, p2]
            self.win = tr_rows[4].text.replace("\t", "").replace("\n", "")
            self.draw = tr_rows[5].text.replace("\t", "").replace("\n", "")
            self.lose = tr_rows[6].text.replace("\t", "").replace("\n", "")
        elif self.category == "SNOOKER":
            try:
                # td list:
                # 0) Date 1) Time 2) Padding 3) WinOdds 4) Players 5) LoseOdds
                tr_rows = self.html_row.findAll('td')

                date = tr_rows[0].text.replace("\t", "").replace("\n", "")
                time = tr_rows[1].text.replace("\t", "").replace("\n", "")
                self.date = date + " " + time
                name = tr_rows[4].text.replace("\t", "").replace("\n", "")
                p1, p2 = name.split(" v ")
                p1 = p1.strip()
                p2 = p2.strip()
                self.player_list = [p1, p2]
                self.win = tr_rows[3].text.replace("\t", "").replace("\n", "")
                self.lose = tr_rows[5].text.replace("\t", "").replace("\n", "")
            except IndexError:
                self.row_parse_error = True
                self.row_parse_error_reason += "IndexError in snooker row parsing"
                pass
            except ValueError:
                self.row_parse_error = True
                self.row_parse_error_reason += "ValueError in snooker row parsing"
                pass

    def parse_row_sportingbet(self):
        self.date = self.html_row.findAll("span", {"class": "StartTime"})[0].text.replace("\t", "").replace("\n", "")
        name = self.html_row.findAll("div", {"class": "eventName"})[0].text.replace("\t", "").replace("\n", "")
        p1, p2 = name.split(" v ")
        p1 = p1.strip()
        p2 = p2.strip()
        self.player_list = [p1, p2]
        self.win = self.html_row.findAll("div", {"class": "market"})[0].findAll("div", {"class": "odds home active"})[0].\
            findAll("div", {"id": "isOffered"})[0].findAll("span", {"class": "priceText wide EU"})[0].text
        try:
            self.draw = self.html_row.findAll("div", {"class": "market"})[0].findAll("div", {"class": "odds draw active"})[0].\
                findAll("div", {"id": "isOffered"})[0].findAll("span", {"class": "priceText wide EU"})[0].text
        except IndexError:
            self.draw = None
        self.lose = self.html_row.findAll("div", {"class": "market"})[0].findAll("div", {"class": "odds away active"})[0].\
            findAll("div", {"id": "isOffered"})[0].findAll("span", {"class": "priceText wide EU"})[0].text

    def parse_row_marathonbet(self):
        # Sometimes the datetime uses a class of 'date ' which I think means the next year
        self.date = self.html_row.findAll("td", {"class": "date"})[0].text.replace("\t", "").replace("\n", "").strip()
        names = self.html_row.findAll("div", {"class": "member-name"})
        # If the match is next year then the class is different too
        if len(names) == 0:
            names = self.html_row.findAll("div", {"class": "date-with-year-member-name"})
        # If the match is today then the class name is different and no date is displayed
        if len(names) == 0:
            names = self.html_row.findAll("div", {"class": "today-member-name"})
            date = time.strftime("%d %b ")
            self.date = date + self.date

        name = names[0].text
        for player in names[1:]:
            name += " v " + player.text

        p1, p2 = name.split(" v ")
        p1 = p1.strip()
        p2 = p2.strip()
        self.player_list = [p1, p2]

        all_odds = self.html_row.findAll("td", {"class": "height-column-with-price"})

        if self.category == "FOOTBALL":
            for odd in all_odds:
                if "\"" + p1 + " To Win\"" in odd.attrs['data-sel']:
                    self.win = odd.text.replace("\t", "").replace("\n", "")
                if "\"Draw\"" in odd.attrs['data-sel']:
                    self.draw = odd.text.replace("\t", "").replace("\n", "")
                if "\"" + p2 + " To Win\"" in odd.attrs['data-sel']:
                    self.lose = odd.text.replace("\t", "").replace("\n", "")
        elif self.category == "SNOOKER":
            for odd in all_odds:
                if p1 + "\",\"mn\":\"Match Winner\"" in odd.attrs['data-sel']:
                    self.win = odd.text.replace("\t", "").replace("\n", "")
                self.draw = None
                if p2 + "\",\"mn\":\"Match Winner\"" in odd.attrs['data-sel']:
                    self.lose = odd.text.replace("\t", "").replace("\n", "")

    def parse_row_ladbrokes(self):
        names = self.html_row.findAll("div", {"class": "name"})
        name = names[0].text

        p1, p2 = name.split(" v ")
        p1 = p1.strip()
        p2 = p2.strip()
        self.player_list = [p1, p2]

        all_odds = self.html_row.findAll("div", {"class": "selection"})

        if self.category == "FOOTBALL":
            self.win = all_odds[0].findAll("div")[0].text.strip()
            self.draw = all_odds[1].findAll("div")[0].text.strip()
            self.lose = all_odds[2].findAll("div")[0].text.strip()