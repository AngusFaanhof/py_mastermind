import unittest
from src.game import MastermindGame
from src.states import OutOfTurnsException, InvalidGuessException

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

    def test_game_starts_with_code(self):
        """Test if the game initialises with a code"""
        self.assertIsNot([], self.game.secret_code)

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
        invalid_guess_long =  ['R', 'G', 'B', 'Y', 'G']
        invalid_guess_short = ['R', 'G', 'B']

        self.assertTrue(self.game.is_valid_guess(valid_guess))
        self.assertFalse(self.game.is_valid_guess(invalid_guess_long))
        self.assertFalse(self.game.is_valid_guess(invalid_guess_short))

    def test_is_valid_guess_for_valid_colors(self):
        """Test if a guess contains only valid colors"""
        valid_guess = ['R', 'G', 'B', 'Y']
        invalid_guess = ['R', 'G', 'B', 'X']  # X is not a valid color

        self.assertTrue(self.game.is_valid_guess(valid_guess))
        self.assertFalse(self.game.is_valid_guess(invalid_guess))

    def test_play_guess_one_turn(self):
        """Test if a valid play is counted as a turn"""
        guess = ['W', 'W', 'W', 'W']

        self.game.play_guess(guess)

        self.assertEqual(self.game.played_turns, 1)

    def test_play_guess_invalid_guess_exception(self):
        """Test if an invalid play raises the InvalidGuessException"""
        long_guess = ['W', 'W', 'W', 'W', 'W']
        short_guess = ['W', 'W', 'W']
        wrong_color_guess = ['X', 'W', 'W', 'W']

        with self.assertRaises(InvalidGuessException):
            self.game.play_guess(long_guess)
            
        with self.assertRaises(InvalidGuessException):
            self.game.play_guess(short_guess)
            
        with self.assertRaises(InvalidGuessException):
            self.game.play_guess(wrong_color_guess)

    def test_play_guess_one_invalid_turn(self):
        """Test that an invalid play is not counted as a turn"""
        long_guess = ['W', 'W', 'W', 'W', 'W']
        short_guess = ['W', 'W', 'W']
        wrong_color_guess = ['X', 'W', 'W', 'W']

        self.game.play_guess(long_guess)
        self.assertEqual(self.game.played_turns, 0)

        self.game.play_guess(short_guess)
        self.assertEqual(self.game.played_turns, 0)

        self.game.play_guess(wrong_color_guess)
        self.assertEqual(self.game.played_turns, 0)

    def test_play_guess_max_turns(self):
        """Test if play after max  turns returns OutOfTurnsException"""
        self.game.secret_code = ['R', 'B', 'B', 'Y']
        guess = ['W', 'W', 'W', 'W']

        for _ in range(self.game.max_turns):
            self.game.play_guess(guess)

        # max turns + 1 guess
        with self.assertRaises(OutOfTurnsException):
            self.game.play_guess(guess)

        