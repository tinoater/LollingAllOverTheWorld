import time
from bs4 import BeautifulSoup
from contextlib import closing
from selenium import webdriver


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


def paddy_get_rows_from_table(table):
    betting_rows = []
    rows = table.find_all('tr')

    for row in rows:
        try:
            classes = dict(row.attrs)["class"]
        except KeyError:
            classes = []

        if 'odd' in classes or 'even' in classes:
            betting_rows.append(row)

    return betting_rows


def paddy_get_table_from_page(html_soup):
    table = html_soup.findAll('table', {"class" : "mkt" })[0]

    return table


def eee_get_rows_from_page(page):
    html = get_page_source("https://www.888sport.com/bet/#/filter/tennis/atp/all/all/matches")




def get_page_source(url):
    with closing(webdriver.Chrome("F:\Coding\PycharmProjects\Arbitrage\chromedriver.exe")) as browser:
        browser.get(url)
        # wait for the page to load
        time.sleep(5)
        page_source = browser.page_source

    html_soup = BeautifulSoup(page_source, "lxml")

    return html_soup


def main():
    paddy_odds = paddy_get_odds_from_page("http://www.paddypower.com/bet/tennis")


def paddy_get_odds_from_page(url):
    html_soup = get_page_source(url)

    table = paddy_get_table_from_page(html_soup)
    rows = paddy_get_rows_from_table(table)

    return rows


def debug():
    #with open('C:\\Users\\Martin\\Desktop\\PPTennis.txt', 'r') as my_file:
    #    html = my_file.read().replace('\n', '')
    #html_soup = BeautifulSoup(html, "lxml")

    rows = paddy_get_odds_from_page("http://www.paddypower.com/bet/tennis")

    KambiBC-event-participants__name

if __name__ == "__main__":
    debug()
