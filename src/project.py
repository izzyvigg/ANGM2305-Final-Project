import pygame
import os
import sys
from pygame.locals import *
import tkinter as tk
from tkinter import filedialog

pygame.init()
# screen setup
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Color Picker")

# store selected colors
selected_colors = []
max_colors = 10

# image variables
image = None
image_rect = None

def load_image(filepath):
    # loading image from user file
    global image, image_rect
    try:
        image = pygame.image.load(filepath).convert()
        # scale img to fit in its panel
        max_width = screen_width // 2 - 40
        max_height = screen_height - 80
        
        # new img dimensions
        width_ratio = max_width / image.get_width()
        height_ratio = max_height / image.get_height()
        scale = min(width_ratio, height_ratio)
        
        new_width = int(image.get_width() * scale)
        new_height = int(image.get_height() * scale)
        
        image = pygame.transform.scale(image, (new_width, new_height))
        image_rect = image.get_rect(center=(screen_width//4, screen_height//2))
        return True
    except:
        return False
