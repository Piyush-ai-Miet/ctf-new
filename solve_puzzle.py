#!/usr/bin/env python3
"""
CTF Puzzle Solver - Arrange image tiles to reveal the hidden message
"""

from PIL import Image
import os
import itertools

def load_tiles():
    """Load all tile images and return them with their info"""
    tiles = {}
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            img = Image.open(filename)
            tiles[i] = {
                'image': img,
                'size': img.size,
                'filename': filename
            }
            print(f"Loaded {filename}: {img.size} pixels, mode: {img.mode}")
    return tiles

def examine_tile_content(tiles):
    """Examine the visual content of each tile"""
    print("\n=== Examining tile contents ===")
    for tile_num, tile_info in tiles.items():
        img = tile_info['image']
        # Convert to RGB for easier analysis
        if img.mode != 'RGB':
            img_rgb = img.convert('RGB')
        else:
            img_rgb = img
        
        # Get some sample pixels to understand the content
        width, height = img.size
        pixels = list(img_rgb.getdata())
        
        # Count unique colors
        unique_colors = set(pixels)
        print(f"Tile {tile_num}: {len(unique_colors)} unique colors")
        
        # Sample some pixels
        sample_pixels = [pixels[i] for i in range(0, len(pixels), len(pixels)//10)]
        print(f"  Sample pixels: {sample_pixels[:5]}")

def create_arrangement(tiles, arrangement):
    """Create an arrangement of tiles based on the given order"""
    # First, let's try a 2x4 arrangement
    rows = 2
    cols = 4
    
    if len(arrangement) != 8:
        return None
    
    # Calculate total dimensions
    # For now, assume all tiles should be the same size for arrangement
    # We'll use the most common size or resize as needed
    target_size = (200, 200)  # Standard size for arrangement
    
    total_width = cols * target_size[0]
    total_height = rows * target_size[1]
    
    # Create new image
    result = Image.new('RGB', (total_width, total_height), 'white')
    
    for i, tile_num in enumerate(arrangement):
        if tile_num not in tiles:
            continue
            
        tile_img = tiles[tile_num]['image']
        # Resize tile if needed
        if tile_img.size != target_size:
            tile_img = tile_img.resize(target_size, Image.LANCZOS)
        
        # Convert to RGB if needed
        if tile_img.mode != 'RGB':
            tile_img = tile_img.convert('RGB')
        
        # Calculate position
        row = i // cols
        col = i % cols
        x = col * target_size[0]
        y = row * target_size[1]
        
        # Paste tile
        result.paste(tile_img, (x, y))
    
    return result

def try_arrangements(tiles):
    """Try different arrangements to find the correct one"""
    print("\n=== Trying arrangements ===")
    
    # Start with the natural order
    arrangements_to_try = [
        [1, 2, 3, 4, 5, 6, 7, 8],  # Natural order
        [1, 3, 6, 8, 2, 4, 5, 7],  # Group by size
        [2, 4, 5, 7, 1, 3, 6, 8],  # Reverse size grouping
    ]
    
    for i, arrangement in enumerate(arrangements_to_try):
        print(f"Trying arrangement {i+1}: {arrangement}")
        result = create_arrangement(tiles, arrangement)
        if result:
            filename = f"arrangement_{i+1}.png"
            result.save(filename)
            print(f"  Saved as {filename}")

def main():
    print("CTF Puzzle Solver - Image Tile Arrangement")
    print("=" * 50)
    
    # Load all tiles
    tiles = load_tiles()
    
    if not tiles:
        print("No tiles found!")
        return
    
    # Examine content
    examine_tile_content(tiles)
    
    # Try different arrangements
    try_arrangements(tiles)
    
    print("\nCheck the generated arrangement images to see if any reveal the flag!")

if __name__ == "__main__":
    main()