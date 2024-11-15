import unittest
from src.game import MastermindGame

class TestMastermind(unittest.TestCase):
    def setUp(self):
        self.game = MastermindGame()

    ## generate_code

    def test_generate_code_length(self):
        """Test if the generated code has correct length"""
        code = self.game.generate_code()

        self.assertEqual(len(code), self.game.code_length)

    def test_generate_code_colors(self):
        """Test if the generated code contains only valid colors"""
        code = self.game.generate_code()
        
        for color in code:
            self.assertIn(color, self.game.colors)

    ## evalute_guess

    # > perfect match
    def test_evaluate_guess_perfect_match(self):
        """Test if a perfect guess returns correct score"""
        self.game.secret_code = ['R', 'G', 'B', 'Y']
        result = self.game.evaluate_guess(['R', 'G', 'B', 'Y'])

        self.assertEqual(result, (4, 0)) # (perfect match, color match)

    def test_evaluate_guess_single_perfect_match(self):
        """Test if a single perfect match returns the correct score"""
        self.game.secret_code = ['R', 'G', 'B', 'Y']
        result = self.game.evaluate_guess(['R', 'W', 'W', 'W'])

        self.assertEqual(result, (1, 0))

    # > color_match
    def test_evaluate_guess_single_color_match(self):
        """Test if a single color match returns the correct score"""
        self.game.secret_code = ['R', 'G', 'B', 'Y']
        result = self.game.evaluate_guess(['W', 'W', 'W', 'R'])

        self.assertEqual(result, (0, 1))

    def test_evaluate_guess_two_colors_match(self):
        """Test if a two color matches returns the correct score"""
        self.game.secret_code = ['R', 'G', 'B', 'Y']
        result = self.game.evaluate_guess(['W', 'W', 'G', 'R'])

        self.assertEqual(result, (0, 2))

    def test_evaluate_guess_three_color_match(self):
        """Test if a three color matches returns the correct score"""
        self.game.secret_code = ['R', 'G', 'B', 'Y']
        result = self.game.evaluate_guess(['B', 'W', 'G', 'R'])

        self.assertEqual(result, (0, 3))

    def test_evaluate_guess_two_duplicate_colors_match(self):
        """Test if a two color matches returns the correct score"""
        self.game.secret_code = ['R', 'B', 'B', 'Y']
        result = self.game.evaluate_guess(['B', 'W', 'G', 'B'])

        self.assertEqual(result, (0, 2))

    # > mix
    def test_evaluate_guess_single_perfect_match(self):
        """Test if a one perfect match and one color match returns the correct score"""
        self.game.secret_code = ['R', 'B', 'B', 'Y']
        result = self.game.evaluate_guess(['R', 'W', 'G', 'B'])

        self.assertEqual(result, (1, 1))

    ## is_valid_guess
    def test_is_valid_guess_for_correct_length(self):
        """"Test if a guess has the correct length"""
        valid_guess = ['R', 'G', 'B', 'Y']
        invalid_guess = ['R', 'G', 'B', 'Y', 'G']

        self.assertTrue(self.game.is_valid_guess(valid_guess))
        self.assertFalse(self.game.is_valid_guess(invalid_guess))

    def test_is_valid_guess_for_valid_colors(self):
        """Test if a guess contains only valid colors"""
        valid_guess = ['R', 'G', 'B', 'Y']
        invalid_guess = ['R', 'G', 'B', 'X']  # X is not a valid color

        self.assertTrue(self.game.is_valid_guess(valid_guess))
        self.assertFalse(self.game.is_valid_guess(invalid_guess))
