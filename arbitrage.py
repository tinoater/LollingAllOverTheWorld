import warnings
import copy
import mwutils as mu
from config import *


class Odds:
    """
    Odds, fractional or decimal
    """
    def __init__(self, odds):
        self.odds = self.fractional_to_decimal_odds(odds)
        self.odds_arb = 1/self.odds

    def __str__(self):
        output = str(self.odds) + " (" + str(self.odds_arb)

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
    Owner of the outcome
    """
    def __init__(self, category, name):
        self.category = category.upper()
        try:
            self.cat_id = CATEGORY_DICT[self.category]
        except KeyError:
            raise KeyError("Category " + category + " not in CATEGORY_DICT")

        self.participant = name.upper()
        try:
            self.participant_id = PARTICIPANT_DICT[self.category][self.participant]
        except KeyError:
            raise KeyError("Participant " + name + " not in PARTICIPANT_DICT for category " + category)

    def __str__(self):
        return self.participant + "(" + str(self.participant_id)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.cat_id == other.cat_id:
                if self.participant_id == other.participant_id:
                    return True

        return False


class Event:
    """
    Real-world event
    """
    def __init__(self, category, sub_category, participant_list, date=None, time=None):
        self.category = category
        self.sub_category = sub_category
        self.participants = copy.deepcopy(participant_list)
        self.date = date
        self.time = time

        # TODO: Make it handle this date as a datetime object, for now it is a string

        self.participant_ids = [x.participant_id for x in self.participants]

        try:
            self.category_id = CATEGORY_DICT[category]
        except IndexError:
            raise IndexError("Category " + category + " not in CATEGORY_DICT")

        try:
            self.sub_category_id = SUBCATEGORY_DICT[category][sub_category]
        except IndexError:
            raise IndexError("Subcategory " + sub_category + " not in SUBCATEGORY_DICT")

    def __str__(self):
        output = self.category + "-" + self.sub_category + "-" + ",".join(self.participant_ids) + "\n"
        if self.date is not None:
            output += str(self.date)

        return output

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            if self.category == other.category and self.sub_category == other.sub_category:
                if set(self.participant_ids) == set(other.participant_ids):
                    return True

        return False

    def __hash__(self):
        participants_tup = tuple(self.participant_ids)
        properties_tup = (self.category, self.sub_category, participants_tup)

        return hash(properties_tup)


class BettableOutcome:
    """
    Bookmaker, event, participant, type of outcome and odds
    """
    def __init__(self, event, participant, outcome_type, outcome, odds, bookmaker):
        self.participant = participant
        self.outcome_type = outcome_type
        self.outcome = outcome
        self.odds = odds
        self.bookmaker = bookmaker
        self.event = event

        # Validations
        if self.participant not in self.event.participants:
            raise ValueError("Participant not in the Event")

    def __str__(self):
        outcome = self.bookmaker + "-" + self.participant.name + "-" + self.outcome_type + ":" + self.odds

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
        output = self.bettable_outcome.bookmaker + ":" + self.bettable_outcome.participant.name + "-" + \
                 self.bettable_outcome.outcome_type + "-" + str(self.bet_amount) + "[" + str(self.return_amount) + \
                 "]"

        return output

    def set_bet_amount(self, amount):
        self.bet_amount = amount
        self.return_amount = round(self.bet_amount * self.bettable_outcome.odds.odds, 2)
        self.profit_amount = self.return_amount - self.bet_amount


class ArbitrageBet:
    """
    Combination of Bets allowing arbitrage
    """
    def __init__(self, bet_list, total_investment=None):
        self.bets = copy.deepcopy(bet_list)

        # First check that all bets are for the same event
        if len(set([x.event for x in self.bets])) != 1:
            raise ValueError("Multiple events in ArbitrageBettableOutomce")
        # Check that all bets are for the same outcome type
        if len(set([x.bettable_outcome.outcome_type for x in self.bets])) != 1:
            raise ValueError("Multiple outcome_types in ArbitrageBettableOutomce")
        else:
            self.outcome_type = self.bets[0].bettable_outcome.outcome_type
        # Check that we have the full set of outcomes for this outcome_type
        # TODO: Make the outcome_type check generic
        self.outcomes = set([x.bettable_outcome.outcome for x in self.bets])
        if self.outcome_type == "FULLTIME_RESULT":
            if "DRAW" not in self.outcomes:
                raise ValueError("Not all outcomes present for FULLTIME_RESULT. Only have :" + str(self.outcomes))

        self.arb_perc = round(sum([x.bettable_outcome.odds.odds_arb for x in self.bets]), 4) * 100

        # Check if this is actually an arbitrage
        if self.arb_perc >= 100:
            warnings.warn("No arbitrage present for this arb\n" + str(self))

        # Get the date of the arb - this may be set on at least one or none of the events
        event_dates = [x.event.date for x in self.bets if x.event.date is not None]
        if len(event_dates) > 0:
            self.event_date = event_dates[0]
        else:
            self.event_date = None

        # Change the betting totals if required
        if total_investment is not None:
            self.set_arb_betting_amounts(total_investment)
            self.total_investment = total_investment
        else:
            self.total_investment = sum([x.bet_amount for x in self.bets])

        # Set the profit values
        self.profit = min(x.return_amount - self.total_investment for x in self.bets)
        self.return_perc = round(self.profit / self.total_investment * 100, 2)

    def __str__(self):
        output = str(self.arb_perc_profit)
        if self.event_date is not None:
            output += " (" + self.event_date

        for bet in self.bets:
            output += "\n" + str(bet)

        return output

    def set_arb_betting_amounts(self, total_investment, integer_round=True):
        """
        Calculate required betting amounts for arb
        :param total_investment:
        :return:
        """
        for bet in self.bets:
            bet.set_bet_amount(bet.odds.odds_arb * 100 * total_investment / self.arb_perc)

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
    Holds all ArbitrageEvents for BettingEvents
    """
    def __init__(self, event_list):
        self.event_list = copy.deepcopy(event_list)
        self.arbitrage_events = []
        self.orphan_events = []

        # Set a False matched flag against all events in the list
        for bookmaker in self.event_list:
            for event in bookmaker:
                event.matched = False

        # First check that we have multiple bookmakers
        if not(all(isinstance(elem, list) for elem in self.event_list)):
            warnings.warn("No market found")
        else:
            for bookmaker in self.event_list:
                # For each bookmaker
                bookmaker_name = bookmaker[0].bookmaker
                # For each event
                for event in bookmaker:
                    # If the event has not already been matched
                    if event.matched is False:
                        # Set the temp player values
                        p1 = event.p1_ind
                        p2 = event.p2_ind

                        # Find matches for it in the OTHER bookmakers
                        matches = [event for bookmaker in self.event_list for event in bookmaker
                                   if event.bookmaker != bookmaker_name and (
                                       (event.p1_ind == p1 and event.p2_ind == p2) or
                                       (event.p1_ind == p2 and event.p2_ind == p1)
                                       )
                                   ]
                        # Add the original event to the matches list
                        matches.append(event)
                        # Mark these events as matched
                        for each in matches:
                            each.matched = True

                        if len(matches) == 1:
                            # No matches were found
                            # warnings.warn("No matches found for event\n" + str(matches[0]))
                            self.orphan_events.append(matches[0])
                        else:
                            self.arbitrage_events.append(ArbitrageEvent(matches))

            # Set the possible_arb_list for all found arbs
            self.possible_arb_list = [x for x in self.arbitrage_events if x.arb_present is True]

            # Order the arbitrage_events by their arb percentage
            self.arbitrage_events.sort(key=lambda x: x.arb_perc)

    def __str__(self):
        """
        Multiple Odds for Events: 21
        Orphaned Odds for Evens: 3
        Arb possibilities: 1
        :return:
        """
        output = "Multiple Odds for Events: " + str(len(self.arbitrage_events)) + "\n"
        output += "Orphaned Odds for Events: " + str(len(self.orphan_events)) + "\n"
        output += "Arb possibilities: " + str(len(self.possible_arb_list)) + "\n"

        for each in self.possible_arb_list:
            output += str(each) + "\n"

        return output

    def get_full_output(self, to_screen=True, out_file_path=None):
        output = "------ SUMMARY -----" + "\n"
        output += str(self) + "\n\n"

        output += "------ All Bet Collections -----" + "\n"
        for arb in self.arbitrage_events:
            output += str(arb) + "\n\n"

        if len(self.orphan_events) > 0:
            output += "------ All Orphaned Events -----" + "\n"
            for orphan in self.orphan_events:
                output += str(orphan) + "\n"
        else:
            output += "------ No Orphaned Events -----" + "\n"

        if len(self.possible_arb_list) > 0:
            output += "------ All Possible Arbs -----" + "\n"
            for arb in self.possible_arb_list:
                output += str(arb) + "\n"
        else:
            output += "------ No Possible Arbs -----" + "\n"

        if out_file_path is not None:
            if not os.path.exists(os.path.dirname(out_file_path)):
                os.makedirs(os.path.dirname(out_file_path))
            out_file = open(out_file_path, "w")
            out_file.write(output)
            out_file.close()

        if to_screen:
            print(output)


class BettingPage:
    """
    Parses html_soup into list of BettingEvents
    """
    def __init__(self, url_soup, bookmaker, sport, IDENTITY_DICT=None):
        self.bookmaker = bookmaker
        self.sport = sport
        self.html_soup = url_soup
        self.category = None
        self.betting_events = []
        self.identity_dict = IDENTITY_DICT

        if bookmaker == "PINNACLE":
            self.parse_pinnacle()
        elif bookmaker == "EIGHT88":
            self.rows = self.html_soup.findAll("div", {"class": "KambiBC-event-item__event-wrapper"})
            for each in self.rows:
                try:
                    self.parse_eight88(each)
                except ValueError:
                    pass
        elif bookmaker == "PADDYPOWER":
            self.parse_paddypower()
        elif bookmaker == "WILLIAMHILL":
            try:
                self.parse_williamhill()
            except IndexError:
                warnings.warn("No odds found")
                pass
        elif bookmaker == "SPORTINGBET":
            self.parse_sportingbet()
        elif bookmaker == "MARATHONBET":
            self.parse_marathonbet()

    def parse_pinnacle(self):
        # Note that some of these are empty
        self.rows = self.html_soup.findAll("tbody", {"class": "ng-scope"})

        for each in self.rows:
            player_list = []

            if self.category is None:
                identifier = self.html_soup.findAll("div", {"ng-click": "triggerCollapse(league.league, date.date)"})
                self.category = identifier[0].text.replace("\t", "").replace("\n", "").replace(" ", "")

            tr_rows = each.findAll("tr")
            # First tr is the home team
            try:
                player_list.append(tr_rows[0].findAll("td", {"class": "game-name name"})[0].text\
                                   .replace("\n", "").replace("\t", ""))
            except IndexError:
                # Indicates this is a dummy tbody with no odds information in it
                break

            win = tr_rows[0].findAll("td", {"class": "oddTip game-moneyline"})[0].text\
                .replace("\n", "").replace("\t", "")

            if win == "":
                # No odds - so break
                warnings.warn("No odds found for " + str(player_list))
                continue

            # Second tr is the away team
            player_list.append(tr_rows[1].findAll("td", {"class": "game-name name"})[0].text\
                               .replace("\n", "").replace("\t", ""))
            lose = tr_rows[1].findAll("td", {"class": "oddTip game-moneyline"})[0].text\
                .replace("\n", "").replace("\t", "")

            # Third tr is the draw
            player_list.append(tr_rows[2].findAll("td", {"class": "game-name name"})[0].text\
                               .replace("\n", "").replace("\t", ""))

            if player_list[2] == "Draw":
                draw = tr_rows[2].findAll("td", {"class": "oddTip game-moneyline"})[0].text\
                    .replace("\n", "").replace("\t", "")
            else:
                warnings.warn("Draw odds not found")

            name = player_list[0] + " v " + player_list[1]

            event = BettingEvent(self.bookmaker, self.sport, self.category, name, player_list[0], player_list[1]
                     , win, lose, draw_odds=draw, IDENTITY_DICT=self.identity_dict)

            self.betting_events.append(event)

    def parse_eight88(self, each):
        if self.category is None:
            identifier = self.html_soup.findAll("span", {"class": "KambiBC-modularized-event-path__fragment"})
            self.category = identifier[2].text

        time_list = each.findAll('span', {"class": "KambiBC-event-item__start-time--time"})
        if len(time_list) != 1:
            warnings.warn("Incorrect length of time list on row. 1 != " + str(len(time_list)))
        else:
            time = time_list[0].text

        players = each.findAll('div', {"class": "KambiBC-event-participants__name"})
        if len(players) != 2:
            warnings.warn("Incorrect length of players list on row. 2 != " + str(len(players)))
        else:
            player_list = [x.text.replace("\n", "").replace("\t", "") for x in players]

        try:
            name = player_list[0] + " v " + player_list[1]
        except UnboundLocalError:
            warnings.warn("Players names not found")
            warnings.warn(str(each))
            raise ValueError("Players names not found")

        odds_list = each.findAll('span', {"class": "KambiBC-mod-outcome__odds"})
        if len(odds_list) < 3:
            warnings.warn("Incorrect length of odds list on row. 3 > " + str(len(odds_list)))
            warnings.warn(str(each))
            raise ValueError("Can't find odds")
        else:
            win = odds_list[0].text
            draw = odds_list[1].text
            lose = odds_list[2].text

        event = BettingEvent(self.bookmaker, self.sport, self.category, name, player_list[0], player_list[1]
                 , win, lose, draw_odds=draw, IDENTITY_DICT=self.identity_dict)

        self.betting_events.append(event)

    def parse_paddypower(self):
        # Get the rows from the page
        self.rows = self.html_soup.findAll('div', {"class": "pp_fb_event"})

        # Extract information from page
        self.category = self.html_soup.findAll('div', {"class": "fb-market-filters"})[0].\
            findAll('span', {"class": "tooltip"})[0].text.replace("\n", "")

        for each in self.rows:
            time_list = each.findAll('div', {"class": "fb_event_time"})
            if len(time_list) != 1:
                warnings.warn("Incorrect length of time list on row. 1 != " + str(len(time_list)))
            else:
                time = time_list[0].text

            name_list = each.findAll('div', {"class": "fb_event_name"})
            if len(name_list) != 1:
                warnings.warn("Incorrect length of name list on row. 1 != " + str(len(name_list)))
            else:
                name = name_list[0].text.replace("\t", "")

            player_list = name.replace("\t", "").replace("\n", "").split(' v ')

            odds_list = each.findAll('div', {"class": "fb_odds item"})
            if len(odds_list) != 1:
                warnings.warn("Incorrect length of odds list on row. 1 != " + str(len(odds_list)))
            else:
                odds = odds_list[0].findAll('div')

            if len(odds) != 3:
                warnings.warn("Incorrect lenght of individual odds on row. 3 != " + str(len(odds)))
            else:
                win = odds[0].text.replace("\t", "").replace("\n", "")
                draw = odds[1].text.replace("\t", "").replace("\n", "")
                lose = odds[2].text.replace("\t", "").replace("\n", "")

            event = BettingEvent(self.bookmaker, self.sport, self.category, name, player_list[0], player_list[1]
                                 , win, lose, draw_odds=draw, IDENTITY_DICT=self.identity_dict)

            self.betting_events.append(event)

    def parse_williamhill(self):
        # Get the rows from the page
        self.rows = self.html_soup.findAll('tbody')[0].findAll('tr', {"class": "rowOdd"})

        # Extract information from page
        self.category = self.html_soup.findAll('h1')[1].text

        print(self.category)

        for each in self.rows:
            # td list:
            # 0) Date 1) Time 2) Teams 4) Home 5) Draw 6) Away
            tr_rows = each.findAll('td')

            date = tr_rows[0].text.replace("\t", "").replace("\n", "")
            time = tr_rows[1].text.replace("\t", "").replace("\n", "")
            name = tr_rows[2].text.replace("\t", "").replace("\n", "")
            p1, p2 = name.split(" v ")
            p1 = p1.strip()
            p2 = p2.strip()
            win = tr_rows[4].text.replace("\t", "").replace("\n", "")
            draw = tr_rows[5].text.replace("\t", "").replace("\n", "")
            lose = tr_rows[6].text.replace("\t", "").replace("\n", "")

            event = BettingEvent(self.bookmaker, self.sport, self.category, name, p1, p2, win, lose,
                                 draw_odds=draw, IDENTITY_DICT=self.identity_dict)

            self.betting_events.append(event)

    def parse_sportingbet(self):
        # Get the rows from the page
        self.rows = self.html_soup.findAll('div', {"class": "event active"})

        # Extract information from page
        banner = self.html_soup.findAll('div', {"id": "content"})[0].findAll('div', {"class": "breadcrumb"})[0]
        self.category = banner.findAll("strong")[0].text

        print(self.category)

        for each in self.rows:
            datetime = each.findAll("span", {"class": "StartTime"})[0].text.replace("\t", "").replace("\n", "")
            name = each.findAll("div", {"class": "eventName"})[0].text.replace("\t", "").replace("\n", "")
            p1, p2 = name.split(" v ")
            p1 = p1.strip()
            p2 = p2.strip()
            win = each.findAll("div", {"class": "market"})[0].findAll("div", {"class": "odds home active"})[0].\
                findAll("div", {"id": "isOffered"})[0].findAll("span", {"class": "priceText wide EU"})[0].text
            draw = each.findAll("div", {"class": "market"})[0].findAll("div", {"class": "odds draw active"})[0].\
                findAll("div", {"id": "isOffered"})[0].findAll("span", {"class": "priceText wide EU"})[0].text
            lose = each.findAll("div", {"class": "market"})[0].findAll("div", {"class": "odds away active"})[0].\
                findAll("div", {"id": "isOffered"})[0].findAll("span", {"class": "priceText wide EU"})[0].text

            event = BettingEvent(self.bookmaker, self.sport, self.category, name, p1, p2, win, lose,
                                 draw_odds=draw, IDENTITY_DICT=self.identity_dict)

            self.betting_events.append(event)


    def parse_marathonbet(self):
        # Get the rows from the page
        self.rows = self.html_soup.findAll("table", {"class": "foot-market"})[0].findAll("tbody", recursive=False)[1:]

        # Extract information from page
        self.category = self.html_soup.findAll("h1", {"class": "category-label"})[0].\
            text.replace("\n","").replace("\t","")

        print(self.category)

        for each in self.rows:
            try:
                datetime = each.findAll("td", {"class": "date"})[0].text.replace("\t", "").replace("\n", "")
                names = each.findAll("div", {"class": "member-name"})
                name = names[0].text
                for player in names[1:]:
                    name += " v " + player.text

                p1, p2 = name.split(" v ")
                p1 = p1.strip()
                p2 = p2.strip()

                all_odds = each.findAll("td", {"class": "height-column-with-price"})

                for odd in all_odds:
                    if "\"" + p1 + " To Win\"" in odd.attrs['data-sel']:
                        win = odd.text.replace("\t","").replace("\n","")
                    if "\"Draw\"" in odd.attrs['data-sel']:
                        draw = odd.text.replace("\t","").replace("\n","")
                    if "\"" + p2 + " To Win\"" in odd.attrs['data-sel']:
                        lose = odd.text.replace("\t","").replace("\n","")

                event = BettingEvent(self.bookmaker, self.sport, self.category, name, p1, p2, win, lose,
                                     draw_odds=draw, IDENTITY_DICT=self.identity_dict)

                self.betting_events.append(event)
            except KeyError as err:
                print("KeyError with MARTAHONBET: " + p1 + " " + p2 + "\n" + format(err))

