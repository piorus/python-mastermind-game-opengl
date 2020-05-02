import pygame

class Keyboard:
    def __init__(self):
        self._watched_inputs = {}

    def process(self, pressed_keys):
        for key_code in self._watched_inputs.keys():
            if pressed_keys[key_code]:
                self.invoke_input_callbacks(self._watched_inputs[key_code])

    def invoke_input_callbacks(self, watched_inputs):
        for watched_input in watched_inputs:
            watched_input.callback()

    def add_listener(self, input_to_watch):
        if input_to_watch.key_code in self._watched_inputs.keys():
            self._watched_inputs[input_to_watch.key_code].append(input_to_watch)
        else:
            self._watched_inputs[input_to_watch.key_code] = [input_to_watch]

class InputToWatch:
    def __init__(self, key_code, callback, name):
        self.name = name
        self.key_code = key_code
        self.callback = callback

class Mouse:
    def __init__(self):
        self.first_time = True
        self.last_x = 0.0
        self.last_y = 0.0

        self.x_offset = 0.0
        self.y_offset = 0.0

    def on_mouse_move(self, event):
        if self.first_time:
            self.last_x, self.last_y = pygame.mouse.get_pos()
            self.first_time = False

        x_pos, y_pos = event.pos
        self.x_offset = x_pos - self.last_x
        self.y_offset = self.last_y - y_pos
        self.last_x = x_pos
        self.last_y = y_pos

class Input:
    M_SCROLL_UP = 4
    M_SCROLL_DOWN = 5
    def __init__(self, mouse, keyboard):
        self.mouse    = mouse
        self.keyboard = keyboard

    def process(self, pressed_keys):
        self.keyboard.process(pressed_keys)

    def on(self, key_code, callback, name=None):
        self.keyboard.add_listener(InputToWatch(key_code, callback, name))

    def add_listeners(self, listeners):
        for listener in listeners:
            self.on(*listener)
