import numpy as np
import matplotlib.pyplot as plt
import time

Nmics = 16
Nsamp = 1000

pitch = 2
dist_per_samp = 0.01
C = 1

src = (0,0)
obstacle = (1.0,1.0)

mics = []

xRES, yRES = 200,200
xMAX = 5
xMIN = -5
yMAX = 5
yMIN = -5
xSTEP = (xMAX-xMIN)/xRES
ySTEP = (yMAX-yMIN)/yRES


for n in range(Nmics):
    mics.append(pitch/2 + (n-Nmics/2)*pitch)
mics = np.array(mics)
print(mics)

SincP = 1.0
def wsrc(t):
    return np.sinc(SincP*t)

def dist(src,x,y):
    (x0,y0) = src
    return np.sqrt((x0-x)**2+(y0-y)**2)

def dist_obj(src,obj,x,y):
    (x0,y0) = src
    (x1,y1) = obj
    return np.sqrt((x0-x1)**2+(y0-y1)**2)+np.sqrt((x1-x)**2+(y1-y)**2)

tsamp = 0

mic_data = np.zeros((Nmics,1))
x = np.arange(xMIN,xMAX,xSTEP)
y = np.arange(yMIN,yMAX,ySTEP)

while tsamp<Nsamp:
    plt.clf()
    X, Y = np.meshgrid(x, y)
    d = dist(src,X,Y)
    t = d/(dist_per_samp*C)
    
    d2 = dist_obj(src,obstacle,X,Y)
    t2 = d2/(dist_per_samp*C)
    
    z = (wsrc(tsamp-t)+wsrc(tsamp-t2))
    # z = (wsrc(tsamp-t))
    
    tmics = dist(src,0,mics)/(dist_per_samp*C)
    tmics2 = dist_obj(src,obstacle,0,mics)/(dist_per_samp*C)
    
    # zmic =  wsrc(tsamp-tmics)+wsrc(tsamp-tmics2)
    # zmic =  wsrc(tsamp-tmics)
    zmic =  wsrc(tsamp-tmics2)
    
    zmic = zmic.reshape(-1,1)
    
    mic_data = np.hstack((mic_data,zmic))
    
        
    plt.imshow(z,cmap='plasma',vmin=0,vmax=1,extent=(x.min(), x.max(), y.min(), y.max()))
    
    # for i in range(Nmics):
    #     circle = plt.Circle((0, (mics[i]-yMIN)*yRES/(yMAX-yMIN)), 10, color='white', fill=True)
    #     plt.gca().add_patch(circle)
        
    # plt.axis([xMIN, xMAX, yMIN, yMAX])
    # plt.pause(0.5)
    
    # plt.pause(0.01)
    
    tsamp+=1

t = np.arange(0,Nsamp,1)
mic_data = np.delete(mic_data,0, axis=1)

print(mic_data[0])
plt.close()
plt.figure(figsize=(5,5))
print(mic_data.shape)
for i in range(Nmics):
    plt.plot(t,mic_data[i])
# plt.show()


print('start')
tsamp = 0

def digital_output(mic_data,d):
    i = ((d//dist_per_samp).astype(int))%Nsamp
    
    return mic_data[i]

mx = -10000
while tsamp<Nsamp:
    print(tsamp)
    plt.clf()
    X, Y = np.meshgrid(x, y)
    for i in range(Nmics):
        d = dist((0,mics[i]),X,Y)
        
        if i==0:
            z = digital_output(mic_data[i],d-tsamp*dist_per_samp)
        else:
            z += digital_output(mic_data[i],d-tsamp*dist_per_samp)
    max_index = np.unravel_index(np.argmax(z), z.shape) 
    zmx = z[max_index[0],max_index[1]]
    if zmx>mx:
        mx_ind = max_index
        mx = zmx
    # plt.imshow(z,cmap='plasma',vmin=0,vmax=1,extent=(x.min(), x.max(), y.min(), y.max()))
    # plt.imshow(z,cmap='plasma',extent=(x.min(), x.max(), y.min(), y.max()))
    
    # for i in range(Nmics):
    #     circle = plt.Circle((0, (mics[i]-yMIN)*yRES/(yMAX-yMIN)), 10, color='white', fill=True)
    #     plt.gca().add_patch(circle)
        
    plt.axis([xMIN, xMAX, yMIN, yMAX])
    # plt.pause(0.01)
    
    
    # plt.pause(0.01)
    
    tsamp+=1
print(mx_ind,mx_ind[0]*xSTEP,mx_ind[1]*ySTEP)
