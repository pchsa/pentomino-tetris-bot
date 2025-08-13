import random
from enum import Enum

from constants import *


class Game:
    def __init__(self, seed=None):
        self.board_state = self.create_empty_board()
        self.rng = random.Random(seed)
        self.queue = self.generate()
        self.current_piece = self.queue.pop()
        self.current_rotation = 0

    def create_empty_board(self):
        return [[0] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]
    
    def drop_piece(self, x_position):
        current_y = INITIAL_Y_POSITION

        while not self.check_collision(x_position, current_y):
            current_y -= 1

        current_y += 1

        for (dx, dy) in SHAPES[self.current_piece][self.current_rotation]:
            x = x_position + dx
            y = current_y + dy

            self.board_state[y][x] = self.current_piece.value
        
    def check_colision(self, x_position, y_position):
        for (dx, dy) in SHAPES[self.current_piece][self.current_rotation]:
            x = x_position + dx
            y = y_position + dy
            if y < 0:
                return True
            
            if self.board_state[y][x] != 0:
                return True
            
        return False

    def check_lost(self):
        for y in range(BOARD_HEIGHT - 3, BOARD_HEIGHT):
            if any(self.board_state[y]):
                return True
            
        return False

    def clear_lines(self):
        lines_to_clear = []
        for y in range(BOARD_HEIGHT):
            if all(self.board_state[y]):
                lines_to_clear.append(y)

        for y in lines_to_clear:
            del self.board_state[y]
            self.board_state.append(0, [0] * BOARD_WIDTH)

        return len(lines_to_clear)

    def generate_bag(self):
        bag = [piece for piece in Pentomino]
        self.rng.shuffle(bag)
        return bag

    def get_next_piece(self, piece_queue):
        next_piece = piece_queue.pop(0)
        if len(piece_queue < 5):
            piece_queue = piece_queue + self.generate_bag()

        return next_piece


