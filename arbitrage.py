import os
import warnings
import copy
import math
import mwutils as mu


class BettingEvent:
    """
    Information for a bettable event. Identifiers, participants and odds
    """
    def __init__(self, bookmaker, sport, category, name, p1, p2, win_odds, lose_odds, draw_odds=None, IDENTITY_DICT=None):
        self.bookmaker = bookmaker
        self.sport = sport
        self.category = category
        self.name = name
        self.p1 = p1
        self.p2 = p2
        self.win_odds = self.translate_odds(win_odds)
        self.lose_odds = self.translate_odds(lose_odds)
        if draw_odds is not None:
            self.draw_odds = self.translate_odds(draw_odds)
        else:
            self.draw_odds = None

        if IDENTITY_DICT is not None:
            self.use_identity_dict = True
            self.identity_dict = IDENTITY_DICT
        else:
            self.use_identity_dict = False
            self.identity_dict = dict()
            self.identity_dict[''] = 0

        self.set_player_inds()

    def __str__(self):
        """
        William Hill-Football-Premier league
        Man United v Everton (Man United,Everton)
        3.1/1.1/2.2
        :return:
        """
        output = self.bookmaker + "-" + self.sport + "-" + self.category + "\n"
        output += self.name + " (" + self.p1 + "," + self.p2 + ")" + "\n"
        output += str(round(self.win_odds, 3)) + "/" + str(round(self.draw_odds, 3)) + "/" + str(round(self.lose_odds, 3))

        return output

    def set_player_inds(self):
        """
        Map the text players into standardised integers

        If a IDENTITY_DICT is passed in then use that and error when not found. Otherwise construct dictionary
        as each new player is found
        """
        if self.use_identity_dict:
            try:
                if self.sport == "FOOTBALL":
                    self.p1_ind = self.identity_dict[self.p1]
                    self.p2_ind = self.identity_dict[self.p2]
            except KeyError:
                raise KeyError("Player not found in dictionary")
        else:
            try:
                self.p1_ind = self.identity_dict[self.p1]
            except KeyError:
                self.identity_dict[self.p1] = max(self.identity_dict.values()) + 1
                self.p1_ind = self.identity_dict[self.p1]

            try:
                self.p2_ind = self.identity_dict[self.p2]
            except KeyError:
                self.identity_dict[self.p2] = max(self.identity_dict.values()) + 1
                self.p2_ind = self.identity_dict[self.p2]

    def translate_odds(self, odds):
        """
        Convert odds from fractional to decimal
        :param odds:
        :return:
        """
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


class ArbitrageEvent:
    """
    Takes a list of BettingEvents for an event and returns the best arb
    """
    def __init__(self, event_list):
        self.events = event_list
        self.p1 = event_list[0].p1
        self.p2 = event_list[0].p2
        self.p1_ind = event_list[0].p1_ind
        self.p2_ind = event_list[0].p2_ind

        # Handle case when only one BettingEvent is passed in
        if len(event_list) > 1:
            # Determine if pairs are ordered
            for event in event_list[1:]:
                if not (event.p1_ind == self.p1_ind and event.p2_ind == self.p2_ind):
                    # Events are not ordered
                    # First check they just need to be switches
                    if event.p1_ind == self.p2_ind and event.p2_ind == self.p1_ind:
                        # We need to switch the odds and participants
                        temp = dict()
                        temp['p1'] = event.p1
                        temp['p1_ind'] = event.p1_ind
                        temp['win_odds'] = event.win_odds
                        temp['lose_odds'] = event.lose_odds

                        event.p1 = event.p2
                        event.p1_ind = event.p2_ind
                        event.p2 = temp['p1']
                        event.p2_ind = temp['p1_ind']
                        event.win_odds = temp['lose_odds']
                        event.lose_odds = temp['win_odds']
                    else:
                        # These pairs are just totally wrong
                        raise ValueError("Events have different participants")
                else:
                    pass

        # Find the best odds
        temp = [event.win_odds for event in self.events]
        self.win_odds = max(temp)
        self.win_bookmaker = [i for i, j in enumerate(temp) if j == self.win_odds][0]

        temp = [event.lose_odds for event in self.events]
        self.lose_odds = max(temp)
        self.lose_bookmaker = [i for i, j in enumerate(temp) if j == self.lose_odds][0]

        temp = [event.draw_odds for event in self.events]
        self.draw_odds = max(temp)
        self.draw_bookmaker = [i for i, j in enumerate(temp) if j == self.draw_odds][0]

        # Calculate Arb percentage
        self.win_odds_arb = round(1/self.win_odds, 5)
        self.lose_odds_arb = round(1/self.lose_odds, 5)
        self.draw_odds_arb = round(1/self.draw_odds, 5)
        self.arb_perc = round(self.win_odds_arb + self.draw_odds_arb + self.lose_odds_arb, 5)
        self.arb_perc_profit = round((1-self.arb_perc)/self.arb_perc, 5)

        if self.arb_perc < 1:
            self.arb_present = True
        else:
            self.arb_present = False

    def __str__(self):
        """
        Man United win 3.1 (WilliamHill): 0.55
        Draw 2.2 (888): 0.22
        Everton win 1.1 (PaddyPower): 0.22
        :return:
        """
        output = self.p1 + " win " + str(self.win_odds) + " (" + self.events[self.win_bookmaker].bookmaker + "): " + \
                 str(self.win_odds_arb) + "\n"
        output += "Draw " + str(self.draw_odds) + " (" + self.events[self.draw_bookmaker].bookmaker + "): " + \
                 str(self.draw_odds_arb) + "\n"
        output += self.p2 + " win " + str(self.lose_odds) + " (" + self.events[self.lose_bookmaker].bookmaker + "): " + \
                 str(self.lose_odds_arb)+ "\n"
        output += str(self.arb_perc)

        if self.arb_present:
            win_bet, draw_bet, lose_bet = self.get_arb_betting_amounts(200)
            output += "\n ARBITRAGE BET\n"
            output += "\n" + self.p1 + " to win:£" + str(win_bet) + " at " + self.events[self.win_bookmaker].bookmaker
            output += "\n" + "Draw" + ":£" + str(draw_bet) + " at " + self.events[self.draw_bookmaker].bookmaker
            output += "\n" + self.p2 + " to win:£" + str(lose_bet) + " at " + self.events[self.lose_bookmaker].bookmaker

        return output

    def get_arb_betting_amounts(self, total_investment, integer_round=True):
        """
        Calculate required betting amounts for arb
        :param total_investment:
        :return:
        """
        win_bet = self.win_odds_arb * total_investment / self.arb_perc
        draw_bet = self.draw_odds_arb * total_investment / self.arb_perc
        lose_bet = self.lose_odds_arb * total_investment / self.arb_perc

        if not integer_round:
            return round(win_bet, 2), round(draw_bet, 2), round(lose_bet, 2)
        else:
            approx_betting = []
            # Test each possible bet and pick the one with the best rate of return
            for win_approx in (math.floor(win_bet), math.ceil(win_bet)):
                for draw_approx in (math.floor(draw_bet), math.ceil(draw_bet)):
                    for lose_approx in (math.floor(lose_bet), math.ceil(lose_bet)):
                        bets = (win_approx, draw_approx, lose_approx)
                        bet_return = min(win_approx * self.win_odds,
                                         draw_approx * self.draw_odds,
                                         lose_approx * self.lose_odds)
                        bet_return -= win_approx + draw_approx + lose_approx
                        bet_return /= (win_approx + draw_approx + lose_approx)
                        approx_betting.append([bet_return, bets])
            # Pick the best return
            t = max(approx_betting, key=lambda x: x[0])
            return t[1]


class Market:
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

