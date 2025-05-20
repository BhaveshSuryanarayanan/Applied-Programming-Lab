import matplotlib.pyplot as plt
import numpy as np

KEYBOARD_BG_COLOR = '#1c1c1c'
KEY_FONT = 'DejaVu Sans Mono'
DEFAULT_KEY_COLOR = '#656363'

class Key:
    def __init__(self, ind, char,row,col, shift_char=None,freq=0):
        self.ind = ind
        self.char = char
        self.shift_char = shift_char
        self.freq=freq
        self.row = row
        self.col = col

listed_keyboard_layout = [
    [['ESC'], ['F1'], ['F2'], ['F3'], ['F4'], ['F5'], ['F6'], ['F7'], ['F8'], ['F9'], ['F10'], ['F11'], ['F12'], ['DELETE']],
    [['`', '~'], ['1', '!'], ['2', '@'], ['3', '#'], ['4', '$'], ['5', '%'], ['6', '^'], ['7', '&'], ['8', '*'], ['9', '('], ['0', ')'], ['-', '_'], ['=', '+'], ['BACKSPACE']],
    [['TAB'], ['q', 'Q'], ['w', 'W'], ['e', 'E'], ['r', 'R'], ['t', 'T'], ['y', 'Y'], ['u', 'U'], ['i', 'I'], ['o', 'O'], ['p', 'P'], ['[', '{'], [']', '}'], ['\\', '|']],
    [['CAPS'], ['a', 'A'], ['s', 'S'], ['d', 'D'], ['f', 'F'], ['g', 'G'], ['h', 'H'], ['j', 'J'], ['k', 'K'], ['l', 'L'], [';', ':'], ['\'', '"'], ['ENTER']],
    [['SHIFT'], ['z', 'Z'], ['x', 'X'], ['c', 'C'], ['v', 'V'], ['b', 'B'], ['n', 'N'], ['m', 'M'], [',', '<'], ['.', '>'], ['/', '?'], ['SHIFT']],
    [['CTRL'], ['FN'], ['WIN'], ['ALT'], ['SPACE'], ['ALT'], ['FN'], ['CTRL']]
]

key_index = {}

keyboard_layout = []

index = 0

for i,row in enumerate(listed_keyboard_layout):
    for j,key_chars in enumerate(row):
        normal_char = key_chars[0]
        shift_char = key_chars[1] if len(key_chars) > 1 else None
        
        key = Key(index, normal_char, shift_char=shift_char,row=i,col=j)
        keyboard_layout.append(key)
        
        key_index[normal_char] = index
        
        if shift_char:
            key_index[shift_char] = index
        
        index += 1

# print(keyboard_layout)
key_index[' '] = key_index['SPACE']
key_index['\n'] = key_index['ENTER']
# Key width multiplier for larger keys
key_size = {
    'BACKSPACE':1.5,
    'TAB': 1.5,
    'CAPS': 1.75,
    'ENTER': 1.85,
    'SHIFT': 2.35,
    'SPACE': 6.35,
    'CTRL': 1.25,
    'WIN': 1.25,
    'ALT': 1.25,
    'FN':1.25,
    'DELETE':1.5
}


def custom_heat_map(grayscale):
    MAX_SCALE = 255
    if grayscale<0:
        col = (0,0,255)
        
    elif grayscale<MAX_SCALE/4:
        col = (0,(grayscale)*4,255)
    
    elif grayscale<MAX_SCALE/2:
        col = (0,255,255-(grayscale-MAX_SCALE/4)*4)
    
    elif grayscale<3*MAX_SCALE/4:
        col = ((grayscale-MAX_SCALE/2)*4,255,0)
    
    elif grayscale<MAX_SCALE:
        col = (255,255-(grayscale-3*MAX_SCALE/4)*4,0)
        
    else:
        col = (255,0,0)
    
    return tuple(value/255 for value in col)
#autum_r - yellow-red
#winter_r - green-blue
def draw_keyboard_layout():
    
    THRESH = -1
    x_start = 0
    y_start = 5  # Start higher to leave space for top row (e.g., ESC and function keys)
    # Iterate over e    ach row in the keyboard layout
    k=0
    for i in range(len(listed_keyboard_layout)):
        x_pos = x_start
        for j in range(len(listed_keyboard_layout[i])):
            key_obj = keyboard_layout[k]
            k+=1
            
            key = key_obj.char
            width = key_size.get(key, 1)  # Get key width, default is 1 unit
            freq = key_obj.freq
            
            # Create a rectangle for each key
            color_map = plt.cm.viridis
            if not freq:
                key_color = DEFAULT_KEY_COLOR
            else:
                # key_color = color_map(max(255-(5+5*freq),50))
                THRESH = max(THRESH,freq)
                key_color =  custom_heat_map(int((freq/THRESH)*255))
                
                
            rect = plt.Rectangle((x_pos, y_start), width, 1, edgecolor='black', facecolor=key_color)
            
            
            ax.add_patch(rect)
            
            # Add text to the center of the key
            ax.text(x_pos + width / 2, y_start + 0.5, key, ha='center', va='center', fontsize=10,font=KEY_FONT)
            
            # Increment x position by the width of the key
            x_pos += width + 0.1  # Add small gap between keys

        # Decrease y position for the next row
        y_start -= 1.1  # Move down for the next row

    # Set limits and hide axes
    ax.set_xlim(0, 16)
    ax.set_ylim(-0.5, 6)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide axes

    # plt.title('Keyboard Layout')
    # plt.show()


fig, ax = plt.subplots(figsize=(12, 8))
fig.patch.set_facecolor(KEYBOARD_BG_COLOR)


s = 'sssssssss'
s="""Beneath the sprawling oak tree, a curious squirrel 
scurried about, gathering acorns and chattering excitedly as the 
golden sunlight filtered through the leaves, creating a mosaic of shadows on the ground; 
nearby, children laughed while flying kites in a vibrant array of colors that danced in 
the gentle breeze, their parents watching with smiles as a dog playfully chased after a 
butterfly, momentarily forgetting the world around them, while a distant train whistled, 
announcing its arrival, reminding everyone of the adventures that lay beyond the horizon,
where dreams and reality intertwined in a symphony of possibilities waiting to be explored."""

i=0
while i<len(s):

    # print('yes')
    # plt.draw()
    # plt.pause(0.1)
    # print('HI')
    key = keyboard_layout[key_index[s[i]]]
    key.freq+=1
    # print(s[i],key.shift_char)
    if key.shift_char==s[i]:
        keyboard_layout[key_index['SHIFT']].freq+=1
    # print(keyboard_layout[key_index[s[i]]].freq)
    i+=1

print(keyboard_layout[key_index['e']].freq)
draw_keyboard_layout()
plt.show()