from game.menu.imenu import Menu

class TicTacToeMenu(Menu):
    """Main Tic-Tac-Toe Menu Class """

    def __init__(self, game):
        super().__init__(game)
        self.state = "LPVP"
        self.local_game_x, self.local_game_y = self.middle_width, self.middle_height + 30
        self.pve_game_x, self.pve_game_y = self.middle_width, self.middle_height + 50
        self.credits_x, self.credits_y = self.middle_width, self.middle_height + 70
        self.cursor_rect.midtop = (self.local_game_x + self.cursor_offset, self.local_game_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 24, self.game.WIDTH/2, self.game.HEIGHT/2 - 20)
            self.game.draw_text("Local PvP Game", 18, self.local_game_x, self.local_game_y)
            self.game.draw_text("PvE Game", 18, self.pve_game_x, self.pve_game_y)
            self.game.draw_text("Author", 18, self.credits_x, self.credits_y)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        """Logic for moving the cursor

        Set new cursor position, cursor sign and menu state according to chosen menu text
        Menu navigation with down key and up key
        """
        if self.game.DOWN_KEY:
            if self.state == 'LPVP':
                self.cursor_rect.midtop = (
                    self.pve_game_x + self.cursor_offset, self.pve_game_y)
                self.cursor = 'o'
                self.state = 'PVE'
            elif self.state == 'PVE':
                self.cursor_rect.midtop = (
                    self.credits_x + self.cursor_offset, self.credits_y)
                self.cursor = 'x'
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.local_game_x + self.cursor_offset, self.local_game_y)
                self.cursor = 'x'
                self.state = 'LPVP'
        elif self.game.UP_KEY:
            if self.state == 'LPVP':
                self.cursor_rect.midtop = (
                    self.credits_x + self.cursor_offset, self.credits_y)
                self.cursor = 'x'
                self.state = 'Credits'
            elif self.state == 'PVE':
                self.cursor_rect.midtop = (
                    self.local_game_x + self.cursor_offset, self.local_game_y)
                self.cursor = 'x'
                self.state = 'LPVP'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (
                    self.pve_game_x + self.cursor_offset, self.pve_game_y)
                self.cursor = 'o'
                self.state = 'PVE'

    def check_input(self):
        """Move cursor and when START_KEY is pressed open LPVP or PVE game mode or Credits screen"""
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'LPVP':
                self.game.game_mode = 'LPVP'
                self.game.playing = True
            elif self.state == 'PVE':
                self.game.game_mode = 'PVE'
                self.game.playing = True
            elif self.state == 'Credits':
                self.game.game_mode = ''
                self.game.current_menu = self.game.credits_menu
            self.run_display = False    # Dont show the menu
