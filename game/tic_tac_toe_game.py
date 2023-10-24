import pygame
from pygame import gfxdraw  # For drawing an anti-aliased circle
import random
import sys
from game.menu.tic_tac_toe_menu import TicTacToeMenu # Import TicTacToeMenu Class
from game.menu.credits_menu import CreditsMenu # Import CreditsMenu Class

class TicTacToeGame():
    """Tic-Tac-Toe Game Class"""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Tic-Tac-Toe")
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSEBUTTONDOWN = False, False, False, False, False
        self.BLOCK_SIZE = 150
        self.MARGIN = 10
        self.PADDING = 5
        self.WIDTH = self.BLOCK_SIZE * 3 + self.MARGIN * 2
        self.HEIGHT = self.BLOCK_SIZE * 3 + self.MARGIN * 2 + 30
        self.PLAYER_NAMES_Y = self.HEIGHT - 15
        self.display = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.window = pygame.display.set_mode(((self.WIDTH, self.HEIGHT)))
        self.font_name = pygame.font.get_default_font()
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.starting_player = ""
        self.computer_turn = False
        self.computer_sign = ''
        self.player_sign_pve = ''
        self.game_mode = 'LPVP'
        self.player_input = ""
        self.player_name_1 = ""
        self.player_sign_1 = ""
        self.player_name_2 = ""
        self.player_sign_2 = ""
        self.winner = ""
        self.player_names_offset = 120
        self.main_menu = TicTacToeMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.current_menu = self.main_menu
        self.field = [[0] * 3 for _ in range(3)]
        self.query = 0

    def check_win(self, field, sign):
        """Checks if the sign has won"""
        zeroes = 0
        for row in field:
            zeroes += row.count(0)
            if row.count(sign) == 3:
                return sign

        for col in range(3):
            if all(field[row][col] == sign for row in range(3)):
                return sign

        if all(field[i][i] == sign for i in range(3)) or all(field[i][2 - i] == sign for i in range(3)):
            return sign

        if zeroes == 0:
            return 'tie!'

        return False

    def return_input_player_name(self):
        """Shows screen for player to enter his name and returns it"""
        while self.START_KEY != True:
            self.check_events()
            self.display.fill(self.BLACK)
            self.draw_text("Enter a name", 14,
                           self.WIDTH / 2, self.HEIGHT / 2)
            self.draw_text("Press Enter to confirm", 14,
                           self.WIDTH / 2, self.HEIGHT / 2 + 150)
            self.draw_text("->" + self.player_input, 14, self.WIDTH /
                           2, self.HEIGHT / 2 + 30)
            self.window.blit(self.display, (0, 0))
            pygame.display.update()
        self.reset_keys()
        return self.player_input

    def generate_player_names(self):
        """Generates Player names based on game mode and already given player names"""
        if self.game_mode == 'LPVP' and (self.player_name_1 == "Computer" or not self.player_name_1):
            self.player_name_1 = self.return_input_player_name()
            self.player_input = ""
            self.player_name_2 = self.return_input_player_name()
            self.player_input = ""
        elif self.game_mode == 'PVE' and self.player_name_1 != "Computer":
            self.player_name_1 = "Computer"
            self.player_name_2 = self.return_input_player_name()
            self.player_input = ""

    def dice_starting_player(self):
        """Dices random number between 0 and 1
        and sets starting player based on the result
        """
        random_number = random.uniform(0, 1)
        if random_number > 0.5:
            self.starting_player = self.player_name_1
        else:
            self.starting_player = self.player_name_2

    def draw_player_names(self):
        """Draws player names with their diced game signs"""
        if self.starting_player == self.player_name_1:
            self.draw_text('x - ' + self.player_name_1, 14,
                           self.WIDTH / 2 - self.player_names_offset, self.PLAYER_NAMES_Y)
            self.draw_text('o - ' + self.player_name_2, 14,
                           self.WIDTH / 2 + self.player_names_offset, self.PLAYER_NAMES_Y)
        elif self.starting_player == self.player_name_2:
            self.draw_text('o - ' + self.player_name_1, 14,
                           self.WIDTH / 2 - self.player_names_offset, self.PLAYER_NAMES_Y)
            self.draw_text('x - ' + self.player_name_2, 14,
                           self.WIDTH / 2 + self.player_names_offset, self.PLAYER_NAMES_Y)

    def set_player_signs(self):
        """Sets player signs (cross or an o) based on game mode and diced results"""
        if self.starting_player == self.player_name_1 and self.game_mode == 'PVE':
            self.computer_turn = True
            self.computer_sign = 'x'
            self.player_sign_pve = 'o'
        elif self.starting_player == self.player_name_2 and self.game_mode == 'PVE':
            self.computer_turn = False
            self.computer_sign = 'o'
            self.player_sign_pve = 'x'
        elif self.starting_player == self.player_name_1 and self.game_mode == 'LPVP':
            self.player_sign_1 = 'x'
            self.player_sign_2 = 'o'
        elif self.starting_player == self.player_name_2 and self.game_mode == 'LPVP':
            self.player_sign_1 = 'o'
            self.player_sign_2 = 'x'

    def draw_turn_sign(self):
        """Draws turn sign pointing at players name who has to make the next move"""
        if self.query % 2 == 0:
            if self.starting_player == self.player_name_1:
                self.draw_text("<<< Turn", 14, self.WIDTH /
                               2, self.PLAYER_NAMES_Y)
            else:
                self.draw_text("Turn >>>", 14, self.WIDTH /
                               2, self.PLAYER_NAMES_Y)
        else:
            if self.starting_player == self.player_name_1:
                self.draw_text("Turn >>>", 14, self.WIDTH /
                               2, self.PLAYER_NAMES_Y)
            else:
                self.draw_text("<<< Turn", 14, self.WIDTH /
                               2, self.PLAYER_NAMES_Y)

    def computer_can_win(self, block1, block2, block3, sign):
        """Checks if any block is empty
        if possible win/win deny was found return index of the block
        otherwise returns 0
        """
        can_win = 0
        if block1 == sign and block2 == sign and block3 == 0:
            can_win = 3
        if block1 == sign and block2 == 0 and block3 == sign:
            can_win = 2
        if block1 == 0 and block2 == sign and block3 == sign:
            can_win = 1
        return can_win

    def check_possible_game_finish(self, sign):
        """Computer logic: row-based, column-based and diagonal-based

        1. If computer has one move win (sign=self.computer_sign)
        Make the winning move
        returns True
        otherwise only returns False

        2. If computer can deny one move win (sign=self.player_sign_pve)
        Denies the win by setting a sign
        returns True
        otherwise only returns False
        """
        for n in range(3):
            row = self.computer_can_win(
                self.field[n][0], self.field[n][1], self.field[n][2], sign)
            if row != 0:
                if row == 1:
                    self.field[n][0] = self.computer_sign
                    return True
                elif row == 2:
                    self.field[n][1] = self.computer_sign
                    return True
                elif row == 3:
                    self.field[n][2] = self.computer_sign
                    return True

            col = self.computer_can_win(
                self.field[0][n], self.field[1][n], self.field[2][n], sign)
            if col != 0:
                if col == 1:
                    self.field[0][n] = self.computer_sign
                    return True
                elif col == 2:
                    self.field[1][n] = self.computer_sign
                    return True
                elif col == 3:
                    self.field[2][n] = self.computer_sign
                    return True

        diagonal = self.computer_can_win(
            self.field[0][0], self.field[1][1], self.field[2][2], sign)
        if diagonal != 0:
            if diagonal == 1:
                self.field[0][0] = self.computer_sign
                return True
            elif diagonal == 2:
                self.field[1][1] = self.computer_sign
                return True
            elif diagonal == 3:
                self.field[2][2] = self.computer_sign
                return True
        diagonal = self.computer_can_win(
            self.field[2][0], self.field[1][1], self.field[0][2], sign)
        if diagonal != 0:
            if diagonal == 1:
                self.field[2][0] = self.computer_sign
                return True
            elif diagonal == 2:
                self.field[1][1] = self.computer_sign
                return True
            elif diagonal == 3:
                self.field[0][2] = self.computer_sign
                return True

        return False

    def computer_move(self):
        """Computer making move

        1. Checks if game can be won
        2. Checks if the game finish can be denied
        3. Otherwise sets a sign randomly
        """
        if self.check_possible_game_finish(self.computer_sign) == False and self.check_possible_game_finish(self.player_sign_pve) == False:
            while True:
                row = random.randint(0, 2)
                col = random.randint(0, 2)
                if self.field[row][col] == 0:
                    self.field[row][col] = self.computer_sign
                    break

    def start_new_game(self):
        """Starts a new game with reset game field, query and player names"""
        self.field = [[0] * 3 for i in range(3)]
        self.query = 0
        self.generate_player_names()
        self.dice_starting_player()
        self.set_player_signs()

    def game_loop(self):
        """Game Loop"""
        self.display.fill(self.BLACK)
        self.window.blit(self.display, (0, 0))

        self.start_new_game()

        while self.playing:
            self.display.fill(self.BLACK)
            self.draw_player_names()
            self.draw_turn_sign()
            self.window.blit(self.display, (0, 0))

            # Check if comouter has to make a move
            if self.computer_turn == True:
                self.computer_move()
                self.computer_turn = False
                self.query += 1

            self.check_events()

            if self.BACK_KEY:
                # Goes to main menu
                self.playing = False
                self.window.blit(self.display, (0, 0))
            elif self.START_KEY:
                # Starts a new game when enter is pressed
                self.start_new_game()
                self.display.fill(self.BLACK)
                self.window.blit(self.display, (0, 0))
                self.reset_keys()
            elif self.MOUSEBUTTONDOWN:
                # Sets a sign based on mouse position on mouse click
                x_mouse, y_mouse = pygame.mouse.get_pos()   # Get mouse position (x,y)
                # Calculate which col and row was clocked
                col = x_mouse // (self.BLOCK_SIZE + self.MARGIN)
                row = y_mouse // (self.BLOCK_SIZE + self.MARGIN)

                # Sets a sign based on query
                if self.field[row][col] == 0:
                    if self.query % 2 == 0:
                        self.field[row][col] = 'x'
                    else:
                        self.field[row][col] = 'o'
                    self.query += 1
                    # If sign was set in PVE, next turn makes the computer
                    if self.game_mode == 'PVE':
                        self.computer_turn = True
                # Resets pressed keys
                self.reset_keys()
            # Going through the field (2D array)
            for row in range(3):
                for col in range(3):
                    # Calculates x,y coordinates where to draw the white rectangle (empty field or background of the set sign)
                    x = col * self.BLOCK_SIZE + (col) * self.MARGIN
                    y = row * self.BLOCK_SIZE + (row) * self.MARGIN
                    # Draws rectangle on self.window-> our game window, color of the field is self.WHITE
                    # x,y position and dimensions -> our block size, height, width -> identical
                    pygame.draw.rect(self.window, self.WHITE,
                                     (x, y, self.BLOCK_SIZE, self.BLOCK_SIZE))
                    # Based on set sign in the field array draw according sign in the game field
                    if self.field[row][col] == 'x':
                        # Draws a line from left top corner to bottom right corner
                        # self.padding is used to adjust drawn line from the box corners
                        pygame.draw.line(self.window, self.BLACK, (x + self.PADDING, y + self.PADDING),
                                         (x + self.BLOCK_SIZE - self.PADDING, y + self.BLOCK_SIZE - self.PADDING), 1)
                        # Draws a line from left bottom corner to top right corner
                        # self.padding used for line adjustment like before
                        pygame.draw.line(self.window, self.BLACK, (x + self.BLOCK_SIZE - self.PADDING,
                                                                   y + self.PADDING), (x + self.PADDING, y + self.BLOCK_SIZE - self.PADDING), 1)
                    elif self.field[row][col] == 'o':
                        # Draw antialised (not pixeled) circle
                        #
                        self.draw_aacircle(self.window, (x + self.BLOCK_SIZE // 2), (y +
                                           self.BLOCK_SIZE // 2), self.BLOCK_SIZE // 2 - self.PADDING, self.BLACK)

            # Check if there is a winner based on previous turn
            if (self.query-1) % 2 == 0:
                game_over = self.check_win(self.field, 'x')
            else:
                game_over = self.check_win(self.field, 'o')
            # Game is over: display a winner or tie
            if game_over:
                # Disable computer in PVE mode from making a turn after game_over
                if self.game_mode == 'PVE':
                    self.computer_turn = False
                self.display.fill(self.BLACK)
                text_x = self.WIDTH / 2
                text_y = self.HEIGHT / 2
                # There is a winner
                if game_over == 'x' or game_over == 'o':
                    # Set winner in LPVP game mode
                    if self.game_mode == 'LPVP':
                        if self.player_sign_1 == game_over:
                            self.winner = self.player_name_1
                        elif self.player_sign_2 == game_over:
                            self.winner = self.player_name_2
                    # Set winner in PVE game mode
                    elif self.game_mode == 'PVE':
                        if self.player_sign_pve == game_over:
                            self.winner = self.player_name_2
                        elif self.computer_sign == game_over:
                            self.winner = self.player_name_1
                    # Draw win screen with winners player_name
                    self.draw_text(self.winner, 48, text_x, text_y - 50)
                    self.draw_text('won!', 24, text_x, text_y)
                # There is no winner but a tie game
                else:
                    self.draw_text(game_over, 32, text_x,
                                   text_y)   # Unentschieden
                self.draw_text(
                    "Press Enter to play again", 14, text_x, text_y + 150)
                self.draw_text(
                    "Backspace | Main Menu", 14, text_x, text_y + 180)
                self.window.blit(self.display, (0, 0))
            pygame.display.update()

    def check_events(self):
        """Checks pressed events and pressed keyboard and mouse buttons

        and sets according constants to true or quits the game"""
        for event in pygame.event.get():
            # When window close sign (X) is clicked
            if event.type == pygame.QUIT:
                self.running, self.playing = False, False   # Exit from game
                self.current_menu.run_display = False   # Dont show the menu
                sys.exit(0)  # Close the window
            # Buttons where pressed DOWN
            if event.type == pygame.KEYDOWN:
                # Any letters are pressed
                if event.unicode.isalpha():
                    self.player_input += event.unicode  # Add input letters to self.player_input
                # Down key is pressed
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                # Up key is pressed
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                # Enter is pressed
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                # Backspace is pressed
                if event.key == pygame.K_BACKSPACE:
                    # Delete last character from self.input (when generating player names)
                    self.player_input = self.player_input[:-1]
                    self.BACK_KEY = True
            # Mouse was clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.MOUSEBUTTONDOWN = True

    def reset_keys(self):
        """Sets key constants to False"""
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.MOUSEBUTTONDOWN = False, False, False, False, False

    def draw_text(self, text, size, x, y):
        """Draws white text centered at the given coordinates"""
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)

    def draw_aacircle(self, surface, x, y, radius, color):
        """Draws anti-aliased circle with given position and radius on the surface"""
        gfxdraw.aacircle(surface, x, y, radius, color)
        