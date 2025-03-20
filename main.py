import pygame
import menu
import game

def main():
    pygame.init()
    while True:
        choice = menu.show_menu()  # Show the menu and wait for user selection
        if choice == "play":
            result = game.game_loop()  # Start the game
            if result == "menu":
                continue

if __name__ == "__main__":
    main()
