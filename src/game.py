import random

class MastermindGame:
    def __init__(self):
        self.code_length = 4
        self.colors = ['R', 'G', 'B', 'Y', 'W', 'O']
        self.secret_code = []
        self.max_turns = 10

    def generate_code(self):
        code = []

        for _ in range(4):
            code.append(random.choice(self.colors))

        return code
        
    def evaluate_guess(self, guess):
        perfect_matches = 0
        color_matches = 0

        for i, color in enumerate(guess):
            if self.secret_code[i] == color:
                perfect_matches += 1

            elif color in self.secret_code:
                color_matches += 1
            
        return (perfect_matches, color_matches)

    def is_valid_guess(self, guess):
        if len(guess) != self.code_length:
            return False
        
        for color in guess:
            if color not in self.colors:
                return False

        return True