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
    
    # Save Palette button (only shown when there are colors)
    if selected_colors:
        pygame.draw.rect(screen, LIGHT_BLUE, (50, 130, 200, 40))
        save_text = font.render("Save Palette", True, BLACK)
        screen.blit(save_text, (50 + 100 - save_text.get_width()//2, 130 + 20 - save_text.get_height()//2))


def draw_palette():
    palette_title = big_font.render("Your Color Palette", True, BLACK)
    screen.blit(palette_title, (screen_width//2 + 50, 20))
    
    if not selected_colors:
        # Show empty message
        text = font.render("Click on the image to pick colors!", True, BLACK)
        screen.blit(text, (screen_width//2 + 50, screen_height//2))
    else:
        # Draw color swatches
        swatch_size = 60
        swatches_per_row = 3
        for i, color in enumerate(selected_colors):
            row = i // swatches_per_row
            col = i % swatches_per_row
            x = screen_width//2 + 50 + col * (swatch_size + 20)
            y = 80 + row * (swatch_size + 20)
            
            pygame.draw.rect(screen, color, (x, y, swatch_size, swatch_size))
            
        # Show count
        count_text = font.render(f"Colors: {len(selected_colors)}/{max_colors}", True, BLACK)
        screen.blit(count_text, (screen_width//2 + 50, screen_height - 40))


def get_image_path():
    try:
        file_path = filedialog.askopenfilename(
            title="Select an image",
            filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
        )
        return file_path
    except:
        return None
    
def save_palette():
    try:        
        # prompt user for file path
        file_path = filedialog.asksaveasfilename(
            title="Save Palette As",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png"), ("JPEG Image", "*.jpg")]
        )
        
        if file_path:
            # create new surface for palette
            swatch_size = 100
            margin = 20
            palette_width = min(3, len(selected_colors)) * (swatch_size + margin) + margin
            palette_height = ((len(selected_colors) + 2) // 3) * (swatch_size + margin) + margin
            
            palette_surface = pygame.Surface((palette_width, palette_height))
            palette_surface.fill(WHITE)
            
            # draw swatches
            for i, color in enumerate(selected_colors):
                row = i // 3
                col = i % 3
                x = margin + col * (swatch_size + margin)
                y = margin + row * (swatch_size + margin)
                
                pygame.draw.rect(palette_surface, color, (x, y, swatch_size, swatch_size))
            
            pygame.image.save(palette_surface, file_path)
            return True
    except:
        return False

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
        
        # draw buttons & palette
        draw_buttons()
        draw_palette()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
                
            if event.type == MOUSEBUTTONDOWN:
                # clicked on upload button?
                if 50 <= event.pos[0] <= 250 and 30 <= event.pos[1] <= 70:
                    file_path = get_image_path()
                    if file_path:
                        load_image(file_path)
                        selected_colors = []  # Reset colors when loading new image
                
                # clicked on add img button?
                elif image and 50 <= event.pos[0] <= 250 and 80 <= event.pos[1] <= 120:
                    file_path = get_image_path()
                    if file_path:
                        # Load the new image but keep existing colors
                        load_image(file_path)
                
                # clicked on save button?
                elif selected_colors and 50 <= event.pos[0] <= 250 and 130 <= event.pos[1] <= 170:
                    if save_palette():
                        # success message
                        success_text = font.render("Palette saved!", True, BLACK)
                        screen.blit(success_text, (50, 180))
                        pygame.display.flip()
                        pygame.time.delay(1000)

                # clicked on image?
                elif image_rect and image_rect.collidepoint(event.pos):
                    if len(selected_colors) < max_colors:
                        # get color
                        x_in_image = event.pos[0] - image_rect.left
                        y_in_image = event.pos[1] - image_rect.top
                        
                        if 0 <= x_in_image < image.get_width() and 0 <= y_in_image < image.get_height():
                            color = image.get_at((x_in_image, y_in_image))
                            color = (color[0], color[1], color[2]) # convert to RGB
                            
                            # add to palette
                            if color not in selected_colors:
                                selected_colors.append(color)

        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()