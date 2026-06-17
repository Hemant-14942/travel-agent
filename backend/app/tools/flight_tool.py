import re

import requests

from app.config import get_required_env
from app.logger import get_logger

log = get_logger(__name__)

AVIATIONSTACK_FLIGHTS_URL = "http://api.aviationstack.com/v1/flights"
TAVILY_SEARCH_URL = "https://api.tavily.com/search"
USD_TO_INR_ESTIMATE = 83

CITY_TO_IATA_CODES: dict[str, list[str]] = {
    # ── INDIA ──────────────────────────────────────────────────────────────
    # North India
    "delhi": ["DEL"],
    "new delhi": ["DEL"],
    "indira gandhi": ["DEL"],
    "amritsar": ["ATQ"],
    "golden temple": ["ATQ"],
    "chandigarh": ["IXC"],
    "jammu": ["IXJ"],
    "srinagar": ["SXR"],
    "kashmir": ["SXR"],
    "leh": ["IXL"],
    "ladakh": ["IXL"],
    "shimla": ["SLV"],
    "kullu": ["KUU"],
    "manali": ["KUU"],
    "dehradun": ["DED"],
    "agra": ["AGR"],
    "taj mahal": ["AGR"],
    "lucknow": ["LKO"],
    "varanasi": ["VNS"],
    "benaras": ["VNS"],
    "kashi": ["VNS"],
    "allahabad": ["IXD"],
    "prayagraj": ["IXD"],
    "gorakhpur": ["GOP"],
    "kanpur": ["KNU"],
    "bareilly": ["BEK"],
    # West India
    "mumbai": ["BOM"],
    "bombay": ["BOM"],
    "pune": ["PNQ"],
    "poona": ["PNQ"],
    "ahmedabad": ["AMD"],
    "amdavad": ["AMD"],
    "surat": ["STV"],
    "vadodara": ["BDQ"],
    "baroda": ["BDQ"],
    "rajkot": ["RAJ"],
    "bhavnagar": ["BHU"],
    "goa": ["GOI"],
    "panaji": ["GOI"],
    "dabolim": ["GOI"],
    "mopa": ["GOX"],
    "nasik": ["ISK"],
    "nashik": ["ISK"],
    "kolhapur": ["KLH"],
    "aurangabad": ["IXU"],
    "nanded": ["NDC"],
    "latur": ["LTU"],
    # South India
    "bangalore": ["BLR"],
    "bengaluru": ["BLR"],
    "chennai": ["MAA"],
    "madras": ["MAA"],
    "hyderabad": ["HYD"],
    "secunderabad": ["HYD"],
    "kochi": ["COK"],
    "cochin": ["COK"],
    "ernakulam": ["COK"],
    "thiruvananthapuram": ["TRV"],
    "trivandrum": ["TRV"],
    "kozhikode": ["CCJ"],
    "calicut": ["CCJ"],
    "kannur": ["CNN"],
    "mangaluru": ["IXE"],
    "mangalore": ["IXE"],
    "coimbatore": ["CJB"],
    "tiruchirappalli": ["TRZ"],
    "trichy": ["TRZ"],
    "madurai": ["IXM"],
    "tirupati": ["TIR"],
    "vijayawada": ["VGA"],
    "visakhapatnam": ["VTZ"],
    "vizag": ["VTZ"],
    "rajahmundry": ["RJA"],
    "hubli": ["HBX"],
    "belgaum": ["IXG"],
    "belagavi": ["IXG"],
    "mysore": ["MYQ"],
    "mysuru": ["MYQ"],
    "salem": ["SXV"],
    "tuticorin": ["TCR"],
    "thoothukudi": ["TCR"],
    # East India & North-East
    "kolkata": ["CCU"],
    "calcutta": ["CCU"],
    "bhubaneswar": ["BBI"],
    "bhubaneshwar": ["BBI"],
    "patna": ["PAT"],
    "ranchi": ["IXR"],
    "raipur": ["RPR"],
    "guwahati": ["GAU"],
    "dibrugarh": ["DIB"],
    "jorhat": ["JRH"],
    "imphal": ["IMF"],
    "manipur": ["IMF"],
    "agartala": ["IXA"],
    "aizawl": ["AJL"],
    "shillong": ["SHL"],
    "silchar": ["IXS"],
    "lilabari": ["IXI"],
    "north lakhimpur": ["IXI"],
    "dimapur": ["DMU"],
    "nagaland": ["DMU"],
    "itanagar": ["HGI"],
    "pasighat": ["IXT"],
    # Central India
    "bhopal": ["BHO"],
    "indore": ["IDR"],
    "jabalpur": ["JLR"],
    "gwalior": ["GWL"],
    "nagpur": ["NAG"],
    "jaipur": ["JAI"],
    "jodhpur": ["JDH"],
    "jaisalmer": ["JSA"],
    "udaipur": ["UDR"],
    "ajmer": ["KQH"],
    "kishangarh": ["KQH"],
    "bikaner": ["BKB"],
    # Andaman, Lakshadweep
    "port blair": ["IXZ"],
    "andaman": ["IXZ"],
    "agatti": ["AGX"],
    "lakshadweep": ["AGX"],

    # ── SOUTHEAST ASIA ─────────────────────────────────────────────────────
    "singapore": ["SIN"],
    "bangkok": ["BKK", "DMK"],
    "suvarnabhumi": ["BKK"],
    "don mueang": ["DMK"],
    "phuket": ["HKT"],
    "chiang mai": ["CNX"],
    "krabi": ["KBV"],
    "koh samui": ["USM"],
    "bali": ["DPS"],
    "denpasar": ["DPS"],
    "jakarta": ["CGK", "HLP"],
    "surabaya": ["SUB"],
    "lombok": ["LOP"],
    "medan": ["KNO"],
    "kuala lumpur": ["KUL"],
    "kl": ["KUL"],
    "penang": ["PEN"],
    "kota kinabalu": ["BKI"],
    "langkawi": ["LGK"],
    "manila": ["MNL"],
    "cebu": ["CEB"],
    "davao": ["DVO"],
    "ho chi minh": ["SGN"],
    "saigon": ["SGN"],
    "hanoi": ["HAN"],
    "da nang": ["DAD"],
    "phnom penh": ["PNH"],
    "cambodia": ["PNH"],
    "siem reap": ["REP"],
    "angkor": ["REP"],
    "yangon": ["RGN"],
    "rangoon": ["RGN"],
    "myanmar": ["RGN"],
    "vientiane": ["VTE"],
    "laos": ["VTE"],
    "colombo": ["CMB"],
    "sri lanka": ["CMB"],
    "kathmandu": ["KTM"],
    "nepal": ["KTM"],
    "dhaka": ["DAC"],
    "bangladesh": ["DAC"],
    "chittagong": ["CGP"],
    "male": ["MLE"],
    "maldives": ["MLE"],
    "islamabad": ["ISB"],
    "pakistan": ["ISB"],
    "karachi": ["KHI"],
    "lahore": ["LHE"],
    "kabul": ["KBL"],

    # ── EAST ASIA ───────────────────────────────────────────────────────────
    "tokyo": ["NRT", "HND"],
    "narita": ["NRT"],
    "haneda": ["HND"],
    "osaka": ["KIX", "ITM"],
    "kyoto": ["KIX"],
    "sapporo": ["CTS"],
    "fukuoka": ["FUK"],
    "nagoya": ["NGO"],
    "okinawa": ["OKA"],
    "hiroshima": ["HIJ"],
    "seoul": ["ICN", "GMP"],
    "incheon": ["ICN"],
    "busan": ["PUS"],
    "jeju": ["CJU"],
    "beijing": ["PEK", "PKX"],
    "shanghai": ["PVG", "SHA"],
    "guangzhou": ["CAN"],
    "shenzhen": ["SZX"],
    "chengdu": ["CTU"],
    "chongqing": ["CKG"],
    "hong kong": ["HKG"],
    "macau": ["MFM"],
    "taipei": ["TPE"],
    "taiwan": ["TPE"],
    "kaohsiung": ["KHH"],

    # ── MIDDLE EAST ─────────────────────────────────────────────────────────
    "dubai": ["DXB"],
    "abu dhabi": ["AUH"],
    "sharjah": ["SHJ"],
    "doha": ["DOH"],
    "qatar": ["DOH"],
    "muscat": ["MCT"],
    "oman": ["MCT"],
    "kuwait city": ["KWI"],
    "kuwait": ["KWI"],
    "riyadh": ["RUH"],
    "jeddah": ["JED"],
    "dammam": ["DMM"],
    "bahrain": ["BAH"],
    "amman": ["AMM"],
    "jordan": ["AMM"],
    "beirut": ["BEY"],
    "lebanon": ["BEY"],
    "tel aviv": ["TLV"],
    "israel": ["TLV"],
    "tehran": ["IKA"],
    "iran": ["IKA"],
    "istanbul": ["IST", "SAW"],
    "ankara": ["ESB"],
    "izmir": ["ADB"],
    "antalya": ["AYT"],

    # ── EUROPE ──────────────────────────────────────────────────────────────
    "london": ["LHR", "LGW", "STN"],
    "heathrow": ["LHR"],
    "gatwick": ["LGW"],
    "manchester": ["MAN"],
    "birmingham": ["BHX"],
    "edinburgh": ["EDI"],
    "glasgow": ["GLA"],
    "dublin": ["DUB"],
    "ireland": ["DUB"],
    "paris": ["CDG", "ORY"],
    "nice": ["NCE"],
    "lyon": ["LYS"],
    "marseille": ["MRS"],
    "amsterdam": ["AMS"],
    "brussels": ["BRU"],
    "belgium": ["BRU"],
    "frankfurt": ["FRA"],
    "munich": ["MUC"],
    "berlin": ["BER"],
    "hamburg": ["HAM"],
    "dusseldorf": ["DUS"],
    "zurich": ["ZRH"],
    "switzerland": ["ZRH"],
    "geneva": ["GVA"],
    "vienna": ["VIE"],
    "austria": ["VIE"],
    "rome": ["FCO"],
    "milan": ["MXP", "LIN"],
    "venice": ["VCE"],
    "florence": ["FLR"],
    "naples": ["NAP"],
    "palermo": ["PMO"],
    "madrid": ["MAD"],
    "barcelona": ["BCN"],
    "seville": ["SVQ"],
    "malaga": ["AGP"],
    "lisbon": ["LIS"],
    "portugal": ["LIS"],
    "porto": ["OPO"],
    "athens": ["ATH"],
    "greece": ["ATH"],
    "thessaloniki": ["SKG"],
    "mykonos": ["JMK"],
    "santorini": ["JTR"],
    "heraklion": ["HER"],
    "crete": ["HER"],
    "rhodes": ["RHO"],
    "oslo": ["OSL"],
    "norway": ["OSL"],
    "stockholm": ["ARN"],
    "sweden": ["ARN"],
    "copenhagen": ["CPH"],
    "denmark": ["CPH"],
    "helsinki": ["HEL"],
    "finland": ["HEL"],
    "reykjavik": ["KEF"],
    "iceland": ["KEF"],
    "warsaw": ["WAW"],
    "poland": ["WAW"],
    "prague": ["PRG"],
    "czech republic": ["PRG"],
    "czechia": ["PRG"],
    "budapest": ["BUD"],
    "hungary": ["BUD"],
    "bucharest": ["OTP"],
    "romania": ["OTP"],
    "sofia": ["SOF"],
    "bulgaria": ["SOF"],
    "zagreb": ["ZAG"],
    "croatia": ["ZAG"],
    "dubrovnik": ["DBV"],
    "split": ["SPU"],
    "moscow": ["SVO", "DME"],
    "st petersburg": ["LED"],
    "saint petersburg": ["LED"],

    # ── AFRICA ──────────────────────────────────────────────────────────────
    "cairo": ["CAI"],
    "egypt": ["CAI"],
    "nairobi": ["NBO"],
    "kenya": ["NBO"],
    "johannesburg": ["JNB"],
    "south africa": ["JNB"],
    "cape town": ["CPT"],
    "durban": ["DUR"],
    "lagos": ["LOS"],
    "nigeria": ["LOS"],
    "abuja": ["ABV"],
    "accra": ["ACC"],
    "ghana": ["ACC"],
    "casablanca": ["CMN"],
    "morocco": ["CMN"],
    "marrakech": ["RAK"],
    "addis ababa": ["ADD"],
    "ethiopia": ["ADD"],
    "dar es salaam": ["DAR"],
    "tanzania": ["DAR"],
    "zanzibar": ["ZNZ"],
    "kampala": ["EBB"],
    "uganda": ["EBB"],
    "kigali": ["KGL"],
    "rwanda": ["KGL"],
    "mauritius": ["MRU"],
    "port louis": ["MRU"],
    "tunis": ["TUN"],
    "tunisia": ["TUN"],
    "algiers": ["ALG"],
    "algeria": ["ALG"],
    "tripoli": ["TIP"],
    "libya": ["TIP"],

    # ── NORTH AMERICA ───────────────────────────────────────────────────────
    "new york": ["JFK", "EWR", "LGA"],
    "new york city": ["JFK", "EWR", "LGA"],
    "nyc": ["JFK", "EWR"],
    "jfk": ["JFK"],
    "los angeles": ["LAX"],
    "la": ["LAX"],
    "san francisco": ["SFO"],
    "chicago": ["ORD", "MDW"],
    "miami": ["MIA"],
    "orlando": ["MCO"],
    "las vegas": ["LAS"],
    "seattle": ["SEA"],
    "boston": ["BOS"],
    "washington": ["IAD", "DCA"],
    "washington dc": ["IAD", "DCA"],
    "atlanta": ["ATL"],
    "dallas": ["DFW", "DAL"],
    "houston": ["IAH", "HOU"],
    "denver": ["DEN"],
    "phoenix": ["PHX"],
    "san diego": ["SAN"],
    "minneapolis": ["MSP"],
    "detroit": ["DTW"],
    "philadelphia": ["PHL"],
    "toronto": ["YYZ"],
    "canada": ["YYZ"],
    "vancouver": ["YVR"],
    "montreal": ["YUL"],
    "calgary": ["YYC"],
    "ottawa": ["YOW"],
    "mexico city": ["MEX"],
    "mexico": ["MEX"],
    "cancun": ["CUN"],
    "guadalajara": ["GDL"],
    "monterrey": ["MTY"],

    # ── CENTRAL & SOUTH AMERICA ─────────────────────────────────────────────
    "sao paulo": ["GRU", "CGH"],
    "brazil": ["GRU"],
    "rio de janeiro": ["GIG", "SDU"],
    "rio": ["GIG"],
    "brasilia": ["BSB"],
    "buenos aires": ["EZE", "AEP"],
    "argentina": ["EZE"],
    "bogota": ["BOG"],
    "colombia": ["BOG"],
    "lima": ["LIM"],
    "peru": ["LIM"],
    "santiago": ["SCL"],
    "chile": ["SCL"],
    "caracas": ["CCS"],
    "venezuela": ["CCS"],
    "quito": ["UIO"],
    "ecuador": ["UIO"],
    "la paz": ["LPB"],
    "bolivia": ["LPB"],
    "panama city": ["PTY"],
    "panama": ["PTY"],
    "san jose": ["SJO"],
    "costa rica": ["SJO"],
    "havana": ["HAV"],
    "cuba": ["HAV"],
    "kingston": ["KIN"],
    "jamaica": ["KIN"],

    # ── OCEANIA ─────────────────────────────────────────────────────────────
    "sydney": ["SYD"],
    "australia": ["SYD"],
    "melbourne": ["MEL"],
    "brisbane": ["BNE"],
    "perth": ["PER"],
    "adelaide": ["ADL"],
    "gold coast": ["OOL"],
    "cairns": ["CNS"],
    "auckland": ["AKL"],
    "new zealand": ["AKL"],
    "christchurch": ["CHC"],
    "wellington": ["WLG"],
    "fiji": ["NAN"],
    "nadi": ["NAN"],
    "honolulu": ["HNL"],
    "hawaii": ["HNL"],
    "port moresby": ["POM"],
    "papua new guinea": ["POM"],

    # ── CENTRAL ASIA ────────────────────────────────────────────────────────
    "tashkent": ["TAS"],
    "uzbekistan": ["TAS"],
    "samarkand": ["SKD"],
    "almaty": ["ALA"],
    "astana": ["NQZ"],
    "nur-sultan": ["NQZ"],
    "kazakhstan": ["NQZ"],
    "baku": ["GYD"],
    "azerbaijan": ["GYD"],
    "tbilisi": ["TBS"],
    "georgia": ["TBS"],
    "yerevan": ["EVN"],
    "armenia": ["EVN"],
}


def _city_to_iata_codes(city: str) -> list[str]:
    """Return IATA codes for a city name.

    Tries an exact lower-case match first, then falls back to a substring
    search so that partial names like "new york city" → "new york" still work.
    """
    key = city.lower().strip()
    # 1. Exact match
    if key in CITY_TO_IATA_CODES:
        return CITY_TO_IATA_CODES[key]
    # 2. Substring: city name is contained in a known key  (e.g. "bombay, india" → "bombay")
    for known_key, codes in CITY_TO_IATA_CODES.items():
        if known_key in key or key in known_key:
            return codes
    return []


def _format_datetime(value: str | None) -> str:
    if not value:
        return "time not available"

    return value.replace("T", " ").split("+")[0]


def _safe_int(value: str) -> int | None:
    cleaned = value.replace(",", "").strip()
    if not cleaned:
        return None
    try:
        return int(cleaned)
    except ValueError:
        return None


def _extract_price_in_inr(content: str) -> int | None:
    rupee_match = re.search(r"(?:₹|Rs\.?|INR)\s?(\d[\d,]*)", content, re.IGNORECASE)
    if rupee_match:
        return _safe_int(rupee_match.group(1))

    dollar_match = re.search(r"\$\s?(\d[\d,]*)", content)
    if dollar_match:
        v = _safe_int(dollar_match.group(1))
        return v * USD_TO_INR_ESTIMATE if v is not None else None

    return None


def _normalize_flight(raw_flight: dict, route: str, searched_route: str) -> dict:
    airline = raw_flight.get("airline") or {}
    flight = raw_flight.get("flight") or {}
    departure = raw_flight.get("departure") or {}
    arrival = raw_flight.get("arrival") or {}

    return {
        "airline": airline.get("name") or "Unknown airline",
        "flight_number": flight.get("iata") or flight.get("number") or "Unknown flight",
        "route": route,
        "departure_airport": departure.get("airport") or "Unknown departure airport",
        "arrival_airport": arrival.get("airport") or "Unknown arrival airport",
        "departure_time": _format_datetime(departure.get("scheduled")),
        "arrival_time": _format_datetime(arrival.get("scheduled")),
        "status": raw_flight.get("flight_status") or "unknown",
        "price": None,
        "source": "AviationStack",
        "searched_route": searched_route,
    }


def _fetch_flights_for_route(
    api_key: str,
    dep_iata: str,
    arr_iata: str,
    route: str,
) -> list[dict]:
    log.info(f"AviationStack request: {dep_iata} → {arr_iata}")
    response = requests.get(
        AVIATIONSTACK_FLIGHTS_URL,
        params={
            "access_key": api_key,
            "dep_iata": dep_iata,
            "arr_iata": arr_iata,
            "limit": 5,
        },
        timeout=20,
    )
    response.raise_for_status()

    flights = response.json().get("data", [])
    searched_route = f"{dep_iata} -> {arr_iata}"
    log.info(f"AviationStack returned {len(flights)} flight(s) for {dep_iata} → {arr_iata}")

    return [
        _normalize_flight(raw_flight, route, searched_route)
        for raw_flight in flights
    ]


# ── Domains to BLOCK from fare estimates ──────────────────────────────────────
# Airline direct websites show artificially low "starting from" teaser prices
# to attract search-engine crawlers.  The real checkout price is typically
# 2–3× higher.  We only trust aggregators that display verified live fares.
_BLOCKED_FARE_DOMAINS: set[str] = {
    # Major international carriers — direct booking sites
    "airfrance.in", "airfrance.com", "airfrance.co.in",
    "airfranceklm.com",
    "lufthansa.com", "lufthansa.in",
    "emirates.com", "emirates.in",
    "etihad.com", "etihad.in",
    "qatarairways.com",
    "britishairways.com",
    "singaporeair.com",
    "cathaypacific.com",
    "turkishairlines.com",
    "klm.com",
    "swiss.com",
    "austrian.com",
    "finnair.com",
    "saudia.com",
    "etihadairways.com",
    "flydubai.com",
    "airnewzealand.com",
    "qantas.com",
    # Indian carriers — direct booking sites
    "airindia.in", "airindia.com",
    "spicejet.com",
    "goindigo.in", "indigo.in",
    "goair.in",
    "akasaair.com",
    "vistara.com",
    "starair.in",
    "allianceair.in",
    "bluedart.com",
}

# ── Trusted aggregators — verified real fares ──────────────────────────────────
# These sites scrape multiple carriers and show actual bookable prices.
_TRUSTED_FARE_SOURCES: list[str] = [
    "site:makemytrip.com OR site:goibibo.com OR site:cleartrip.com "
    "OR site:ixigo.com OR site:skyscanner.co.in OR site:skyscanner.net "
    "OR site:kayak.com OR site:google.com/travel OR site:easemytrip.com "
    "OR site:yatra.com",
]


def _is_blocked_domain(url: str) -> bool:
    """Return True if the URL belongs to a known bait-price airline direct site."""
    url_lower = url.lower()
    return any(domain in url_lower for domain in _BLOCKED_FARE_DOMAINS)


def _search_flight_fare_estimates(parsed_request: dict, route: str) -> list[dict]:
    api_key     = get_required_env("TAVILY_API_KEY")
    origin      = parsed_request["origin"]
    destination = parsed_request["destination_city"]
    trip_days   = parsed_request["trip_days"]
    budget      = parsed_request["budget_in_inr"]

    # Target aggregators explicitly so Tavily ranks them over airline direct pages.
    query = (
        f"{origin} to {destination} cheapest flight price INR economy "
        f"{trip_days} days site:makemytrip.com OR site:goibibo.com "
        f"OR site:cleartrip.com OR site:ixigo.com OR site:skyscanner.co.in "
        f"OR site:kayak.com OR site:easemytrip.com OR site:yatra.com"
    )
    log.info(f"Tavily fare-estimate search (aggregators only): {origin} → {destination}")
    log.debug(f"Fare query: '{query[:120]}'")

    response = requests.post(
        TAVILY_SEARCH_URL,
        json={
            "api_key": api_key,
            "query": query,
            "search_depth": "advanced",
            "max_results": 8,
        },
        timeout=20,
    )
    response.raise_for_status()

    raw_results = response.json().get("results", [])
    log.info(f"Tavily returned {len(raw_results)} raw fare result(s)")

    # Filter out airline direct / bait-price domains.
    results = [r for r in raw_results if not _is_blocked_domain(r.get("url", ""))]
    blocked_count = len(raw_results) - len(results)
    if blocked_count:
        log.warning(
            f"Dropped {blocked_count} result(s) from airline direct sites "
            f"(bait prices) — keeping {len(results)} aggregator result(s)"
        )

    if not results:
        # Fallback: broad search without site filter but still block direct sites.
        log.info("No aggregator results — retrying with broader fare search")
        fallback_query = (
            f"cheapest flight {origin} to {destination} price INR economy "
            f"flight booking aggregator compare fares"
        )
        response2 = requests.post(
            TAVILY_SEARCH_URL,
            json={
                "api_key": api_key,
                "query": fallback_query,
                "search_depth": "basic",
                "max_results": 6,
            },
            timeout=20,
        )
        response2.raise_for_status()
        all_fallback = response2.json().get("results", [])
        results = [r for r in all_fallback if not _is_blocked_domain(r.get("url", ""))]
        log.info(f"Fallback search returned {len(results)} non-blocked result(s)")

    estimates = []
    for result in results:
        price = _extract_price_in_inr(result.get("content", ""))
        estimates.append({
            "airline": result.get("title", "Flight fare estimate"),
            "flight_number": "fare estimate",
            "route": route,
            "departure_airport": origin,
            "arrival_airport": destination,
            "departure_time": "check booking site",
            "arrival_time": "check booking site",
            "status": "aggregator fare estimate — verify at checkout",
            "price": price,
            "price_source": "aggregator",
            "source": "Tavily",
            "searched_route": "Tavily aggregator search",
            "url": result.get("url", ""),
            "snippet": result.get("content", ""),
        })

    priced = [e for e in estimates if e["price"] is not None]
    log.info(f"Fare estimates with price: {len(priced)}/{len(estimates)}")
    return estimates


def search_flights(user_query: str, parsed_request: dict) -> list[dict]:
    origin         = parsed_request["origin"]
    destination    = parsed_request["destination_city"]
    dep_iata_codes = _city_to_iata_codes(origin)
    arr_iata_codes = _city_to_iata_codes(destination)
    route          = f"{origin} to {destination}"

    log.info(f"Flight search — {route}")
    log.info(f"IATA codes — dep: {dep_iata_codes or 'NOT FOUND'}  arr: {arr_iata_codes or 'NOT FOUND'}")

    flight_options: list[dict] = []

    if dep_iata_codes and arr_iata_codes:
        try:
            api_key = get_required_env("AVIATIONSTACK_API_KEY")
            for dep_iata in dep_iata_codes:
                for arr_iata in arr_iata_codes:
                    flight_options.extend(
                        _fetch_flights_for_route(api_key, dep_iata, arr_iata, route)
                    )
            log.info(f"AviationStack total: {len(flight_options)} flight(s) across all IATA pairs")
        except Exception as exc:
            log.warning(f"AviationStack call failed ({exc}) — will fall back to Tavily fare estimates")
            flight_options = []
    else:
        missing = []
        if not dep_iata_codes: missing.append(f"origin '{origin}'")
        if not arr_iata_codes: missing.append(f"destination '{destination}'")
        log.warning(f"No IATA codes for {' and '.join(missing)} — skipping AviationStack, using Tavily only")

    priced_flights = [f for f in flight_options if f.get("price") is not None]

    if priced_flights:
        log.info(f"Using {len(priced_flights)} priced AviationStack flight(s)")
        return priced_flights[:5]

    log.info("No priced flights from AviationStack — fetching Tavily fare estimates")
    try:
        fare_estimates = _search_flight_fare_estimates(parsed_request, route)
    except Exception as exc:
        log.error(f"Tavily fare estimate also failed — {exc}")
        fare_estimates = []

    if flight_options:
        combined = flight_options[:3] + fare_estimates[:2]
        log.info(f"Returning {len(combined)} results (AviationStack schedule + Tavily prices)")
        return combined

    log.info(f"Returning {len(fare_estimates[:5])} Tavily fare estimate(s)")
    return fare_estimates[:5]