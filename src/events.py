"""events module"""

import pygame


# pylint: disable=too-few-public-methods
class EventListener:
    """
    EventListener class is a container used in event handling.

    It stores callback, conditions and additional data for the given event_type.
    """

    # pylint: disable=too-many-arguments
    def __init__(self, event_type, callback, name=None, conditions=None, data=None):
        self.name = name
        self.event_type = event_type
        self.callback = callback
        if conditions:
            self.conditions = conditions

        self.data = data


def check_conditions(event, event_listener: EventListener):
    """
    Check if all conditions are met for the event listener.

    :param event:
    :param event_listener:
    :return:
    """
    for k in event_listener.conditions:
        if not hasattr(event, k):
            raise RuntimeError(
                'Invalid conditions for %s: event does not have "%s"' % (event_listener.name, k)
            )

        if getattr(event, k) != event_listener.conditions[k]:
            return False

    return True


def post(event_type, args):
    """
    Post the event of the given type with the args.

    :param event_type: type of the event
    :param args: arguments
    :return: None
    """
    pygame.event.post(pygame.event.Event(event_type, args))


class Subject:
    """
    Subject class is used to register event listeners and invoke callbacks.

    Callbacks are invoked only if conditions are met.
    """

    def __init__(self):
        self.event_listeners = {}

    def register_event_listener(self, event_listener: EventListener):
        """
        Register event listener.

        :param event_listener: event listener to register
        :return: None
        """
        if event_listener.event_type in self.event_listeners.keys():
            self.event_listeners[event_listener.event_type].append(event_listener)
        else:
            self.event_listeners[event_listener.event_type] = [event_listener]

    def invoke_event_callbacks(self, event):
        """
        Invoke all callbacks for the given event.

        Check if conditions are met (if any) and invoke callbacks
        of listeners that listen to the received event.
        Received event is passed as an callback argument.
        Optionally, there can be additional data set when registering event listener
        that is also passed when invoking a callback.

        :param event: event to check
        :return: None
        """
        if event.type in self.event_listeners.keys():
            for event_listener in self.event_listeners[event.type]:
                if hasattr(event_listener, 'conditions') \
                        and not check_conditions(event, event_listener):
                    continue

                if event_listener.data:
                    event_listener.callback(event, event_listener.data)
                else:
                    event_listener.callback(event)


class Events:
    """
    Events class that is used to handle all of the pygame events.

    List of custom events defined below:
    - Events.DRAW - executed in the each iteration of main game loop
    - Events.GAME_OVER - executed after the game is over
    - Events.GAME_WON - executed after the game is won
    - Events.GAME_RESET - executed after pressing R
    - Events.AFTER_GAME_RESET - executed after resetting the game
    - Events.CHEATER_CHECK - executed after pressing O
    - Events.SHOW_VALIDATION_ERROR - executed when validation error occurs
    - Events.HIDE_VALIDATION_ERROR - executed after 2s to hide validation error
    """
    DRAW = pygame.USEREVENT
    GAME_OVER = pygame.USEREVENT + 1
    GAME_WON = pygame.USEREVENT + 2
    GAME_RESET = pygame.USEREVENT + 3
    AFTER_GAME_RESET = pygame.USEREVENT + 4
    CHEATER_CHECK = pygame.USEREVENT + 5
    SHOW_VALIDATION_ERROR = pygame.USEREVENT + 6
    HIDE_VALIDATION_ERROR = pygame.USEREVENT + 7

    def __init__(self):
        self.subject = Subject()

    def process(self, events):
        """
        Process pygame events.

        :param events:
        :return: None
        """
        for event in events:
            self.subject.invoke_event_callbacks(event)

    # pylint: disable=invalid-name,too-many-arguments
    def on(self, event_type, callback, name=None, conditions=None, data=None):
        """
        Register event listener for the event_type.

        If event is posted by the pygame, there is a conditions check after
        which a callback is invoked with received event and data (if any) as an arguments.

        :param event_type:
        :param callback:
        :param name:
        :param conditions:
        :param data:
        :return: None
        """
        self.subject.register_event_listener(
            EventListener(event_type, callback, name, conditions, data)
        )
