import pygame
import sys
import numpy as np
import copy
from Board import Board
from Piece import Piece

cell_size = 30
maxfps = 50

colors = [
    (0, 0, 0),
    (220, 0, 20),
    (60, 165, 50),
    (100, 100, 255),
    (255, 90, 0),
    (255, 200, 40),
    (160, 50, 210),
    (70, 230, 210),
    (35, 35, 35)
]

class Game:

    def __init__(self):
        # Initialize classes
        self.board_class = Board()
        self.pieces = Piece()
        # Initialize game variables
        self.score = 0
        # Initialize PyGame
        pygame.init()
        pygame.key.set_repeat(250, 25)
        # Initialize front-end board settings
        self.width = cell_size * (self.board_class.x_size + 6)
        self.height = cell_size * self.board_class.y_size
        self.rlim = cell_size * self.board_class.x_size
        self.bground_grid = [
            [8 if x % 2 == y % 2 else 0 for x in range(self.board_class.x_size)] for y in range(self.board_class.y_size)
            ]
        self.default_font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.event.set_blocked(pygame.MOUSEMOTION)
        self.pieces.next_piece = self.pieces.tetris_shapes[ np.random.choice(np.arange(1, 8), p=[0.12, 0.12, 0.12, 0.12, 0.12, 0.2, 0.2]) ]
        self.new_stone()


    def disp_msg(self, msg, topleft):
        """ Front-end: Displays message """
        x, y= topleft
        for line in msg.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    False,
                    (255, 255, 255),
                    (0, 0, 0)),
                (x, y))
            y += 14


    def center_msg(self, msg):
        """ Front-end: Displays message in center """
        for i, line in enumerate(msg.splitlines()):
            msg_image=self.default_font.render(line, False,
                (255, 255, 255), (0, 0, 0))

            msgim_center_x, msgim_center_y=msg_image.get_size()
            msgim_center_x //= 2
            msgim_center_y //= 2

            self.screen.blit(msg_image, (
              self.width // 2 - msgim_center_x,
              self.height // 2 - msgim_center_y + i * 22))


    def draw_matrix(self, board, offset):
        """ Front-end: Draws the matrix """
        off_x, off_y = offset
        matrix = self.concat_dictionary(board)
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val:
                    pygame.draw.rect(
                        self.screen,
                        colors[val],
                        pygame.Rect(
                            (off_x + x) *
                              cell_size,
                            (off_y + y) *
                              cell_size,
                            cell_size,
                            cell_size), 0)


    def check_collision(self, board, shape, offset_x, offset_y):
        """
        Util: Check collisions
        """
        matrix = self.concat_dictionary(board)
        for cy, row in enumerate(shape):
            for cx, cell in enumerate(row):
                try:
                    if cell and matrix[cy + offset_y][cx + offset_x]:
                        return 1
                except:
                    return 2
        return 0


    def concat_dictionary(self, dictionary):
        """
        Util: Combines the arrays in dictionary for board
        """
        return_matrix=[]
        if isinstance(dictionary, dict):
            for i in range(len(dictionary.keys())):
                return_matrix.append(dictionary[i])
            return return_matrix
        return dictionary

    def new_stone(self):
        """ Back-end: Adds a new stone """
        # Copy the next shape into curr_piece
        self.pieces.curr_piece = self.pieces.next_piece[:]
        # Randomly select next piece
        self.pieces.next_piece = self.pieces.tetris_shapes[ np.random.choice(np.arange(1, 8), p=[0.12, 0.12, 0.12, 0.12, 0.12, 0.28, 0.12]) ]
        # Add in constraints for x-position and y-position
        self.piece_x = int(self.board_class.x_size // 2 - len(self.pieces.curr_piece) // 2)
        self.piece_y = 0

    def move(self, delta_x):
        """ Back-end: Move the piece """
        if not self.gameover and not self.paused:
            new_x = self.piece_x + delta_x
            if new_x < 0:
                new_x = 0
            if new_x > self.board_class.x_size - len(self.pieces.curr_piece[0]):
                new_x = self.board_class.x_size - len(self.pieces.curr_piece[0])
            if not self.check_collision(self.board_class.board,
                                   self.pieces.curr_piece,
                                   new_x, self.piece_y):
                self.piece_x = new_x


    def quit(self):
        """ Back-end: Quit game """
        self.center_msg("Exiting...")
        pygame.display.update()
        sys.exit()


    def drop(self):
        """ Back-end: Drop the tetris piece """
        if not self.gameover and not self.paused:
            self.piece_y += 1
            board_arr = self.concat_dictionary(self.board_class.board)
            if self.check_collision(self.board_class.board,
                               self.pieces.curr_piece,
                               self.piece_x, self.piece_y):
                self.board_class.board = self.board_class.join_board(
                  self.board_class.board,
                  self.pieces.curr_piece,
                  (self.piece_x, self.piece_y))
                self.new_stone()
                cleared_rows = 0
                matrix = self.concat_dictionary(self.board_class.board)
                try:
                    for i, row in enumerate(matrix):
                        if 0 not in row:
                            self.board_class.remove_row(i)
                            cleared_rows += 1
                except:
                    print(matrix, self.board_class.board) # debugging
                self.add_cl_lines(cleared_rows)
                return True
        return False


    def rotate_piece_with_constraints(self):
        """ Back-end: rotate tetris piece """
        if not self.gameover and not self.paused:
            new_piece = self.pieces.rotate_right(self.pieces.curr_piece)
            col_val = self.check_collision(self.board_class.board,
                                   new_piece,
                                   self.piece_x, self.piece_y)
            if not col_val:
                self.pieces.curr_piece = new_piece
            elif col_val == 1: # not index error
                pass
            else:
                print(new_piece)


    def game_over(self):
        """ Back-end: Checks if game is over """
        top_row = self.board_class.board[0]
        for val in top_row:
            if val != 0:
                self.gameover = True


    def toggle_pause(self):
        """ Back-end: Pauses the game """
        self.paused = not self.paused


    def start_game(self):
        """ Back-end: Starts game """
        game = Game()
        game.run()


    def add_cl_lines(self, n):
        """ Back-end: Adds score to the game """
        self.score += self.add_score(n)


    def add_score(self, line_number):
        """ Back-end: Scoring function """
        temp_score = (20 * line_number) * (1.2 ** (line_number - 1))
        return int(round(temp_score, -1))


    def run(self):
        key_actions = {
            'ESCAPE':	self.quit,
            'LEFT':		lambda: self.move(-1),
            'RIGHT':	lambda: self.move(1),
            'DOWN':		lambda: self.drop(),
            'UP':		self.rotate_piece_with_constraints,
            'p':		self.toggle_pause,
            'SPACE':	self.start_game,
        }
        self.gameover = False
        self.paused = False
        clock = pygame.time.Clock()
        while True:
            self.screen.fill((0,0,0))
            if self.gameover:
                self.center_msg("""Game Over!
Press space to continue""")
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(
                        self.screen,
                        (255,255,255),
                        (self.rlim + 1, 0),
                        (self.rlim + 1, self.height - 1)
                        )
                    self.disp_msg("Next:", (self.rlim + cell_size, 2))
                    self.disp_msg(str(self.score), (self.rlim + cell_size, cell_size * 5))
                    self.draw_matrix(self.bground_grid, (0, 0))
                    self.draw_matrix(self.board_class.board, (0, 0))
                    self.draw_matrix(self.pieces.curr_piece, (self.piece_x, self.piece_y))
                    self.draw_matrix(self.pieces.next_piece, (self.board_class.x_size + 1, 2))
            pygame.display.update()
            self.game_over()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()
            self.drop()
            # print(self.board_class.board)
            clock.tick(maxfps)

    ###################
    # AI CONSTRUCTION #
    ###################
    def start_game_ai(self):
        """ Back-end: Starts game """
        game = Game()
        game.run_ai()

    def drop_ai(self, board, piece, piece_x, piece_y):
        """ Back-end: Drop for AI """
        while not self.check_collision(board,
                           piece,
                           piece_x, piece_y):
            piece_y += 1

        return self.board_class.join_board(board, piece, (piece_x, piece_y))


    def heights(self, board):
        """
        AI algorithm
        ------------
        Return: an array of heights / column of the tetris board
        """
        height_array = [0 for _ in range(self.board_class.x_size)]
        for i in range(self.board_class.y_size):
            current_row = board[i]
            for j in range(len(current_row)):
                if current_row[j] != 0:
                    if height_array[j] == 0:
                        height_array[j] += self.board_class.y_size - i
        return height_array


    def height_max(self, board):
        """
        AI algorithm
        ------------
        Return: Max of heights
        """
        heights = self.heights(board)
        return max(heights)

    def height_std(self, board):
        """
        AI algorithm
        ------------
        Return: Standard deviation of heights
        """
        heights = self.heights(board)
        return np.std(heights)


    def holes_blockages(self, board):
        """
        AI algorithm
        ------------
        Return: Number of holes / blockages in tetris
        """
        num_holes = 0
        num_blockages = 0
        matrix = self.concat_dictionary(board)
        # Loop on every column
        for x in range(self.board_class.x_size):
            holes = 0
            blockages = 0
            firstblock_y = 0
            isblock = False
            # Looping on y-axis, going down
            while not isblock and firstblock_y < self.board_class.y_size:
                if matrix[firstblock_y][x] != 0:
                    isblock = True
                firstblock_y += 1
            # Move onto next instance
            if firstblock_y == self.board_class.y_size:
                continue
            # Set y
            y = self.board_class.y_size - 1
            # Looping on y-axis, going up
            while y >= firstblock_y:
                if matrix[y][x] > 0 and holes > 0:
                    blockages += 1
                elif matrix[y][x] == 0:
                    holes += 1
                y -= 1
            # If no holes, move onto next instance
            if holes == 0:
                continue
            num_holes += holes
            num_blockages += blockages
        return num_holes


    def num_lines_cleared(self, board):
        """
        AI algorithm
        ------------
        Return: Number of lines to be cleared
        """
        num_rows = 0
        for key, value in board.items():
            if 0 not in value:
                num_rows += 1
        return num_rows


    def fullness(self, board):
        """
        AI algorithm
        ------------
        Return: How full the board is currently
        """
        row_fullness = []
        for i in range(self.board_class.y_size):
            current_row = board[i]
            if int(sum(current_row)) == 0:
                continue
            for j in range(len(current_row)):
                col_fullness = 0
                if current_row[j] != 0:
                    col_fullness += 1
                row_fullness.append(col_fullness / 10)
        return np.mean(row_fullness)



    def game_states(self):
        """
        AI algorithm
        ------------
        Return: All the game game states

        Implementation
        --------------
        - Consider all possible rotations of the pieces (loop)
        - Consider all possible places to put the pieces (loop)
        """
        game_state_dictionary = {}
        curr_piece_copy = self.pieces.curr_piece[:]
        num_rotations = self.pieces.tetris_rotation[self.pieces.return_curr_piece_key()]
        list_rotations = []
        for _ in range(num_rotations):
            list_rotations.append(curr_piece_copy)
            curr_piece_copy = self.pieces.rotate_right(curr_piece_copy)
        for j in range(len(list_rotations)):
            for i in range(self.pieces.num_places(list_rotations[j])):
                board_copy = copy.deepcopy(self.board_class.board)
                game_state = self.drop_ai(board_copy, list_rotations[j], i, 0)
                game_state_dictionary[(j, i - 4)] = game_state # rotation, number of movements
        return game_state_dictionary


    def evaluate(self, board, weights):
        """
        AI algorithm
        ------------
        Return: utility for a game state
        """
        std_height_feature = self.height_std(board)
        holes_blockages_feature = self.holes_blockages(board)
        cleared_rows_feature = self.num_lines_cleared(board)
        fullness_feature = self.fullness(board)
        max_height_feature = self.height_max(board)
        utility = 0
        for weight, feature in zip(weights, [std_height_feature, holes_blockages_feature, cleared_rows_feature, fullness_feature, max_height_feature]):
                utility += weight * feature
        return utility


    def find_best(self):
        """
        AI algorithm
        ------------
        Return: The best move to take
        """
        score_holder = {}
        game_states_dictionary = self.game_states()
        score = -float('inf')
        keys = []
        for key, value in game_states_dictionary.items():
            score_holder[key] = self.evaluate(value, [-1, -2, 10000, 1, -1])
            if score_holder[key] > score:
                keys = [key]
                score = score_holder[key]
            elif score_holder[key] == score:
                keys.append(key)
        move = float('inf')
        movement = None
        for i in range(len(keys)):
            if keys[i][1] < move:
                move = i
                movement = keys[i]
        return movement


    def move_best(self):
        """
        AI algorithm
        ------------
        Return: Move according to the best move found in find_best
        """
        num_rotations, num_moves = self.find_best()
        # print(num_moves, num_rotations)
        for _ in range(num_rotations):
            self.rotate_piece_with_constraints()
        is_six = False
        for val in self.pieces.curr_piece[0]:
            if val == 6:
                is_six = True
        if is_six:
            self.move(num_moves - 1)
        # self.move(-5)
        else:
            self.move(num_moves)


    def run_ai(self):
        key_actions = {
            'ESCAPE':	self.quit,
            'p':		self.toggle_pause,
            'SPACE':	self.start_game_ai,
        }
        clock = pygame.time.Clock()
        self.gameover = False
        self.paused = False
        curr = self.pieces.curr_piece
        while True:
            self.screen.fill((0, 0, 0))
            if self.gameover:
                self.center_msg("""Game Over! \n Your score is: {} \n Press space to continue""".format(self.score))
            else:
                if self.paused:
                    self.center_msg("Paused")
                else:
                    pygame.draw.line(
                        self.screen,
                        (255, 255, 255),
                        (self.rlim + 1, 0),
                        (self.rlim + 1, self.height - 1)
                        )
                    self.disp_msg("Next:", (self.rlim + cell_size, 2))
                    self.disp_msg(str(self.score), (self.rlim + cell_size, cell_size * 5))
                    self.draw_matrix(self.bground_grid, (0, 0))
                    self.draw_matrix(self.board_class.board, (0, 0))
                    self.draw_matrix(self.pieces.curr_piece, (self.piece_x, self.piece_y))
                    self.draw_matrix(self.pieces.next_piece, (self.board_class.x_size + 1, 2))
            pygame.display.update()
            self.game_over()
            # Do not update unless we are on a new piece
            if curr is not self.pieces.curr_piece:
                self.move_best()
            curr = self.pieces.curr_piece
            # Pausing, quitting controls
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == eval("pygame.K_" + key):
                            key_actions[key]()
            self.drop()
            clock.tick(maxfps)

def main():
    game = Game()
    # Start the game with AI
    game.run_ai()
    # Start the game with user playing
    #game.run()

if __name__ == '__main__':
    main()