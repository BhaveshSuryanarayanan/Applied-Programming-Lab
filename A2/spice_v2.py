import numpy as np


nodes = ['GND']

def evalSpice(file):
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
        
        line = line.split('#')[0].strip()
        words = line.strip().split()
        print(words)
        
        if len(words)<3:
            continue
        
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
        
        if len(words)<3:
            continue
        
        words = line.strip().split()
        component1  = Component(words[0][0],words[0],float(words[-1]))
        
        n1, n2 = words[1], words[2]
        circuit[label[n1]].append([label[n2],component1])
        
        if words[0][0].upper()=='R':
            component2  = Component(words[0][0],words[0],float(words[-1]))
        else :
            component2  = Component(words[0][0],words[0],-float(words[-1]))
            
        circuit[label[n2]].append([label[n1],component2])
        
    def print_circuit_graph(circuit):
        for i in range(len(circuit)):
            print(i,end="  ")
            for el in circuit[i]:
                print(f'[{el[0]} ({el[1].type}, {el[1].name}, {el[1].value})]', end = "  ")
            print()

    n = len(nodes)-1
    A = np.zeros((n,n))
    B = np.zeros(n)

    n = len(nodes)-1
    size = n
    A = np.zeros((size,size))
    B = np.zeros(size)

    visited = np.zeros(n+1,dtype=bool)
    print(visited)

    from collections import defaultdict
    visited_sources = defaultdict(int)

    for i in range(0,n+1):
        p = 0
        q = 0
        for el in circuit[i]:
            if(el[1].type=='V'):
                circuit[i][p], circuit[i][q] = circuit[i][q],circuit[i][p]
                p+=1
            q+=1

    print_circuit_graph(circuit)
    stack = []
    last = size-1
    def update(i,r):
        visited[i] = 1 
        
        vpresent = 0
        updated = 0
        for el in circuit[i]:
            n1 = i
            n2 = el[0]
            print(n1,n2)
            print(A,B,r)
            comp = el[1]
            val = comp.value
            if comp.type == 'R':
                # if vpresent:
                #     break
                updated+=1
                if n1:
                    A[r][n1-1]+=1/val
                if n2:
                    A[r][n2-1]+=-1/val
            elif comp.type == 'I':
                # if vpresent:
                #     break
                updated+=1
                B[r]+=val
            else:   
                print(visited)
                if visited_sources[comp.name]>=2:
                    break
                visited_sources[comp.name]+=1
                if visited[n2]==0:
                    update(n2,r) 
                    print('yes')
                    t = [0,0,0]
                    t[0] = n1
                    t[1] = n2
                    t[2] = val
                    stack.append(t)
                    print('STACK APPENDED',n1,n2)
                # last-=1
        
        if updated:
            r+=1
        return r
            
                
    r = 0
    last = size-1
    for i in range(1,n+1):
        print('og r:',r)
        r = update(i,r)
        print(f'DONE {i}')
    #     # print('last :',last)
    # update(1,0)
    print('stack: ',stack)
    print(A)
    # A = A[:-1]
    # print(A)
    r-=1
    # newrow = np.zeros(size)
    for i,row in enumerate(stack):
        for k in range(len(A[-1-i])):
            A[-1-i]=0
        B[-1-i]=0
        
        if row[0]:
            A[-1-i][row[0]-1]=1
        if row[1]:
            A[-1-i][row[1]-1]=-1
        B[-1-i]+= row[2]
            
    #     if row[0]:
    #         newrow[row[0]-1]=1
    #     if row[1]:
    #         newrow[row[1]-1]=1
    #     B[r]+= row[2]
    # A = np.vstack([A,newrow])
    print(A,B)

    node_voltage = np.linalg.solve(A,B)
    print(node_voltage)

    output = [{'GND':0}]
    for i in range(1,len(nodes)):
        output.append({nodes[i]:node_voltage[i-1]})
    print(output)

        
    # print(A,B)


filename = open(r"D:\sem3\APL\A2\testcases\tc3.txt",'r')
evalSpice(filename)