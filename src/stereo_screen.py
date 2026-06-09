import os

SCREEN_HEIGHT = 19
INNER_HEIGHT  = 17
SCREEN_WIDTH  = 58
INNER_WIDTH   = 56

divider    = '+' + '-' * INNER_WIDTH + '+'
altdivider = '-' + '+' * INNER_WIDTH + '-'

def row(text=''):
    return '| ' + text.ljust(INNER_WIDTH - 1)[:INNER_WIDTH - 1] + '|'

def print_screen(lines):
    os.system('clear')
    print(divider)  # Top border
    
    for line in lines[:INNER_HEIGHT]:
        print(row(line))  # Wrap each line in border
    
    # Pad remaining rows
    remaining = INNER_HEIGHT - len(lines)
    for _ in range(remaining):
        print(row())
    
    print(divider)  # Bottom border