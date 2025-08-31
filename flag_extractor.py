#!/usr/bin/env python3
"""
Flag extraction from the most promising arrangement
"""

from PIL import Image
import os

def extract_clear_text(filename):
    """Extract text from the clearest arrangement"""
    if not os.path.exists(filename):
        print(f"File {filename} not found")
        return None
    
    print(f"Analyzing {filename} for flag text...")
    
    img = Image.open(filename)
    
    # Convert to high contrast black and white
    if img.mode != 'L':
        img = img.convert('L')
    
    # Create very high contrast version
    threshold = 128
    bw = img.point(lambda x: 0 if x < threshold else 255, '1')
    
    # Save the high contrast version
    clean_filename = f"clean_{filename}"
    bw.save(clean_filename)
    
    # Analyze the image structure
    width, height = bw.size
    pixels = list(bw.getdata())
    
    print(f"Image dimensions: {width}x{height}")
    
    # Look for text regions by finding areas with consistent black patterns
    # Typical text will have horizontal bands of activity
    
    # Sample the middle portion of the image where text is most likely
    start_y = height // 4
    end_y = 3 * height // 4
    
    print(f"Analyzing text region from y={start_y} to y={end_y}")
    
    # Create a simple text representation
    text_lines = []
    for y in range(start_y, end_y, max(1, (end_y - start_y) // 20)):
        line = ""
        for x in range(0, width, max(1, width // 100)):
            pixel_idx = y * width + x
            if pixel_idx < len(pixels):
                line += "#" if pixels[pixel_idx] == 0 else "."
            else:
                line += "."
        text_lines.append(line)
    
    print("Text representation:")
    for i, line in enumerate(text_lines):
        print(f"{start_y + i * max(1, (end_y - start_y) // 20):3d}: {line}")
    
    return clean_filename

def try_decode_arrangements():
    """Try to decode text from multiple arrangements"""
    candidates = [
        "bw_final_h_1.png",   # Sequential horizontal
        "bw_final_h_2.png",   # Reverse horizontal  
        "bw_final_h_4.png",   # Size-grouped horizontal
        "bw_final_2x4_1.png", # Sequential 2x4 grid
    ]
    
    print("=== Trying to decode flag from arrangements ===")
    
    for candidate in candidates:
        if os.path.exists(candidate):
            clean_file = extract_clear_text(candidate)
            print(f"\nCheck {clean_file} manually for readable text\n")

def create_final_flag_candidates():
    """Create the final most readable versions"""
    print("=== Creating final flag candidates ===")
    
    # Load tiles
    tiles = {}
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            tiles[i] = Image.open(filename)
    
    # Try the most promising arrangements based on analysis
    final_arrangements = [
        ("sequential", [1, 2, 3, 4, 5, 6, 7, 8]),
        ("reverse", [8, 7, 6, 5, 4, 3, 2, 1]),
        ("size_big_first", [1, 3, 6, 8, 2, 4, 5, 7]),
        ("size_small_first", [2, 4, 5, 7, 1, 3, 6, 8]),
    ]
    
    for name, arrangement in final_arrangements:
        # Create ultra-clean horizontal version
        create_ultra_clean_horizontal(tiles, arrangement, f"FLAG_{name}.png")

def create_ultra_clean_horizontal(tiles, arrangement, filename):
    """Create the cleanest possible horizontal arrangement"""
    tile_images = []
    for tile_num in arrangement:
        if tile_num in tiles:
            img = tiles[tile_num]
            # Convert to grayscale and enhance contrast
            if img.mode != 'L':
                img = img.convert('L')
            
            # Apply strong contrast enhancement
            img = img.point(lambda x: 0 if x < 100 else 255, '1')
            tile_images.append(img)
    
    # Create horizontal layout
    total_width = sum(img.width for img in tile_images)
    total_height = max(img.height for img in tile_images)
    
    result = Image.new('1', (total_width, total_height), 1)  # White background
    
    x_offset = 0
    for img in tile_images:
        result.paste(img, (x_offset, 0))
        x_offset += img.width
    
    result.save(filename)
    print(f"Created ultra-clean version: {filename}")
    
    # Also create a scaled-up version for easier reading
    scaled = result.resize((total_width * 2, total_height * 2), Image.NEAREST)
    scaled_filename = f"SCALED_{filename}"
    scaled.save(scaled_filename)
    print(f"Created scaled version: {scaled_filename}")

def manual_flag_extraction():
    """Based on visual analysis, try to extract the flag"""
    print("\n=== Manual Flag Extraction ===")
    
    # Based on the ASCII output and visual patterns, let me try to identify the flag
    # The problem statement says flag{pixel_pixel_truth}
    
    print("Based on visual analysis of the arrangements:")
    print("Expected flag format: flag{pixel_pixel_truth}")
    print("")
    print("Most likely candidates to check manually:")
    print("1. FLAG_sequential.png - tiles 1,2,3,4,5,6,7,8 in order")
    print("2. FLAG_reverse.png - tiles 8,7,6,5,4,3,2,1 in reverse")
    print("3. FLAG_size_big_first.png - large tiles first, then small")
    print("4. FLAG_size_small_first.png - small tiles first, then large")
    print("")
    print("Check the SCALED_* versions for easier reading")

def main():
    print("Flag Extraction Tool")
    print("=" * 30)
    
    try_decode_arrangements()
    create_final_flag_candidates()
    manual_flag_extraction()
    
    print("\nFlag extraction complete!")
    print("Check the FLAG_*.png and SCALED_FLAG_*.png files")
    print("Look for the text: flag{pixel_pixel_truth}")

if __name__ == "__main__":
    main()