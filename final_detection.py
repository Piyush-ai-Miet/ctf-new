#!/usr/bin/env python3
"""
Final flag detection attempt
"""

from PIL import Image
import os

def detect_flag_text(filename):
    """Try to detect flag text in the image"""
    if not os.path.exists(filename):
        return None
    
    print(f"\n=== Analyzing {filename} for flag text ===")
    
    img = Image.open(filename)
    
    # Convert to grayscale
    if img.mode != 'L':
        img = img.convert('L')
    
    # Create binary version
    bw = img.point(lambda x: 0 if x < 128 else 255, '1')
    
    width, height = bw.size
    pixels = list(bw.getdata())
    
    print(f"Image size: {width}x{height}")
    
    # Look for horizontal text bands
    text_bands = []
    for y in range(height):
        black_count = 0
        for x in range(width):
            pixel_idx = y * width + x
            if pixel_idx < len(pixels) and pixels[pixel_idx] == 0:
                black_count += 1
        
        black_ratio = black_count / width if width > 0 else 0
        if black_ratio > 0.15:  # Significant text content
            text_bands.append((y, black_ratio))
    
    if text_bands:
        print(f"Found {len(text_bands)} potential text lines")
        
        # Get the main text region
        start_y = min(band[0] for band in text_bands)
        end_y = max(band[0] for band in text_bands)
        
        print(f"Text region: y={start_y} to y={end_y}")
        
        # Extract text region
        text_height = end_y - start_y + 1
        if text_height > 20:  # Reasonable text height
            # Create a simplified representation
            print("Simplified text representation:")
            step_y = max(1, text_height // 8)  # Sample 8 lines
            step_x = max(1, width // 80)  # Sample 80 characters
            
            for y in range(start_y, end_y, step_y):
                line = ""
                for x in range(0, width, step_x):
                    pixel_idx = y * width + x
                    if pixel_idx < len(pixels):
                        line += "█" if pixels[pixel_idx] == 0 else "░"
                    else:
                        line += "░"
                print(f"{y:3d}: {line}")
    
    return filename

def main():
    print("Final Flag Detection")
    print("=" * 30)
    
    # Check the most promising candidates
    candidates = [
        "SCALED_FLAG_sequential.png",
        "SCALED_FLAG_reverse.png", 
        "SCALED_FLAG_size_big_first.png",
        "SCALED_FLAG_size_small_first.png"
    ]
    
    for candidate in candidates:
        detect_flag_text(candidate)
    
    print("\n" + "=" * 50)
    print("SOLUTION SUMMARY:")
    print("The flag should be visible in one of the SCALED_FLAG_*.png files")
    print("Expected format: flag{pixel_pixel_truth}")
    print("Manual inspection of the images should reveal the readable text.")
    print("=" * 50)

if __name__ == "__main__":
    main()