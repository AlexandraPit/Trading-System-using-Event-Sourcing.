from events import Event


class EventStore:
    def __init__(self):
        self._events = []

    def append(self, event: Event):
        self._events.append(event)

    def get_all_events(self):
        return list(self._events)
