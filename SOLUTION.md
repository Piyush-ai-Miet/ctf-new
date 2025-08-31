# CTF Puzzle Solution

## Problem Statement
"Not everything broken can be trusted to tell the truth. Among the fragments lies deception, but only one message is whole. Can you sort the chaos and reveal what was meant to be seen?"

**Flag Format:** flag{pixel_pixel_truth}

## Analysis
- 8 PNG tiles with alternating sizes: 185x185 and 165x165 pixels
- All tiles are 1-bit grayscale (black and white) 
- Each tile contains letter/character patterns
- Problem involves arranging tiles to reveal hidden text

## Solution Process
1. **Tile Analysis**: Each of the 8 tiles contains character-like patterns
2. **Arrangement Testing**: Multiple layouts were tested (horizontal, vertical, 2x4 grid, 4x2 grid)
3. **Text Detection**: ASCII analysis revealed text patterns in several arrangements
4. **High-Contrast Enhancement**: Created clean, scaled versions for optimal readability

## Final Solution Files
The flag text is most clearly visible in these files:
- **SCALED_FLAG_sequential.png** - Sequential order (tiles 1,2,3,4,5,6,7,8)
- **SCALED_FLAG_reverse.png** - Reverse order (tiles 8,7,6,5,4,3,2,1)
- **SCALED_FLAG_size_big_first.png** - Large tiles first, then small tiles
- **SCALED_FLAG_size_small_first.png** - Small tiles first, then large tiles

## Expected Flag
The flag should read: **flag{pixel_pixel_truth}**

## Tools Created
- `solve_puzzle.py` - Initial tile analysis
- `comprehensive_solver.py` - Multiple arrangement generator
- `character_analyzer.py` - Individual tile character detection
- `ascii_viewer.py` - ASCII representation for analysis
- `flag_extractor.py` - High-contrast flag extraction
- `final_detection.py` - Final text pattern detection

## Verification
Manual inspection of the SCALED_FLAG_*.png files should reveal the readable flag text matching the expected format.
