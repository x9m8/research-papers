# common.py — paths, constants, beach/station assignment, shared helpers.
# Paper 22: New York State Park beach water quality on Long Island, 2015-2025.

import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, 'data', 'raw')
DERIVED = os.path.join(ROOT, 'data', 'derived')
RESULTS = os.path.join(ROOT, 'results')
FIG = os.path.join(ROOT, 'figures')

for d in (DERIVED, RESULTS, FIG):
    os.makedirs(d, exist_ok=True)

# Enterococcus/Enterococci single-sample state standard for ocean (saltwater) beaches,
# applies to the Long Island region (NYS DOH sanitary code; OPRHP Beach Water Testing
# Data Dictionary, "Results" field).
ENTEROCOCCUS_THRESHOLD = 104  # CFU/100 mL

# NOAA GHCN-Daily first-order stations with continuous 2000-2025 PRCP records used as
# rainfall proxies. There is no official weather station at any individual beach, so
# each of the 15 OPRHP Long Island beach stations is assigned to whichever of the two
# approved stations is in its county: JFK International Airport (Queens, the nearest
# long-record station to the Nassau County shoreline) for the four Jones Beach State
# Park stations, and Islip-LI MacArthur Airport (central Suffolk County) for the
# eleven Suffolk County beach stations. This is a coarse, county-level proxy, not a
# beach-specific rain gauge; see Limitations.
STATION_JFK = 'USW00094789'
STATION_ISP = 'USW00004781'

NASSAU_BEACHES = {
    "Jones Beach SP Central-Central Mall",
    "Jones Beach SP Central-Field 2",
    "Jones Beach SP Central-Field 6",
    "Jones Beach SP Zach's Bay",
}


def beach_station(beach_name):
    return STATION_JFK if beach_name in NASSAU_BEACHES else STATION_ISP


# Waterbody is reported directly in the source data (Atlantic Ocean, Great South Bay,
# Long Island Sound) and is used as the exposure category throughout.
WATERBODIES = ("Atlantic Ocean", "Great South Bay", "Long Island Sound")

RAIN_RELATED_REASONS = {"Weather", "Preemptive: rainfall"}
