"""State class tests."""
import unittest

import pygame

from src.game import state


class TestState(unittest.TestCase):
    def setUp(self) -> None:
        self.state = state.State()

    def test_reset(self):
        self.state.reset()
        self.assertEqual(self.state.answers, [[0 for j in range(4)] for i in range(12)])
        self.assertEqual(self.state.feedback, [[] for i in range(12)])
        self.assertEqual(self.state.active_indices, [1, 0, 0, 0])
        self.assertEqual(self.state.current_row, len(self.state.answers) - 1)
        self.assertEqual(self.state.input_enabled, True)

    def test_get_active_index(self):
        self.assertEqual(self.state.get_active_index(), 0)

    def test_change_active_index(self):
        self.state.change_active_index()
        self.assertEqual(self.state.get_active_index(), 1)
        self.state.change_active_index()
        self.assertEqual(self.state.get_active_index(), 2)
        self.state.change_active_index()
        self.assertEqual(self.state.get_active_index(), 3)
        self.state.change_active_index()
        self.assertEqual(self.state.get_active_index(), 0)

    def test_get_feedback(self):
        self.assertEqual(self.state.get_feedback(0), [])

    def test_append_feedback_digit(self):
        self.state.append_feedback_digit(5)
        self.assertEqual(self.state.get_feedback_digit(self.state.current_row, 0), 5)

    def test_get_answer(self):
        self.assertEqual(self.state.get_answer(self.state.current_row), [0, 0, 0, 0])

    def test_get_answer_digit(self):
        self.assertEqual(self.state.get_answer_digit(self.state.current_row, 0), 0)

    def test_set_answer_digit(self):
        self.state.set_answer_digit(6, self.state.current_row, 3)
        self.assertEqual(self.state.get_answer_digit(self.state.current_row, 3), 6)

    def test_disable_input(self):
        self.state.disable_input()
        self.assertFalse(self.state.input_enabled)


if __name__ == '__main__':
    pygame.init()
    unittest.main()
