#!/usr/bin/env python3
"""
Character/letter detection in individual tiles
"""

from PIL import Image
import os

def analyze_individual_tile_content():
    """Analyze each tile to see if it contains letter-like patterns"""
    print("=== Individual Tile Analysis ===")
    
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if not os.path.exists(filename):
            continue
            
        print(f"\n--- Tile {i} ---")
        img = Image.open(filename)
        
        # Convert to grayscale and then black/white
        gray = img.convert('L')
        bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
        
        width, height = bw.size
        pixels = list(bw.getdata())
        
        # Count black pixels
        black_pixels = sum(1 for p in pixels if p == 0)
        total_pixels = len(pixels)
        black_ratio = black_pixels / total_pixels
        
        print(f"Size: {width}x{height}, Black ratio: {black_ratio:.2%}")
        
        # Look for character-like features
        # Check if black pixels form concentrated areas (like letters)
        black_regions = find_black_regions(pixels, width, height)
        print(f"Black regions found: {len(black_regions)}")
        
        # Create an enhanced version for inspection
        enhanced = bw.resize((width * 4, height * 4), Image.NEAREST)
        enhanced_filename = f"tile_{i}_enhanced.png"
        enhanced.save(enhanced_filename)
        
        # Try to identify if this looks like a letter
        if black_ratio > 0.05 and black_ratio < 0.5:  # Reasonable for letters
            print(f"  -> Tile {i} might contain a letter/character")

def find_black_regions(pixels, width, height):
    """Find connected regions of black pixels"""
    visited = set()
    regions = []
    
    def flood_fill(start_x, start_y):
        """Flood fill to find connected black pixels"""
        stack = [(start_x, start_y)]
        region = []
        
        while stack:
            x, y = stack.pop()
            if (x, y) in visited or x < 0 or x >= width or y < 0 or y >= height:
                continue
                
            pixel_idx = y * width + x
            if pixel_idx >= len(pixels) or pixels[pixel_idx] != 0:  # Not black
                continue
                
            visited.add((x, y))
            region.append((x, y))
            
            # Add neighbors
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                stack.append((x + dx, y + dy))
        
        return region
    
    # Find all black regions
    for y in range(height):
        for x in range(width):
            if (x, y) not in visited:
                pixel_idx = y * width + x
                if pixel_idx < len(pixels) and pixels[pixel_idx] == 0:  # Black pixel
                    region = flood_fill(x, y)
                    if len(region) > 10:  # Ignore tiny regions
                        regions.append(region)
    
    return regions

def try_reading_order():
    """Try different reading orders based on potential letter content"""
    print("\n=== Trying Reading Orders ===")
    
    # Load tiles
    tiles = {}
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            tiles[i] = Image.open(filename)
    
    # Try different reading patterns
    reading_orders = [
        # Left to right, top to bottom
        ("left_to_right", [1, 2, 3, 4, 5, 6, 7, 8]),
        # Right to left
        ("right_to_left", [8, 7, 6, 5, 4, 3, 2, 1]),
        # Potential word arrangement
        ("word_order", [3, 1, 4, 2, 7, 5, 8, 6]),
        # Size-based arrangement
        ("by_size", [1, 3, 6, 8, 2, 4, 5, 7]),  # 185px first, then 165px
        ("by_size_rev", [2, 4, 5, 7, 1, 3, 6, 8]),  # 165px first, then 185px
        # Checkerboard pattern
        ("checkerboard", [1, 2, 6, 5, 3, 4, 8, 7]),
    ]
    
    for name, order in reading_orders:
        # Create horizontal arrangement (good for reading text)
        create_horizontal_text(tiles, order, f"reading_{name}.png")

def create_horizontal_text(tiles, order, filename):
    """Create a horizontal arrangement optimized for text reading"""
    tile_images = []
    for tile_num in order:
        if tile_num in tiles:
            img = tiles[tile_num]
            if img.mode != 'RGB':
                img = img.convert('RGB')
            tile_images.append(img)
    
    # Calculate total dimensions for horizontal layout
    total_width = sum(img.width for img in tile_images)
    total_height = max(img.height for img in tile_images)
    
    # Create result
    result = Image.new('RGB', (total_width, total_height), 'white')
    
    # Place tiles horizontally
    x_offset = 0
    for img in tile_images:
        result.paste(img, (x_offset, 0))
        x_offset += img.width
    
    result.save(filename)
    print(f"Created {filename}: {result.size}")
    
    # Also create an enhanced black/white version
    gray = result.convert('L')
    bw = gray.point(lambda x: 0 if x < 128 else 255, '1')
    bw_enhanced = bw.resize((bw.width * 2, bw.height * 2), Image.NEAREST)
    bw_filename = f"bw_{filename}"
    bw_enhanced.save(bw_filename)
    print(f"  Enhanced B/W version: {bw_filename}")

def main():
    print("Character Detection and Reading Order Analysis")
    print("=" * 50)
    
    analyze_individual_tile_content()
    try_reading_order()
    
    print("\nDone! Check the reading_*.png and bw_reading_*.png files for text.")

if __name__ == "__main__":
    main()