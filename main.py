from game.tic_tac_toe_game import TicTacToeGame

game = TicTacToeGame()  # set game to initialised TicTacToeGame Class

# Main loop for running menu and game
# game.running is set to False in TicTacToeGame Class
while game.running:
    game.current_menu.display_menu()  # Display current menu of the game
    game.game_loop()    # Run game loop for key input and menu choices
