import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from scrapers.Suncorp.SuncorpEvent import SuncorpEvent


def _get_suncorp_events():
    url = "https://suncorpstadium.com.au/whats-on"
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')

    eventlist = soup.find("event-list").get(
        ":items")  # Get the value of prop 'items' in element <event-list> in the DOM
    data = json.loads(eventlist)

    return [SuncorpEvent.fromJson(event) for event in data]


def get_suncorp_events(days=1) -> list[SuncorpEvent]:
    """
    Retrieves Suncorp events occurring within a specified number of days from today.

    Args:
        days (int): Number of days ahead to look for events. Defaults to 1.

    Returns:
        list: A list of SuncorpEvent objects that occur between today and the specified number of days ahead.
    """
    events = _get_suncorp_events()
    return [event for event in events if datetime.now().date() <= event.date.date() <= (datetime.now().date() + timedelta(days=days))]
