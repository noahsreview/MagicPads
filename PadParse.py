import time
import launchpad_py as launchpad
import colour_logs
from launchpad_py import Launchpad
import logging
from PIL import Image

original_pixel_data = [[(0, 0, 0) for _ in range(8)] for _ in range(8)]  # 8x8 RGB color grid

def image_to_launchpad_colors(image_path):
    """Convert an 8x8 PNG image into a list of RGB values."""
    img = Image.open(image_path).convert("RGB")  # Open image and convert to RGB
    img = img.resize((8, 8))  # Ensure it's 8x8 pixels

    pixel_data = []
    
    for y in range(8):
        row = []
        for x in range(8):
            r, g, b = img.getpixel((x, y))  # Get pixel RGB values
            
            # Convert full 0-255 RGB values into 0-63 range (Launchpad scale)
            r = int((r / 255) * 63)
            g = int((g / 255) * 63)
            b = int((b / 255) * 63)
            
            row.append((r, g, b))  # Store as (Red, Green, Blue)
        
        pixel_data.append(row)

    return pixel_data  # Returns a list of lists (8x8 grid of (R, G, B) tuples)

def display_image_on_launchpad(lp, image_path):
    """Display an 8x8 PNG image only on the center 8x8 grid (1,1) to (8,8)."""
    global original_pixel_data
    original_pixel_data = image_to_launchpad_colors(image_path)  # Get color data

    for y in range(8):
        for x in range(8):
            r, g, b = original_pixel_data[y][x]  # Extract RGB values
            lp.LedCtrlXY(x+1, y+1, r, g, b, mode="pro")  # Shift coordinates to (1,1) → (8,8)

def invert_color(r, g, b):
    """Invert RGB color (63 - current value) to get a negative effect."""
    return (63 - r, 63 - g, 63 - b)

def send_led_message(lp, x, y, pressed):
    """Inverts button color while pressed and restores original color on release."""
    if x != 9 or x != 8:  # Only process center grid
        r, g, b = original_pixel_data[y-1][x]  # Get original color (adjusted for list index)
        
        if pressed:
            inv_r, inv_g, inv_b = invert_color(r, g, b)  # Invert the color
            lp.LedCtrlXY(x+1, y, inv_r, inv_g, inv_b, mode="pro")  # Show inverted color
        else:
            lp.LedCtrlXY(x+1, y, r, g, b, mode="pro")  # Restore original color

def parse_button_press(button_state, lp):
    """Handles button presses and calls the LED function."""
    if button_state:
        x, y, vel = button_state
        if(vel > 0):
            print(x, y)
        
        # Ignore buttons **outside** the center 8x8 grid
        if x == 9 or x == 8:
           
            print(f"Button at ({x}, {y}) is an outer button, ignoring.")
            return
        elif(y == 0 or y == 9):
            print(f"Button at ({x}, {y}) is an outer button, ignoring.")
            return

        if vel > 0:
            send_led_message(lp, x, y, True)  # Invert color
        else:
            send_led_message(lp, x, y, False)  # Restore original image color