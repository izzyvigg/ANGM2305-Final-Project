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

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)

# font
font = pygame.font.SysFont('Helvetica', 20)
big_font = pygame.font.SysFont('Helvetica', 30)

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

def draw_buttons():
    # upload img button
    pygame.draw.rect(screen, LIGHT_BLUE, (50, 30, 200, 40))
    upload_text = font.render("Upload Image", True, BLACK)
    screen.blit(upload_text, (50 + 100 - upload_text.get_width()//2, 30 + 20 - upload_text.get_height()//2))
    
    # add img button
    if image:
        pygame.draw.rect(screen, LIGHT_BLUE, (50, 80, 200, 40))
        add_text = font.render("Add Another Image", True, BLACK)
        screen.blit(add_text, (50 + 100 - add_text.get_width()//2, 80 + 20 - add_text.get_height()//2))

def main():
    global selected_colors, image, image_rect
    
    running = True
    while running:
        screen.fill(WHITE)
        
        # draw img space
        pygame.draw.rect(screen, GRAY, (20, 20, screen_width//2 - 40, screen_height - 40), 2)
        
        # draw img
        if image:
            screen.blit(image, image_rect)
            
        # draw palette space
        pygame.draw.rect(screen, GRAY, (screen_width//2 + 20, 20, screen_width//2 - 40, screen_height - 40), 2)
        
        # draw buttons
        draw_buttons()
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    
    main()