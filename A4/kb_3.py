import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

KEYBOARD_BG_COLOR = '#1c1c1c'
KEY_FONT = 'DejaVu Sans Mono'
DEFAULT_KEY_COLOR = '#656363'

def custom_heat_map(grayscale):
    Mself.ax_SCALE = 255
    if grayscale<0:
        col = (0,0,255)
        
    elif grayscale<Mself.ax_SCALE/4:
        col = (0,(grayscale)*4,255)
    
    elif grayscale<Mself.ax_SCALE/2:
        col = (0,255,255-(grayscale-Mself.ax_SCALE/4)*4)
    
    elif grayscale<3*Mself.ax_SCALE/4:
        col = ((grayscale-Mself.ax_SCALE/2)*4,255,0)
    
    elif grayscale<Mself.ax_SCALE:
        col = (255,255-(grayscale-3*Mself.ax_SCALE/4)*4,0)
        
    else:
        col = (255,0,0)
    
    return tuple(value/255 for value in col)

class Key:
    def __init__(self, ind, char,row,col, shift_char=None,freq=0):
        self.ind = ind
        self.char = char
        self.shift_char = shift_char
        self.freq=freq
        self.row = row
        self.col = col
        
class Keyboard():
    def __init__(self, listed_keyboard_layout, key_size, keyboard_layout, key_index,THRESH):
        self.listed_keyboard_layout = listed_keyboard_layout
        self.keyboard_layout = keyboard_layout  
        self.key_index = key_index
        self.THRESH = THRESH
        self.key_size = key_size
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.patch.set_facecolor(KEYBOARD_BG_COLOR)
    
    def draw_keyboard_layout(self):
        self.ax.cla()
        
        x_start = 0
        y_start = 5  
        x = np.linspace(-1, 1, 50)
        y = np.linspace(-1, 1, 50)
        X, Y = np.meshgrid(x, y)
        R = np.sqrt(X**2 + Y**2)
        gradient = 1-R
        # gradient = np.clip(gradient, 0, 1)
        Z = np.sqrt(X*X + Y*Y)
        
        k=0
        for rowi in range(len(self.listed_keyboard_layout)):
            x_pos = x_start
            for j in range(len(self.listed_keyboard_layout[rowi])):
                key_obj = self.keyboard_layout[k]
                k+=1
                
                key = key_obj.char
                width = self.key_size.get(key, 1)  
                freq = key_obj.freq
                
                
                # color_map = plt.cm.autumn_r
                if freq==0:
                    key_color = DEFAULT_KEY_COLOR
                    rect = plt.Rectangle((x_pos, y_start), width, 1, edgecolor='black', facecolor=key_color)
                
                else:
                    print(freq,self.THRESH)
                    # key_color = color_map((freq/THRESH))
                    # THRESH = mself.ax(THRESH,freq)
                    factor = 0.4
                    
                    key_color =  self.custom_heat_map((freq/self.THRESH)*255)
                    low_col =  tuple( (min(255,key_color[i]*factor) for i in range(3)))
                    color_map = LinearSegmentedColormap.from_list("custom_cmap", [key_color,low_col])
                    self.ax.imshow(Z, extent=(x_pos, x_pos+width, y_start,y_start+1), origin='lower',cmap = color_map)
                    rect = plt.Rectangle((x_pos, y_start), width, 1, edgecolor='black', facecolor='none')


                self.ax.add_patch(rect)
                
                self.ax.text(x_pos + width / 2, y_start + 0.5, str(freq).upper(), ha='center', va='center', fontsize=10,font=KEY_FONT)
                # self.ax.text(x_pos + width / 2, y_start + 0.5, key.upper(), ha='center', va='center', fontsize=10,font=KEY_FONT)
                
                x_pos += width + 0.1  

            y_start -= 1.1  

        self.ax.set_xlim(0, 16)
        self.ax.set_ylim(-0.5, 6)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
    def clear_keyboard(self):
        for key in self.keyboard_layout:
            key.freq = 0
        
    def run(self):
        s = 'sssssssss'
        s="""Beneath the sprawling oak tree, a curious squirrel 
        scurried about, gathering acorns and chattering excitedly as the 
        golden sunlight filtered through the leaves, creating a mosaic of shadows on the ground; 
        nearby, children laughed while flying kites in a vibrant array of colors that danced in 
        the gentle breeze, their parents watching with smiles as a dog playfully chased after a 
        butterfly, momentarily forgetting the world around them, while a distant train whistled, 
        announcing its arrival, reminding everyone of the adventures that lay beyond the horizon,
        where dreams and reality intertwined in a symphony of possibilities waiting to be explored."""
        s = "11112345678a"
        s = "abcdefghijklmnopqrstuvwxyza"

        i=0
        self.THRESH=0
        
        while True:
            while i<len(s):
                key = self.keyboard_layout[self.key_index[s[i]]]
                if s[i]!=' ':
                    key.freq+=1
                    print('updated')
                self.THRESH = max(self.THRESH,key.freq)
                # print(s[i],key.shift_char)
                if key.shift_char==s[i]:
                    self.keyboard_layout[self.key_index['SHIFT']].freq+=1
                    self.THRESH = max(self.THRESH,self.keyboard_layout[self.key_index['SHIFT']].freq)
                # print(keyboard_layout[key_index[s[i]]].freq)
                i+=1
                print(i)
                
            self.ax.cla()
            self.draw_keyboard_layout()
            plt.draw()
            plt.pause(0.01)
            
            t = input()
            
            if t.lower().strip()=='quit':
                break
            
            if t.lower().strip()=='clear':
                self.clear_keyboard()
                self.THRESH=0
                s = ""
                i=0
                print('cleared')
            
            s+=t
            print(s)

listed_keyboard_layout = [
    [['ESC'], ['F1'], ['F2'], ['F3'], ['F4'], ['F5'], ['F6'], ['F7'], ['F8'], ['F9'], ['F10'], ['F11'], ['F12'], ['DELETE']],
    [['`', '~'], ['1', '!'], ['2', '@'], ['3', '#'], ['4', '$'], ['5', '%'], ['6', '^'], ['7', '&'], ['8', '*'], ['9', '('], ['0', ')'], ['-', '_'], ['=', '+'], ['BACKSPACE']],
    [['TAB'], ['q', 'Q'], ['w', 'W'], ['e', 'E'], ['r', 'R'], ['t', 'T'], ['y', 'Y'], ['u', 'U'], ['i', 'I'], ['o', 'O'], ['p', 'P'], ['[', '{'], [']', '}'], ['\\', '|']],
    [['CAPS'], ['a', 'A'], ['s', 'S'], ['d', 'D'], ['f', 'F'], ['g', 'G'], ['h', 'H'], ['j', 'J'], ['k', 'K'], ['l', 'L'], [';', ':'], ['\'', '"'], ['ENTER']],
    [['SHIFT'], ['z', 'Z'], ['x', 'X'], ['c', 'C'], ['v', 'V'], ['b', 'B'], ['n', 'N'], ['m', 'M'], [',', '<'], ['.', '>'], ['/', '?'], ['SHIFT']],
    [['CTRL'], ['FN'], ['WIN'], ['ALT'], ['SPACE'], ['ALT'], ['FN'], ['CTRL']]
]