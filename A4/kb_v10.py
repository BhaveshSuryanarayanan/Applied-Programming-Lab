import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from layouts import keyboard_layouts

KEYBOARD_BG_COLOR = '#1c1c1c'
KEY_FONT = 'DejaVu Sans Mono'
DEFAULT_KEY_COLOR = '#656363'
            
class Key:
    def __init__(self, ind, char,x,y,width,height,side,start,shift_char=None,freq=0):
        self.ind = ind
        self.char = char
        self.shift_char = shift_char
        self.freq=freq
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.travel = 0
        self.start = start
        self.side = side

class Keyboard():
    def __init__(self, s):
        self.listed_keyboard_layout = keyboard_layouts[s.lower()]
        self.total_travel = 0
    
        self.store_layout()
        self.calc_travel()
        
        self.fig, self.ax = plt.subplots(figsize=((self.x_end-self.x_start)*12/16,(self.y_start-self.y_end)*8/6.5))
        self.fig.patch.set_facecolor(KEYBOARD_BG_COLOR)
        
    def store_layout(self):
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
            (w,h) = key['dimensions']
            start = key['start']
            normal_char = chars[0]
            side = key['side']
            if len(chars)>1:
                shift_char = chars[1] 
                self.key_index[shift_char] = index
            else:
                shift_char = None
                
            keyobj = Key(index, normal_char, shift_char=shift_char,x=x,y=y,width=w,height=h,start = start, side = side)
            self.keyboard_layout.append(keyobj)
            self.key_index[normal_char] = index
            
            index+=1
            
            # print(x,y)
            x_start = min(x_start,x)
            y_start = max(y_start,y+h)
            x_end = max(x_end,x+w)
            y_end = min(y_end,y)
            
        self.x_start = x_start
        self.y_start = y_start
        self.x_end = x_end
        self.y_end = y_end
        # print(self.x_start,self.x_end,self.y_start,self.y_end)
                
        self.key_index[' '] = self.key_index['SPACE']
        self.key_index['\n'] = self.key_index['ENTER']
    
    def calc_travel(self):
        for key in self.keyboard_layout:
            x1, y1 = key.x+key.width/2, key.y+key.height/2
            start_key = self.keyboard_layout[self.key_index[key.start]]
            x2, y2 = start_key.x+start_key.width/2, start_key.y+start_key.height/2
            key.travel = np.sqrt((x1-x2)**2+(y1-y2)**2)
            
    def create_radial_gradient(self, grayscale, xcentre, ycentre, xradius, yradius):
        # MAX_RAD = radius
        grayscale *= 0.8
        mid = grayscale

        # Calculate coordinates and radii in normalized units
        x0 = int(self.xRES * (xcentre - self.x_start) / (self.x_end - self.x_start))
        y0 = int(self.yRES * (ycentre - self.y_start) / (self.y_end - self.y_start))
        rx = abs(int(self.xRES * xradius / (self.x_end - self.x_start)))
        ry = abs(int(self.yRES * yradius / (self.y_end - self.y_start)))
        fact = 3
        xmin = max(0,x0 - fact * rx)
        xmax = min(self.xRES, x0 + fact * rx)
        ymin = max(0,y0 - fact * ry)
        ymax = min(self.yRES, y0 + fact * ry)
        # Create meshgrid of x and y coordinates
        x = np.arange(xmin, xmax)
        y = np.arange(ymin, ymax)
        xx, yy = np.meshgrid(x, y)
        # print(yy)
        # Calculate distances from the center
        r = np.sqrt((xx - x0)**2 + (yy - y0)**2)
        # print(r)
        # Calculate grayscale and alpha values
        val = grayscale * np.exp(-(r**2) * 0.0005)
        alpha = grayscale * np.exp(-(r**2) * 0.0004)

        # Apply values to masks, ensuring they don't exceed maximum values
        self.grey_mask[-yy-1, xx] = np.minimum(0.9, val + self.grey_mask[-yy-1, xx])
        self.alpha_mask[-yy-1, xx] = np.minimum(0.8, alpha + self.alpha_mask[-yy-1, xx])

                
    def colorize(self):
        
        cmap = plt.cm.jet
        colored = cmap(self.grey_mask)
        colored[...,3] = self.alpha_mask
        self.color_mask = colored
        # print('colorized')
              
    def draw_keyboard_layout(self):
        
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
        
        
        self.ax.cla()
        
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
            x_pos,y_pos,width, height = key_obj.x, key_obj.y, key_obj.width, key_obj.height
            rect = FancyBboxPatch((x_pos, y_pos), width, height, edgecolor='black', facecolor=key_color,boxstyle="round,pad=0.0,rounding_size=0.1")
            # rect = plt.Rectangle((x_pos, y_pos), width, height, edgecolor='black', facecolor=key_color)
            
            self.ax.add_patch(rect)
            
            if freq and self.THRESH:
                factor = 0.4
                
                # cmap = plt.cm.jet_r
                # key_color = cmap((freq/(self.THRESH)))
                offset = 0.6
                # print(x_pos+width/2,y_pos+height/2)
                self.create_radial_gradient(grayscale=(freq/self.THRESH),xcentre=x_pos+width/2,ycentre=y_pos+height/2,xradius=width/2+offset,yradius=height/2+offset)
                
                # Gradient = self.create_radial_gradient(freq/self.THRESH)
                # self.ax.imshow(Gradient, extent=(x_pos-offset, x_pos+width+offset, y_pos-offset,y_pos+1+offset), origin='lower',zorder=5)

            
            # self.ax.text(x_pos + width / 2, y_pos + 0.5, str(freq).upper(), ha='center', va='center', fontsize=10,font=KEY_FONT)
            label = key.upper() #if 'SHIFT' not in key.upper() else 'SHIFT'
            self.ax.text(x_pos + width / 2, y_pos + height/2, label, ha='center', va='center', fontsize=10,font=KEY_FONT,zorder=100)
            
            shift_key = key_obj.shift_char
            
            if shift_key != None and not shift_key.isalpha():
                self.ax.text(x_pos + width / 5, y_pos + 0.75, shift_key.upper(), ha='center', va='center', fontsize=10,font=KEY_FONT,zorder=100)
                # Zor+=1
        print(self.x_start,self.x_end,self.y_start,self.y_end)
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
        self.THRESH = 0
        print('cleared')
        
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
                self.total_travel+=key.travel
                if s[i]==' ':
                    i+=1
                    continue
                key.freq+=1
                self.THRESH = max(self.THRESH,key.freq)
                
                if key.shift_char==s[i]:
                    shift = 'R' if key.side =='L' else 'L'
                    self.keyboard_layout[self.key_index[shift+'SHIFT']].freq+=1
                    self.THRESH = max(self.THRESH,self.keyboard_layout[self.key_index[key.side+'SHIFT']].freq)
                
                i+=1
               
            print(self.total_travel)
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
                self.THRESH=0
                s = ""
                t = ""
                i=0
                self.total_travel=0
            s+=t
        print(s)

d1 = 1.1
a1 = 0.2
a2 = 0.4
a3 = 0.2
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
# s= 'abcd\nancd  \n'
# s = "11112345678a"
# s = "abcdefghijklmnopqrstuvwxyza"
# s = "1234567890-=qwertyuiop[asdfghjkl;zxcvbnm,.234567890-qwertyuiopasdfghjklzxcvbnm,10987654321qwertyuioasdfghjkzxcvbnm123456789qwertyuiasdfghjzxcvbn12345678qwertyuasdfghzxcvb1234567qwertyasdfgzxcv123456qwertasdfzxc12345qwerasdzx1234qweasz123qwa12q1"
s = '      \n\nPPPPP'
import time
# t1 = time.time() 

keyboard = Keyboard('ergodox')
keyboard.run(s)   # 42.362 seconds

# t2 = time.time()
# print(int(1000*(t2-t1)),'ms')

#After converting for loops into numpy vectors - 747ms
