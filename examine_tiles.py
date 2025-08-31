#!/usr/bin/env python3
"""
Individual tile examiner - Look at each tile in detail
"""

from PIL import Image
import os

def examine_individual_tiles():
    """Save each tile as a larger image for manual inspection"""
    print("=== Examining individual tiles ===")
    
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            img = Image.open(filename)
            
            # Convert to RGB and scale up for easier viewing
            if img.mode != 'RGB':
                img_rgb = img.convert('RGB')
            else:
                img_rgb = img
                
            # Scale up by 3x for easier viewing
            scaled = img_rgb.resize((img_rgb.width * 3, img_rgb.height * 3), Image.NEAREST)
            
            output_filename = f"tile_{i}_scaled.png"
            scaled.save(output_filename)
            print(f"Saved {output_filename} - Original size: {img.size}, Scaled size: {scaled.size}")

def try_native_size_arrangements():
    """Try arrangements respecting the original tile sizes"""
    print("\n=== Trying arrangements with native sizes ===")
    
    # Load tiles
    tiles = {}
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            tiles[i] = Image.open(filename)
    
    # Group by size
    size_185 = [i for i in tiles.keys() if tiles[i].size == (185, 185)]
    size_165 = [i for i in tiles.keys() if tiles[i].size == (165, 165)]
    
    print(f"185x185 tiles: {size_185}")
    print(f"165x165 tiles: {size_165}")
    
    # Try different grid arrangements
    arrangements = [
        # 2x4 grid
        ([1, 2, 3, 4], [5, 6, 7, 8]),
        # 4x2 grid  
        ([1, 2], [3, 4], [5, 6], [7, 8]),
        # Mixed arrangements
        ([1, 3, 6, 8], [2, 4, 5, 7]),  # Group by size
    ]
    
    for idx, arrangement in enumerate(arrangements):
        if len(arrangement) == 2 and len(arrangement[0]) == 4:  # 2x4
            create_2x4_arrangement(tiles, arrangement, f"native_2x4_{idx+1}.png")
        elif len(arrangement) == 4 and len(arrangement[0]) == 2:  # 4x2
            create_4x2_arrangement(tiles, arrangement, f"native_4x2_{idx+1}.png")
        elif len(arrangement) == 2:  # Custom 2-row
            create_custom_arrangement(tiles, arrangement, f"native_custom_{idx+1}.png")

def create_2x4_arrangement(tiles, arrangement, filename):
    """Create a 2x4 arrangement"""
    row1_tiles = [tiles[i] for i in arrangement[0]]
    row2_tiles = [tiles[i] for i in arrangement[1]]
    
    # Calculate dimensions
    row1_width = sum(tile.width for tile in row1_tiles)
    row2_width = sum(tile.width for tile in row2_tiles)
    total_width = max(row1_width, row2_width)
    
    row1_height = max(tile.height for tile in row1_tiles)
    row2_height = max(tile.height for tile in row2_tiles)
    total_height = row1_height + row2_height
    
    # Create result image
    result = Image.new('RGB', (total_width, total_height), 'white')
    
    # Place row 1
    x_offset = 0
    for tile in row1_tiles:
        if tile.mode != 'RGB':
            tile = tile.convert('RGB')
        result.paste(tile, (x_offset, 0))
        x_offset += tile.width
    
    # Place row 2
    x_offset = 0
    for tile in row2_tiles:
        if tile.mode != 'RGB':
            tile = tile.convert('RGB')
        result.paste(tile, (x_offset, row1_height))
        x_offset += tile.width
    
    result.save(filename)
    print(f"Saved {filename} (2x4): {result.size}")

def create_custom_arrangement(tiles, arrangement, filename):
    """Create a custom arrangement with two rows"""
    row1_tiles = [tiles[i] for i in arrangement[0]]
    row2_tiles = [tiles[i] for i in arrangement[1]]
    
    # Calculate dimensions
    row1_width = sum(tile.width for tile in row1_tiles)
    row2_width = sum(tile.width for tile in row2_tiles)
    total_width = max(row1_width, row2_width)
    
    row1_height = max(tile.height for tile in row1_tiles)
    row2_height = max(tile.height for tile in row2_tiles)
    total_height = row1_height + row2_height
    
    # Create result image
    result = Image.new('RGB', (total_width, total_height), 'white')
    
    # Place row 1
    x_offset = 0
    for tile in row1_tiles:
        if tile.mode != 'RGB':
            tile = tile.convert('RGB')
        result.paste(tile, (x_offset, 0))
        x_offset += tile.width
    
    # Place row 2
    x_offset = 0
    for tile in row2_tiles:
        if tile.mode != 'RGB':
            tile = tile.convert('RGB')
        result.paste(tile, (x_offset, row1_height))
        x_offset += tile.width
    
    result.save(filename)
    print(f"Saved {filename} (custom): {result.size}")

def main():
    examine_individual_tiles()
    try_native_size_arrangements()

if __name__ == "__main__":
    main()