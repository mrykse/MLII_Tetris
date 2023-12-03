from random import randrange as rand
import pygame
import sys
import numpy as np
import copy
import random

class Board:
    def __init__(self, x_size=10, y_size=20):
        self.x_size = x_size
        self.y_size = y_size
        self.board = np.zeros((y_size, x_size), dtype=int)


    def new_board(self):
        """
        Creates new board - dictionary with arrays
        """
        board = {}
        for i in range(self.y_size):
            board[i] = [0] * self.x_size
        return board

    def remove_row(self, row):
        """
        Removes row from board
        """
        new_board = dict.copy(self.board)
        for i in range(1, row + 1):
            new_board[i] = self.board[i - 1]
        new_board[0] = [0] * self.x_size
        self.board = new_board

    def join_board(self, mat1, mat2, mat2_off):
        """
        Join two board together
        """
        matrix = self.concat_dictionary(mat1)
        off_x, off_y = mat2_off
        try:
            for cy, row in enumerate(mat2):
                for cx, val in enumerate(row):
                    new_val = (matrix[cy + off_y - 1][cx + off_x] + val) % 8
                    matrix[cy + off_y - 1][cx + off_x] = new_val
        except:
            pass

        unconcat_dict = self.unconcat_dict(matrix)
        return unconcat_dict

    def concat_dictionary(self, dictionary):
        """
        Combines the arrays in dictionary for board
        """
        return_matrix = []
        if isinstance(dictionary, dict):
            for i in range(len(dictionary.keys())):
                return_matrix.append(dictionary[i])
            return return_matrix
        return dictionary

    def unconcat_dict(self, arr):
        unconcat_dictionary = {}
        for i in range(len(arr)):
            unconcat_dictionary[i] = arr[i]
        return unconcat_dictionary

    pass