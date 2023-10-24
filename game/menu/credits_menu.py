from game.menu.imenu import Menu

class CreditsMenu(Menu):
    """Credits Page as a Menu"""

    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        """Show Credits Page"""
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.current_menu = self.game.main_menu    # Set current menu to main menu
                self.run_display = False                        # Hide the Credits Page
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text(
                'Author', 24, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20)
            self.game.draw_text('psylocube', 15,
                                self.game.WIDTH / 2, self.game.HEIGHT / 2 + 50)
            self.game.draw_text(
                'github.com/psylocube', 12, self.game.WIDTH / 2, self.game.HEIGHT / 2 + 110)
            self.blit_screen()
