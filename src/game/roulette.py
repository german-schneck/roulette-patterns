from typing import List, Dict, Tuple
import random

class Roulette:
    def __init__(self):
        # Define the wheel numbers and their properties
        self.numbers = list(range(0, 37))  # 0-36
        self.colors = {
            0: 'green',
            32: 'red', 19: 'red', 21: 'red', 25: 'red', 34: 'red', 27: 'red',
            36: 'red', 30: 'red', 23: 'red', 5: 'red', 16: 'red', 1: 'red',
            14: 'red', 9: 'red', 18: 'red', 7: 'red', 12: 'red', 3: 'red',
            15: 'black', 4: 'black', 2: 'black', 17: 'black', 6: 'black',
            13: 'black', 11: 'black', 8: 'black', 10: 'black', 24: 'black',
            33: 'black', 20: 'black', 31: 'black', 22: 'black', 29: 'black',
            28: 'black', 35: 'black', 26: 'black'
        }
        
        # Define number properties
        self.even_numbers = [n for n in self.numbers if n != 0 and n % 2 == 0]
        self.odd_numbers = [n for n in self.numbers if n != 0 and n % 2 == 1]
        self.red_numbers = [n for n, color in self.colors.items() if color == 'red']
        self.black_numbers = [n for n, color in self.colors.items() if color == 'black']
        self.zero = 0
        
        # Define dozens
        self.first_dozen = list(range(1, 13))
        self.second_dozen = list(range(13, 25))
        self.third_dozen = list(range(25, 37))
        
        # Define columns
        self.first_column = [n for n in self.numbers if n != 0 and n % 3 == 1]
        self.second_column = [n for n in self.numbers if n != 0 and n % 3 == 2]
        self.third_column = [n for n in self.numbers if n != 0 and n % 3 == 0]
        
        # Define streets (rows)
        self.streets = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12],
            5: [13, 14, 15],
            6: [16, 17, 18],
            7: [19, 20, 21],
            8: [22, 23, 24],
            9: [25, 26, 27],
            10: [28, 29, 30],
            11: [31, 32, 33],
            12: [34, 35, 36]
        }
        
        # Define corners
        self.corners = {
            (1,2,4,5): [1, 2, 4, 5],
            (2,3,5,6): [2, 3, 5, 6],
            (4,5,7,8): [4, 5, 7, 8],
            (5,6,8,9): [5, 6, 8, 9],
            (7,8,10,11): [7, 8, 10, 11],
            (8,9,11,12): [8, 9, 11, 12],
            (10,11,13,14): [10, 11, 13, 14],
            (11,12,14,15): [11, 12, 14, 15],
            (13,14,16,17): [13, 14, 16, 17],
            (14,15,17,18): [14, 15, 17, 18],
            (16,17,19,20): [16, 17, 19, 20],
            (17,18,20,21): [17, 18, 20, 21],
            (19,20,22,23): [19, 20, 22, 23],
            (20,21,23,24): [20, 21, 23, 24],
            (22,23,25,26): [22, 23, 25, 26],
            (23,24,26,27): [23, 24, 26, 27],
            (25,26,28,29): [25, 26, 28, 29],
            (26,27,29,30): [26, 27, 29, 30],
            (28,29,31,32): [28, 29, 31, 32],
            (29,30,32,33): [29, 30, 32, 33],
            (31,32,34,35): [31, 32, 34, 35],
            (32,33,35,36): [32, 33, 35, 36]
        }

    def spin(self) -> int:
        """Simulate a spin of the roulette wheel and return the winning number."""
        return random.choice(self.numbers)

    def get_number_properties(self, number: int) -> Dict:
        """Get all properties of a given number."""
        return {
            'number': number,
            'color': self.colors[number],
            'is_even': number in self.even_numbers,
            'is_odd': number in self.odd_numbers,
            'is_zero': number == self.zero,
            'dozen': self._get_dozen(number),
            'column': self._get_column(number),
            'street': self._get_street(number)
        }

    def _get_dozen(self, number: int) -> int:
        """Get which dozen a number belongs to."""
        if number == 0:
            return 0
        return (number - 1) // 12 + 1

    def _get_column(self, number: int) -> int:
        """Get which column a number belongs to."""
        if number == 0:
            return 0
        return number % 3 or 3

    def _get_street(self, number: int) -> int:
        """Get which street (row) a number belongs to."""
        if number == 0:
            return 0
        return (number - 1) // 3 + 1 