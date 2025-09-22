GAME_STATES = [
    # Starting Game - Fresh Board
    {
        "name": "Starting Game - Fresh Board",
        "board": [
            [1, 0, 2, 0],
            [0, 3, 0, 1],
            [2, 0, 1, 0],
            [0, 1, 0, 2]
        ],
        "score": 0,
        "moves": 0
    },
    
    # Early Game - First Merges
    {
        "name": "Early Game - First Merges",
        "board": [
            [3, 2, 6, 1],
            [1, 0, 3, 2],
            [2, 3, 1, 0],
            [0, 6, 2, 3]
        ],
        "score": 45,
        "moves": 8
    },
    
    # Mid Game - Building Up
    {
        "name": "Mid Game - Building Up",
        "board": [
            [12, 24, 6, 3],
            [48, 3, 12, 6],
            [6, 12, 24, 1],
            [3, 48, 6, 2]
        ],
        "score": 387,
        "moves": 45
    },
    
    # Advanced Game - Getting Crowded
    {
        "name": "Advanced Game - Getting Crowded",
        "board": [
            [96, 192, 48, 24],
            [384, 96, 192, 48],
            [48, 384, 96, 24],
            [24, 48, 192, 12]
        ],
        "score": 2156,
        "moves": 89
    },
    
    # Late Game - High Values
    {
        "name": "Late Game - High Values",
        "board": [
            [768, 1536, 384, 192],
            [3072, 768, 1536, 384],
            [384, 3072, 768, 192],
            [192, 384, 1536, 96]
        ],
        "score": 18945,
        "moves": 156
    },
    
    # Expert Game - Massive Numbers
    {
        "name": "Expert Game - Massive Numbers",
        "board": [
            [6144, 12288, 3072, 1536],
            [24576, 6144, 12288, 3072],
            [3072, 24576, 6144, 1536],
            [1536, 3072, 12288, 768]
        ],
        "score": 125670,
        "moves": 234
    },
    
    # Empty Board
    {
        "name": "Empty Board",
        "board": [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        "score": 0,
        "moves": 0
    },
    
    # Single Large Tile
    {
        "name": "Single Large Tile",
        "board": [
            [0, 0, 0, 0],
            [0, 49152, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ],
        "score": 49152,
        "moves": 500
    },
    
    # Mixed Width Challenge
    {
        "name": "Mixed Width Challenge",
        "board": [
            [1, 12345, 2, 3],
            [67890, 6, 789, 12],
            [3, 456, 24, 1],
            [2, 3, 98765, 6]
        ],
        "score": 195678,
        "moves": 123
    }
]
