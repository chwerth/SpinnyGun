"""This module contains any helper functions"""
import pygame
import sys


def exit_game():
    """Exits the game"""
    pygame.quit()
    sys.exit()


def text_objects(text, font, color, pos):
    """Return text surface and rect"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    return text_surface, text_rect
