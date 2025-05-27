from datetime import datetime


class SuncorpEvent:
    category: str
    date: datetime
    series: str
    startTime: datetime
    title: str
    url: str

    @staticmethod
    def fromJson(data: dict) -> 'SuncorpEvent':
        """
        Creates a SuncorpEvent instance from a dictionary.

        Args:
            data: Dictionary containing event data

        Returns:
            SuncorpEvent: A new instance of SuncorpEvent
        """
        new = SuncorpEvent()

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