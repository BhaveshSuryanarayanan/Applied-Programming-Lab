import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
# from layout import keyboard_layouts
# from layout import keyboard_layouts

KEYBOARD_BG_COLOR = '#1c1c1c'
KEY_FONT = 'DejaVu Sans Mono'
DEFAULT_KEY_COLOR = '#656363'

def custom_heat_map(grayscale):
    Max_SCALE = 255
    Min_SCALE =0
    DIFF = Max_SCALE-Min_SCALE
    # grayscale*=(Max_SCALE-Min_SCALE)
    # grayscale+=Min_SCALE
    if grayscale<0:
        col = (Max_SCALE,Min_SCALE,Max_SCALE)
        
    elif grayscale<=0.2:
        seg = 5*(grayscale)
        col = (Max_SCALE-seg*(Max_SCALE-Min_SCALE),Min_SCALE,Max_SCALE)
    
    elif grayscale<=0.4:
        seg = 5*(grayscale-0.2)
        col = (Min_SCALE,Min_SCALE+seg*(Max_SCALE-Min_SCALE),Max_SCALE)
    
    elif grayscale<=0.6:
        seg = 5*(grayscale-0.4)
        col = (Min_SCALE,Max_SCALE,Max_SCALE-seg*(Max_SCALE-Min_SCALE))
    
    elif grayscale<=0.8:
        seg = 5*(grayscale-0.6)
        col = (Min_SCALE+seg*(Max_SCALE-Min_SCALE),Max_SCALE,Min_SCALE)
        
    elif grayscale<=1:
        seg = 5*(grayscale-0.8)
        col = (Max_SCALE,Max_SCALE-seg*(Max_SCALE-Min_SCALE),Min_SCALE)
    
    return tuple(value/255 for value in col)



            
class Key:
    def __init__(self, ind, char,x,y,width, shift_char=None,freq=0):
        self.ind = ind
        self.char = char
        self.shift_char = shift_char
        self.freq=freq
        self.x = x
        self.y = y
        self.width = width

class Keyboard():
    def __init__(self, listed_keyboard_layout):
        self.listed_keyboard_layout = listed_keyboard_layout
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.patch.set_facecolor(KEYBOARD_BG_COLOR)
        
        self.key_index = {}
        self.keyboard_layout = []
        index = 0
        
        x_start = 100.0
        y_start = -100.0
        x_end = -100.0
        y_end = +100.0
        
        for key in self.listed_keyboard_layout:
            chars = key['chars']
            (x,y) = key['position']
            w = key['width']
            normal_char = chars[0]
            
            if len(chars)>1:
                shift_char = chars[1] 
                self.key_index[shift_char] = index
            else:
                shift_char = None
                
            keyobj = Key(index, normal_char, shift_char=shift_char,x=x,y=y,width=w)
            self.keyboard_layout.append(keyobj)
            self.key_index[normal_char] = index
            
            index+=1
            
            # print(x,y)
            x_start = min(x_start,x)
            y_start = max(y_start,y+1)
            x_end = max(x_end,x+w)
            y_end = min(y_end,y)
            
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        # print(self.x_start,self.x_end,self.y_start,self.y_end)
                
        self.key_index[' '] = self.key_index['SPACE']
        self.key_index['\n'] = self.key_index['ENTER']
        
    def create_radial_gradient(self,grayscale,xcentre,ycentre,xradius,yradius):
        # MAX_RAD = radius
        grayscale*=0.8
        mid = grayscale
        # print('yes')
        
        x0 = int(self.xRES*(xcentre-self.x_start)/(self.x_end-self.x_start))
        y0 = int(self.yRES*(ycentre-self.y_start)/(self.y_end-self.y_start))
        rx = abs(int(self.xRES*xradius/(self.x_end-self.x_start)))
        ry = abs(int(self.yRES*yradius/(self.y_end-self.y_start)))
        fact = 3
        xmin = max(int(x0 - fact*rx), 0)
        xmax = min(int(x0 + fact*rx), self.xRES)
        ymin = max(int(y0 - fact*ry), 0)
        ymax = min(int(y0 + fact*ry), self.yRES)
    
        # print(xmin,xmax,ymin,ymax)
        
        y,x = np.ogrid[ymin:ymax,xmin:xmax]
        distance = np.sqrt((x-x0)**2+(y-y0)**2)
        # print(x.shape,y.shape,distance.shape)
        # print(xmin,xmax,ymin,ymax)
        val = grayscale*np.exp(-(distance**2)*0.0005)
        alpha = grayscale*np.exp(-(distance**2)*0.0004)
        
        self.grey_mask[ymin:ymax,xmin:xmax] = np.minimum(0.9,val[::-1,:] + self.grey_mask[ymin:ymax,xmin:xmax])
        self.alpha_mask[ymin:ymax, xmin:xmax] = np.minimum(0.8, alpha[::-1,:] + self.alpha_mask[ymin:ymax, xmin:xmax])
    
        
    def colorize(self):
        
        cmap = plt.cm.jet
        colored = cmap(self.grey_mask)
        colored[...,3] = self.alpha_mask
        self.color_mask = colored
        # print('colorized')
              
    def draw_keyboard_layout(self):
        self.ax.cla()
        
        self.xRES = 1000
        self.yRES = abs(int(self.xRES*(self.y_end-self.y_start)/(self.x_end-self.x_start)))
        
        self.color_mask = np.zeros((self.yRES,self.xRES,4))
        self.grey_mask = np.zeros((self.yRES,self.xRES))
        self.alpha_mask = np.zeros((self.yRES,self.xRES))
        
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
        Zor = 5
        for key_obj in self.keyboard_layout:
            k+=1
            
            key = key_obj.char
            freq = key_obj.freq
            
            '''
            autumn_r = yellow-red
            winter_r = green-blue
            blues = blues
            BuGn = green
            BuPu = purple
            CMRmap = darkblue-darkyellow
            OrRd - red
            Pastel1 - light colors
            plasma_r - blue-magenta-yellow  
            jet_r - rainbow < custom
            '''     
            
            key_color = DEFAULT_KEY_COLOR
            x_pos,y_pos,width = key_obj.x, key_obj.y, key_obj.width
            rect = plt.Rectangle((x_pos, y_pos), width, 1, edgecolor='black', facecolor=key_color)
            
            self.ax.add_patch(rect)
            
            if freq:
                factor = 0.4
                
                # cmap = plt.cm.jet_r
                # key_color = cmap((freq/(self.THxRESH)))
                offset = 0.6
                self.create_radial_gradient(grayscale=(freq/self.THxRESH),xcentre=x_pos+width/2,ycentre=y_pos+1/2,xradius=width/2+offset,yradius=1+offset)
                
                # Gradient = self.create_radial_gradient(freq/self.THxRESH)
                # self.ax.imshow(Gradient, extent=(x_pos-offset, x_pos+width+offset, y_pos-offset,y_pos+1+offset), origin='lower',zorder=5)

            
            # self.ax.text(x_pos + width / 2, y_pos + 0.5, str(freq).upper(), ha='center', va='center', fontsize=10,font=KEY_FONT)
            self.ax.text(x_pos + width / 2, y_pos + 0.5, key.upper(), ha='center', va='center', fontsize=10,font=KEY_FONT,zorder=100)
            
            shift_key = key_obj.shift_char
            
            if shift_key != None and not shift_key.isalpha():
                self.ax.text(x_pos + width / 5, y_pos + 0.75, shift_key.upper(), ha='center', va='center', fontsize=10,font=KEY_FONT,zorder=100)
                # Zor+=1
        
        self.colorize()
        # print(self.color_mask[200:210,200:210])
        self.ax.imshow(self.color_mask, extent=(self.x_start,self.x_end,self.y_end, self.y_start), origin='lower',zorder=5)
        self.ax.set_xlim(self.x_start, self.x_end )
        self.ax.set_ylim(self.y_end, self.y_start)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
    def clear_keyboard(self):
        for key in self.keyboard_layout:
            key.freq = 0
        print('cleared')
        
    def run(self,s = ""):

        i=0
        self.THxRESH=0
        
        while True:
            while i<len(s):
                if s[i] not in self.key_index:
                    # print(s[i])
                    # print(i)
                    i+=1
                    continue
                key = self.keyboard_layout[self.key_index[s[i]]]
                if s[i]!=' ':
                    key.freq+=1
                self.THxRESH = max(self.THxRESH,key.freq)
                if key.shift_char==s[i]:
                    self.keyboard_layout[self.key_index['RSHIFT']].freq+=1
                    self.THxRESH = max(self.THxRESH,self.keyboard_layout[self.key_index['RSHIFT']].freq)
                i+=1
               
            self.ax.cla()
            self.draw_keyboard_layout()
            plt.draw()
            plt.pause(0.01)
            # break
            t = input()
            
            if t.lower().strip()=='quit':
                break
            
            if t.lower().strip()=='clear':
                self.clear_keyboard()
                self.THxRESH=0
                s = ""
                t = ""
                i=0
            s+=t
        print(s)

qwerty_keyboard_layout = [
    [['ESC'], ['F1'], ['F2'], ['F3'], ['F4'], ['F5'], ['F6'], ['F7'], ['F8'], ['F9'], ['F10'], ['F11'], ['F12'], ['DELETE']],
    [['`', '~'], ['1', '!'], ['2', '@'], ['3', '#'], ['4', '$'], ['5', '%'], ['6', '^'], ['7', '&'], ['8', '*'], ['9', '('], ['0', ')'], ['-', '_'], ['=', '+'], ['BACKSPACE']],
    [['TAB'], ['q', 'Q'], ['w', 'W'], ['e', 'E'], ['r', 'R'], ['t', 'T'], ['y', 'Y'], ['u', 'U'], ['i', 'I'], ['o', 'O'], ['p', 'P'], ['[', '{'], [']', '}'], ['\\', '|']],
    [['CAPS'], ['a', 'A'], ['s', 'S'], ['d', 'D'], ['f', 'F'], ['g', 'G'], ['h', 'H'], ['j', 'J'], ['k', 'K'], ['l', 'L'], [';', ':'], ['\'', '"'], ['ENTER']],
    [['SHIFT'], ['z', 'Z'], ['x', 'X'], ['c', 'C'], ['v', 'V'], ['b', 'B'], ['n', 'N'], ['m', 'M'], [',', '<'], ['.', '>'], ['/', '?'], ['SHIFT']],
    [['CTRL'], ['FN'], ['WIN'], ['ALT'], ['SPACE'], ['ALT'], ['FN'], ['CTRL']]
]

ergodox_keyboard_layout = [
    # Left hand
    
        [['ESC'], ['1', '!'], ['2', '@'], ['3', '#'], ['4', '$'],['5', '%'],['DEL'], ['%4%'], ['DEL'],['6', '^'] , ['7', '&'], ['8', '*'], ['9', '('], ['0', ')'], ['=', '+'], ['ESC']],
        [['TAB'], ['q', 'Q'], ['w', 'W'], ['e', 'E'], ['r', 'R'], ['t', 'T'], ['BACKSPACE'],['%4%'],['BACKSPACE'], ['y', 'Y'], ['u', 'U'], ['i', 'I'], ['o', 'O'], ['p', 'P'], ['[', '{'], [']', '}'], ['TAB']],
        [['SHIFT'], ['a', 'A'], ['s', 'S'], ['d', 'D'], ['f', 'F'], ['g', 'G'], ['ENTER'],['%4%'], ['ENTER'],['h', 'H'], ['j', 'J'], ['k', 'K'], ['l', 'L'], [';', ':'], ['\'', '"'], ['SHIFT']],
        [['L1'], ['z', 'Z'], ['x', 'X'], ['c', 'C'], ['v', 'V'], ['b', 'B'],['%4%'],['n', 'N'], ['m', 'M'], [',', '<'], ['.', '>'], ['/', '?'], ['L1']],
        [['CTRL'], ['WIN'], ['ALT'], ['SPACE'],['%8%'],['SPACE'], ['ALT'], ['WIN'], ['CTRL']],
        [['FN'], ['CTRL'],['%8%'],['ALT'], ['SPACE']]
]

ergodox_key_size = {
    'ESC': 1.5,'DEL':1,
    '1': 1, '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    'TAB': 1, 'q': 1, 'w': 1, 'e': 1, 'r': 1, 't': 1, '-': 1,
    'CAPS': 1, 'a': 1, 's': 1, 'd': 1, 'f': 1, 'g': 1,
    'SHIFT': 1.5, 'z': 1, 'x': 1, 'c': 1, 'v': 1, 'b': 1,
    'CTRL': 1.5, 'WIN': 1.25, 'ALT': 1.25, 'SPACE': 3,
    '^': 1, '7': 1, '8': 1, '9': 1, '0': 1, '=': 1, 'BACKSPACE': 1.5,
    'y': 1, 'u': 1, 'i': 1, 'o': 1, 'p': 1, '[': 1, ']': 1,
    'h': 1, 'j': 1, 'k': 1, 'l': 1, ';': 1, '\'': 1, 'ENTER': 1.75,
    'n': 1, 'm': 1, ',': 1, '.': 1, '/': 1, 'SHIFT': 1.75,
    'FN': 1.25, 'CTRL': 1.25, 'ALT': 1.25, 'WIN': 1.25,
}
keyboard_layouts = {
    'qwerty': [
        {'chars': ['ESC'], 'position': (0, 5), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['F1'], 'position': (1.1, 5), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['F2'], 'position': (2.2, 5), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['F3'], 'position': (3.3, 5), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['F4'], 'position': (4.4, 5), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['F5'], 'position': (5.5, 5), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['F6'], 'position': (6.6, 5), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['F7'], 'position': (7.7, 5), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['F8'], 'position': (8.8, 5), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['F9'], 'position': (9.9, 5), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['F10'], 'position': (11.0, 5), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['F11'], 'position': (12.1, 5), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['F12'], 'position': (13.2, 5), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['DELETE'], 'position': (14.3, 5), 'width': 1.5, 'side': 'R', 'start': 'j'},
        {'chars': ['`', '~'], 'position': (0, 3.9), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['1', '!'], 'position': (1.1, 3.9), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['2', '@'], 'position': (2.2, 3.9), 'width': 1, 'side': 'L', 'start': 's'},
        {'chars': ['3', '#'], 'position': (3.3, 3.9), 'width': 1, 'side': 'L', 'start': 'd'},
        {'chars': ['4', '$'], 'position': (4.4, 3.9), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['5', '%'], 'position': (5.5, 3.9), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['6', '^'], 'position': (6.6, 3.9), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['7', '&'], 'position': (7.7, 3.9), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['8', '*'], 'position': (8.8, 3.9), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['9', '('], 'position': (9.9, 3.9), 'width': 1, 'side': 'R', 'start': 'k'},
        {'chars': ['0', ')'], 'position': (11.0, 3.9), 'width': 1, 'side': 'R', 'start': 'l'},
        {'chars': ['-', '_'], 'position': (12.1, 3.9), 'width': 1, 'side': 'R', 'start': 'l'},
        {'chars': ['=', '+'], 'position': (13.2, 3.9), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': ['BACKSPACE'], 'position': (14.3, 3.9), 'width': 1.5, 'side': 'R', 'start': ';'},
        {'chars': ['TAB'], 'position': (0, 2.8), 'width': 1.5, 'side': 'L', 'start': 'a'},
        {'chars': ['q', 'Q'], 'position': (1.6, 2.8), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['w', 'W'], 'position': (2.7, 2.8), 'width': 1, 'side': 'L', 'start': 's'},
        {'chars': ['e', 'E'], 'position': (3.8, 2.8), 'width': 1, 'side': 'L', 'start': 'd'},
        {'chars': ['r', 'R'], 'position': (4.9, 2.8), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['t', 'T'], 'position': (6.0, 2.8), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['y', 'Y'], 'position': (7.1, 2.8), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['u', 'U'], 'position': (8.2, 2.8), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['i', 'I'], 'position': (9.3, 2.8), 'width': 1, 'side': 'R', 'start': 'k'},
        {'chars': ['o', 'O'], 'position': (10.4, 2.8), 'width': 1, 'side': 'R', 'start': 'l'},
        {'chars': ['p', 'P'], 'position': (11.5, 2.8), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': ['[', '{'], 'position': (12.6, 2.8), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': [']', '}'], 'position': (13.7, 2.8), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': ['\\', '|'], 'position': (14.8, 2.8), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': ['CAPS'], 'position': (0, 1.7), 'width': 1.75, 'side': 'L', 'start': 'a'},
        {'chars': ['a', 'A'], 'position': (1.85, 1.7), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['s', 'S'], 'position': (2.95, 1.7), 'width': 1, 'side': 'L', 'start': 's'},
        {'chars': ['d', 'D'], 'position': (4.05, 1.7), 'width': 1, 'side': 'L', 'start': 'd'},
        {'chars': ['f', 'F'], 'position': (5.15, 1.7), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['g', 'G'], 'position': (6.25, 1.7), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['h', 'H'], 'position': (7.35, 1.7), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['j', 'J'], 'position': (8.45, 1.7), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['k', 'K'], 'position': (9.55, 1.7), 'width': 1, 'side': 'R', 'start': 'k'},
        {'chars': ['l', 'L'], 'position': (10.65, 1.7), 'width': 1, 'side': 'R', 'start': 'l'},
        {'chars': [';', ':'], 'position': (11.75, 1.7), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': ['\'', '\"'], 'position': (12.85, 1.7), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': ['ENTER'], 'position': (13.95, 1.7), 'width': 1.75, 'side': 'R', 'start': ';'},
        {'chars': ['LSHIFT'], 'position': (0, 0.6), 'width': 2.25, 'side': 'L', 'start': 'a'},
        {'chars': ['z', 'Z'], 'position': (2.3, 0.6), 'width': 1, 'side': 'L', 'start': 'a'},
        {'chars': ['x', 'X'], 'position': (3.4, 0.6), 'width': 1, 'side': 'L', 'start': 's'},
        {'chars': ['c', 'C'], 'position': (4.5, 0.6), 'width': 1, 'side': 'L', 'start': 'd'},
        {'chars': ['v', 'V'], 'position': (5.6, 0.6), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['b', 'B'], 'position': (6.7, 0.6), 'width': 1, 'side': 'L', 'start': 'f'},
        {'chars': ['n', 'N'], 'position': (7.8, 0.6), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': ['m', 'M'], 'position': (8.9, 0.6), 'width': 1, 'side': 'R', 'start': 'j'},
        {'chars': [',', '<'], 'position': (10.0, 0.6), 'width': 1, 'side': 'R', 'start': 'k'},
        {'chars': ['.', '>'], 'position': (11.1, 0.6), 'width': 1, 'side': 'R', 'start': 'l'},
        {'chars': ['/', '?'], 'position': (12.2, 0.6), 'width': 1, 'side': 'R', 'start': ';'},
        {'chars': ['RSHIFT'], 'position': (13.3, 0.6), 'width': 2.25, 'side': 'R', 'start': ';'},
        {'chars': ['LCTRL'], 'position': (0, -0.5), 'width': 1.25, 'start' : 'a'},
        {'chars': ['FN'], 'position': (1.35, -0.5), 'width': 1.25},
        {'chars': ['WIN'], 'position': (2.7, -0.5), 'width': 1.25},
        {'chars': ['ALT'], 'position': (4.05, -0.5), 'width': 1.25},
        {'chars': ['SPACE'], 'position': (5.4, -0.54), 'width': 6.35, 'start': 'SPACE'},
        {'chars': ['ALT'], 'position': (11.85, -0.5), 'width': 1.25},
        {'chars': ['FN'], 'position': (13.2, -0.5), 'width': 1.25},
        {'chars': ['RCTRL'], 'position': (14.55, -0.5), 'width': 1.25, 'start' : ';'}
    ],
    
    'dvorak': [
        {'chars': ['ESC'], 'position': (0, 5), 'width': 1},
        {'chars': ['F1'], 'position': (1.1, 5), 'width': 1},
        {'chars': ['F2'], 'position': (2.2, 5), 'width': 1},
        {'chars': ['F3'], 'position': (3.3000000000000003, 5), 'width': 1},
        {'chars': ['F4'], 'position': (4.4, 5), 'width': 1},
        {'chars': ['F5'], 'position': (5.5, 5), 'width': 1},
        {'chars': ['F6'], 'position': (6.6, 5), 'width': 1},
        {'chars': ['F7'], 'position': (7.699999999999999, 5), 'width': 1},
        {'chars': ['F8'], 'position': (8.799999999999999, 5), 'width': 1},
        {'chars': ['F9'], 'position': (9.899999999999999, 5), 'width': 1},
        {'chars': ['F10'], 'position': (10.999999999999998, 5), 'width': 1},
        {'chars': ['F11'], 'position': (12.099999999999998, 5), 'width': 1},
        {'chars': ['F12'], 'position': (13.199999999999998, 5), 'width': 1},
        {'chars': ['DELETE'], 'position': (14.299999999999997, 5), 'width': 1.5},
        {'chars': ['`', '~'], 'position': (0, 3.9), 'width': 1},
        {'chars': ['1', '!'], 'position': (1.1, 3.9), 'width': 1},
        {'chars': ['2', '@'], 'position': (2.2, 3.9), 'width': 1},
        {'chars': ['3', '#'], 'position': (3.3000000000000003, 3.9), 'width': 1},
        {'chars': ['4', '$'], 'position': (4.4, 3.9), 'width': 1},
        {'chars': ['5', '%'], 'position': (5.5, 3.9), 'width': 1},
        {'chars': ['6', '^'], 'position': (6.6, 3.9), 'width': 1},
        {'chars': ['7', '&'], 'position': (7.699999999999999, 3.9), 'width': 1},
        {'chars': ['8', '*'], 'position': (8.799999999999999, 3.9), 'width': 1},
        {'chars': ['9', '('], 'position': (9.899999999999999, 3.9), 'width': 1},
        {'chars': ['0', ')'], 'position': (10.999999999999998, 3.9), 'width': 1},
        {'chars': ['[', '{'], 'position': (12.099999999999998, 3.9), 'width': 1},
        {'chars': [']', '}'], 'position': (13.199999999999998, 3.9), 'width': 1},
        {'chars': ['BACKSPACE'], 'position': (14.299999999999997, 3.9), 'width': 1.5},
        {'chars': ['TAB'], 'position': (0, 2.8), 'width': 1.5},
        {'chars': ["'", '"'], 'position': (1.6, 2.8), 'width': 1},
        {'chars': [',', '<'], 'position': (2.7, 2.8), 'width': 1},
        {'chars': ['.', '>'], 'position': (3.8000000000000003, 2.8), 'width': 1},
        {'chars': ['p', 'P'], 'position': (4.9, 2.8), 'width': 1},
        {'chars': ['y', 'Y'], 'position': (6.0, 2.8), 'width': 1},
        {'chars': ['f', 'F'], 'position': (7.1, 2.8), 'width': 1},
        {'chars': ['g', 'G'], 'position': (8.2, 2.8), 'width': 1},
        {'chars': ['c', 'C'], 'position': (9.299999999999999, 2.8), 'width': 1},
        {'chars': ['r', 'R'], 'position': (10.399999999999999, 2.8), 'width': 1},
        {'chars': ['l', 'L'], 'position': (11.499999999999998, 2.8), 'width': 1},
        {'chars': ['/', '?'], 'position': (12.599999999999998, 2.8), 'width': 1},
        {'chars': ['=', '+'], 'position': (13.699999999999998, 2.8), 'width': 1},
        {'chars': ['\\', '|'], 'position': (14.799999999999997, 2.8), 'width': 1},
        {'chars': ['CAPS'], 'position': (0, 1.6999999999999997), 'width': 1.75},
        {'chars': ['a', 'A'], 'position': (1.85, 1.6999999999999997), 'width': 1},
        {'chars': ['o', 'O'], 'position': (2.95, 1.6999999999999997), 'width': 1},
        {'chars': ['e', 'E'], 'position': (4.050000000000001, 1.6999999999999997), 'width': 1},
        {'chars': ['u', 'U'], 'position': (5.15, 1.6999999999999997), 'width': 1},
        {'chars': ['i', 'I'], 'position': (6.25, 1.6999999999999997), 'width': 1},
        {'chars': ['d', 'D'], 'position': (7.35, 1.6999999999999997), 'width': 1},
        {'chars': ['h', 'H'], 'position': (8.45, 1.6999999999999997), 'width': 1},
        {'chars': ['t', 'T'], 'position': (9.549999999999999, 1.6999999999999997), 'width': 1},
        {'chars': ['n', 'N'], 'position': (10.649999999999999, 1.6999999999999997), 'width': 1},
        {'chars': ['s', 'S'], 'position': (11.749999999999998, 1.6999999999999997), 'width': 1},
        {'chars': ['-', '_'], 'position': (12.849999999999998, 1.6999999999999997), 'width': 1},
        {'chars': ['ENTER'], 'position': (13.949999999999998, 1.6999999999999997), 'width': 1.85},
        {'chars': ['SHIFT'], 'position': (0, 0.5999999999999996), 'width': 2.35},
        {'chars': [';', ':'], 'position': (2.45, 0.5999999999999996), 'width': 1},
        {'chars': ['q', 'Q'], 'position': (3.5500000000000003, 0.5999999999999996), 'width': 1},
        {'chars': ['j', 'J'], 'position': (4.65, 0.5999999999999996), 'width': 1},
        {'chars': ['k', 'K'], 'position': (5.75, 0.5999999999999996), 'width': 1},
        {'chars': ['x', 'X'], 'position': (6.85, 0.5999999999999996), 'width': 1},
        {'chars': ['b', 'B'], 'position': (7.949999999999999, 0.5999999999999996), 'width': 1},
        {'chars': ['m', 'M'], 'position': (9.049999999999999, 0.5999999999999996), 'width': 1},
        {'chars': ['w', 'W'], 'position': (10.149999999999999, 0.5999999999999996), 'width': 1},
        {'chars': ['v', 'V'], 'position': (11.249999999999998, 0.5999999999999996), 'width': 1},
        {'chars': ['z', 'Z'], 'position': (12.349999999999998, 0.5999999999999996), 'width': 1},
        {'chars': ['SHIFT'], 'position': (13.449999999999998, 0.5999999999999996), 'width': 2.35},
        {'chars': ['CTRL'], 'position': (0, -0.5000000000000004), 'width': 1.25},
        {'chars': ['FN'], 'position': (1.35, -0.5000000000000004), 'width': 1.25},
        {'chars': ['WIN'], 'position': (2.7, -0.5000000000000004), 'width': 1.25},
        {'chars': ['ALT'], 'position': (4.050000000000001, -0.5000000000000004), 'width': 1.25},
        {'chars': ['SPACE'], 'position': (5.4, -0.5000000000000004), 'width': 6.35},
        {'chars': ['ALT'], 'position': (11.85, -0.5000000000000004), 'width': 1.25},
        {'chars': ['FN'], 'position': (13.2, -0.5000000000000004), 'width': 1.25},
        {'chars': ['CTRL'], 'position': (14.549999999999999, -0.5000000000000004), 'width': 1.25}
    ],
    
    'colemak':[
        {'chars': ['ESC'], 'position': (0, 5), 'width': 1},
        {'chars': ['F1'], 'position': (1.1, 5), 'width': 1},
        {'chars': ['F2'], 'position': (2.2, 5), 'width': 1},
        {'chars': ['F3'], 'position': (3.3000000000000003, 5), 'width': 1},
        {'chars': ['F4'], 'position': (4.4, 5), 'width': 1},
        {'chars': ['F5'], 'position': (5.5, 5), 'width': 1},
        {'chars': ['F6'], 'position': (6.6, 5), 'width': 1},
        {'chars': ['F7'], 'position': (7.699999999999999, 5), 'width': 1},
        {'chars': ['F8'], 'position': (8.799999999999999, 5), 'width': 1},
        {'chars': ['F9'], 'position': (9.899999999999999, 5), 'width': 1},
        {'chars': ['F10'], 'position': (10.999999999999998, 5), 'width': 1},
        {'chars': ['F11'], 'position': (12.099999999999998, 5), 'width': 1},
        {'chars': ['F12'], 'position': (13.199999999999998, 5), 'width': 1},
        {'chars': ['DELETE'], 'position': (14.299999999999997, 5), 'width': 1.5},
        {'chars': ['`', '~'], 'position': (0, 3.9), 'width': 1},
        {'chars': ['1', '!'], 'position': (1.1, 3.9), 'width': 1},
        {'chars': ['2', '@'], 'position': (2.2, 3.9), 'width': 1},
        {'chars': ['3', '#'], 'position': (3.3000000000000003, 3.9), 'width': 1},
        {'chars': ['4', '$'], 'position': (4.4, 3.9), 'width': 1},
        {'chars': ['5', '%'], 'position': (5.5, 3.9), 'width': 1},
        {'chars': ['6', '^'], 'position': (6.6, 3.9), 'width': 1},
        {'chars': ['7', '&'], 'position': (7.699999999999999, 3.9), 'width': 1},
        {'chars': ['8', '*'], 'position': (8.799999999999999, 3.9), 'width': 1},
        {'chars': ['9', '('], 'position': (9.899999999999999, 3.9), 'width': 1},
        {'chars': ['0', ')'], 'position': (10.999999999999998, 3.9), 'width': 1},
        {'chars': ['-', '_'], 'position': (12.099999999999998, 3.9), 'width': 1},
        {'chars': ['=', '+'], 'position': (13.199999999999998, 3.9), 'width': 1},
        {'chars': ['BACKSPACE'], 'position': (14.299999999999997, 3.9), 'width': 1.5},
        {'chars': ['TAB'], 'position': (0, 2.8), 'width': 1.5},
        {'chars': ['q', 'Q'], 'position': (1.6, 2.8), 'width': 1},
        {'chars': ['w', 'W'], 'position': (2.7, 2.8), 'width': 1},
        {'chars': ['f', 'F'], 'position': (3.8000000000000003, 2.8), 'width': 1},
        {'chars': ['p', 'P'], 'position': (4.9, 2.8), 'width': 1},
        {'chars': ['g', 'G'], 'position': (6.0, 2.8), 'width': 1},
        {'chars': ['j', 'J'], 'position': (7.1, 2.8), 'width': 1},
        {'chars': ['l', 'L'], 'position': (8.2, 2.8), 'width': 1},
        {'chars': ['u', 'U'], 'position': (9.299999999999999, 2.8), 'width': 1},
        {'chars': ['y', 'Y'], 'position': (10.399999999999999, 2.8), 'width': 1},
        {'chars': [';', ':'], 'position': (11.499999999999998, 2.8), 'width': 1},
        {'chars': ['[', '{'], 'position': (12.599999999999998, 2.8), 'width': 1},
        {'chars': [']', '}'], 'position': (13.699999999999998, 2.8), 'width': 1},
        {'chars': ['\\', '|'], 'position': (14.799999999999997, 2.8), 'width': 1},
        {'chars': ['CAPS'], 'position': (0, 1.6999999999999997), 'width': 1.75},
        {'chars': ['a', 'A'], 'position': (1.85, 1.6999999999999997), 'width': 1},
        {'chars': ['r', 'R'], 'position': (2.95, 1.6999999999999997), 'width': 1},
        {'chars': ['s', 'S'], 'position': (4.050000000000001, 1.6999999999999997), 'width': 1},
        {'chars': ['t', 'T'], 'position': (5.15, 1.6999999999999997), 'width': 1},
        {'chars': ['d', 'D'], 'position': (6.25, 1.6999999999999997), 'width': 1},
        {'chars': ['h', 'H'], 'position': (7.35, 1.6999999999999997), 'width': 1},
        {'chars': ['n', 'N'], 'position': (8.45, 1.6999999999999997), 'width': 1},
        {'chars': ['e', 'E'], 'position': (9.549999999999999, 1.6999999999999997), 'width': 1},
        {'chars': ['i', 'I'], 'position': (10.649999999999999, 1.6999999999999997), 'width': 1},
        {'chars': ['o', 'O'], 'position': (11.749999999999998, 1.6999999999999997), 'width': 1},
        {'chars': ["'", '"'], 'position': (12.849999999999998, 1.6999999999999997), 'width': 1},
        {'chars': ['ENTER'], 'position': (13.949999999999998, 1.6999999999999997), 'width': 1.85},
        {'chars': ['SHIFT'], 'position': (0, 0.5999999999999996), 'width': 2.35},
        {'chars': ['z', 'Z'], 'position': (2.45, 0.5999999999999996), 'width': 1},
        {'chars': ['x', 'X'], 'position': (3.5500000000000003, 0.5999999999999996), 'width': 1},
        {'chars': ['c', 'C'], 'position': (4.65, 0.5999999999999996), 'width': 1},
        {'chars': ['v', 'V'], 'position': (5.75, 0.5999999999999996), 'width': 1},
        {'chars': ['b', 'B'], 'position': (6.85, 0.5999999999999996), 'width': 1},
        {'chars': ['k', 'K'], 'position': (7.949999999999999, 0.5999999999999996), 'width': 1},
        {'chars': ['m', 'M'], 'position': (9.049999999999999, 0.5999999999999996), 'width': 1},
        {'chars': [',', '<'], 'position': (10.149999999999999, 0.5999999999999996), 'width': 1},
        {'chars': ['.', '>'], 'position': (11.249999999999998, 0.5999999999999996), 'width': 1},
        {'chars': ['/', '?'], 'position': (12.349999999999998, 0.5999999999999996), 'width': 1},
        {'chars': ['SHIFT'], 'position': (13.449999999999998, 0.5999999999999996), 'width': 2.35},
        {'chars': ['CTRL'], 'position': (0, -0.5000000000000004), 'width': 1.25},
        {'chars': ['FN'], 'position': (1.35, -0.5000000000000004), 'width': 1.25},
        {'chars': ['WIN'], 'position': (2.7, -0.5000000000000004), 'width': 1.25},
        {'chars': ['ALT'], 'position': (4.050000000000001, -0.5000000000000004), 'width': 1.25},
        {'chars': ['SPACE'], 'position': (5.4, -0.5000000000000004), 'width': 6.35},
        {'chars': ['ALT'], 'position': (11.85, -0.5000000000000004), 'width': 1.25},
        {'chars': ['FN'], 'position': (13.2, -0.5000000000000004), 'width': 1.25},
        {'chars': ['CTRL'], 'position': (14.549999999999999, -0.5000000000000004), 'width': 1.25}]
}
s = 'sssssssss'

s="""Beneath the sprawling oak tree, a curious squirrel 
scurried about, gathering acorns and chattering excitedly as the 
golden sunlight filtered through the leaves, creating a mosaic of shadows on the ground; 
nearby, children laughed while flying kites in a vibrant array of colors that danced in 
the gentle breeze, their parents watching with smiles as a dog playfully chased after a 
butterfly, momentarily forgetting the world around them, while a distant train whistled, 
announcing its arrival, reminding everyone of the adventures that lay beyond the horizon,
where dreams and reality intertwined in a symphony of possibilities waiting to be explored."""

s = """In publishing and graphic design, Lorem ipsum (/ˌlɔː.rəm ˈɪp.səm/) is a placeholder text commonly used to demonstrate the visual form of a document or a typeface without relying on meaningful content. Lorem ipsum may be used as a placeholder before the final copy is available. It is also used to temporarily replace text in a process called greeking, which allows designers to consider the form of a webpage or publication, without the meaning of the text influencing the design.

Lorem ipsum is typically a corrupted version of De finibus bonorum et malorum, a 1st-century BC text by the Roman statesman and philosopher Cicero, with words altered, added, and removed to make it nonsensical and improper Latin. The first two words themselves are a truncation of dolorem ipsum ("pain itself").

Versions of the Lorem ipsum text have been used in typesetting at least since the 1960s, when it was popularized by advertisements for Letraset transfer sheets.[1] Lorem ipsum was introduced to the digital world in the mid-1980s, when Aldus employed it in graphic and word-processing templates for its desktop publishing program PageMaker. Other popular word processors, including Pages and Microsoft Word, have since adopted Lorem ipsum,[2] as have many LaTeX packages,[3][4][5] web content managers such as Joomla! and WordPress, and CSS libraries such as Semantic UI.

Example text
A common form of Lorem ipsum reads:

Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.

Source text
The Lorem ipsum text is derived from sections 1.10.32 and 1.10.33 of Cicero's De finibus bonorum et malorum.[6][7] The physical source may have been the 1914 Loeb Classical Library edition of De finibus, where the Latin text, presented on the left-hand (even) pages, breaks off on page 34 with "Neque porro quisquam est qui do-" and continues on page 36 with "lorem ipsum ...", suggesting that the galley type of that page was mixed up to make the dummy text seen today.[1]

The discovery of the text's origin is attributed to Richard McClintock, a Latin scholar at Hampden–Sydney College. McClintock connected Lorem ipsum to Cicero's writing sometime before 1982 while searching for instances of the Latin word consectetur, which was rarely used in classical literature.[2] McClintock first published his discovery in a 1994 letter to the editor of Before & After magazine,[8] contesting the editor's earlier claim that Lorem ipsum held no meaning.[2]

The relevant section of Cicero as printed in the source is reproduced below with fragments used in Lorem ipsum highlighted. Letters in brackets were added to Lorem ipsum and were not present in the source text:

[32] Sed ut perspiciatis, unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam eaque ipsa, quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, quia voluptas sit, aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos, qui ratione voluptatem sequi nesciunt, neque porro quisquam est, qui dolorem ipsum, quia dolor sit amet consectetur adipisci[ng] velit, sed quia non numquam [do] eius modi tempora inci[di]dunt, ut labore et dolore magnam aliquam quaerat voluptatem. Ut enim ad minima veniam, quis nostrum[d] exercitationem ullam corporis suscipit laboriosam, nisi ut aliquid ex ea commodi consequatur? [D]Quis autem vel eum i[r]ure reprehenderit, qui in ea voluptate velit esse, quam nihil molestiae consequatur, vel illum, qui dolorem eum fugiat, quo voluptas nulla pariatur?

[33] At vero eos et accusamus et iusto odio dignissimos ducimus, qui blanditiis praesentium voluptatum deleniti atque corrupti, quos dolores et quas molestias excepturi sint, obcaecati cupiditate non provident, similique sunt in culpa, qui officia deserunt mollitia animi, id est laborum et dolorum fuga. Et harum quidem reru[d]um facilis est e[r]t expedita distinctio. Nam libero tempore, cum soluta nobis est eligendi optio, cumque nihil impedit, quo minus id, quod maxime placeat facere possimus, omnis voluptas assumenda est, omnis dolor repellend[a]us. Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet, ut et voluptates repudiandae sint et molestiae non recusandae. Itaque earum rerum hic tenetur a sapiente delectus, ut aut reiciendis voluptatibus maiores alias consequatur aut perferendis doloribus asperiores repellat.

What follows is H. Rackham's translation, as printed in the 1914 Loeb edition, with words at least partially represented in Lorem ipsum highlighted:[7]

[32] But I must explain to you how all this mistaken idea of reprobating pleasure and extolling pain arose. To do so, I will give you a complete account of the system, and expound the actual teachings of the great explorer of the truth, the master-builder of human happiness. No one rejects, dislikes or avoids pleasure itself, because it is pleasure, but because those who do not know how to pursue pleasure rationally encounter consequences that are extremely painful. Nor again is there anyone who loves or pursues or desires to obtain pain of itself, because it is pain, but occasionally circumstances occur in which toil and pain can procure him some great pleasure. To take a trivial example, which of us ever undertakes laborious physical exercise, except to obtain some advantage from it? But who has any right to find fault with a man who chooses to enjoy a pleasure that has no annoying consequences, or one who avoids a pain that produces no resultant pleasure?

[33] On the other hand, we denounce with righteous indignation and dislike men who are so beguiled and demoralized by the charms of pleasure of the moment, so blinded by desire, that they cannot foresee the pain and trouble that are bound to ensue; and equal blame belongs to those who fail in their duty through weakness of will, which is the same as saying through shrinking from toil and pain. These cases are perfectly simple and easy to distinguish. In a free hour, when our power of choice is untrammeled and when nothing prevents our being able to do what we like best, every pleasure is to be welcomed and every pain avoided. But in certain circumstances and owing to the claims of duty or the obligations of business it will frequently occur that pleasures have to be repudiated and annoyances accepted. The wise man therefore always holds in these matters to this principle of selection: he rejects pleasures to secure other greater pleasures, or else he endures pains to avoid worse pains.

See also"""
# s = "11112345678a"
# s = "abcdefghijklmnopqrstuvwxyza"
# s = "1234567890-=qwertyuiop[asdfghjkl;zxcvbnm,.234567890-qwertyuiopasdfghjklzxcvbnm,10987654321qwertyuioasdfghjkzxcvbnm123456789qwertyuiasdfghjzxcvbn12345678qwertyuasdfghzxcvb1234567qwertyasdfgzxcv123456qwertasdfzxc12345qwerasdzx1234qweasz123qwa12q1"

import time
# t1 = time.time() 

keyboard = Keyboard(keyboard_layouts['qwerty'])
keyboard.run(s)   # 42.362 seconds

# t2 = time.time()
# print(int(1000*(t2-t1)),'ms')

#After converting for loops into numpy vectors - 747ms



