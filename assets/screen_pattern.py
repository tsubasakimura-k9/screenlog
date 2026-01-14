"""
Minecraft-style monitor/screen pattern for ScreenLog app.
A blocky pixel-art monitor with screen content visualization.
"""

COLORS = {
    '.': (0, 0, 0, 0),           # transparent
    # Frame colors (dark gray)
    'F': (60, 65, 70, 255),      # frame base
    'f': (45, 50, 55, 255),      # frame dark
    'D': (30, 35, 40, 255),      # frame darkest
    'H': (80, 85, 90, 255),      # frame highlight
    # Screen colors (blue)
    'B': (40, 120, 180, 255),    # screen base blue
    'b': (30, 100, 160, 255),    # screen dark blue
    'L': (60, 150, 210, 255),    # screen light blue
    'W': (100, 180, 230, 255),   # screen bright/highlight
    # Content lines (representing captured text)
    'C': (180, 220, 250, 255),   # content line (light cyan)
    'c': (140, 190, 230, 255),   # content line dim
    # Stand
    'S': (50, 55, 60, 255),      # stand
    's': (35, 40, 45, 255),      # stand dark
}

PATTERN_32 = [
    "................................",
    "................................",
    "..HHHHHHHHHHHHHHHHHHHHHHHHHH....",
    "..HFFFFFFFFFFFFFFFFFFFFFFFFD....",
    "..HFWWLLLLLLLLLLLLLLLLLLBFD....",
    "..HFLLLLLLLLLLLLLLLLLLLBBFD....",
    "..HFLLCCCCCCCCCCCCcc...BBFD....",
    "..HFLLB............BBBBBFD....",
    "..HFLLCCCCCCCCCcc......BBFD....",
    "..HFLLB............BBBBBFD....",
    "..HFLLCCCCCCCCCCCCCc...BBFD....",
    "..HFLLB............BBBBBFD....",
    "..HFLLCCCCCCCCcc.......BBFD....",
    "..HFLLB............BBBBBFD....",
    "..HFLLCCCCCCCCCCCCcc...BBFD....",
    "..HFLLB............BBBBBFD....",
    "..HFLLCCCCCCCcc........BBFD....",
    "..HFLLB............BBBbbFD....",
    "..HFBBBBBBBBBBBBBBBBBbbbFD....",
    "..HFBBBBBBBBBBBBBBBBbbbbFD....",
    "..HFbbbbbbbbbbbbbbbbbbbbFD....",
    "..HFFFFFFFFFFFFFFFFFFFFFFFDD....",
    "..DDDDDDDDDDDDDDDDDDDDDDDDDDD...",
    "..........HHHHHHHHH.............",
    "..........HFFFFFFFDD............",
    "..........HFFFFFFFDD............",
    "..........DDDDDDDDDDD...........",
    ".......HHHHHHHHHHHHHHHHHH.......",
    ".......HSSSSSSSSSSSSSSSSsD......",
    ".......DssssssssssssssssDD......",
    "................................",
    "................................",
]

PATTERN_16 = [
    "................",
    ".HHHHHHHHHHHHHD.",
    ".HFFFFFFFFFFD.D.",
    ".HFWLLLLLLBFD.D.",
    ".HFLCCCCc.BFD.D.",
    ".HFLB.....BFD.D.",
    ".HFLCCCc..BFD.D.",
    ".HFLB.....BFD.D.",
    ".HFLCCCCc.bFD.D.",
    ".HFBBBBBBbbFD.D.",
    ".HFFFFFFFFFDD.D.",
    ".DDDDDDDDDDDD.D.",
    "....HHHHHH......",
    "....HFFFFD......",
    "..HHHHHHHHHHH...",
    "..DsssssssssD...",
]
