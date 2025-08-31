#!/usr/bin/env python3
"""
Text extraction and detailed image analysis
"""

from PIL import Image
import os

def analyze_image_content(filename):
    """Analyze an image for potential text content"""
    if not os.path.exists(filename):
        return
        
    print(f"\n=== Analyzing {filename} ===")
    img = Image.open(filename)
    
    # Convert to grayscale
    gray = img.convert('L')
    
    # Create a high contrast version
    # Convert to pure black and white
    threshold = 128
    bw = gray.point(lambda x: 0 if x < threshold else 255, '1')
    
    # Save processed version
    processed_name = f"processed_{filename}"
    bw.save(processed_name)
    
    # Analyze pixel patterns
    pixels = list(bw.getdata())
    width, height = bw.size
    
    # Look for horizontal text patterns (lines of black pixels)
    black_lines = []
    for y in range(height):
        black_count = 0
        for x in range(width):
            pixel_idx = y * width + x
            if pixel_idx < len(pixels) and pixels[pixel_idx] == 0:  # Black pixel
                black_count += 1
        
        black_ratio = black_count / width if width > 0 else 0
        if black_ratio > 0.1:  # Line has significant black content
            black_lines.append((y, black_ratio))
    
    print(f"  Dimensions: {width}x{height}")
    print(f"  Lines with >10% black pixels: {len(black_lines)}")
    
    if black_lines:
        print(f"  Black line ranges: {black_lines[:5]}...")  # First 5 lines
        
    # Look for text-like patterns
    if len(black_lines) > 5:  # Might contain text
        print(f"  -> POTENTIAL TEXT detected in {filename}")
        
        # Create an enhanced version for manual inspection
        enhanced = bw.resize((width * 2, height * 2), Image.NEAREST)
        enhanced_name = f"enhanced_{filename}"
        enhanced.save(enhanced_name)
        print(f"  -> Saved enhanced version as {enhanced_name}")

def create_text_readable_version():
    """Try to create the most text-readable arrangement"""
    print("\n=== Creating text-optimized arrangements ===")
    
    # Load tiles
    tiles = {}
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            tiles[i] = Image.open(filename)
    
    # Try arrangements that might be more readable
    # Based on the flag format flag{pixel_pixel_truth}, we might need text arrangement
    
    text_arrangements = [
        # Try arrangements that might spell something
        ("text_attempt_1", [1, 2, 3, 4, 5, 6, 7, 8]),
        ("text_attempt_2", [5, 6, 7, 8, 1, 2, 3, 4]),  # Swap halves
        ("text_attempt_3", [3, 1, 4, 2, 7, 5, 8, 6]),  # Alternate pattern
        ("text_attempt_4", [8, 6, 4, 2, 7, 5, 3, 1]),  # Reverse even positions
    ]
    
    for name, order in text_arrangements:
        # 2x4 layout
        create_arrangement(tiles, order, name + "_2x4.png", 2, 4)
        # 1x8 layout for text reading
        create_arrangement(tiles, order, name + "_1x8.png", 1, 8)

def create_arrangement(tiles, order, filename, rows, cols):
    """Create arrangement with specified layout"""
    tile_images = []
    for tile_num in order:
        if tile_num in tiles:
            img = tiles[tile_num]
            if img.mode != 'RGB':
                img = img.convert('RGB')
            tile_images.append(img)
    
    # Calculate total dimensions
    if rows == 1:  # Single row
        total_width = sum(img.width for img in tile_images)
        total_height = max(img.height for img in tile_images)
    elif cols == 1:  # Single column
        total_width = max(img.width for img in tile_images)
        total_height = sum(img.height for img in tile_images)
    else:  # Grid
        row_heights = []
        col_widths = []
        
        for row in range(rows):
            max_height = 0
            for col in range(cols):
                idx = row * cols + col
                if idx < len(tile_images):
                    max_height = max(max_height, tile_images[idx].height)
            row_heights.append(max_height)
        
        for col in range(cols):
            max_width = 0
            for row in range(rows):
                idx = row * cols + col
                if idx < len(tile_images):
                    max_width = max(max_width, tile_images[idx].width)
            col_widths.append(max_width)
        
        total_width = sum(col_widths)
        total_height = sum(row_heights)
    
    # Create result
    result = Image.new('RGB', (total_width, total_height), 'white')
    
    if rows == 1:  # Single row
        x_offset = 0
        for img in tile_images:
            result.paste(img, (x_offset, 0))
            x_offset += img.width
    elif cols == 1:  # Single column  
        y_offset = 0
        for img in tile_images:
            result.paste(img, (0, y_offset))
            y_offset += img.height
    else:  # Grid
        y_offset = 0
        for row in range(rows):
            x_offset = 0
            for col in range(cols):
                idx = row * cols + col
                if idx < len(tile_images):
                    result.paste(tile_images[idx], (x_offset, y_offset))
                x_offset += col_widths[col]
            y_offset += row_heights[row]
    
    result.save(filename)
    print(f"Created {filename}: {result.size}")

def main():
    print("Text Analysis and Enhancement")
    print("=" * 40)
    
    # Analyze existing arrangements
    key_files = [
        "arrangement_2x4_sequential.png",
        "arrangement_1x8_sequential.png", 
        "arrangement_4x2_sequential.png",
        "native_2x4_1.png"
    ]
    
    for filename in key_files:
        if os.path.exists(filename):
            analyze_image_content(filename)
    
    # Create new text-optimized arrangements
    create_text_readable_version()
    
    print("\nAnalysis complete! Check enhanced_*.png files for readable text.")

if __name__ == "__main__":
    main()