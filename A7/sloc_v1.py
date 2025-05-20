import numpy as np
import matplotlib.pyplot as plt
import time

Nmics = 5
Nsamp = 100

src = (1,2)

pitch = 0.1

dist_per_samp = 0.8

C = 1

obstacle = (8,5)

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

print(mics)

SincP = 5.0
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
# Nsamp = 10
img = np.zeros((xRES,yRES))

while tsamp < Nsamp:
    mn = 10000
    mx = -10000
    img = np.zeros((xRES,yRES))
    
    for i in range(xRES):
        for j in range(yRES):
            d = dist(src,i*xSTEP,j*ySTEP)
            t = d/(dist_per_samp*C)
            d2 = dist_obj(src,obstacle,i*xSTEP,j*ySTEP)
            t2 = d2/(dist_per_samp*C)
            
            img[i][j] += wsrc(tsamp-t)+wsrc(tsamp-t2)+0.2
            mn = min(mn,img[i][j])
            mx = max(mn,img[i][j])
            # img[i][j] += d
            
            # print(img)
            
    print(mn,mx)
    
    plt.clf()
    plt.imshow(img,cmap='plasma',vmin=0,vmax=1)
    plt.axis('off')
    # plt.show()
    # time.sleep(0.2)
    plt.pause(0.01)
    
    tsamp+=1
# print(img)
    
    





