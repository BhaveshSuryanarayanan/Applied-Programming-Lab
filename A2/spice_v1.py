import numpy as np

file = open('input.txt','r')

nodes = ['GND']

class Component():
    def __init__(self,type,name,value):
        self.type = type
        self.name = name
        self.value = value
        
start = 0
lines = file.readlines()
for line in lines:
    if '.circuit' in line:
        start = 1
        continue
    
    if '.end' in line:
        start = 0
        continue
    
    if not start:
        continue
    
    words = line.strip().split()
    print(words)
    
    if words[1] not in nodes:
        nodes.append(words[1])
        
    if words[2] not in nodes:
        nodes.append(words[2])

print('Node list : ',nodes)

label = {}
for i,n in enumerate(nodes):
    label[n] = i
print('label dict :', label)

circuit = [[] for _ in range(len(nodes))]

for line in lines:
    if '.circuit' in line:
        start = 1
        continue
    
    if '.end' in line:
        start = 0
        continue
    
    if not start:
        continue
    
    words = line.strip().split()
    component1  = Component(words[0][0],words[0],int(words[-1]))
    
    n1, n2 = words[1], words[2]
    circuit[label[n1]].append([label[n2],component1])
    
    if words[0][0].upper()=='R':
        component2  = Component(words[0][0],words[0],int(words[-1]))
    else :
        component2  = Component(words[0][0],words[0],-int(words[-1]))
        
    circuit[label[n2]].append([label[n1],component2])
    
# print(circuit[0][0][0],circuit[0][0][1].name)#,circuit[0][1].name)
def print_circuit_graph(circuit):
    for i in range(len(circuit)):
        print(i,end="  ")
        for el in circuit[i]:
            print(f'[{el[0]} ({el[1].type}, {el[1].name}, {el[1].value})]', end = "  ")
        print()


# print_circuit_graph(circuit)

n = len(nodes)-1
A = np.zeros((n,n))
B = np.zeros(n)

# should try recursive
# def build_matrix(circuit):
n = len(nodes)-1
size = 6
A = np.zeros((size,size))
B = np.zeros(size)

visited = np.zeros(n+1,dtype=bool)
print(visited)

for i in range(0,n+1):
    p = 0
    q = 0
    for el in circuit[i]:
        if(el[1].type=='V'):
            circuit[i][p], circuit[i][q] = circuit[i][q],circuit[i][p]
            p+=1
        q+=1

print_circuit_graph(circuit)

last = size-1
def update(i,r):
    # if visited[i]:
    #     return
    visited[i] = 1 
    
    for el in circuit[i]:
        n1 = i
        n2 = el[0]
        print(n1,n2)
        print(A,B,r)
        comp = el[1]
        val = comp.value
        if comp.type == 'R':
            if n1:
                A[r][n1-1]+=1/val
            if n2:
                A[r][n2-1]+=-1/val
        elif comp.type == 'I':
            B[r]+=val
        else:   
            print(visited)
            if visited[n2]==0:
                update(n2,r) 
                print('yes')
                if not (np.all(A[r]==0) and B[r]==0):
                    r+=1
                if n1:
                    A[r][n1-1]+=1
                if n2:
                    A[r][n2-1]-=1
                B[r] += val
                r+=1
            # last-=1
    return r
        
            
r = 0
last = size-1
for i in range(1,n+1):
    print('og r:',r)
    r = update(i,r)+1
#     # print('last :',last)
# update(1,0)
print(A,B)
# for i in range(1,n+1):
#     for el in circuit[i]:
#         n1 = i
#         n2 = el[0]
#         comp = el[1]
#         val = comp.value
#         if comp.type == 'R':
#             A[i][n1-1]+=1/val
#             A[i][n2-1]+=-1/val
#         elif comp.type == 'I':
#             B[i]+=val
#         else:
#             pass

            
    
# print(A,B)
    