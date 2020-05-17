import pygame, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from bootstrap import events, run
from utils import load_texture, ObjectFactory
import shaders
import vertex_data
import game.gui, game.state, game.objects3d.sphere
import random

game_state = game.state.State()

app_objects = [
    game.gui.GUI(events=events, show_gui=True)
]

sphere = game.objects3d.sphere.Sphere()

active_color = glm.vec3(0.0, 1.0, 0.0)
inactive_color = glm.vec3(1.0, 1.0, 1.0)

# got colors from: https://www.random.org/colors/hex
# got normalized values from: http://doc.instantreality.org/tools/color_calculator/
colors = [
    glm.vec3(0.474, 0.847, 0.031),
    glm.vec3(0.752, 0.247, 0.627),
    glm.vec3(0.450, 0.752, 0.768),
    glm.vec3(0.172, 0.333, 0.564),
    glm.vec3(0.635, 0.274, 0.070),
    glm.vec3(1.000, 1.000, 0.000)
]


def get_color(row, col, is_selected=False):
    if game_state.get_answer_digit(row, col):
        return colors[game_state.get_answer_digit(row, col) - 1]

    return active_color if is_selected else inactive_color


def get_feedback_color(row, col):
    color = None
    feedback_digit = game_state.get_feedback_digit(row, col)
    if feedback_digit == 1:
        color = glm.vec3(1.0, 0.0, 0.0)
    elif feedback_digit == 2:
        color = glm.vec3(1.0, 1.0, 1.0)

    return color


def draw_spheres(event):
    view = event.view
    projection = event.projection
    x_start, z_start = 0, 0
    offset = 2.5
    feedback_offset = offset / 3

    for row in range(12):
        x1 = x_start + 10
        x2 = x1 + feedback_offset
        z1 = z_start - feedback_offset / 2 + row * offset
        z2 = z1 + feedback_offset

        for index, feedback_pos in enumerate([(x1, z1), (x2, z1), (x1, z2), (x2, z2)]):
            if len(game_state.get_feedback(row)) < index + 1 or game_state.get_feedback_digit(row, index) == 0:
                continue

            feedback_x, feedback_z = feedback_pos
            model = glm.translate(glm.mat4(1.0), glm.vec3(feedback_x, 0.0, feedback_z))
            sphere.draw(model, view, projection, get_feedback_color(row, index), scale=glm.vec3(0.25, 0.25, 0.25))

        for col in range(4):
            is_selected = row == game_state.get_current_row() and col == game_state.get_selected_index()
            color = get_color(row, col, is_selected)
            model = glm.translate(glm.mat4(1.0), glm.vec3(x_start + col * offset, 0.0, z_start + row * offset))
            sphere.draw(model, view, projection, color, show_wireframe=is_selected)


events.on(events.DRAW, draw_spheres)

events.on(pygame.KEYDOWN, lambda event: game_state.change_selected_index(), conditions={'key': pygame.K_SPACE})

# bind keys 1-6 as active selection switchers
keys_to_bind = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
for index, key in enumerate(keys_to_bind):
    events.on(
        pygame.KEYDOWN,
        lambda event, data: game_state.set_answer_digit(data['digit']),
        conditions={'key': key},
        data={'digit': index + 1}
    )


def check_row(event):
    global game_state
    current_row = game_state.get_current_row()
    answer = game_state.get_answer(current_row)
    if 0 in answer:
        print('Błąd. Nie wybrano wszystkich wartości z wiersza.')
        # @TODO trigger validation error
        return

    if answer == game_state.get_combination():
        print('YOU WIN. Congratulations.')
        # @TODO trigger game end event
        return

    indices_to_check = []
    combination = game_state.get_combination()

    for index, selection in enumerate(answer):
        if combination[index] == selection:
            game_state.append_feedback_digit(1)
            continue

        indices_to_check.append(index)

    combination_copy = [combination[i] for i in indices_to_check]

    for index in indices_to_check:
        if answer[index] in combination_copy:
            game_state.append_feedback_digit(2)

    if current_row == 0:
        print('Game over.')
        # @TODO trigger gameover event
        return

    game_state.decrement_current_row()


events.on(pygame.KEYDOWN, check_row, conditions={'key': pygame.K_RETURN})

glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)  # blend is used in GUI texts
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
run()
