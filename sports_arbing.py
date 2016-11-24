import time
import mwutils as mu
import arbitrage
from config import *

# TODO: Add in more bookies

# TODO: Add in more football leagues
# TODO: Add in football odds for other types - win and draw etc
# TODO: Add in odds for tennis


def calc_arbs_for_date(date, category_list=CATEGORY_LIST, ignore_files=False):
    """
    For given date draw odds from online or file, compare and output ArbitrageBets
    :param date:
    :param sub_category: list of wanted categories. Defaults to all
    :return:
    """
    # Summary information
    all_arbs = []
    events_count = 0
    orphan_count = 0
    summary_filename = date + ".log"

    for sub_category in category_list:
        print(sub_category + " start")
        filename = date + "-" + sub_category + ".log"

        # Loop through each bookmaker for this sub_category and download or load up the data
        for bet_provider in BOOKMAKERS_LIST:
            bookmaker = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]]["Bookmaker"]
            try:
                url = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]][sub_category]
            except KeyError:
                # No link found - this booky doesn't do these odds
                continue

            file_path = os.path.join(ARBITRAGE_PATH, bookmaker, date, sub_category + ".txt")

            # Get the soup from file (if it exists) or get it from the website
            html_soup = mu.get_page_source(file_path=file_path, url=url, ignore_files=ignore_files,
                                           sleep_time=1)
        print(sub_category + " done")

    print("All data loaded")
    # Now load and use the data
    for sub_category in category_list:
        print(sub_category + " start")
        filename = date + "-" + sub_category + ".log"

        # Loop through each bookmaker for this sub_category and download or load up the data
        category_bettable_outcomes = []
        for bet_provider in BOOKMAKERS_LIST:
            bookmaker = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]]["Bookmaker"]
            try:
                url = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]][sub_category]
            except KeyError:
                # No link found - this booky doesn't do these odds
                continue

            file_path = os.path.join(ARBITRAGE_PATH, bookmaker, date, sub_category + ".txt")

            # Get the soup from file (if it exists) or get it from the website
            html_soup = mu.get_page_source(file_path=file_path, url=url, ignore_files=ignore_files,
                                           sleep_time=SLEEP_TIME)
            # Create the class from the soup
            page = arbitrage.BettingPage(html_soup, bet_provider, "FOOTBALL")

            # Add events to the events list
            if len(page.bettable_outcomes) > 0:
                category_bettable_outcomes += page.bettable_outcomes

        # Create the arbs for these events
        category_arbitrage_bets = arbitrage.ArbitrageBetParser(category_bettable_outcomes)

        # Update the summary information
        if len(category_arbitrage_bets.possible_arbitrage_events) > 0:
            all_arbs += category_arbitrage_bets.arbitrage_bets
        events_count += len(category_arbitrage_bets.possible_arbitrage_events)
        orphan_count += len(category_arbitrage_bets.singleton_events)

        # Output the category_arbitrage_bets to a file
        category_arbitrage_bets.get_full_output(to_screen=False, out_file_path=os.path.join(RESULTS_PATH, filename))
        print(sub_category + " done")

    # Output summary information to file
    if not os.path.exists(os.path.dirname(SUMMARY_RESULTS_PATH)):
        os.makedirs(os.path.dirname(SUMMARY_RESULTS_PATH))
    out_file = open(os.path.join(SUMMARY_RESULTS_PATH, summary_filename), "w")

    out_file.write("Total Events: " + str(events_count) + "\n")
    out_file.write("Total Orphans: " + str(orphan_count) + "\n")
    out_file.write("Arbs found: " + str(len(all_arbs)) + "\n")

    all_arbs.sort(key=lambda x: x.arb_perc)

    for each in all_arbs:
        out_file.write(str(each))
        out_file.write("\n------------\n")

    out_file.close()


def adding_a_new_bookmaker():
    # Get an example page source of theirs and save it in the tests folder
    # mu.get_page_source_url("https://www.marathonbet.co.uk/en/popular/Football/England/Premier+League/?menu=21520",
    #                        WEBDRIVER_PATH,
    #                        out_file_path="/home/bobby/Documents/Arbing/MarathonBet_Football_PL.txt")

    # Create a new test for them to read the data from the file
    # This follows exactly the form of the other ones

    # Create the new class and check the tests pass
    # soup = get_page_source_file("F:\Coding\PycharmProjects\Arbitrage\Tests\WilliamHill_Football_PL.txt")
    # thing = BettingPage(soup, "WILLIAMHILL", "FOOTBALL")

    # Add to the dictionaries
    pass


def debug():
    adding_a_new_bookmaker()


if __name__ == "__main__":
    date = time.strftime("%Y_%m_%d_%H")
    calc_arbs_for_date(date)

    #debug()

    #adding_a_new_bookmaker()