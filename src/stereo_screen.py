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
    # Move cursor to top-left without clearing
    print('\033[H', end='')
    
    output = []
    output.append(divider)
    for line in lines[:INNER_HEIGHT]:
        output.append(row(line))
    remaining = INNER_HEIGHT - len(lines)
    for _ in range(remaining):
        output.append(row())
    output.append(divider)
    
    # Print everything at once to minimize flicker
    print('\n'.join(output), end='', flush=True)

def hide_cursor():
    print('\033[?25l', end='', flush=True)

def show_cursor():
    print('\033[?25h', end='', flush=True)