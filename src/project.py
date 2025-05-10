import math
import PIL
import extcolors
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from matplotlib import gridspec
from tkinter import Tk, filedialog

def main():
    # Get the image file from the user and run the window
    image_path = get_image_file()
    if image_path:
        study_image(image_path)
    else:
        print("No image file selected.")

def fetch_image(image_path):
    return PIL.Image.open(image_path)

def study_image(image_path):
    img = fetch_image(image_path)

def get_image_file():
    root = Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Select an image file",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )

if __name__ == "__main__":
    main()