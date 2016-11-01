import time
import os
import mwutils as mu

# Load the constants
c = mu.Constants('config.const')
c.CATEGORY_LIST = ["Football_PL", "Football_C", "Football_L1", "Football_L2", "Football_CL", "Football_LaLig",
                   "Football_GeBun"]
c.BOOKMAKERS = [c.EIGHT88_DICT,
                c.PADDY_DICT,
                c.PINNACLE_DICT,
                c.WILLIAMHILL_DICT
                ]

def calc_arbs_for_date(date, category_list=c.CATEGORY_LIST, ignore_files=False):
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
    #calc_arbs_for_date(date)

    #adding_a_new_bookmaker()