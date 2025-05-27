import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from itertools import chain

from scrapers.Stadiums.StadiumEvent import StadiumEvent

SUNCORP_URL = "https://suncorpstadium.com.au/whats-on"
GABBA_URL = "https://thegabba.com.au/whats-on"


def _scrape_events(url: str, location: str) -> list[StadiumEvent]:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    eventlist = soup.find("event-list").get(":items")
    data = json.loads(eventlist)
    events = [StadiumEvent.fromJson(event) for event in data]
    for event in events:
        event.location = location
    return events


def _get_suncorp_events() -> list[StadiumEvent]:
    return _scrape_events(SUNCORP_URL, "Suncorp")


def _get_gabba_events() -> list[StadiumEvent]:
    return _scrape_events(GABBA_URL, "Gabba")


def get_events(days=1) -> list[StadiumEvent]:
    """
    Retrieves Stadiums events occurring within a specified number of days from today.

    Args:
        days (int): Number of days ahead to look for events. Defaults to 1.

    Returns:
        list: A list of SuncorpEvent objects that occur between today and the specified number of days ahead.
    """
    events = chain(_get_suncorp_events(), _get_gabba_events())
    # Use combine to get today's midnight (today's date and time from datetime.min)
    start_date = datetime.combine(datetime.today(), datetime.min.time()).date()
    filtered_events = [event for event in events if
                       start_date <= event.date.date() <= (start_date + timedelta(days=days-1))]
    return sorted(filtered_events, key=lambda event: event.date)
