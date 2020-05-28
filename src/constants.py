"""constants"""

import glm

COMBINATION_LENGTH = 4
NUMBER_OF_TRIES = 12
FEEDBACK_OF_CORRECT_POSITION = 1
FEEDBACK_OF_WRONG_POSITION = 2

COLOR_RED = glm.vec4(1.0, 0.0, 0.0, 1.0)
COLOR_GREEN = glm.vec4(0.0, 1.0, 0.0, 1.0)
COLOR_LIGHT_BLUE = glm.vec4(0.0, 1.0, 1.0, 1.0)
COLOR_WHITE = glm.vec4(1.0, 1.0, 1.0, 1.0)

ANSWERS_START_POS = glm.vec3(0.0, 0.0, 0.0)
ANSWERS_OFFSET = 2.5

ACTIVE_COLOR = glm.vec3(0.0, 1.0, 0.0)
INACTIVE_COLOR = glm.vec3(1.0, 1.0, 1.0)
# got colors from: https://www.random.org/colors/hex
# got normalized values from: http://doc.instantreality.org/tools/color_calculator/
SELECTION_COLORS = [
    glm.vec3(0.474, 0.847, 0.031),
    glm.vec3(0.752, 0.247, 0.627),
    glm.vec3(0.450, 0.752, 0.768),
    glm.vec3(0.172, 0.333, 0.564),
    glm.vec3(0.635, 0.274, 0.070),
    glm.vec3(1.000, 1.000, 0.000)
]
