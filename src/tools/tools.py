from langchain_community.utilities import WikipediaAPIWrapper
from langchain.agents.tools import tool
from langchain_community.tools import WikipediaQueryRun, BraveSearch
from langchain_community.document_loaders import WebBaseLoader
import json
import requests
from typing import List 
import os
from dotenv import load_dotenv
load_dotenv()
os.environ['BRAVE_API_KEY'] = os.getenv("BRAVE_API_KEY")



@tool
def brave_search(question: str) -> List[str]:
    """
    Perform a web search using Brave Search and return content from the top result pages.

    This tool fetches live data from the internet using the Brave Search engine. It extracts
    links from the search results for a given query, loads the content from those pages,
    and returns the cleaned text content for further processing.

    Args:
        question (str): A search query string (e.g., "famous attractions in Kerala").

    Returns:
        List[str]: A list of cleaned text content extracted from the top web pages returned by the search.
    """
    brave = BraveSearch(description="To search over internet about anything")
    # MODIFICATION: Use the 'question' argument dynamically
    res = brave.run(question).lstrip()

    urls = [result['link'] for result in json.loads(res)]


    docs = WebBaseLoader(web_paths=urls).load()
    text = [doc.page_content.replace('\\n',"").strip() for doc in docs]

    return text


def get_coordinates(city: str):
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
    response = requests.get(geo_url).json()
    if "results" not in response or len(response["results"]) == 0:
        return None, None
    loc = response["results"][0]
    return loc["latitude"], loc["longitude"]

@tool
def get_weekly_weather(city: str, start_date: str, end_date: str) -> str:
    """
    Retrieve a daily weather forecast summary for a specific city over a given date range.

    This tool fetches the 7-day weather forecast using the Open-Meteo API. It includes:
    - Minimum and maximum temperatures
    - Daily precipitation
    - Date-wise summary for the specified period

    Steps performed:
    1. Geocodes the city name into latitude and longitude using Open-Meteo Geocoding API.
    2. Calls the Open-Meteo Forecast API with daily weather parameters.
    3. Formats the response into a human-readable forecast report.

    Args:
        city (str): Name of the city to retrieve the weather for.
        start_date (str): Start date of the forecast in 'YYYY-MM-DD' format.
        end_date (str): End date of the forecast in 'YYYY-MM-DD' format.

    Returns:
        str: A formatted weather report or an error message if data is unavailable.
    """

    print("\n ------------Getting Weather Forecast------------------- \n")

    # Step 1: Get latitude and longitude
    lat, lon = get_coordinates(city)
    if lat is None or lon is None:
        weather_forecast = f"❌ Could not find location: {city}"
        return weather_forecast

    # Step 2: Call Open-Meteo API with date range
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}"
        f"&daily=temperature_2m_min,temperature_2m_max,precipitation_sum,weathercode"
        f"&timezone=auto"
    )
    res = requests.get(url).json()

    # Step 3: Build forecast output
    if "daily" not in res:
        weather_forecast  = f"❌ Weather forecast not available for {city}."
        return weather_forecast

    daily = res["daily"]
    forecast = f"📍 Weather Forecast for {city.title()} ({start_date} to {end_date}):\n"
    for i in range(len(daily["time"])):
        date = daily["time"][i]
        tmin = daily["temperature_2m_min"][i]
        tmax = daily["temperature_2m_max"][i]
        rain = daily["precipitation_sum"][i]
        forecast += f"{date}: 🌡️ {tmin}°C – {tmax}°C, 🌧️ {rain}mm\n"


    return forecast


wiki_wrapper = WikipediaAPIWrapper()
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_wrapper)

tools = [brave_search, wiki_tool, get_weekly_weather]