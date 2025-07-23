#!/usr/bin/env python3
"""
Create a simple icon for the LunarBit Modpack Updater
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create a simple icon for the application"""
    # Create a 64x64 image with transparent background
    size = 64
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # LunarBit colors
    bg_color = (13, 17, 23, 255)  # Dark background
    primary_color = (88, 166, 255, 255)  # Blue accent
    
    # Draw background circle
    margin = 4
    draw.ellipse([margin, margin, size-margin, size-margin], fill=bg_color)
    
    # Draw border
    draw.ellipse([margin, margin, size-margin, size-margin], outline=primary_color, width=2)
    
    # Draw rocket emoji or simple shape
    center = size // 2
    
    # Simple rocket shape
    rocket_points = [
        (center, margin + 8),      # Top
        (center - 8, center + 8),  # Left
        (center - 4, center + 8),  # Left inner
        (center - 4, size - margin - 8),  # Left bottom
        (center + 4, size - margin - 8),  # Right bottom
        (center + 4, center + 8),  # Right inner
        (center + 8, center + 8),  # Right
    ]
    
    draw.polygon(rocket_points, fill=primary_color)
    
    # Add flames
    flame_points = [
        (center - 3, size - margin - 8),
        (center, size - margin - 2),
        (center + 3, size - margin - 8),
    ]
    draw.polygon(flame_points, fill=(248, 81, 73, 255))  # Red color
    
    return img

if __name__ == "__main__":
    try:
        icon = create_icon()
        icon.save("icon.png")
        print("Icon created successfully: icon.png")
    except ImportError:
        print("PIL (Pillow) not installed. Skipping icon creation.")
        print("Install with: pip install Pillow")
    except Exception as e:
        print(f"Error creating icon: {e}")
