import multiprocessing
import time
import sys
import traceback

import mwutils.email_utils as eu
import mwutils.utils as mu
from joblib import Parallel, delayed

import arbitrage.arbitrage_classes as arbitrage
from arbitrage.config import *


NUM_CORES = multiprocessing.cpu_count()

# TODO: Add in football odds for other types - win + draw, total goals scored etc

def download_html_soup_to_file(sub_category, bet_provider, date):
    """Download html_soup for a sub_category and bet_provider"""
    bookmaker = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]]["Bookmaker"]
    try:
        url = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]][sub_category]
    except IndexError:
        # No link found - this booky doesn't do these odds
        return

    file_path = os.path.join(ARBITRAGE_PATH, bookmaker, date, sub_category + ".txt")

    if not os.path.exists(file_path):
        # Get the soup from file (if it exists) or get it from the website
        html_soup = mu.get_page_source(file_path=file_path, url=url, sleep_time=1)


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

    # First we check if we have the webpage data, if not then we download it
    download_input_list = []
    for sub_category in category_list:
        # For each sub_category and each bookmaker add inputs to the list
        for bet_provider in BOOKMAKERS_LIST:
            try:
                t = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]][sub_category]
                download_input_list.append((sub_category, bet_provider, date))
            except IndexError:
                continue
            except KeyError:
                continue

    # Run the jobs in parallel
    _ = Parallel(n_jobs=NUM_CORES)(delayed(download_html_soup_to_file)(i, j, k) for (i, j, k) in download_input_list)

    # Now load and use the data
    print("All data loaded")
    for sub_category in category_list:
        print(sub_category + " start")
        filename = date + "-" + sub_category + ".log"

        # Loop through each bookmaker for this sub_category and download or load up the data
        category_bettable_outcomes = []
        for bet_provider in BOOKMAKERS_LIST:
            bookmaker = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]]["Bookmaker"]
            class_to_poll = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]]["class_to_poll"]
            print("   ", bookmaker, end=": ")
            try:
                url = BOOKMAKERS[BOOKMAKERS_LIST[bet_provider]][sub_category]
            except IndexError:
                print("IndexError")
                continue
            except KeyError:
                # No link found - this booky doesn't do these odds
                print("No URL for this booky")
                continue

            file_path = os.path.join(ARBITRAGE_PATH, bookmaker, date, sub_category + ".txt")

            # Get the soup from file (if it exists) or get it from the website
            html_soup = mu.get_page_source(file_path=file_path, url=url, ignore_files=ignore_files,
                                           sleep_time=SLEEP_TIME, class_to_poll=class_to_poll)
            # Create the class from the soup
            category = sub_category.split("_")[0].upper()

            # Do the parsing of the page
            page = arbitrage.OddsPageParser(html_soup, bet_provider, category)

            # Add events to the events list
            if len(page.bettable_outcomes) > 0:
                category_bettable_outcomes += page.bettable_outcomes

            # Create the display output string
            output_string = ""
            output_string += str(len(page.bettable_outcomes))
            if len(page.parsing_row_error_reason) != 0:
                output_string += " (" + str(len(page.parsing_row_error_reason)) + " errors)"
            print(output_string)

        # Create the arbs for these events
        category_arbitrage_bets = arbitrage.ArbitrageBetParser(category_bettable_outcomes)

        # Update the summary information
        if len(category_arbitrage_bets.possible_arbitrage_events) > 0:
            all_arbs += category_arbitrage_bets.arbitrage_bets
        events_count += len(category_arbitrage_bets.possible_arbitrage_events)
        orphan_count += len(category_arbitrage_bets.singleton_events)

        # Output the category_arbitrage_bets to a file
        category_arbitrage_bets.get_full_output(to_screen=False, out_file_path=os.path.join(RESULTS_PATH, filename))

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

    if len(all_arbs) > 0:
        arbs_str = "Arbs found: " + str(len(all_arbs)) + "\n"
        for each in all_arbs:
            arbs_str += str(each) + "\n"
            arbs_str += "--------------------------------------\n"
    else:
        arbs_str = "No arbs found"

    return arbs_str


def adding_a_new_bookmaker():
    # Get an example page source of theirs and save it in the tests folder
    mu.get_page_source_url("https://sports.ladbrokes.com/en-gb/betting/football/english/premier-league/",
                           WEBDRIVER_PATH,
                           out_file_path="F:\Coding\PycharmProjects\LollingAllOverTheWorld\Tests\LadBrokes_Football_PL.txt")

    # Create a new test for them to read the data from the file
    # This follows exactly the form of the other ones

    # Create the new class and check the tests pass
    # soup = get_page_source_file("F:\Coding\PycharmProjects\Arbitrage\Tests\WilliamHill_Football_PL.txt")
    # thing = BettingPage(soup, "WILLIAMHILL", "FOOTBALL")

    # Add to the dictionaries
    pass


def debug():
    #adding_a_new_bookmaker()
    html_soup = mu.get_page_source_url("https://www.888sport.com/bet/#/filter/football/england/the_championship",
                                       WEBDRIVER_PATH, class_to_poll="KambiBC-event-participants__name")
    t = arbitrage.OddsPageParser(html_soup, "EIGHT88", "FOOTBALL")
    print(t)

if __name__ == "__main__":
    date = time.strftime("%Y_%m_%d_%H")
    try:
        arbs_str = calc_arbs_for_date(date)
        arbs_subject = None
    except:
        exception = traceback.format_exc()
        arbs_str = "ERROR" + str(exception)
        arbs_subject = "Arbitrage ERROR"

    # Email the text summary
    email = eu.AhabEmailSender("arbitrage",
                               "martinleewatts@gmail.com",
                               arbs_str,
                               subject=arbs_subject)
    email.send()

    # Kill leftover chromedriver processes
    processed_killed = mu.kill_processes_by_name("chromedriver_win.exe")
    print(str(processed_killed))
    #debug()

    # adding_a_new_bookmaker()
