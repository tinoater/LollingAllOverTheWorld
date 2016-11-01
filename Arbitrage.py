import time
import os
from bs4 import BeautifulSoup
from contextlib import closing
from selenium import webdriver
import warnings
import copy

# TODO: Add in more bookies

# TODO: Add in more football leagues
# TODO: Add in football odds for other types - win and draw etc
# TODO: Add in odds for tennis

WEBDRIVER_PATH = "F:\Coding\PycharmProjects\Arbitrage\chromedriver.exe"
ARBITRAGE_PATH = "F:\Coding\PycharmProjects\Arbitrage\ScrapedFiles"
RESULTS_PATH = "F:\Coding\PycharmProjects\Arbitrage\Results"
SUMMARY_RESULTS_PATH = "F:\Coding\PycharmProjects\Arbitrage\SummaryResults"

BOOKMAKERS_LIST = {"EIGHT88": 0,
                   "PADDYPOWER": 1,
                   # "PINNACLE": 2,
                   "WILLIAMHILL": 3
                   }

EIGHT88_DICT = {"Bookmaker": "888",
                "Football_L2": "https://www.888sport.com/bet/#/filter/football/england/league_two",
                "Football_L1": "https://www.888sport.com/bet/#/filter/football/england/league_one",
                "Football_C": "https://www.888sport.com/bet/#/filter/football/england/the_championship",
                "Football_PL": "https://www.888sport.com/bet/#/filter/football/england/premier_league",
                "Football_CL": "https://www.888sport.com/bet/#/filter/football/champions_league",
                "Football_LaLig": "https://www.888sport.com/bet/#/filter/football/spain/laliga",
                "Football_GeBun": "https://www.888sport.com/bet/#/filter/football/germany/bundesliga"
                }

PADDY_DICT = {"Bookmaker": "PaddyPower",
              "Football_L2": "http://www.paddypower.com/football/football-matches/english-league-2",
              "Football_L1": "http://www.paddypower.com/football/football-matches/english-league-1",
              "Football_PL": "http://www.paddypower.com/football/football-matches/premier-league",
              "Football_CL": "http://www.paddypower.com/football/football-matches/champions-league",
              "Football_LaLig": "http://www.paddypower.com/football/football-matches/spanish-la-liga-matches",
              "Football_GeBun": "http://www.paddypower.com/football/football-matches/Germany-Bundesliga-1"
              }

PINNACLE_DICT = {"Bookmaker": "Pinnacle",
                 "Football_PL": "https://www.pinnacle.com/en/odds/match/soccer/england/england-premier-league?sport=True",
                 "Football_C": "https://www.pinnacle.com/en/odds/match/soccer/england/england-championship",
                 "Football_L1": "https://www.pinnacle.com/en/odds/match/soccer/england/england-league-1",
                 "Football_CL": "https://www.pinnacle.com/en/odds/match/soccer/uefa/uefa-champions-league"
                 }

WILLIAMHILL_DICT = {"Bookmaker": "WilliamHill",
                    "Football_PL": "http://sports.williamhill.com/bet/en-gb/betting/t/295/English+Premier+League.html",
                    "Football_C": "http://sports.williamhill.com/bet/en-gb/betting/t/292/English+Championship.html",
                    "Football_L1": "http://sports.williamhill.com/bet/en-gb/betting/t/293/English+League+1.html",
                    "Football_L2": "http://sports.williamhill.com/bet/en-gb/betting/t/294/English+League+2.html",
                    "Football_LaLig": "http://sports.williamhill.com/bet/en-gb/betting/t/338/Spanish-La-Liga-Primera.html",
                    "Football_GeBun": "http://sports.williamhill.com/bet/en-gb/betting/t/315/German+Bundesliga.html"
                   }

CATEGORY_LIST = ["Football_PL", "Football_C", "Football_L1", "Football_L2", "Football_CL", "Football_LaLig", "Football_GeBun"]
BOOKMAKERS = [EIGHT88_DICT,
              PADDY_DICT,
              PINNACLE_DICT,
              WILLIAMHILL_DICT
              ]

FOOTBALL_DICT = {"Arsenal": 1,
                 "Bournemouth": 2,
                 "Bournemouth AFC" : 2,
                 "Burnley": 3,
                 "Chelsea": 4,
                 "Crystal Palace": 5,
                 "Everton": 6,
                 "Hull City": 7,
                 "Hull": 7,
                 "Leicester City": 8,
                 "Leicester": 8,
                 "Liverpool": 9,
                 "Manchester City": 10,
                 "Man City": 10,
                 "Manchester United": 11,
                 "Man Utd": 11,
                 "Middlesbrough": 12,
                 "Southampton": 13,
                 "Stoke City": 14,
                 "Stoke": 14,
                 "Sunderland": 15,
                 "Swansea City": 16,
                 "Swansea": 16,
                 "Tottenham Hotspur": 17,
                 "Tottenham": 17,
                 "Watford": 18,
                 "West Bromwich Albion": 19,
                 "West Bromwich": 19,
                 "West Brom": 19,
                 "W.B.A": 19,
                 "West Ham United": 20,
                 "West Ham": 20,
                 "Aston Villa": 101,
                 "Barnsley": 102,
                 "Birmingham": 103,
                 "Birmingham City": 103,
                 "Blackburn": 104,
                 "Blackburn Rovers": 104,
                 "Brentford": 105,
                 "Brighton": 106,
                 "Brighton & Hove Albion": 106,
                 "Bristol City": 107,
                 "Burton Albion": 108,
                 "Burton": 108,
                 "Cardiff City": 109,
                 "Cardiff": 109,
                 "Derby County": 110,
                 "Derby": 110,
                 "Fulham": 111,
                 "Huddersfield": 112,
                 "Huddersfield Town": 112,
                 "Ipswich Town": 113,
                 "Ipswich": 113,
                 "Leeds United": 114,
                 "Leeds": 114,
                 "Newcastle": 115,
                 "Newcastle United": 115,
                 "Norwich City": 116,
                 "Norwich": 116,
                 "Nottm Forest": 117,
                 "Nottingham Forest": 117,
                 "Preston": 118,
                 "Preston North End": 118,
                 "QPR": 119,
                 "Queens Park Rangers": 119,
                 "Reading": 120,
                 "Rotherham": 121,
                 "Rotherham United": 121,
                 "Sheff Wed": 122,
                 "Sheffield Wednesday": 122,
                 "Wigan Athletic": 123,
                 "Wigan": 123,
                 "Wolves": 124,
                 "Wolverhampton Wanderers": 124,
                 "AFC Wimbledon": 201,
                 "Wimbledon": 201,
                 "Bolton": 202,
                 "Bolton Wanderers": 202,
                 "Bradford City": 203,
                 "Bradford": 203,
                 "Bristol Rovers": 204,
                 "Bury": 205,
                 "Charlton": 206,
                 "Charlton Athletic": 206,
                 "Chesterfield": 207,
                 "Coventry": 208,
                 "Coventry City": 208,
                 "Fleetwood": 209,
                 "Fleetwood Town": 209,
                 "Gillingham": 210,
                 "Millwall": 211,
                 "MK Dons": 212,
                 "Milton Keynes Dons": 212,
                 "Northampton": 213,
                 "Northampton Town": 213,
                 "Oldham": 214,
                 "Oldham Athletic": 214,
                 "Oxford": 215,
                 "Oxford United": 215,
                 "Peterborough": 216,
                 "Peterborough United": 216,
                 "Port Vale": 217,
                 "Rochdale": 218,
                 "Scunthorpe": 219,
                 "Scunthorpe United": 219,
                 "Sheff Utd": 220,
                 "Sheffield United": 220,
                 "Shrewsbury": 221,
                 "Shrewsbury Town": 221,
                 "Southend Utd": 222,
                 "Southend": 222,
                 "Southend United": 222,
                 "Swindon Town": 223,
                 "Swindon": 223,
                 "Walsall": 224,
                 "Wallsall": 224,
                 "Accrington Stanley": 301,
                 "Accrington": 301,
                 "Barnet": 302,
                 "Blackpool": 303,
                 "Cambridge United": 304,
                 "Cambridge": 304,
                 "Carlisle United": 305,
                 "Cheltenham Town": 306,
                 "Colchester United": 307,
                 "Crawley Town": 308,
                 "Crewe Alexandra": 309,
                 "Doncaster Rovers": 310,
                 "Exeter City": 311,
                 "Grimsby Town": 312,
                 "Hartlepool United": 313,
                 "Leyton Orient": 314,
                 "Luton Town": 315,
                 "Mansfield Town": 316,
                 "Morecambe": 317,
                 "Newport County": 318,
                 "Newport": 318,
                 "Notts County": 319,
                 "Plymouth Argyle": 320,
                 "Portsmouth": 321,
                 "Stevenage": 322,
                 "Wycombe Wanderers": 323,
                 "Yeovil Town": 324,
                 "Exeter": 311,
                 "Cheltenham": 306,
                 "Stevenage FC": 322,
                 "Carlisle": 305,
                 "Doncaster": 310,
                 "Colchester": 307,
                 "Crawley": 308,
                 "Crewe": 309,
                 "Yeovil": 324,
                 "Grimsby": 312,
                 "Hartlepool": 313,
                 "Luton": 315,
                 "Mansfield": 316,
                 "Plymouth": 320,
                 "Wycombe": 323,
                 "Besiktas": 401,
                 "Beikta A..": 401,
                 "Napoli": 402,
                 "Atltico Madrid": 403,
                 "Atletico Madrid": 403,
                 "FC Rostov": 404,
                 "Rostov FK": 404,
                 "Basel": 405,
                 "FC Basel": 405,
                 "FX Rostov": 404,
                 "FK Rostov": 404,
                 "Paris SG": 407,
                 "Paris Saint Germain": 407,
                 "PSG": 407,
                 "Benfica": 408,
                 "Dynamo Kiev": 409,
                 "Dynamo Kyiv": 409,
                 "Borussia Monchengladbach": 410,
                 "Borussia Mnchengladbach": 410,
                 "Celtic": 411,
                 "Celtic FC": 411,
                 "Ludogorets Razgrad": 412,
                 "Ludogorets Razgrad (n)": 412,
                 "Barcelona": 413,
                 "FC Barcelona": 413,
                 "PSV": 414,
                 "PSV Eindhoven": 414,
                 "Bayern Munich": 415,
                 "Bayern Mnchen": 415,
                 "Bayern Munchen": 415,
                 "Borussia Dortmund": 416,
                 "Dortmund": 416,
                 "Sporting Lisbon": 417,
                 "FC Copenhagen": 418,
                 "Juventus": 419,
                 "Lyon": 420,
                 "FC Porto": 421,
                 "Porto": 421,
                 "Legia Warsaw": 422,
                 "Legia Warszawa": 422,
                 "Club Brugge": 423,
                 "Real Madrid": 424,
                 "Monaco": 425,
                 "AS Monaco": 425,
                 "CSKA Moscow": 426,
                 "Dinamo Zagreb": 428,
                 "Bayer Leerkusen": 429,
                 "Bayer Leverkusen": 429,
                 "Leverkusen": 429,
                 "Real Madrd": 430,
                 "Sevilla": 431,
                 "Villarreal": 433,
                 "Athletic Bilbao": 435,
                 "Athletic Club Bilbao": 435,
                 "Real Sociedad": 436,
                 "Celta Vigo": 437,
                 "Las Palmas": 438,
                 "Deportiva Las Palmas": 438,
                 "Malaga": 439,
                 "Mlaga": 439,
                 "Eibar": 440,
                 "Real Betis": 441,
                 "Betis": 441,
                 "Alaves": 442,
                 "Alavs": 442,
                 "Valencia": 443,
                 "Espanyol": 444,
                 "Deportivo La Coruna": 445,
                 "Deportivo La Corua": 445,
                 "Sporting Gijon": 446,
                 "Sporting de Gijn": 446,
                 "Granada": 447,
                 "Granada CF": 447,
                 "Leganes": 448,
                 "Legans": 448,
                 "Osasuna": 449,
                 "RB Leipzig": 451,
                 "Leipzig": 451,
                 "Hertha Berlin": 452,
                 "Hoffenheim": 453,
                 "Cologne": 454,
                 "1. FC Kln": 454,
                 "FC Koln": 454,
                 "Eintracht Frankfurt": 456,
                 "SC Freiburg": 457,
                 "Freiburg": 457,
                 "Mainz": 458,
                 "Mainz 05": 458,
                 "FSV Mainz 05": 458,
                 "M'gladbach": 459,
                 "FC Augsburg": 461,
                 "Augsburg": 461,
                 "Schalke": 462,
                 "Schalke 04": 462,
                 "Werder Bremen": 463,
                 "Wolfsburg": 464,
                 "VfL Wolfsburg": 464,
                 "FC Ingolstadt 04": 465,
                 "FC Ingolstadt": 465,
                 "Ingolstadt": 465,
                 "Hamburg": 466,
                 "Hamburger SV": 466,
                 "SV Darmstadt 98": 467,
                 "Darmstadt 98": 467,
                 "Darmstadt": 467
                 }


class BettingEvent:
    def __init__(self, bookmaker, sport, category, name, p1, p2, win_odds, lose_odds, draw_odds=None):
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

        self.set_player_inds()

    def __str__(self):
        output = self.bookmaker + "-" + self.sport + "-" + self.category + "\n"
        output += self.name + " (" + self.p1 + "," + self.p2 + ")" + "\n"
        output += str(round(self.win_odds, 3)) + "/" + str(round(self.draw_odds, 3)) + "/" + str(round(self.lose_odds, 3))

        return output

    def set_player_inds(self):
        try:
            if self.sport == "FOOTBALL":
                self.p1_ind = FOOTBALL_DICT[self.p1]
                self.p2_ind = FOOTBALL_DICT[self.p2]
        except KeyError:
            raise KeyError("Player not found in dictionary")

    def translate_odds(self, odds):
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
    def __init__(self, event_list):
        self.events = event_list
        self.p1 = event_list[0].p1
        self.p2 = event_list[0].p2
        self.p1_ind = event_list[0].p1_ind
        self.p2_ind = event_list[0].p2_ind

        # Determine if pairs are ordered
        for event in event_list[1:]:
            if not (event.p1_ind == self.p1_ind and event.p2_ind == self.p2_ind):
                # Events are not ordered
                # First check they just need to be switches
                if event.p1_ind == self.p2_ind and event.p2_ind == self.p1_ind:
                    # We need to switch the odds and participants
                    temp = {}
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
        output = self.p1 + " win " + str(self.win_odds) + " (" + self.events[self.win_bookmaker].bookmaker + "): " + \
                 str(self.win_odds_arb) + "\n"
        output += "draw " + str(self.draw_odds) + " (" + self.events[self.draw_bookmaker].bookmaker + "): " + \
                 str(self.draw_odds_arb) + "\n"
        output += self.p2 + " win " + str(self.lose_odds) + " (" + self.events[self.lose_bookmaker].bookmaker + "): " + \
                 str(self.lose_odds_arb)+ "\n"
        output += str(self.arb_perc)

        return output


    def get_arb_betting_amounts(self, total_investment):
        win_bet = self.win_odds_arb * total_investment / self.arb_perc
        draw_bet = self.draw_odds_arb * total_investment / self.arb_perc
        lose_bet = self.lose_odds_arb * total_investment / self.arb_perc

        return win_bet, draw_bet, lose_bet


class Market:
    """
    Class to hold all ArbitrageEvents for BettingEvents
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
                    # If the even has not already been matched
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
    def __init__(self, url_soup, bookmaker, sport):
        self.bookmaker = bookmaker
        self.sport = sport
        self.url_soup = url_soup
        self.category = None
        self.betting_events = []

        if bookmaker == "PINNACLE":
            # Note that some of these are empty
            self.rows = url_soup.findAll("tbody", {"class": "ng-scope"})

            for each in self.rows:
                player_list = []

                if self.category is None:
                    identifier = self.url_soup.findAll("div", {"ng-click": "triggerCollapse(league.league, date.date)"})
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
                         , win, lose, draw_odds=draw)

                self.betting_events.append(event)
        elif bookmaker == "EIGHT88":
            self.rows = url_soup.findAll("div", {"class": "KambiBC-event-item__event-wrapper"})

            for each in self.rows:

                if self.category is None:
                    identifier = self.url_soup.findAll("span", {"class": "KambiBC-modularized-event-path__fragment"})
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

                name = player_list[0] + " v " + player_list[1]

                odds_list = each.findAll('span', {"class": "KambiBC-mod-outcome__odds"})
                if len(odds_list) != 3:
                    warnings.warn("Incorrect length of odds list on row. 3 != " + str(len(players)))
                    warnings.warn(each)
                    continue
                else:
                    win = odds_list[0].text
                    draw = odds_list[1].text
                    lose = odds_list[2].text

                event = BettingEvent(self.bookmaker, self.sport, self.category, name, player_list[0], player_list[1]
                         , win, lose, draw_odds=draw)

                self.betting_events.append(event)
        elif bookmaker == "PADDYPOWER":
            # Get the rows from the page
            self.rows = self.url_soup.findAll('div', {"class": "pp_fb_event"})

            # Extract information from page
            self.category = self.url_soup.findAll('div', {"class": "fb-market-filters"})[0].\
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
                                     , win, lose, draw_odds=draw)

                self.betting_events.append(event)
        elif bookmaker == "WILLIAMHILL":
            # Get the rows from the page
            self.rows = self.url_soup.findAll('tbody')[0].findAll('tr', {"class": "rowOdd"})

            # Extract information from page
            self.category = self.url_soup.findAll('h1')[1].text

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

                event = BettingEvent(self.bookmaker, self.sport, self.category, name, p1, p2, win, lose, draw_odds=draw)

                self.betting_events.append(event)


def get_page_source_url(url, out_file_path=None, sleep_time=5):
    """
    Get page html (including javascript generated elements)
    :param url: Full url (including http://)
    :param out_file_path: Full path to output file (if wanted)
    :param sleep_time: Time in seconds to wait for JS to load
    :return: BeautifulSoup object
    """
    with closing(webdriver.Chrome(WEBDRIVER_PATH)) as browser:
        browser.get(url)
        # wait for the page to load
        time.sleep(sleep_time)
        page_source = browser.page_source.encode("ascii", errors="ignore").decode()

    html_soup = BeautifulSoup(page_source, "lxml")

    if out_file_path is not None:
        if not os.path.exists(os.path.dirname(out_file_path)):
            os.makedirs(os.path.dirname(out_file_path))
        out_file = open(out_file_path, "w")
        out_file.write(page_source)
        out_file.close()

    return html_soup


def get_page_source_file(file_path):
    """
    Return html soup from a html file
    :param file_path:
    :return: BeautifulSoup object
    """
    with open(file_path) as my_file:
        html = my_file.read()
        html_soup = BeautifulSoup(html, "lxml")

    return html_soup


def get_page_source(file_path=None, url=None, sleep_time=5, ignore_files=False):
    if file_path is not None:
        from_file = True
    else:
        from_file = False

    if url is not None:
        from_url = True
    else:
        from_url = False

    if ignore_files:
        from_file = False
        from_url = True

    if from_file:
        # Check if the file_path exists
        try:
            html_soup = get_page_source_file(file_path)
            return html_soup
        except FileNotFoundError:
            if not from_url:
                raise FileNotFoundError("File not found, specify URL instead")

    if from_url:
        html_soup = get_page_source_url(url, file_path, sleep_time)
        return html_soup
    else:
        return None


def adding_a_new_bookmaker():
    # Get an example page source of theirs and save it in the tests folder
    # get_page_source_url("http://sports.williamhill.com/bet/en-gb/betting/t/295/English+Premier+League.html",
    #                     out_file_path="F:\Coding\PycharmProjects\Arbitrage\Tests\WilliamHill_Football_PL.txt")

    # Create a new test for them to read the data from the file
    # This follows exactly the form of the other ones

    # Create the new class and check the tests pass
    # soup = get_page_source_file("F:\Coding\PycharmProjects\Arbitrage\Tests\WilliamHill_Football_PL.txt")
    # thing = BettingPage(soup, "WILLIAMHILL", "FOOTBALL")

    # Add to the dictionaries

    # Add to the if statement in calc_arbs_for_date
    pass


def calc_arbs_for_date(date, category_list=CATEGORY_LIST, ignore_files=False):
    """
    For given date draw odds from online or file, compare and output Market object
    :param date:
    :param category: list of wanted categories. Defaults to all
    :return:
    """
    # Summary information
    all_arbs = []
    events_count = 0
    orphan_count = 0

    for category in category_list:
        print(category + " start")
        filename = date + "-" + category + ".log"
        summary_filename = date + ".log"

        # Loop through each bookmaker for this category
        events = []
        for bet_provider in BOOKMAKERS_LIST:
            bookmaker = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]]["Bookmaker"]
            try:
                url = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]][category]
            except KeyError:
                # No link found - this booky doesn't do these odds
                continue

            file_path = os.path.join(ARBITRAGE_PATH, bookmaker, date, category + ".txt")

            # Get the soup from file (if it exists) or get it from the website
            html_soup = get_page_source(file_path=file_path, url=url, ignore_files=ignore_files, sleep_time=5)
            # Create the class from the soup
            page = BettingPage(html_soup, bet_provider, "FOOTBALL")

            # Add events to the events list
            if len(page.betting_events) > 0:
                events.append(page.betting_events)

        # Create the market for these events
        m = Market(events)

        # Update the summary information
        if len(m.arbitrage_events) > 0:
            all_arbs += m.possible_arb_list
        events_count += len(m.event_list)
        orphan_count += len(m.orphan_events)

        # Output the Market to a file
        m.get_full_output(to_screen=False, out_file_path=os.path.join(RESULTS_PATH, filename))
        print(category + " done")

    # Output summary information to file
    if not os.path.exists(os.path.dirname(SUMMARY_RESULTS_PATH)):
        os.makedirs(os.path.dirname(SUMMARY_RESULTS_PATH))
    out_file = open(os.path.join(SUMMARY_RESULTS_PATH, summary_filename), "w")

    out_file.write("Total Events: " + str(events_count) + "\n")
    out_file.write("Total Orphans: " + str(orphan_count) + "\n")
    out_file.write("Arbs found: " + str(len(all_arbs)) + "\n")

    for each in all_arbs:
        out_file.write(str(each))
        out_file.write("\n")

    out_file.close()


def debug():
    particular_date = "2016_10_23_18"
    calc_arbs_for_date(particular_date)

if __name__ == "__main__":
    date = time.strftime("%Y_%m_%d_%H")
    calc_arbs_for_date(date)

    #adding_a_new_bookmaker()
