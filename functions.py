"""This module contains any helper functions"""
import sys
import pygame


def exit_game():
    """Exits the game"""
    pygame.quit()
    sys.exit()


def text_objects(text, font, color, pos):
    """Return text surface and rect"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    return text_surface, text_rect


def fib(index):
    """recursive fibonacci sequence function"""
    if index <= 1:
        return index
    return fib(index - 1) + fib(index - 2)
