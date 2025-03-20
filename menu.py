import sys
import random
import pygame
import pygame.mixer
from classes.constants import WIDTH, HEIGHT, BLACK, WHITE, RED


def animate_screen(screen, mainmenu_img):
    for i in range(20):
        screen.blit(mainmenu_img, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        screen.blit(mainmenu_img, (random.randint(-5, 5), random.randint(-5, 5)))
        pygame.display.flip()
        pygame.time.wait(10)

def show_menu():
    pygame.mixer.init()
    pygame.init()
    pygame.mixer.music.load('game_sounds/menu.mp3')
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1)
    pygame.mixer.set_num_channels(20)
    for i in range(20):
        channel = pygame.mixer.Channel(i)
        channel.set_volume(0.25)

    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Main Menu")
    clock = pygame.time.Clock()

    mainmenu_img = pygame.image.load('images/mainmenu2.jpg').convert()
    mainmenu_img = pygame.transform.scale(mainmenu_img, (WIDTH, HEIGHT))

    logo_img = pygame.image.load('images/spaceshooterlogo.png').convert_alpha()
    logo_img = pygame.transform.scale(logo_img, (800, 900))
    logo_x = (WIDTH - logo_img.get_width()) // 2
    logo_y = -240

    play_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 205, 50)
    quit_button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 205, 50)

    explosion_sound = pygame.mixer.Sound('game_sounds/explosions/explosion1.wav')
    explosion_sound.set_volume(0.25)
    selected_button = 0
    running = True

    joystick = None
    if pygame.joystick.get_count() > 0:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if play_button_rect.collidepoint(x, y):
                    explosion_sound.play()
                    animate_screen(screen, mainmenu_img)
                    # Instead of calling game_loop(), return a flag idea #54
                    return "play"
                elif quit_button_rect.collidepoint(x, y):
                    pygame.quit()
                    sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_button = 0
                elif event.key == pygame.K_DOWN:
                    selected_button = 1
                elif event.key == pygame.K_RETURN:
                    if selected_button == 0:
                        explosion_sound.play()
                        animate_screen(screen, mainmenu_img)
                        return "play"
                    elif selected_button == 1:
                        pygame.quit()
                        sys.exit()

            if joystick:
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0:
                        if selected_button == 0:
                            explosion_sound.play()
                            animate_screen(screen, mainmenu_img)
                            return "play"
                        elif selected_button == 1:
                            pygame.quit()
                            sys.exit()
                elif event.type == pygame.JOYHATMOTION:
                    if event.value[1] == 1:
                        selected_button = 0
                    elif event.value[1] == -1:
                        selected_button = 1

        screen.blit(mainmenu_img, (0, 0))
        screen.blit(logo_img, (logo_x, logo_y))

        font = pygame.font.SysFont('Comic Sans MS', 40)
        text = font.render("Play", True, WHITE)
        pygame.draw.rect(screen, BLACK, play_button_rect, border_radius=10)
        if selected_button == 0:
            pygame.draw.rect(screen, RED, play_button_rect, border_radius=10, width=4)
        text_rect = text.get_rect()
        text_rect.center = play_button_rect.center
        screen.blit(text, text_rect)

        text = font.render("Exit", True, WHITE)
        pygame.draw.rect(screen, BLACK, quit_button_rect, border_radius=10)
        if selected_button == 1:
            pygame.draw.rect(screen, RED, quit_button_rect, border_radius=10, width=4)
        text_rect = text.get_rect()
        text_rect.center = quit_button_rect.center
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

# Only call show_menu() if this file is run directly
if __name__ == "__main__":
    # Running menu.py individually will only show the menu
    choice = show_menu()
    print("User selected:", choice)
