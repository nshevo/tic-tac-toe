import pygame

class Menu():
    """Base Menu Class"""

    def __init__(self, game):   # Self always first, needs game as an attribute
        """Initialises Class with its content"""
        self.game = game
        self.middle_width, self.middle_height = self.game.WIDTH / 2, self.game.HEIGHT / 2
        self.run_display = True   # Display Menu
        # Cursor to show the choise in menu
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.cursor_offset = - 120   # Offset for positioning the cursor
        self.cursor = 'x'   # Cursor sign

    def draw_cursor(self):
        """Draws cursor in the Menu"""
        self.game.draw_text(
            self.cursor, 25, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        """Blits the screen, helps drawing elements"""
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
