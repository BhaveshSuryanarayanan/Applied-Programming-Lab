import matplotlib.pyplot as plt
import numpy as np

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

def create_radial_gradient(grayscale):
    resolution = 100
    gradient = np.zeros((resolution,resolution,4))
    centre = resolution//2
    MAX_RAD = np.sqrt(2*centre*centre)
    radius = 3*MAX_RAD/4
    mid = grayscale

    def expo(r):
        return np.exp(-r*r*0.0005)
    
    for x in range(resolution):
        for y in range(resolution):
            r = np.sqrt((x-centre)**2+(y-centre)**2)
            
            val = grayscale*expo(r)
            
            # R,G,B = custom_heat_map(val)
            
            val = max(val,0.2)
            cmap = plt.cm.jet_r
            R,G,B,alpha= cmap(1-val)
            
            alpha = grayscale*expo(r*1.5)
            gradient[x,y] = (R,G,B,alpha)
    
    return gradient
            
            
            
class Key:
    def __init__(self, ind, char,row,col, shift_char=None,freq=0):
        self.ind = ind
        self.char = char
        self.shift_char = shift_char
        self.freq=freq
        self.row = row
        self.col = col

class Keyboard():
    def __init__(self, listed_keyboard_layout, key_size):
        self.listed_keyboard_layout = listed_keyboard_layout
        self.key_size = key_size
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.fig.patch.set_facecolor(KEYBOARD_BG_COLOR)
        
        self.key_index = {}
        self.keyboard_layout = []
        index = 0
        for i,row in enumerate(self.listed_keyboard_layout):
            for j,key_chars in enumerate(row):
                normal_char = key_chars[0]
                shift_char = key_chars[1] if len(key_chars) > 1 else None
                
                key = Key(index, normal_char, shift_char=shift_char,row=i,col=j)
                self.keyboard_layout.append(key)
                
                self.key_index[normal_char] = index
                
                if shift_char:
                    self.key_index[shift_char] = index
                
                index += 1
                
        self.key_index[' '] = self.key_index['SPACE']
        self.key_index['\n'] = self.key_index['ENTER']
        
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
        Zor = 5
        for rowi in range(len(self.listed_keyboard_layout)):
            x_pos = x_start
            for j in range(len(self.listed_keyboard_layout[rowi])):
                dist = self.listed_keyboard_layout[rowi][j][0]
                if dist[0]=='%' and len(dist)>0:
                    x_pos +=int(dist[1:-1])
                    continue
                key_obj = self.keyboard_layout[k]
                k+=1
                
                key = key_obj.char
                width = self.key_size.get(key, 1)  
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
                rect = plt.Rectangle((x_pos, y_start), width, 1, edgecolor='black', facecolor=key_color)
                
                self.ax.add_patch(rect)
                
                if freq:
                    factor = 0.4
                    
                    # cmap = plt.cm.jet_r
                    # key_color = cmap((freq/(self.THRESH)))
                    key_color =  custom_heat_map((freq/self.THRESH))
                    
                    offset = 0.6
                    Gradient = create_radial_gradient(freq/self.THRESH)
                    self.ax.imshow(Gradient, extent=(x_pos-offset, x_pos+width+offset, y_start-offset,y_start+1+offset), origin='lower',zorder=Zor)
                    Zor+=1
                
                # self.ax.text(x_pos + width / 2, y_start + 0.5, str(freq).upper(), ha='center', va='center', fontsize=10,font=KEY_FONT)
                self.ax.text(x_pos + width / 2, y_start + 0.5, key.upper(), ha='center', va='center', fontsize=10,font=KEY_FONT,zorder=100)
                
                shift_key = key_obj.shift_char
                
                if shift_key != None and not shift_key.isalpha():
                    self.ax.text(x_pos + width / 5, y_start + 0.75, shift_key.upper(), ha='center', va='center', fontsize=10,font=KEY_FONT,zorder=100)
                    
                    
                    
                x_pos += width + 0.1  

            y_start -= 1.1  

        self.ax.set_xlim(0, 16 )
        self.ax.set_ylim(-0.5, 6)
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
    def clear_keyboard(self):
        for key in self.keyboard_layout:
            key.freq = 0
        
    def run(self,s = ""):

        i=0
        self.THRESH=0
        
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
                self.THRESH = max(self.THRESH,key.freq)
                if key.shift_char==s[i]:
                    self.keyboard_layout[self.key_index['SHIFT']].freq+=1
                    self.THRESH = max(self.THRESH,self.keyboard_layout[self.key_index['SHIFT']].freq)
                i+=1
                
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
                t = ""
                i=0
                print('cleared')
            
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

qwerty_key_size = {
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
dvorak_keyboard_layout = [
    [['ESC'], ['F1'], ['F2'], ['F3'], ['F4'], ['F5'], ['F6'], ['F7'], ['F8'], ['F9'], ['F10'], ['F11'], ['F12'], ['DELETE']],
    [['`', '~'], ['1', '!'], ['2', '@'], ['3', '#'], ['4', '$'], ['5', '%'], ['6', '^'], ['7', '&'], ['8', '*'], ['9', '('], ['0', ')'], ['[', '{'], [']', '}'], ['BACKSPACE']],
    [['TAB'], ['\'', '"'], [',', '<'], ['.', '>'], ['p', 'P'], ['y', 'Y'], ['f', 'F'], ['g', 'G'], ['c', 'C'], ['r', 'R'], ['l', 'L'], ['/', '?'], ['=', '+'], ['\\', '|']],
    [['CAPS'], ['a', 'A'], ['o', 'O'], ['e', 'E'], ['u', 'U'], ['i', 'I'], ['d', 'D'], ['h', 'H'], ['t', 'T'], ['n', 'N'], ['s', 'S'], ['-', '_'], ['ENTER']],
    [['SHIFT'], [';', ':'], ['q', 'Q'], ['j', 'J'], ['k', 'K'], ['x', 'X'], ['b', 'B'], ['m', 'M'], ['w', 'W'], ['v', 'V'], ['z', 'Z'], ['SHIFT']],
    [['CTRL'], ['FN'], ['WIN'], ['ALT'], ['SPACE'], ['ALT'], ['FN'], ['CTRL']]
]
dvorak_key_size = {
    'BACKSPACE': 1.5,
    'TAB': 1.5,
    'CAPS': 1.75,
    'ENTER': 1.85,
    'SHIFT': 2.35,
    'SPACE': 6.35,
    'CTRL': 1.25,
    'WIN': 1.25,
    'ALT': 1.25,
    'FN': 1.25,
    'DELETE': 1.5
}
colemak_keyboard_layout = [
    [['ESC'], ['F1'], ['F2'], ['F3'], ['F4'], ['F5'], ['F6'], ['F7'], ['F8'], ['F9'], ['F10'], ['F11'], ['F12'], ['DELETE']],
    [['`', '~'], ['1', '!'], ['2', '@'], ['3', '#'], ['4', '$'], ['5', '%'], ['6', '^'], ['7', '&'], ['8', '*'], ['9', '('], ['0', ')'], ['-', '_'], ['=', '+'], ['BACKSPACE']],
    [['TAB'], ['q', 'Q'], ['w', 'W'], ['f', 'F'], ['p', 'P'], ['g', 'G'], ['j', 'J'], ['l', 'L'], ['u', 'U'], ['y', 'Y'], [';', ':'], ['[', '{'], [']', '}'], ['\\', '|']],
    [['CAPS'], ['a', 'A'], ['r', 'R'], ['s', 'S'], ['t', 'T'], ['d', 'D'], ['h', 'H'], ['n', 'N'], ['e', 'E'], ['i', 'I'], ['o', 'O'], ['\'', '"'], ['ENTER']],
    [['SHIFT'], ['z', 'Z'], ['x', 'X'], ['c', 'C'], ['v', 'V'], ['b', 'B'], ['k', 'K'], ['m', 'M'], [',', '<'], ['.', '>'], ['/', '?'], ['SHIFT']],
    [['CTRL'], ['FN'], ['WIN'], ['ALT'], ['SPACE'], ['ALT'], ['FN'], ['CTRL']]
]
colemak_key_size = {
    'BACKSPACE': 1.5,
    'TAB': 1.5,
    'CAPS': 1.75,
    'ENTER': 1.85,
    'SHIFT': 2.35,
    'SPACE': 6.35,
    'CTRL': 1.25,
    'WIN': 1.25,
    'ALT': 1.25,
    'FN': 1.25,
    'DELETE': 1.5
}
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

keyboard = Keyboard(ergodox_keyboard_layout,qwerty_key_size)

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
s = "1234567890-=qwertyuiop[asdfghjkl;zxcvbnm,.234567890-qwertyuiopasdfghjklzxcvbnm,10987654321qwertyuioasdfghjkzxcvbnm123456789qwertyuiasdfghjzxcvbn12345678qwertyuasdfghzxcvb1234567qwertyasdfgzxcv123456qwertasdfzxc12345qwerasdzx1234qweasz123qwa12q1"

keyboard.run(s)