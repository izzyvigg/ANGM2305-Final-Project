import pygame
import os
import sys
from pygame.locals import *
import tkinter as tk
from tkinter import filedialog

pygame.init()

# screen setup
screen_width = 1000
screen_height = 900
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("My Color Picker")

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (33, 145, 119)

# font
font = pygame.font.SysFont('Helvetica', 24)
big_font = pygame.font.SysFont('Helvetica', 36)

# store selected colors
max_colors = 12
palettes = [[]]  # List of palettes, starts with one empty palette
current_palette = 0  # Index of currently active palette

# image variables
image = None
image_rect = None
palette_height = 350  # Height for each palette section

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
        image_rect = image.get_rect(center=(screen_width//4, screen_height//1.6))
        return True
    except:
        return False

def draw_buttons():
    # left panel buttons
    button_width = 250
    button_height = 50
    start_x = 60
    start_y = 40
    spacing = 20
    
    # upload img button
    pygame.draw.rect(screen, LIGHT_BLUE, (start_x, start_y, button_width, button_height))
    upload_text = font.render("Upload Image", True, BLACK)
    screen.blit(upload_text, (start_x + button_width//2 - upload_text.get_width()//2, 
                             start_y + button_height//2 - upload_text.get_height()//2))
    
    # add img button
    if image:
        pygame.draw.rect(screen, LIGHT_BLUE, (start_x, start_y + button_height + spacing, button_width, button_height))
        add_text = font.render("Add Another Image", True, BLACK)
        screen.blit(add_text, (start_x + button_width//2 - add_text.get_width()//2, 
                              start_y + button_height + spacing + button_height//2 - add_text.get_height()//2))
    
    # right panel buttons
    palette_start_x = screen_width // 2 + 40
    button_width_right = 180
    
    # add palette button
    pygame.draw.rect(screen, GREEN, (palette_start_x, start_y, button_width_right, button_height))
    add_palette_text = font.render("Add Palette", True, BLACK)
    screen.blit(add_palette_text, (palette_start_x + button_width_right//2 - add_palette_text.get_width()//2, 
                                 start_y + button_height//2 - add_palette_text.get_height()//2))
    
    # save palette button
    if palettes:
        pygame.draw.rect(screen, LIGHT_BLUE, (palette_start_x + button_width_right + spacing, start_y, button_width_right, button_height))
        save_text = font.render("Save Palette", True, BLACK)
        screen.blit(save_text, (palette_start_x + button_width_right + spacing + button_width_right//2 - save_text.get_width()//2, 
                               start_y + button_height//2 - save_text.get_height()//2))

def draw_palettes():
    palette_start_x = screen_width // 2 + 40
    start_y = 100
    swatch_size = 70
    swatches_per_row = 4
    
    for palette_idx, palette in enumerate(palettes):
        current_y = start_y + palette_idx * (palette_height + 20)
        
        # draw palette background
        pygame.draw.rect(screen, GRAY, (palette_start_x, current_y, screen_width//2 - 80, palette_height), 2)
        
        # draw palette title
        title = big_font.render(f"Palette {palette_idx + 1}", True, BLACK)
        screen.blit(title, (palette_start_x + 20, current_y + 20))
        
        if not palette:
            text = font.render("Click image to add colors", True, BLACK)
            screen.blit(text, (palette_start_x + (screen_width//2 - 80)//2 - text.get_width()//2, 
                             current_y + palette_height//2))
        else:
            # draw color swatches
            for i, color in enumerate(palette):
                row = i // swatches_per_row
                col = i % swatches_per_row
                x = palette_start_x + 20 + col * (swatch_size + 30)
                y = current_y + 80 + row * (swatch_size + 30)
                
                pygame.draw.rect(screen, color, (x, y, swatch_size, swatch_size))

        # show count  
        if palette_idx == current_palette:
            count_text = font.render(f"{len(palette)}/{max_colors}", True, BLACK)
            screen.blit(count_text, (palette_start_x + (screen_width//2 - 80) - 70, current_y + 20))

def get_image_path():
    try:
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        return file_path
    except:
        return None

def save_current_palette():
    try:        
        # prompt user for file path
        file_path = filedialog.asksaveasfilename(
            title="Save Current Palette",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")]
        )
        
        if file_path and palettes[current_palette]:
            # create new surface for palette
            swatch_size = 100
            margin = 20
            swatches_per_row = 4
            palette = palettes[current_palette]
            
            palette_width = min(swatches_per_row, len(palette)) * (swatch_size + margin) + margin
            palette_height = ((len(palette) + swatches_per_row - 1) // swatches_per_row) * (swatch_size + margin) + margin
            
            palette_surface = pygame.Surface((palette_width, palette_height))
            palette_surface.fill(WHITE)
            
            # draw swatches
            for i, color in enumerate(palette):
                row = i // swatches_per_row
                col = i % swatches_per_row
                x = margin + col * (swatch_size + margin)
                y = margin + row * (swatch_size + margin)
                
                pygame.draw.rect(palette_surface, color, (x, y, swatch_size, swatch_size))
                
            pygame.image.save(palette_surface, file_path)
            return True
    except:
        return False

def main():
    global image, image_rect, current_palette, palettes
    
    running = True
    while running:
        screen.fill(WHITE)
        
        pygame.draw.rect(screen, GRAY, (20, 20, screen_width//2 - 40, screen_height - 40), 2)
        
        # draw img
        if image:
            screen.blit(image, image_rect)
            
        # draw buttons & palette
        draw_buttons()
        draw_palettes()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
            if event.type == MOUSEBUTTONDOWN:
                button_width = 250
                button_height = 50
                start_x = 60
                start_y = 40
                spacing = 20
                
                # left panel buttons
                if start_x <= event.pos[0] <= start_x + button_width:
                    if start_y <= event.pos[1] <= start_y + button_height:
                        file_path = get_image_path()
                        if file_path:
                            load_image(file_path)
                            palettes[current_palette] = []
                    
                    elif image and start_y + button_height + spacing <= event.pos[1] <= start_y + 2*button_height + spacing:
                        file_path = get_image_path()
                        if file_path:
                            load_image(file_path)
                
                # right panel buttons
                palette_start_x = screen_width // 2 + 40
                button_width_right = 180
                
                # add Palette button
                if (palette_start_x <= event.pos[0] <= palette_start_x + button_width_right and 
                    start_y <= event.pos[1] <= start_y + button_height):
                    palettes.append([])
                    current_palette = len(palettes) - 1
                
                # save Palette button
                elif (palette_start_x + button_width_right + spacing <= event.pos[0] <= palette_start_x + 2*button_width_right + spacing and
                      start_y <= event.pos[1] <= start_y + button_height):
                    if save_current_palette():
                        success_text = font.render("Palette saved!", True, BLACK)
                        screen.blit(success_text, (palette_start_x, start_y + button_height + 10))
                        pygame.display.flip()
                        pygame.time.delay(1000)
                
                # palette selection
                elif event.pos[0] > screen_width // 2 + 40:
                    for i in range(len(palettes)):
                        palette_y = 100 + i * (palette_height + 20)
                        if (screen_width // 2 + 40 <= event.pos[0] <= screen_width - 40 and
                            palette_y <= event.pos[1] <= palette_y + 60):
                            current_palette = i
                
                # image click
                elif image_rect and image_rect.collidepoint(event.pos):
                    if len(palettes[current_palette]) < max_colors:
                        x_in_image = event.pos[0] - image_rect.left
                        y_in_image = event.pos[1] - image_rect.top
                        
                        if 0 <= x_in_image < image.get_width() and 0 <= y_in_image < image.get_height():
                            color = image.get_at((x_in_image, y_in_image))
                            color = (color[0], color[1], color[2])
                            
                            if color not in palettes[current_palette]:
                                palettes[current_palette].append(color)

        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()