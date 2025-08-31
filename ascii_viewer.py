#!/usr/bin/env python3
"""
ASCII viewer for image analysis
"""

from PIL import Image
import os

def image_to_ascii(filename, max_width=120):
    """Convert image to ASCII for analysis"""
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return
    
    print(f"\n=== ASCII view of {filename} ===")
    
    img = Image.open(filename)
    
    # Convert to grayscale
    if img.mode != 'L':
        img = img.convert('L')
    
    # Scale down if too wide
    if img.width > max_width:
        scale_factor = max_width / img.width
        new_height = int(img.height * scale_factor)
        img = img.resize((max_width, new_height), Image.LANCZOS)
    
    # Convert to ASCII
    pixels = list(img.getdata())
    width, height = img.size
    
    ascii_chars = " .:-=+*#%@"
    
    for y in range(height):
        line = ""
        for x in range(width):
            pixel_idx = y * width + x
            if pixel_idx < len(pixels):
                pixel_value = pixels[pixel_idx]
                # Map 0-255 to ASCII characters (inverted: 0=black=dense char)
                char_idx = min(len(ascii_chars) - 1, (255 - pixel_value) * len(ascii_chars) // 256)
                line += ascii_chars[char_idx]
            else:
                line += " "
        print(line.rstrip())

def analyze_key_images():
    """Analyze the most promising images"""
    key_images = [
        "bw_final_h_1.png",    # Horizontal arrangement 1
        "bw_final_h_2.png",    # Horizontal arrangement 2 (reverse)
        "bw_final_2x4_1.png",  # 2x4 grid arrangement 1
        "final_h_1.png",       # Grayscale version
    ]
    
    for img_file in key_images:
        if os.path.exists(img_file):
            image_to_ascii(img_file)
        else:
            print(f"{img_file} not found")

def simple_pixel_analysis(filename):
    """Simple pixel analysis to understand content"""
    if not os.path.exists(filename):
        return
        
    print(f"\n=== Pixel analysis of {filename} ===")
    img = Image.open(filename)
    
    if img.mode != 'L':
        img = img.convert('L')
    
    pixels = list(img.getdata())
    width, height = img.size
    
    print(f"Dimensions: {width}x{height}")
    
    # Look for text-like patterns by examining horizontal lines
    text_lines = []
    for y in range(0, height, max(1, height // 20)):  # Sample every 5% of height
        line_pixels = []
        for x in range(width):
            pixel_idx = y * width + x
            if pixel_idx < len(pixels):
                line_pixels.append(pixels[pixel_idx])
        
        # Count black pixels in this line
        black_count = sum(1 for p in line_pixels if p < 128)
        black_ratio = black_count / len(line_pixels) if line_pixels else 0
        
        if black_ratio > 0.1:  # Significant black content
            # Convert line to simple representation
            line_repr = ""
            for p in line_pixels[::max(1, width // 100)]:  # Sample pixels
                line_repr += "#" if p < 128 else "."
            text_lines.append((y, black_ratio, line_repr))
    
    print("Sample lines with text content:")
    for y, ratio, repr_line in text_lines[:10]:
        print(f"  Line {y:3d}: {ratio:.1%} black - {repr_line[:80]}")

def main():
    print("ASCII Image Viewer for CTF Analysis")
    print("=" * 50)
    
    # First do simple analysis
    key_images = ["bw_final_h_1.png", "bw_final_h_2.png", "bw_final_2x4_1.png"]
    
    for img in key_images:
        if os.path.exists(img):
            simple_pixel_analysis(img)
    
    # Then try ASCII representation
    analyze_key_images()

if __name__ == "__main__":
    main()