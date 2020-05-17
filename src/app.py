import glm
import pygame
from OpenGL.GL import *

import game.gui
import game.logic
import game.model.feedback
import game.model.answer
import game.objects3d.sphere
import game.scene
import game.state
from bootstrap import events, run

game_state = game.state.State()

app_objects = [
    game.logic.Logic(events=events, state=game_state),
    game.gui.GUI(events=events, show_gui=True)
]

sphere = game.objects3d.sphere.Sphere()

scene_children = []
answers_offset = 2.5
start_pos = glm.vec3(0.0, 0.0, 0.0)

for row in range(12):
    feedback = game.model.feedback.Feedback(row, start_pos, answers_offset, game_state, sphere)
    scene_children.append(feedback)
    answer = game.model.answer.Answer(row, start_pos, answers_offset, game_state, sphere)
    scene_children.append(answer)

scene = game.scene.Scene(events=events, state=game_state, children=scene_children)

# bind spacebar as active selection switcher
events.on(pygame.KEYDOWN, lambda event: game_state.change_selected_index(), conditions={'key': pygame.K_SPACE})

# bind keys 1-6 as selection changers
keys_to_bind = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6]
for index, key in enumerate(keys_to_bind):
    events.on(
        pygame.KEYDOWN,
        lambda event, data: game_state.set_answer_digit(data['digit']),
        conditions={'key': key},
        data={'digit': index + 1}
    )

glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)  # blend is used in GUI texts
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
run()
