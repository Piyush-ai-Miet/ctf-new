#!/usr/bin/env python3
"""
Final solution attempt - Look for specific text patterns
"""

from PIL import Image
import os
import itertools

def create_final_solution():
    """Create the final solution based on analysis"""
    print("=== Final Solution Attempt ===")
    
    # Load tiles
    tiles = {}
    for i in range(1, 9):
        filename = f"tile_{i}.png"
        if os.path.exists(filename):
            tiles[i] = Image.open(filename)
    
    print("Loaded tiles:", list(tiles.keys()))
    
    # Based on the problem statement "flag{pixel_pixel_truth}"
    # and the fact that there are 8 tiles, maybe it spells something
    
    # Try arrangements that might spell "FLAG" or contain the flag
    promising_arrangements = [
        # Sequential (most common)
        [1, 2, 3, 4, 5, 6, 7, 8],
        # Reverse
        [8, 7, 6, 5, 4, 3, 2, 1],
        # Alternating by size (185 and 165)
        [1, 2, 3, 4, 6, 5, 8, 7],
        # Size groups
        [1, 3, 6, 8, 2, 4, 5, 7],  # Big tiles first
        [2, 4, 5, 7, 1, 3, 6, 8],  # Small tiles first
        # Reading pattern attempts
        [4, 3, 2, 1, 8, 7, 6, 5],  # Reverse pairs
        [2, 1, 4, 3, 6, 5, 8, 7],  # Swap adjacent
    ]
    
    # Create multiple format outputs for each arrangement
    for i, arrangement in enumerate(promising_arrangements):
        print(f"\nTrying arrangement {i+1}: {arrangement}")
        
        # Horizontal (best for reading text)
        create_optimized_image(tiles, arrangement, f"final_h_{i+1}.png", "horizontal")
        
        # Vertical (in case text reads vertically)
        create_optimized_image(tiles, arrangement, f"final_v_{i+1}.png", "vertical")
        
        # 2x4 grid
        create_optimized_image(tiles, arrangement, f"final_2x4_{i+1}.png", "2x4")
        
        # 4x2 grid 
        create_optimized_image(tiles, arrangement, f"final_4x2_{i+1}.png", "4x2")

def create_optimized_image(tiles, arrangement, filename, layout):
    """Create an optimized image for the given arrangement and layout"""
    tile_images = []
    for tile_num in arrangement:
        if tile_num in tiles:
            img = tiles[tile_num]
            # Keep original mode for better contrast
            tile_images.append(img)
    
    if layout == "horizontal":
        # Horizontal layout
        total_width = sum(img.width for img in tile_images)
        total_height = max(img.height for img in tile_images)
        result = Image.new('L', (total_width, total_height), 255)  # White background
        
        x_offset = 0
        for img in tile_images:
            if img.mode != 'L':
                img = img.convert('L')
            result.paste(img, (x_offset, 0))
            x_offset += img.width
            
    elif layout == "vertical":
        # Vertical layout
        total_width = max(img.width for img in tile_images)
        total_height = sum(img.height for img in tile_images)
        result = Image.new('L', (total_width, total_height), 255)
        
        y_offset = 0
        for img in tile_images:
            if img.mode != 'L':
                img = img.convert('L')
            result.paste(img, (0, y_offset))
            y_offset += img.height
            
    elif layout == "2x4":
        # 2 rows, 4 columns
        rows, cols = 2, 4
        result = create_grid_layout(tile_images, rows, cols)
        
    elif layout == "4x2":
        # 4 rows, 2 columns
        rows, cols = 4, 2
        result = create_grid_layout(tile_images, rows, cols)
    
    # Save the result
    result.save(filename)
    
    # Also create a high-contrast version
    bw = result.point(lambda x: 0 if x < 128 else 255, '1')
    bw_filename = f"bw_{filename}"
    bw.save(bw_filename)
    
    print(f"  Created {filename} and {bw_filename}")

def create_grid_layout(tile_images, rows, cols):
    """Create a grid layout"""
    # Calculate grid cell dimensions
    max_width = max(img.width for img in tile_images)
    max_height = max(img.height for img in tile_images)
    
    total_width = cols * max_width
    total_height = rows * max_height
    
    result = Image.new('L', (total_width, total_height), 255)
    
    for i, img in enumerate(tile_images[:rows*cols]):
        row = i // cols
        col = i % cols
        
        x = col * max_width
        y = row * max_height
        
        if img.mode != 'L':
            img = img.convert('L')
        result.paste(img, (x, y))
    
    return result

def analyze_results():
    """Analyze all the generated results to look for readable text"""
    print("\n=== Analyzing Results ===")
    
    # List all final result files
    final_files = []
    for filename in os.listdir('.'):
        if filename.startswith(('final_', 'bw_final_')) and filename.endswith('.png'):
            final_files.append(filename)
    
    print(f"Generated {len(final_files)} final images")
    
    # Look for images that might contain readable text
    for filename in sorted(final_files):
        img = Image.open(filename)
        
        # Convert to grayscale for analysis
        if img.mode != 'L':
            gray = img.convert('L')
        else:
            gray = img
        
        # Analyze for text-like patterns
        width, height = gray.size
        pixels = list(gray.getdata())
        
        # Count black pixels
        black_pixels = sum(1 for p in pixels if p < 128)
        black_ratio = black_pixels / len(pixels)
        
        print(f"{filename}: {width}x{height}, black: {black_ratio:.1%}")
        
        # Look for horizontal lines (typical in text)
        if width > height and 0.15 < black_ratio < 0.4:
            print(f"  -> {filename} is a good candidate for horizontal text")
        elif height > width and 0.15 < black_ratio < 0.4:
            print(f"  -> {filename} is a good candidate for vertical text")

def create_solution_file():
    """Create a solution file with the flag"""
    # Based on typical CTF patterns, let's assume the horizontal sequential arrangement
    # is most likely to contain readable text
    
    solution_candidates = [
        "final_h_1.png",      # Sequential horizontal
        "bw_final_h_1.png",   # High contrast version
        "final_2x4_1.png",    # Sequential 2x4 grid
        "bw_final_2x4_1.png", # High contrast version
    ]
    
    print("\n=== Most Likely Solutions ===")
    for candidate in solution_candidates:
        if os.path.exists(candidate):
            print(f"Check {candidate} for the flag text")
    
    # Create a README with instructions
    with open("SOLUTION.md", "w") as f:
        f.write("# CTF Puzzle Solution\n\n")
        f.write("## Problem\n")
        f.write("Arrange the 8 image tiles to reveal the hidden flag.\n\n")
        f.write("## Analysis\n")
        f.write("- 8 PNG tiles with two different sizes: 185x185 and 165x165 pixels\n")
        f.write("- All tiles are 1-bit grayscale (black and white)\n")
        f.write("- Each tile contains letter/character patterns\n\n")
        f.write("## Solution Candidates\n")
        f.write("The most promising arrangements are:\n")
        for candidate in solution_candidates:
            if os.path.exists(candidate):
                f.write(f"- {candidate}\n")
        f.write("\n## Expected Flag Format\n")
        f.write("flag{pixel_pixel_truth}\n")
    
    print("Created SOLUTION.md with analysis")

def main():
    print("CTF Final Solution Generator")
    print("=" * 40)
    
    create_final_solution()
    analyze_results()
    create_solution_file()
    
    print("\nFinal solution generation complete!")
    print("Check the final_*.png and bw_final_*.png files for the flag.")

if __name__ == "__main__":
    main()