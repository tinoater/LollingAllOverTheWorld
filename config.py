import os
from sys import platform

if platform == "linux" or platform == "linux2":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Files\\chromedriver")
elif platform == "win32":
    WEBDRIVER_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Files\\chromedriver_win.exe")

ARBITRAGE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "ScrapedFiles\\")
RESULTS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "Results\\")
SUMMARY_RESULTS_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), "SummaryResults\\")

# TODO: This needs to be fixed in the mwutils package
SELENIUM_IMPLICIT_WAIT = 30
SLEEP_TIME = 3

BOOKMAKERS_LIST = {"EIGHT88": 0,
                   "PADDYPOWER": 1,
                   #"PINNACLE": 2,
                   "WILLIAMHILL": 3,
                   "SPORTINGBET": 4,
                   "MARATHONBET": 5,
                   "LADBROKES": 6
                   }

CATEGORY_LIST = ["Football_PL",
                 "Football_C",
                 "Football_L1",
                 "Football_L2",
                 #"Football_CL",
                 "Football_LaLig",
                 "Football_GeBun"
                 #"Snooker_UKChamps"
                 ]

EIGHT88_DICT = {"Bookmaker": "888",
                "class_to_poll": "KambiBC-event-participants__name",
                "Football_L2": "https://www.888sport.com/bet/#/filter/football/england/league_two",
                "Football_L1": "https://www.888sport.com/bet/#/filter/football/england/league_one",
                "Football_C": "https://www.888sport.com/bet/#/filter/football/england/the_championship",
                "Football_PL": "https://www.888sport.com/bet/#/filter/football/england/premier_league",
                "Football_CL": "https://www.888sport.com/bet/#/filter/football/champions_league",
                "Football_LaLig": "https://www.888sport.com/bet/#/filter/football/spain/laliga",
                "Football_GeBun": "https://www.888sport.com/bet/#/filter/football/germany/bundesliga",
                "Snooker_UKChamps": "https://www.888sport.com/bet/#/filter/snooker/uk_championship"
                }

PADDY_DICT = {"Bookmaker": "PaddyPower",
              "class_to_poll": "pp_fb_event",
              "Football_L2": "http://www.paddypower.com/football/football-matches/english-league-2",
              "Football_L1": "http://www.paddypower.com/football/football-matches/english-league-1",
              "Football_PL": "http://www.paddypower.com/football/football-matches/premier-league",
              "Football_CL": "http://www.paddypower.com/football/football-matches/champions-league",
              "Football_LaLig": "http://www.paddypower.com/football/football-matches/spanish-la-liga-matches",
              "Football_GeBun": "http://www.paddypower.com/football/football-matches/Germany-Bundesliga-1",
              "Snooker_UKChamps": "http://www.paddypower.com/bet/snooker/uk-championship"
              }

PINNACLE_DICT = {"Bookmaker": "Pinnacle",
                 "class_to_poll": "",
                 "Football_PL": "https://www.pinnacle.com/en/odds/match/soccer/england/england-premier-league?sport=True",
                 "Football_C": "https://www.pinnacle.com/en/odds/match/soccer/england/england-championship",
                 "Football_L1": "https://www.pinnacle.com/en/odds/match/soccer/england/england-league-1",
                 "Football_CL": "https://www.pinnacle.com/en/odds/match/soccer/uefa/uefa-champions-league"
                 }

WILLIAMHILL_DICT = {"Bookmaker": "WilliamHill",
                    "class_to_poll": "rowOdd",
                    "Football_PL": "http://sports.williamhill.com/bet/en-gb/betting/t/295/English+Premier+League.html",
                    "Football_C": "http://sports.williamhill.com/bet/en-gb/betting/t/292/English+Championship.html",
                    "Football_L1": "http://sports.williamhill.com/bet/en-gb/betting/t/293/English+League+1.html",
                    "Football_L2": "http://sports.williamhill.com/bet/en-gb/betting/t/294/English+League+2.html",
                    "Football_LaLig": "http://sports.williamhill.com/bet/en-gb/betting/t/338/Spanish-La-Liga-Primera.html",
                    "Football_GeBun": "http://sports.williamhill.com/bet/en-gb/betting/t/315/German+Bundesliga.html",
                    "Snooker_UKChamps": "http://sports.williamhill.com/bet/en-gb/betting/t/16405/UK+Championship.html"
                   }

SPORTINGBET_DICT = {"Bookmaker": "SportingBet",
                    "class_to_poll": "event active",
                    "Football_PL": "http://www.sportingbet.com/sports-football/england-premier-league/1-102-386195.html",
                    "Football_C": "http://www.sportingbet.com/sports-football/england-championship/1-102-851891.html",
                    "Football_L1": "http://www.sportingbet.com/sports-football/england-league-one/1-102-851967.html",
                    "Football_L2": "http://www.sportingbet.com/sports-football/england-league-two/1-102-851968.html",
                    "Football_CL": "http://www.sportingbet.com/sports-football/champions-league-201617-matches/1-102-302288.html",
                    "Football_LaLig": "http://www.sportingbet.com/sports-football/spain-primera-division/1-102-84041.html",
                    "Football_GeBun": "http://www.sportingbet.com/sports-football/germany-bundesliga/1-102-84042.html",
                    "Snooker_UKChamps": "http://www.sportingbet.com/sports-snooker/uk-championship-2016-nov-22nd-4th-dec-match-coupon/1-5-603419.html"
                   }

MARATHONBET_DICT = {"Bookmaker": "MarathonBet",
                    "class_to_poll": "foot-market",
                    "Football_PL": "https://www.marathonbet.co.uk/en/popular/Football/England/Premier+League/?menu=21520",
                    "Football_C": "https://www.marathonbet.co.uk/en/popular/Football/England/Championship/?menu=22807",
                    "Football_L1": "https://www.marathonbet.co.uk/en/popular/Football/England/League+1/?menu=22808",
                    "Football_L2": "https://www.marathonbet.co.uk/en/popular/Football/England/League+2/?menu=22809",
                    "Football_CL": "https://www.marathonbet.co.uk/en/popular/Football/Clubs.+International/UEFA+Champions+League/?menu=21255",
                    "Football_LaLig": "https://www.marathonbet.co.uk/en/popular/Football/Spain/Primera+Division/?menu=8736",
                    "Football_GeBun": "https://www.marathonbet.co.uk/en/popular/Football/Germany/Bundesliga/?menu=22436",
                    "Snooker_UKChamps": "https://www.marathonbet.co.uk/en/betting/Snooker/UK+Championship/?menu=95572"
                    }

LADBROKES_DICT = {"Bookmaker": "Ladbrokes",
                  "class_to_poll": "name",
                  "Football_PL": "https://sports.ladbrokes.com/en-gb/betting/football/english/premier-league/",
                  "Football_C": "https://sports.ladbrokes.com/en-gb/betting/football/english/championship/",
                  "Football_L1": "https://sports.ladbrokes.com/en-gb/betting/football/english/league-one/",
                  "Football_L2": "https://sports.ladbrokes.com/en-gb/betting/football/english/league-two/"
                 }

FOOTBALL_DICT = {"ARSENAL": 1,
                 "BOURNEMOUTH": 2,
                 "BOURNEMOUTH AFC": 2,
                 "BURNLEY": 3,
                 "CHELSEA": 4,
                 "CRYSTAL PALACE": 5,
                 "EVERTON": 6,
                 "HULL CITY": 7,
                 "HULL": 7,
                 "LEICESTER CITY": 8,
                 "LEICESTER": 8,
                 "LIVERPOOL": 9,
                 "MANCHESTER CITY": 10,
                 "MAN CITY": 10,
                 "MANCHESTER UNITED": 11,
                 "MANCHESTER UTD": 11,
                 "MAN UTD": 11,
                 "MIDDLESBROUGH": 12,
                 "MIDDLESBOROUGH": 12,
                 "SOUTHAMPTON": 13,
                 "STOKE CITY": 14,
                 "STOKE": 14,
                 "SUNDERLAND": 15,
                 "SWANSEA CITY": 16,
                 "SWANSEA": 16,
                 "TOTTENHAM HOTSPUR": 17,
                 "TOTTENHAM": 17,
                 "WATFORD": 18,
                 "WEST BROMWICH ALBION": 19,
                 "WEST BROMWICH": 19,
                 "WEST BROM": 19,
                 "W.B.A": 19,
                 "WEST HAM UNITED": 20,
                 "WEST HAM": 20,
                 "ASTON VILLA": 101,
                 "BARNSLEY": 102,
                 "BIRMINGHAM": 103,
                 "BIRMINGHAM CITY": 103,
                 "BLACKBURN": 104,
                 "BLACKBURN ROVERS": 104,
                 "BRENTFORD": 105,
                 "BRIGHTON": 106,
                 "BRIGHTON & HOVE ALBION": 106,
                 "BRISTOL CITY": 107,
                 "BURTON ALBION": 108,
                 "BURTON": 108,
                 "CARDIFF CITY": 109,
                 "CARDIFF": 109,
                 "DERBY COUNTY": 110,
                 "DERBY": 110,
                 "FULHAM": 111,
                 "HUDDERSFIELD": 112,
                 "HUDDERSFIELD TOWN": 112,
                 "IPSWICH TOWN": 113,
                 "IPSWICH": 113,
                 "LEEDS UNITED": 114,
                 "LEEDS": 114,
                 "NEWCASTLE": 115,
                 "NEWCASTLE UNITED": 115,
                 "NORWICH CITY": 116,
                 "NORWICH": 116,
                 "NOTTM FOREST": 117,
                 "NOTTINGHAM FOREST": 117,
                 "PRESTON": 118,
                 "PRESTON NORTH END": 118,
                 "QPR": 119,
                 "QUEENS PARK RANGERS": 119,
                 "READING": 120,
                 "ROTHERHAM": 121,
                 "ROTHERHAM UNITED": 121,
                 "SHEFF WED": 122,
                 "SHEFFIELD WEDNESDAY": 122,
                 "WIGAN ATHLETIC": 123,
                 "WIGAN": 123,
                 "WOLVES": 124,
                 "WOLVERHAMPTON WANDERERS": 124,
                 "AFC WIMBLEDON": 201,
                 "WIMBLEDON": 201,
                 "BOLTON": 202,
                 "BOLTON WANDERERS": 202,
                 "BRADFORD CITY": 203,
                 "BRADFORD": 203,
                 "BRISTOL ROVERS": 204,
                 "BURY": 205,
                 "BURY TOWN": 205,
                 "CHARLTON": 206,
                 "CHARLTON ATHLETIC": 206,
                 "CHESTERFIELD": 207,
                 "COVENTRY": 208,
                 "COVENTRY CITY": 208,
                 "FLEETWOOD": 209,
                 "FLEETWOOD TOWN": 209,
                 "GILLINGHAM": 210,
                 "MILLWALL": 211,
                 "MK DONS": 212,
                 "MILTON KEYNES DONS": 212,
                 "NORTHAMPTON": 213,
                 "NORTHAMPTON TOWN": 213,
                 "OLDHAM": 214,
                 "OLDHAM ATHLETIC": 214,
                 "OXFORD": 215,
                 "OXFORD UNITED": 215,
                 "PETERBOROUGH": 216,
                 "PETERBOROUGH UNITED": 216,
                 "PORT VALE": 217,
                 "ROCHDALE": 218,
                 "SCUNTHORPE": 219,
                 "SCUNTHORPE UNITED": 219,
                 "SHEFF UTD": 220,
                 "SHEFFIELD UNITED": 220,
                 "SHREWSBURY": 221,
                 "SHREWSBURY TOWN": 221,
                 "SOUTHEND UTD": 222,
                 "SOUTHEND": 222,
                 "SOUTHEND UNITED": 222,
                 "SWINDON TOWN": 223,
                 "SWINDON": 223,
                 "WALSALL": 224,
                 "WALLSALL": 224,
                 "ACCRINGTON STANLEY": 301,
                 "ACCRINGTON": 301,
                 "BARNET": 302,
                 "BLACKPOOL": 303,
                 "CAMBRIDGE UNITED": 304,
                 "CAMBRIDGE": 304,
                 "CAMBRIDGE U": 304,
                 "CARLISLE UNITED": 305,
                 "CHELTENHAM TOWN": 306,
                 "COLCHESTER UNITED": 307,
                 "CRAWLEY TOWN": 308,
                 "CREWE ALEXANDRA": 309,
                 "DONCASTER ROVERS": 310,
                 "EXETER CITY": 311,
                 "GRIMSBY TOWN": 312,
                 "HARTLEPOOL UNITED": 313,
                 "LEYTON ORIENT": 314,
                 "LUTON TOWN": 315,
                 "MANSFIELD TOWN": 316,
                 "MORECAMBE": 317,
                 "NEWPORT COUNTY": 318,
                 "NEWPORT": 318,
                 "NOTTS COUNTY": 319,
                 "NOTTS CO.": 319,
                 "PLYMOUTH ARGYLE": 320,
                 "PORTSMOUTH": 321,
                 "STEVENAGE": 322,
                 "WYCOMBE WANDERERS": 323,
                 "YEOVIL TOWN": 324,
                 "EXETER": 311,
                 "CHELTENHAM": 306,
                 "STEVENAGE FC": 322,
                 "CARLISLE": 305,
                 "DONCASTER": 310,
                 "COLCHESTER": 307,
                 "CRAWLEY": 308,
                 "CREWE": 309,
                 "YEOVIL": 324,
                 "GRIMSBY": 312,
                 "HARTLEPOOL": 313,
                 "LUTON": 315,
                 "MANSFIELD": 316,
                 "PLYMOUTH": 320,
                 "WYCOMBE": 323,
                 "BESIKTAS": 401,
                 "BEIKTA A..": 401,
                 "NAPOLI": 402,
                 "SSC NAPOLI": 402,
                 "ATLTICO MADRID": 403,
                 "ATLETICO MADRID": 403,
                 "FC ROSTOV": 404,
                 "ROSTOV FK": 404,
                 "ROSTOV": 404,
                 "BASEL": 405,
                 "FC BASEL": 405,
                 "FX ROSTOV": 404,
                 "FK ROSTOV": 404,
                 "PARIS SG": 407,
                 "PARIS SAINT GERMAIN": 407,
                 "PARIS SAINT-GERMAIN": 407,
                 "PSG": 407,
                 "BENFICA": 408,
                 "DYNAMO KIEV": 409,
                 "DYNAMO KYIV": 409,
                 "BORUSSIA MONCHENGLADBACH": 410,
                 "BORUSSIA MNCHENGLADBACH": 410,
                 "BORUSSIA MOENCHENGLADBACH": 410,
                 "CELTIC": 411,
                 "CELTIC FC": 411,
                 "LUDOGORETS RAZGRAD": 412,
                 "LUDOGORETS RAZGRAD (N)": 412,
                 "BARCELONA": 413,
                 "FC BARCELONA": 413,
                 "PSV": 414,
                 "PSV EINDHOVEN": 414,
                 "BAYERN MUNICH": 415,
                 "BAYERN MNCHEN": 415,
                 "BAYERN MUNCHEN": 415,
                 "BORUSSIA DORTMUND": 416,
                 "DORTMUND": 416,
                 "SPORTING LISBON": 417,
                 "SPORTING LISBOA": 417,
                 "SPORTING CP": 417,
                 "FC COPENHAGEN": 418,
                 "FC KOBENHAVN": 418,
                 "JUVENTUS": 419,
                 "LYON": 420,
                 "FC PORTO": 421,
                 "PORTO": 421,
                 "LEGIA WARSAW": 422,
                 "LEGIA WARSZAWA": 422,
                 "CLUB BRUGGE": 423,
                 "CLUB BRUGES": 423,
                 "BRUGGE": 423,
                 "REAL MADRID": 424,
                 "MONACO": 425,
                 "AS MONACO": 425,
                 "CSKA MOSCOW": 426,
                 "DINAMO ZAGREB": 428,
                 "BAYER LEERKUSEN": 429,
                 "BAYER LEVERKUSEN": 429,
                 "BAYER 04 LEVERKUSEN": 429,
                 "LEVERKUSEN": 429,
                 "REAL MADRD": 430,
                 "SEVILLA": 431,
                 "VILLARREAL": 433,
                 "ATHLETIC BILBAO": 435,
                 "ATHLETIC CLUB BILBAO": 435,
                 "REAL SOCIEDAD": 436,
                 "CELTA VIGO": 437,
                 "CELTA DE VIGO": 437,
                 "LAS PALMAS": 438,
                 "DEPORTIVA LAS PALMAS": 438,
                 "MALAGA": 439,
                 "MLAGA": 439,
                 "EIBAR": 440,
                 "REAL BETIS": 441,
                 "BETIS": 441,
                 "ALAVES": 442,
                 "ALAVS": 442,
                 "VALENCIA": 443,
                 "ESPANYOL": 444,
                 "DEPORTIVO LA CORUNA": 445,
                 "DEPORTIVO LA CORUA": 445,
                 "DEPORTIVO DE LA CORUNA": 445,
                 "SPORTING GIJON": 446,
                 "SPORTING DE GIJN": 446,
                 "GRANADA": 447,
                 "GRANADA CF": 447,
                 "LEGANES": 448,
                 "LEGANS": 448,
                 "OSASUNA": 449,
                 "RB LEIPZIG": 451,
                 "LEIPZIG": 451,
                 "RASENBALLSPORT LEIPZIG": 451,
                 "HERTHA BERLIN": 452,
                 "HERTHA BSC": 452,
                 "HOFFENHEIM": 453,
                 "1899 HOFFENHEIM": 453,
                 "COLOGNE": 454,
                 "FC COLOGNE": 454,
                 "1. FC KLN": 454,
                 "FC KOLN": 454,
                 "1.FC KOELN": 454,
                 "KOLN": 454,
                 "EINTRACHT FRANKFURT": 456,
                 "SC FREIBURG": 457,
                 "FREIBURG": 457,
                 "MAINZ": 458,
                 "MAINZ 05": 458,
                 "FSV MAINZ 05": 458,
                 "1. FSV MAINZ 05": 458,
                 "M'GLADBACH": 459,
                 "FC AUGSBURG": 461,
                 "AUGSBURG": 461,
                 "SCHALKE": 462,
                 "SCHALKE 04": 462,
                 "WERDER BREMEN": 463,
                 "WOLFSBURG": 464,
                 "VFL WOLFSBURG": 464,
                 "FC INGOLSTADT 04": 465,
                 "FC INGOLSTADT": 465,
                 "INGOLSTADT": 465,
                 "INGOLSTADT 04": 465,
                 "HAMBURG": 466,
                 "HAMBURGER SV": 466,
                 "HAMBURGER": 466,
                 "SV DARMSTADT 98": 467,
                 "DARMSTADT 98": 467,
                 "DARMSTADT": 467
                 }
SNOOKER_DICT = {"BRECEL, LUCA": 1,
                "DALE, DOMINIC": 2,
                "DUNN, MIKE": 3,
                "HIGGINS, JOHN": 4,
                "HIGHFIELD, LIAM": 5,
                "LINES, PETER": 6,
                "MAGUIRE, STEPHEN": 7,
                "WELLS, DANIEL": 8,
                "WILLIAMS, MARK": 9,
                "BAIRD, SAM": 10,
                "BINGHAM, STUART": 11,
                "CARTER, ALLISTER": 12,
                "CARTER, ALI": 12,
                "HAWKINS, BARRY": 13,
                "MCMANUS, ALAN": 14,
                "STEVENS, MATTHEW": 15,
                "YUELONG, ZHOU": 16,
                "ALLEN, MARK": 17,
                "BINGTAO, YAN": 18,
                "CLARK, RHYS": 19,
                "GILBERT, DAVID": 20,
                "JUNHUI, DING": 21,
                "MIAH, HAMMAD": 22,
                "WOOLLASTON, BEN": 23,
                "XIWEN, MEI": 24,
                "ANDA, ZHANG": 25,
                "DAY, RYAN": 26,
                "GUODONG, XIAO": 27,
                "HULL, ROBIN": 28,
                "LINES, OLIVER": 29,
                "MCLEOD, RORY": 30,
                "ROBERTSON, JIMMY": 31,
                "WALDEN, RICKY": 32,
                "CRAIGIE, SAM": 33,
                "DOTT, GRAEME": 34,
                "GEORGIOU, MICHAEL": 35,
                "SAENGKHAM, NOPPON": 36,
                "YUCHEN, WANG": 37,
                "WAKELIN, CHRIS": 38,
                "XINTONG, ZHAO": 39,
                "SELBY, MARK": 40,
                "HIGGINSON, ANDREW": 41,
                "MANN, MITCHELL": 42,
                "DELU, YU": 43,
                "YU DELU": 43,
                "WILLIAMS, ROBBIE": 44,
                "O'BRIEN, FERGAL": 45,
                "FERGAL O BRIEN": 45,
                "JONES, JAMIE": 46,
                "WHITE, MICHAEL": 47,
                "HOLT, MICHAEL": 48,
                "LAWLER, ROD": 49,
                "WENBO, LIANG": 50,
                "O'SULLIVAN, RONNIE": 51,
                "JOYCE, MARK": 52,
                "MUIR, ROSS": 53,
                "MILKINS, ROBERT": 54,
                "DAVISON, PAUL": 55,
                "GOULD, MARTIN": 56,
                "MCGILL, ANTHONY": 57,
                "MAFLIN, KURT": 58,
                "PERRY, JOE": 59,
                "MURPHY, SHAUN": 60,
                "TRUMP, JUDD": 61,
                "FU, MARCO": 62,
                "DAVIS, MARK": 63,
                "DONALDSON, SCOTT": 64,
                "LUCA BRECEL": 1,
                "DANIEL WELLS": 8,
                "LIAM HIGHFIELD": 5,
                "DOMINIC DALE": 2,
                "MARK WILLIAMS": 9,
                "JOHN HIGGINS": 4,
                "MIKE DUNN": 3,
                "STEPHEN MAGUIRE": 7,
                "ZHOU YUELONG": 16,
                "SAM BAIRD": 10,
                "ALI CARTER": 12,
                "MATTHEW STEVENS": 15,
                "BARRY HAWKINS": 13,
                "STUART BINGHAM": 11,
                "ALAN MCMANUS": 14,
                "PETER LINES": 6,
                "BEN WOOLLASTON": 23,
                "YAN BINGTAO": 18,
                "DAVID GILBERT": 20,
                "HAMMAD MIAH": 22,
                "HAMMD MIAH": 22,
                "RHYS CLARK": 19,
                "DING JUNHUI": 21,
                "MEI XIWEN": 24,
                "MEI XI WEN": 24,
                "MARK ALLEN": 17,
                "RYAN DAY": 26,
                "RORY MCLEOD": 30,
                "ZHANG ANDA": 25,
                "OLIVER LINES": 29,
                "ROBIN HULL": 28,
                "RICKY WALDEN": 32,
                "XIAO GUODONG": 27,
                "JIMMY ROBERTSON": 31,
                "SAM CRAIGIE": 33,
                "MARK SELBY": 40,
                "WANG YUCHEN": 37,
                "GRAEME DOTT": 34,
                "ANDREW HIGGINSON": 41,
                "NOPPON SAENGKHAM": 36,
                "MICHAEL GEORGIOU": 35,
                "ZHAO XINTONG": 39,
                "MICHAEL HOLT": 48,
                "MITCHELL MANN": 42,
                "ROBBIE WILLIAMS": 44,
                "MICHAEL WHITE": 47,
                "FERGAL O'BRIEN": 45,
                "YU DE LU": 43,
                "JAMIE JONES": 46,
                "CHRIS WAKELIN": 38,
                "PAUL DAVISON": 55,
                "LIANG WENBO": 50,
                "MARK JOYCE": 52,
                "ROBERT MILKINS": 54,
                "RONNIE O'SULLIVAN": 51,
                "RONNIE O SULLIVAN": 51,
                "ROSS MUIR": 53,
                "MARTIN GOULD": 56,
                "ROD LAWLER": 49,
                "KURT MAFLIN": 58,
                "MARCO FU": 62,
                "ANTHONY MCGILL": 57,
                "JUDD TRUMP": 61,
                "SHAUN MURPHY": 60,
                "SCOTT DONALDSON": 64,
                "JOE PERRY": 59,
                "MARK DAVIS": 63
                }
CATEGORY_DICT = {"FOOTBALL": 1,
                 "SNOOKER": 2}

PARTICIPANT_DICT = dict()
PARTICIPANT_DICT["FOOTBALL"] = FOOTBALL_DICT
PARTICIPANT_DICT["SNOOKER"] = SNOOKER_DICT

SUBCATEGORY_DICT = dict()
SUBCATEGORY_DICT["FOOTBALL"] = {"PREMIER LEAGUE": 1,
                                "ENGLAND-PREMIERLEAGUE": 1,
                                "ENGLISH PREMIER LEAGUE": 1,
                                "ENGLAND - PREMIER LEAGUE": 1,
                                "ENGLAND. PREMIER LEAGUE": 1,
                                "THE CHAMPIONSHIP": 2,
                                "ENGLISH CHAMPIONSHIP": 2,
                                "CHAMPIONSHIP": 2,
                                "ENGLAND - CHAMPIONSHIP": 2,
                                "ENGLAND. CHAMPIONSHIP": 2,
                                "ENGLAND. LEAGUE 1": 3,
                                "ENGLISH LEAGUE 1": 3,
                                "ENGLAND - LEAGUE ONE": 3,
                                "LEAGUE ONE": 3,
                                "ENGLAND. LEAGUE 2": 4,
                                "ENGLISH LEAGUE 2": 4,
                                "LEAGUE TWO": 4,
                                "ENGLAND - LEAGUE TWO": 4,
                                "CLUBS. INTERNATIONAL. UEFA CHAMPIONS LEAGUE. GROUP STAGE": 11,
                                "CHAMPIONS LEAGUE": 11,
                                "CHAMPIONS LEAGUE - 2016/17 - MATCHES": 11,
                                "SPANISH LA LIGA PRIMERA": 12,
                                "SPANISH LA LIGA": 12,
                                "SPAIN - PRIMERA DIVISION": 12,
                                "LALIGA": 12,
                                "SPANISH. PRIMERA DIVISION": 12,
                                "SPAIN. PRIMERA DIVISION": 12,
                                "GERMAN BUNDESLIGA": 13,
                                "GERMANY. BUNDESLIGA": 13,
                                "GERMANY - BUNDESLIGA": 13,
                                "BUNDESLIGA": 13,
                                "FA CUP": 20}
SUBCATEGORY_DICT["SNOOKER"] = {"UK CHAMPIONSHIPS": 1,
                               "UK CHAMPIONSHIP": 1}

BOOKMAKERS = [EIGHT88_DICT,
              PADDY_DICT,
              PINNACLE_DICT,
              WILLIAMHILL_DICT,
              SPORTINGBET_DICT,
              MARATHONBET_DICT,
              LADBROKES_DICT
              ]
