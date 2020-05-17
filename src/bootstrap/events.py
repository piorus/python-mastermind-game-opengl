import pygame


def check_conditions(event, watched_event):
    for k in watched_event.conditions:
        if not hasattr(event, k):
            raise RuntimeError('Invalid conditions for %s: event does not have "%s"' % (watched_event.name, k))

        if getattr(event, k) != watched_event.conditions[k]:
            return False

    return True


class Subject:
    def __init__(self):
        self._watched_events = {}

    def register_event(self, event_to_watch):
        if event_to_watch.type in self._watched_events.keys():
            self._watched_events[event_to_watch.type].append(event_to_watch)
        else:
            self._watched_events[event_to_watch.type] = [event_to_watch]

    def register_events(self, events_to_watch):
        for event_to_watch in events_to_watch:
            self.register_event(event_to_watch)

    def invoke_event_callbacks(self, event):
        if event.type in self._watched_events.keys():
            for watched_event in self._watched_events[event.type]:
                if hasattr(watched_event, 'conditions') and not check_conditions(event, watched_event):
                    continue

                if watched_event.data:
                    watched_event.callback(event, watched_event.data)
                else:
                    watched_event.callback(event)

class Observer:
    def __init__(self, observable, events_to_watch):
        observable.register_events(events_to_watch)


class EventToWatch:
    def __init__(self, type, callback, name=None, conditions=None, data=None):
        self.name = name
        self.type = type
        self.callback = callback
        if conditions:
            self.conditions = conditions

        self.data = data


class Events:
    DRAW = pygame.USEREVENT
    UPDATE_CAMERA_FRONT = pygame.USEREVENT + 1

    def __init__(self):
        self.subject = Subject()

        listeners = [
            (pygame.QUIT, app_quit, 'App::pygameQuit'),
            (pygame.KEYDOWN, app_quit, 'App::escepeKeyPressed', {'key': pygame.K_ESCAPE})
        ]
        self.add_listeners(listeners)

    def process(self, events):
        for event in events:
            self.subject.invoke_event_callbacks(event)

    def add_listeners(self, listeners):
        for listener in listeners:
            self.on(*listener)

    def on(self, type, callback, name=None, conditions=None, data=None):
        self.subject.register_event(EventToWatch(type, callback, name, conditions, data))

    def post(self, type, args):
        pygame.event.post(pygame.event.Event(type, args))


def app_quit(event):
    pygame.quit()
    quit()
