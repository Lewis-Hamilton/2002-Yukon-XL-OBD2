import os

SCREEN_HEIGHT = 20
INNER_HEIGHT  = 18
SCREEN_WIDTH  = 58
INNER_WIDTH   = 56

top_bottom_border    = '█' + '━' * INNER_WIDTH + '█'

def row(text=''):
    # return '| ' + text.ljust(INNER_WIDTH - 1)[:INNER_WIDTH - 1] + '|'
    return '█ ' + text.ljust(INNER_WIDTH - 1)[:INNER_WIDTH - 1] + '█'

def print_screen(lines):
    # Move cursor to top-left without clearing
    print('\033[H', end='')
    
    output = []
    output.append(top_bottom_border)
    for line in lines[:INNER_HEIGHT]:
        output.append(row(line))
    remaining = INNER_HEIGHT - len(lines)
    for _ in range(remaining):
        output.append(row())
    output.append(top_bottom_border)
    
    # Print everything at once to minimize flicker
    print('\n'.join(output), end='', flush=True)

def hide_cursor():
    print('\033[?25l', end='', flush=True)

def show_cursor():
    print('\033[?25h', end='', flush=True)