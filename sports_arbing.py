import time
import os
import mwutils as mu
import arbitrage
from config import *


# TODO: Add in more bookies

# TODO: Add in more football leagues
# TODO: Add in football odds for other types - win and draw etc
# TODO: Add in odds for tennis


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
            html_soup = mu.get_page_source(file_path=file_path, url=url, ignore_files=ignore_files,
                                           sleep_time=SLEEP_TIME)
            # Create the class from the soup
            page = arbitrage.BettingPage(html_soup, bet_provider, "FOOTBALL", IDENTITY_DICT=FOOTBALL_DICT)

            # Add events to the events list
            if len(page.betting_events) > 0:
                events.append(page.betting_events)

        # Create the market for these events
        m = arbitrage.Market(events)

        # Update the summary information
        if len(m.arbitrage_events) > 0:
            all_arbs += m.possible_arb_list
        events_count += len(m.arbitrage_events)
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
    soup = mu.get_page_source_file("F:\Coding\PycharmProjects\Arbitrage\ScrapedFiles\888\\2016_11_05_18\Football_GeBun.txt")
    page = arbitrage.BettingPage(soup, "EIGHT88", "FOOTBALL", IDENTITY_DICT=FOOTBALL_DICT)
    arb = arbitrage.ArbitrageEvent([page.betting_events[0]])
    m = arbitrage.Market([page.betting_events])
    print(str(len(m.arbitrage_events)))


if __name__ == "__main__":
    date = time.strftime("%Y_%m_%d_%H")
    calc_arbs_for_date(date)

    #debug()

    #adding_a_new_bookmaker()