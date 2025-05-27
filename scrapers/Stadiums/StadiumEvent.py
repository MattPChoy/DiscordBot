from datetime import datetime


class StadiumEvent:
    category: str
    date: datetime
    series: str
    startTime: datetime
    title: str
    url: str
    location: str # At this point, either Suncorp or Gabba

    @staticmethod
    def fromJson(data: dict) -> 'StadiumEvent':
        """
        Creates a StadiumEvent instance from a dictionary.

        Args:
            data: Dictionary containing event data

        Returns:
            StadiumEvent: A new instance of StadiumEvent
        """
        new = StadiumEvent()

        new.category = data['eventCategory']['title']
        new.date = datetime.strptime(data['eventDate'], '%b %d, %Y, %I:%M:%S\u202f%p')
        new.openTime = None if data['eventOpenTime']['time'] == 'TBC' else datetime.strptime(
            data['eventOpenTime']['time'], '%I:%M%p')
        new.series = data.get('eventSeries', '')
        new.startTime = None if data['eventStartTime']['time'] == 'TBC' else datetime.strptime(
            data['eventStartTime']['time'], '%I:%M%p')
        new.title = data['title']
        new.url = data['url']

        return new