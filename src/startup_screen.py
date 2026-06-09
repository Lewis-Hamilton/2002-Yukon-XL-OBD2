import time
import os
from stereo_screen import print_screen, INNER_WIDTH, INNER_HEIGHT

DELAY = 1

def startup_screen(connect_thread):
    # Perfectly symmetrical 15-character wide G
    G = [
        "░░░░░░░░░░░░░░░",
        "░░░░░░░░░░░░░░░",
        "░░░░           ",
        "░░░░           ",
        "░░░░     ░░░░░░",
        "░░░░     ░░░░░░",
        "░░░░       ░░░░",
        "░░░░       ░░░░",
        "░░░░░░░░░░░░░░░",
        "░░░░░░░░░░░░░░░",
        "               "
    ]

    # Cleaned up and perfectly symmetrical 15-character wide M
    # Outer pillars: 4 blocks. Center point: 3 blocks.
    M = [
        "░░░░        ░░░░",
        "░░░░░░    ░░░░░░",
        "░░░░░░░░░░░░░░░░",
        "░░░░░░░░░░░░░░░░",
        "░░░░ ░░░░░░ ░░░░",
        "░░░░  ░░░░  ░░░░",
        "░░░░        ░░░░",
        "░░░░        ░░░░",
        "░░░░        ░░░░",
        "░░░░        ░░░░",
        "                "
    ]

    # Perfectly symmetrical 15-character wide C
    C = [
        "░░░░░░░░░░░░░░░",
        "░░░░░░░░░░░░░░░",
        "░░░░           ",
        "░░░░           ",
        "░░░░           ",
        "░░░░           ",
        "░░░░           ",
        "░░░░           ",
        "░░░░░░░░░░░░░░░",
        "░░░░░░░░░░░░░░░",
        "               "
    ]

    # Hardcoded spacers to balance the 52-character constraint perfectly
    spacer = "   "   # 3 spaces

    letter_height = len(G)
    v_pad = (INNER_HEIGHT - letter_height) // 2
    blank = [' ' * len(G[0])] * letter_height

    def make_frame(g_lines, m_lines, c_lines):
        lines = [''] * v_pad
        for g, m, c in zip(g_lines, m_lines, c_lines):
            # 1 (pad) + 15 (G) + 3 (spacer1) + 15 (M) + 4 (spacer2) + 15 (C) = 53 characters exactly.
            lines.append(' ' + g + spacer + m + spacer + c)
        lines += [''] * v_pad
        return lines

    # Show G
    print_screen(make_frame(G, blank, blank))
    time.sleep(DELAY)

    # Show G + M
    print_screen(make_frame(G, M, blank))
    time.sleep(DELAY)

    # Show G + M + C and wait for connection
    print_screen(make_frame(G, M, C))
    while connect_thread.is_alive():
        time.sleep(0.5)