#!/usr/bin/env python3
"""
Comprehensive tile arrangement solver for CTF
"""

from PIL import Image
import os
import itertools

def load_tiles():
    """Load all tiles"""
    tiles = {}
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            tiles[i] = Image.open(filename)
    return tiles

def create_grid_arrangement(tiles, tile_order, rows, cols, output_name):
    """Create a grid arrangement of tiles"""
    if len(tile_order) != rows * cols:
        return False
    
    # Get all tiles and convert to RGB
    tile_images = []
    for tile_num in tile_order:
        if tile_num in tiles:
            img = tiles[tile_num]
            if img.mode != 'RGB':
                img = img.convert('RGB')
            tile_images.append(img)
        else:
            return False
    
    # Calculate grid dimensions (using original tile sizes)
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
    
    # Create result image
    result = Image.new('RGB', (total_width, total_height), 'white')
    
    # Place tiles
    y_offset = 0
    for row in range(rows):
        x_offset = 0
        for col in range(cols):
            idx = row * cols + col
            if idx < len(tile_images):
                tile = tile_images[idx]
                result.paste(tile, (x_offset, y_offset))
            x_offset += col_widths[col]
        y_offset += row_heights[row]
    
    result.save(output_name)
    print(f"Saved {output_name}: {result.size}")
    return True

def try_all_arrangements():
    """Try various systematic arrangements"""
    tiles = load_tiles()
    if len(tiles) != 8:
        print(f"Error: Expected 8 tiles, found {len(tiles)}")
        return
    
    print("Trying systematic arrangements...")
    
    # Common arrangements to try
    arrangements = [
        # 2x4 arrangements
        ("2x4_sequential", [1, 2, 3, 4, 5, 6, 7, 8], 2, 4),
        ("2x4_by_size", [1, 3, 6, 8, 2, 4, 5, 7], 2, 4),
        ("2x4_reverse_size", [2, 4, 5, 7, 1, 3, 6, 8], 2, 4),
        
        # 4x2 arrangements  
        ("4x2_sequential", [1, 2, 3, 4, 5, 6, 7, 8], 4, 2),
        ("4x2_by_size", [1, 3, 2, 4, 6, 5, 8, 7], 4, 2),
        
        # 1x8 arrangement
        ("1x8_sequential", [1, 2, 3, 4, 5, 6, 7, 8], 1, 8),
        ("1x8_reverse", [8, 7, 6, 5, 4, 3, 2, 1], 1, 8),
        
        # 8x1 arrangement
        ("8x1_sequential", [1, 2, 3, 4, 5, 6, 7, 8], 8, 1),
    ]
    
    for name, order, rows, cols in arrangements:
        output_file = f"arrangement_{name}.png"
        create_grid_arrangement(tiles, order, rows, cols, output_file)

def try_permutations_sample():
    """Try a sample of permutations to find meaningful arrangements"""
    tiles = load_tiles()
    
    print("\nTrying sample permutations...")
    
    # Try some specific permutations that might make sense
    specific_perms = [
        [1, 2, 3, 4, 5, 6, 7, 8],  # Sequential
        [8, 7, 6, 5, 4, 3, 2, 1],  # Reverse
        [1, 3, 5, 7, 2, 4, 6, 8],  # Odd first, then even
        [2, 4, 6, 8, 1, 3, 5, 7],  # Even first, then odd
        [4, 3, 2, 1, 8, 7, 6, 5],  # Reverse pairs
        [5, 6, 7, 8, 1, 2, 3, 4],  # Split and swap
    ]
    
    for i, perm in enumerate(specific_perms):
        output_file = f"perm_{i+1:02d}.png"
        create_grid_arrangement(tiles, perm, 2, 4, output_file)

def examine_for_text():
    """Look for text patterns in the arrangements"""
    print("\nChecking arrangements for readable text...")
    
    # List all arrangement files
    arrangement_files = []
    for filename in os.listdir('.'):
        if filename.startswith('arrangement_') and filename.endswith('.png'):
            arrangement_files.append(filename)
        elif filename.startswith('perm_') and filename.endswith('.png'):
            arrangement_files.append(filename)
        elif filename.startswith('native_') and filename.endswith('.png'):
            arrangement_files.append(filename)
    
    for filename in sorted(arrangement_files):
        img = Image.open(filename)
        print(f"{filename}: {img.size} pixels")
        
        # Convert to grayscale for analysis
        gray = img.convert('L')
        
        # Get pixel data
        pixels = list(gray.getdata())
        
        # Count black vs white pixels
        black_pixels = sum(1 for p in pixels if p < 128)
        total_pixels = len(pixels)
        black_ratio = black_pixels / total_pixels
        
        print(f"  Black pixels: {black_pixels}/{total_pixels} ({black_ratio:.2%})")
        
        if 0.1 < black_ratio < 0.4:  # Reasonable amount of black for text
            print(f"  -> {filename} might contain text!")

def main():
    print("CTF Puzzle Comprehensive Solver")
    print("=" * 40)
    
    try_all_arrangements()
    try_permutations_sample()
    examine_for_text()
    
    print("\nDone! Check the generated images for readable text/flags.")

if __name__ == "__main__":
    main()