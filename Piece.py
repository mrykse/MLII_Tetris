from random import randrange as rand
import pygame
import sys
import numpy as np
import copy
import random
class Piece:
    def __init__(self):
        self.tetris_shapes = {
        1: 	[[1, 1, 1],
             [0, 1, 0]],

        2:	[[0, 2, 2],
             [2, 2, 0]],

        3:	[[3, 3, 0],
             [0, 3, 3]],

        4:	[[4, 0, 0],
             [4, 4, 4]],

        5:	[[0, 0, 5],
             [5, 5, 5]],

        6:	[[6, 6, 6, 6]],

        7:	[[7, 7],
             [7, 7]]
        }

        self.tetris_rotation = {
        1: 4,
        2: 2,
        3: 2,
        4: 4,
        5: 4,
        6: 2,
        7: 1
        }

        self.curr_piece = self.tetris_shapes[1]

        self.next_piece = self.tetris_shapes[1]

    def return_curr_piece_key(self):
        for item in self.curr_piece[0]:
            if item != 0:
                return item

    def rotate_right(self, shape):
        """
        Rotate clockwise / right
        """
        rot_shape = np.rot90(shape)
        return rot_shape.tolist()

    def num_places(self, shape):
        length = len(shape[0])
        return 11 - length # hard coded

pass