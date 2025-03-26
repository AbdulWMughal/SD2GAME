import os
import pygame
import pytest
from unittest.mock import patch
from functions import music_background, show_game_over, show_game_win  # Replace 'functions' with your actual module

#  Use a fake SDL display to prevent "display Surface quit" errors
os.environ["SDL_VIDEODRIVER"] = "dummy"

#  Initialize pygame to prevent missing display errors
pygame.init()
pygame.display.set_mode((800, 600))  # Dummy screen to avoid display errors

# Test for game over screen
@patch("pygame.mixer.music.load")
@patch("pygame.mixer.music.play")
@patch("pygame.font.SysFont")
@patch("pygame.display.flip")
def test_show_game_over(mock_flip, mock_font, mock_play, mock_load):
    mock_instance = mock_font.return_value
    mock_instance.render.return_value = pygame.Surface((100, 50))  # Mock text rendering
    
    show_game_over(100)  # Call function

    #  Verify music load calls in any order
    expected_calls = [
        (("game_sounds/gameover.mp3",),),
        (("game_sounds/background_music.mp3",),)
    ]
    mock_load.assert_has_calls(expected_calls, any_order=True)

    #  Ensure display update was called
    mock_flip.assert_called()

#  Test for game win screen
@patch("pygame.mixer.music.load")
@patch("pygame.mixer.music.play")
@patch("pygame.font.SysFont")
@patch("pygame.display.flip")
def test_show_game_win(mock_flip, mock_font, mock_play, mock_load):
    mock_instance = mock_font.return_value
    mock_instance.render.return_value = pygame.Surface((100, 50))  # Mock text rendering

    show_game_win()  # Call function

    #  Ensure correct music file was loaded
    mock_load.assert_called_with("game_sounds/background_music.mp3")

    #  Ensure display update was called
    mock_flip.assert_called()

#  Test for background music function
@patch("pygame.mixer.music.load")
@patch("pygame.mixer.music.play")
def test_music_background(mock_play, mock_load):
    music_background()  # Call function

    #  Ensure background music loads and plays
    mock_load.assert_called_with("game_sounds/background_music.mp3")
    mock_play.assert_called()
