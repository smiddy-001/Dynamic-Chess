# ╔════════╗
# ║♜♞♝♛♚♝♞♜║
# ║♟♟♟♟♟♟♟♟║
# ║▒█▒█▒█▒█║
# ║█▒█▒█▒█▒║
# ║▒█▒█▒█▒█║
# ║█▒█▒█▒█▒║
# ║♙♙♙♙♙♙♙♙║
# ║♖♘♗♕♔♗♘♖║
# ╚════════╝

NORMAL_CHESS_ICONS = {
    "use_xml_template": True,
    "empty": set({"▤", "▥"}),  # idk man
    "white": {
        "pawn": "♙",
        "rook": "♖",
        "knight": "♘",
        "bishop": "♗",
        "king": "♔",
        "queen": "♕",
        "wizard": "🧙"
    },
    "black": {
        "pawn": "♟",
        "rook": "♜",
        "knight": "♞",
        "bishop": "♝",
        "king": "♚",
        "queen": "♛",
        "wizard": "🧙"
},
}

# 🐙🦐🦑‍🦞🦀🦑‍🦐🐙
# 🍤🍤🍤🍤🍤🍤🍤🍤
# ⛰🌊⛰🌊⛰🌊⛰🌊
# 🌊⛰🌊⛰🌊⛰🌊⛰
# ⛰🌊⛰🌊⛰🌊⛰🌊
# 🌊⛰🌊⛰🌊⛰🌊⛰
# 👮👮👮👮👮👮👮👮
# 🏰🏇‍🤺👸🤴‍🤺🏇🏰

CRAB_CHESS_ICONS = {
    "use_xml_template": True,
    "empty": [" ", "🌊 ", "💭"],  # idk man
    "white": {  # human
        "pawn": "👮",
        "rook": "🏰",
        "knight": "🏇",
        "bishop": "🤺",
        "king": "🤴",
        "queen": "👸",
        "wizard": "🧙"
    },
    "black": {  # crab
        "pawn": "🍤",
        "rook": "🐙",
        "knight": "🦐",
        "bishop": "🦑",
        "king": "🦞",
        "queen": "🦀",
        "wizard": "🎏"
    },
}

# assuming we have tailwindcss installed
# assuming all of this is wrapped inside a div element

SQUARE_SIZE = "24px"

# attempt #1
# def TILE_XML_TEMPLATE(emoji, id, size: int, color1:str, color2:str): return f"""\
# <div id={id} style="display: grid; width: {size}px; aspect-ratio: 1; background-color: {color1}; border: 4px solid {color1}; outline: 2px {color2} solid; outline-offset: -3px;">
#     <span style="place-self: center; font-size: {(size*0.85) - 0.1}px; aspect-ratio: 1;">
#         {emoji}
#     </span>
# </div>
# """

