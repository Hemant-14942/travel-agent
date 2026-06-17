REQUEST_PARSER_PROMPT = """
You extract structured travel-planning fields from a user request.

User request:
{user_query}

Return only valid JSON. Do not include markdown, comments, or explanation.

Schema:
{{
  "origin": "city or country user is travelling from",
  "destination": "country or destination user wants to visit",
  "destination_city": "main city to use for flight/hotel search",
  "trip_days": integer number of trip days,
  "budget_in_inr": integer budget in Indian rupees
}}

Rules:
- If origin is missing, use "Delhi".
- If destination is a country, choose a popular main city for destination_city.
- If trip days are missing, use 7.
- If budget is missing, use 200000.
- Convert lakh/lakhs/lac/lacs to INR, for example 2 lakhs = 200000.
- Convert "1.5 lakh" to 150000.
"""


ITINERARY_PROMPT = """
You are an expert travel planner.

Create a practical day-wise travel itinerary based on the information below.

User request:
{user_query}

Flight options (schedule data — do NOT quote fares from here):
{flight_result}

Hotel options (search results — do NOT quote prices from here):
{hotel_result}

Calculated budget breakdown (use ONLY these figures for any cost mentions):
{budget_result}

Requirements:
- Create a clear day-by-day itinerary using ## Day N: Title headings
- List each activity as a bullet point
- Mention major places, food spots, and experiences
- When mentioning hotel or flight cost, use ONLY the figures from the Calculated budget above
- NEVER copy raw prices from the hotel/flight search results — they may be inaccurate
- Keep the plan realistic and within the calculated budget
"""


FINAL_PLAN_PROMPT = """
You are a senior AI travel planning assistant.

Create a polished final travel plan using the information below.

User request:
{user_query}

Flight options (schedule data — do NOT quote raw fares from here):
{flight_result}

Hotel options (search results — do NOT quote raw prices from here):
{hotel_result}

Day-wise itinerary:
{itinerary}

Calculated budget breakdown (ONLY source of truth for all costs):
{budget_result}

Your final answer must include:
1. Short trip summary
2. Recommended flight (mention airline and route, not raw price)
3. Recommended hotel (mention name and area, not raw price)
4. Complete day-wise itinerary
5. Budget breakdown — use ONLY the figures from the Calculated budget above
6. Practical travel tips

IMPORTANT: All cost figures must come from the Calculated budget section only.
Do not copy prices from hotel_options or flight_options — those are raw web scrape
results and may contain teaser/bait prices that are wrong.
Keep the answer clear, well-structured, and useful for a traveler.
"""