import time
import os
from bs4 import BeautifulSoup
from contextlib import closing
from selenium import webdriver
import warnings

WEBDRIVER_PATH = "F:\Coding\PycharmProjects\Arbitrage\chromedriver.exe"
ARBITRAGE_PATH = "F:\Coding\PycharmProjects\Arbitrage\ScrapedFiles\\"
BOOKMAKERS_LIST = {"Eight88": 0,
                   "PaddyPower": 1
                   }
BOOKMAKERS = [{"Bookmaker": "888",
               "Football_L2": "https://www.888sport.com/bet/#/filter/football/england/league_two"},
              {"Bookmaker": "PaddyPower",
               "Football_L2": "http://www.paddypower.com/football/football-matches/english-league-2"}
              ]

FOOTBALL_DICT = {"Accrington Stanley": 1,
                 "Barnet": 2,
                 "Blackpool": 3,
                 "Cambridge United": 4,
                 "Carlisle United": 5,
                 "Cheltenham Town": 6,
                 "Colchester United": 7,
                 "Crawley Town": 8,
                 "Crewe Alexandra": 9,
                 "Doncaster Rovers": 10,
                 "Exeter City": 11,
                 "Grimsby Town": 12,
                 "Hartlepool United": 13,
                 "Leyton Orient": 14,
                 "Luton Town": 15,
                 "Mansfield Town": 16,
                 "Morecambe": 17,
                 "Newport County": 18,
                 "Notts County": 19,
                 "Plymouth Argyle": 20,
                 "Portsmouth": 21,
                 "Stevenage": 22,
                 "Wycombe Wanderers": 23,
                 "Yeovil Town": 24,
                 "Exeter": 11,
                 "Cheltenham": 6,
                 "Stevenage FC": 22,
                 "Carlisle": 5,
                 "Doncaster": 10,
                 "Colchester": 7,
                 "Crawley": 8,
                 "Crewe": 9,
                 "Yeovil": 24,
                 "Grimsby": 12,
                 "Hartlepool": 13,
                 "Luton": 15,
                 "Mansfield": 16,
                 "Plymouth": 20,
                 "Wycombe": 23
                 }


class ArbitrageEvent:
    def __init__(self, event_list):
        self.events = event_list
        self.p1 = event_list[0].p1
        self.p2 = event_list[0].p2
        self.p1_ind = event_list[0].p1_ind
        self.p2_ind = event_list[0].p2_ind

        # Determine if pairs are ordered
        # TODO: Make this handle (and fix) non-ordered players
        for event in event_list[1:]:
            if not (event.p1_ind == self.p1_ind and event.p2_ind == self.p2_ind):
                raise ValueError("Events are not ordered correctly")
            else:
                print("Ordered OK")

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
            if odds.lower() == "evens":
                return 1
        except AttributeError:
            pass

        try:
            odds = float(odds)
            return round(odds, 5)
        except ValueError:
            num, dem = odds.replace(" ", "").split("/")
            return float(num)/float(dem)


class PaddyPowerFootballMatchPage:
    def __init__(self, url_soup):
        self.bookmaker = "PADDYPOWER"
        self.sport = "FOOTBALL"
        self.url_soup = url_soup
        self.betting_events = []

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



    def paddy_tennis_singles_get_odds_from_row(row):
        players_temp = row.findAll('td', {"class" : "mkt-td-label"})[0].findAll('a')[0].string
        odds_temp = row.findAll('div', {"class" : "odds"})

        odds_str = []
        odds = []
        odds_str.append(odds_temp[0].string.replace("\n", "").replace("\t", ""))
        odds_str.append(odds_temp[1].string.replace("\n", "").replace("\t", ""))
        players = players_temp.split(' v ')

        for each in odds_str:
            if each == 'evens':
                odds.append(1)
            else:
                num, den = each.split('/')
                odds.append(float(num)/float(den) + 1)

        result = {}
        for i in range(0, len(players)):
            result[players[i]] = odds[i]

        return result


class Eight88FootballMatchPage:
    def __init__(self, url_soup):
        self.bookmaker = "888"
        self.sport = "FOOTBALL"
        self.category = None
        self.url_soup = url_soup
        self.betting_events = []

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
            else:
                win = odds_list[0].text
                draw = odds_list[1].text
                lose = odds_list[2].text

            event = BettingEvent(self.bookmaker, self.sport, self.category, name, player_list[0], player_list[1]
                     , win, lose, draw_odds=draw)

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
        if not os.path.exists(out_file_path):
            os.makedirs(os.path.dirname(out_file_path))
        out_file = open(out_file_path, "w")
        out_file.write(page_source)
        out_file.close()

    return html_soup


def get_page_source_file(file_path):
    with open(file_path) as my_file:
        html = my_file.read()
        html_soup = BeautifulSoup(html, "lxml")

    return html_soup


def get_page_source(file_path=None, url=None, sleep_time=5):
    if file_path is not None:
        from_file = True
    else:
        from_file = False

    if url is not None:
        from_url = True
    else:
        from_url = False

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


def debug():
    eee = BettingEvent("888", "FOOTBALL", "L2", "Blackpool v Doncaster Rovers", "Blackpool", "Doncaster Rovers",
                       2.1, 2.5, 1.65)
    paddy = BettingEvent("PaddyPower", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                       1.625, 5.82, 1.5)
    fake = BettingEvent("Fake", "FOOTBALL", "L2", "Blackpool v Doncaster", "Blackpool", "Doncaster",
                       1.625, 5, 3.8)

    arb = ArbitrageEvent([eee, paddy, fake])
    print(arb)
    print(arb.get_arb_betting_amounts(1000))


def main(date, category):
    # Loop through each bookmaker for this category
    events = []
    for bet_provider in BOOKMAKERS_LIST:
        bookmaker = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]]["Bookmaker"]
        url = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]][category]
        file_path = os.path.join(ARBITRAGE_PATH, bookmaker, date, category + ".txt")

        html_soup = get_page_source(file_path=file_path, url=url)
        if bet_provider == 'Eight88':
            page = Eight88FootballMatchPage(html_soup)
        elif bet_provider == 'PaddyPower':
            page = PaddyPowerFootballMatchPage(html_soup)

        events.append(page.betting_events)

    # Loop through the events and pair them all up
    for i in range(0, len(events[0])):
        print(str(events[0][i].p1_ind) + "-" + str(events[1][i].p1_ind))
        arb = ArbitrageEvent([events[0][i], events[1][i]])
        print(arb)
        print("\n\n\n")


if __name__ == "__main__":
    date = time.strftime("%Y_%m_%d")
    main(date, "Football_L2")
    #debug()
