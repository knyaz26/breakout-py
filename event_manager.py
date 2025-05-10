class EventManager:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_name, callback):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(callback)

    def unsubscribe(self, event_name, callback):
        if event_name in self._listeners:
            if callback in self._listeners[event_name]:
                self._listeners[event_name].remove(callback)
            if not self._listeners[event_name]:
                del self._listeners[event_name]

    def emit(self, event_name, *args, **kwargs):
        if event_name in self._listeners:
            for callback in list(self._listeners[event_name]):
                callback(*args, **kwargs)

event_handler = EventManager()