import pygame, glm
from OpenGL.GL import *
from OpenGL.GLU import *
from bootstrap import events, run
from utils import load_texture, ObjectFactory
import shaders
import vertex_data
import text
# @TODO replace it with static colors later on
import random

factory = ObjectFactory()

factory \
    .set_vertices(vertex_data.get_vertices('sphere')) \
    .set_indices(vertex_data.get_indices('sphere')) \
    .set_stride(3 * sizeof(GLfloat)) \
    .set_attrib_pointer(index=0, size=3, type=GL_FLOAT, normalized=GL_FALSE, offset=0)
sphere = factory.create()

factory \
    .set_vertices(vertex_data.get_vertices('plane')) \
    .set_stride(5 * sizeof(GLfloat)) \
    .set_attrib_pointer(index=0, size=3, type=GL_FLOAT, normalized=GL_FALSE, offset=0) \
    .set_attrib_pointer(index=1, size=2, type=GL_FLOAT, normalized=GL_FALSE, offset=3)
plane = factory.create()

sphere_shader = shaders.Shader('shaders/sphere.vert', 'shaders/sphere.frag')

# combination = [random.randint(1, 6) for i in range(4)]
combination = [1, 2, 3, 4]
answers = [[0 for j in range(4)] for i in range(12)]
feedback = [[] for i in range(12)]
selected = [1 if i == 0 else 0 for i in range(4)]
current_row = len(answers) - 1

print('combination:', combination)

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
    if answers[row][col]:
        return colors[answers[row][col] - 1]

    return active_color if is_selected else inactive_color


def get_feedback_color(row, col):
    color = None
    if feedback[row][col] == 1:
        color = glm.vec3(1.0, 0.0, 0.0)
    elif feedback[row][col] == 2:
        color = glm.vec3(1.0, 1.0, 1.0)

    return color


def draw_spheres(event):
    sphere_shader.use()

    sphere_shader.set_mat4('view', event.view)
    sphere_shader.set_mat4('projection', event.projection)

    glBindVertexArray(sphere.vao)

    x_start, z_start = 0, 0
    offset = 2.5
    feedback_offset = offset / 3

    for row in range(12):
        x1 = x_start + 10
        x2 = x1 + feedback_offset
        z1 = z_start - feedback_offset / 2 + row * offset
        z2 = z1 + feedback_offset

        for index, feedback_pos in enumerate([(x1, z1), (x2, z1), (x1, z2), (x2, z2)]):
            if len(feedback[row]) < index + 1 or feedback[row][index] == 0:
                continue

            feedback_x, feedback_z = feedback_pos
            model = glm.translate(glm.mat4(1.0), glm.vec3(feedback_x, 0.0, feedback_z))
            sphere_shader.set_mat4('model', glm.scale(model, glm.vec3(0.25, 0.25, 0.25)))
            sphere_shader.set_vec3('aColor', get_feedback_color(row, index))
            glDrawElements(GL_TRIANGLES, vertex_data.get_indices_count('sphere'), GL_UNSIGNED_INT, None)

    for row in range(12):
        for col in range(4):
            is_selected = row == current_row and col == selected.index(1)
            color = get_color(row, col, is_selected)

            model = glm.translate(glm.mat4(1.0), glm.vec3(x_start + col * offset, 0.0, z_start + row * offset))
            sphere_shader.set_mat4('model', model)
            sphere_shader.set_vec3('aColor', color)

            if is_selected: glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glDrawElements(GL_TRIANGLES, vertex_data.get_indices_count('sphere'), GL_UNSIGNED_INT, None)
            if is_selected: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


events.on(events.DRAW, draw_spheres)

texts = [
    'W, S, A, D - ruch kamerą',
    'SCROLL UP / SCROLL DOWN - przybliżenie / oddalenie',
    '1, 2, 3, 4, 5, 6 - wybór wartości dla danej komórki',
    'SPACJA - zmiana aktywnej komórki',
    'ENTER - sprawdzenie wartości z danego wiersza'
]

print(texts)

text_object_factory = lambda text_to_draw, position: text.Text(text_to_draw, position=position, font_size=35,
                                                               font_color=(1.0, 1.0, 0.0, 1.0))
text_objects = []
for index, text_to_draw in enumerate(texts):
    text_object = text_object_factory(text_to_draw, (0.0, 0.9 - 0.05 * index))
    text_objects.append(text_object)

events.on(events.DRAW, lambda event: [text_object.draw() for text_object in text_objects])


def change_active_cell(event):
    index = selected.index(1)
    next_index = 0
    selected[index] = 0
    if index + 1 < len(selected):
        next_index = index + 1
    selected[next_index] = 1


events.on(pygame.KEYDOWN, change_active_cell, conditions={'key': pygame.K_SPACE})


def change_selection(to):
    answers[current_row][selected.index(1)] = to


# bind keys 1-6 as active selection switchers
events.on(pygame.KEYDOWN, lambda event: change_selection(1), conditions={'key': pygame.K_1})
events.on(pygame.KEYDOWN, lambda event: change_selection(2), conditions={'key': pygame.K_2})
events.on(pygame.KEYDOWN, lambda event: change_selection(3), conditions={'key': pygame.K_3})
events.on(pygame.KEYDOWN, lambda event: change_selection(4), conditions={'key': pygame.K_4})
events.on(pygame.KEYDOWN, lambda event: change_selection(5), conditions={'key': pygame.K_5})
events.on(pygame.KEYDOWN, lambda event: change_selection(6), conditions={'key': pygame.K_6})


def check_row(event):
    global current_row
    if 0 in answers[current_row]:
        print('Błąd. Nie wybrano wszystkich wartości z wiersza.')
        # @TODO trigger validation error
        return

    if answers[current_row] == combination:
        print('YOU WIN. Congratulations.')
        # @TODO trigger game end event
        return

    indices_to_check = []

    for index, selection in enumerate(answers[current_row]):
        if combination[index] == selection:
            feedback[current_row].append(1)
            continue

        indices_to_check.append(index)

    combination_copy = [combination[i] for i in indices_to_check]
    print('combination_copy:', combination_copy)

    for index in indices_to_check:
        if answers[current_row][index] in combination_copy:
            feedback[current_row].append(2)

    print(feedback[current_row])

    if current_row == 0:
        print('Game over.')
        # @TODO trigger gameover event
        return

    current_row -= 1


events.on(pygame.KEYDOWN, check_row, conditions={'key': pygame.K_RETURN})

glEnable(GL_DEPTH_TEST)
# blend is used in GUI texts
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
run()
