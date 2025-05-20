import numpy as np
from collections import defaultdict
import os

def evalSpice(filename):
    
    if not os.path.exists(filename):
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")
    
    file = open(filename,'r')

    nodes = ['GND']

    class Component():
        def __init__(self,type,name,value):
            self.type = type
            self.name = name
            self.value = value

    class Vsource():
        def __init__(self,name,value,node1,node2,ind):
            self.name = name
            self.val = value
            self.n1 = node1
            self.n2 = node2
            self.ind = ind

    vsource_dict = {}
    vlist = []
    
    start = 0
    malform_check = 0
    lines = file.readlines()
    for line in lines:
        if '.circuit' in line:
            start = 1
            if malform_check%2:
                raise ValueError('Malformed circuit file')
            malform_check+=1
            continue
        
        if '.end' in line:
            start = 0
            if not malform_check%2:
                raise ValueError('Malformed circuit file')
            malform_check+=1
            continue

        if not start:
            continue
        
        line = line.split('#')[0].strip()
        words = line.strip().split()
        print(words)
        
        
        if len(words)<3:
            continue
        
        if words[0][0]!='V' and words[0][0]!='R' and words[0][0]!='I':
            raise ValueError('Only V, I, R elements are permitted')
        
        if words[1] not in nodes:
            nodes.append(words[1])
            
        if words[2] not in nodes:
            nodes.append(words[2])
        
    if malform_check <2:
        raise ValueError('Malformed circuit file')
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
        
        line = line.split('#')[0].strip()
        words = line.strip().split()
        
        
        component1  = Component(words[0][0],words[0],float(words[-1]))
        
        n1, n2 = words[1], words[2]
        circuit[label[n1]].append([label[n2],component1])
        
        
        if words[0][0].upper() == 'V':
            vsource_dict[words[0]] = Vsource(words[0][0],float(words[-1]),label[n1],label[n2],len(vlist))
            vlist.append(words[0])
            
            
        if words[0][0].upper()=='R':
            component2  = Component(words[0][0],words[0],float(words[-1]))
        else :
            component2  = Component(words[0][0],words[0],-float(words[-1]))
            
        circuit[label[n2]].append([label[n1],component2])
        
    # print(circuit[0][0][0],circuit[0][0][1].name)#,circuit[0][1].name)
    def print_circuit_graph(circuit):
        for i in range(len(circuit)):
            print(i,end="  ")
            for el in circuit[i]:
                print(f'[{el[0]} ({el[1].type}, {el[1].name}, {el[1].value})]', end = "  ")
            print()

    keys = list(vsource_dict.keys())
    values = list(vsource_dict.values())
    print('VVVVV:',keys,values)
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            v1 = values[i]
            v2 = values[j]
            # print(f'{v1.n1} {v1.n2} {v1.val}')
            # print(f'{v2.n1} {v2.n2} {v2.val}')
            if v1.n1==v2.n1 and v1.n2==v2.n2 and v1.val!=v2.val:
                raise ValueError('Circuit error: no solution')
            if v1.n2==v2.n1 and v1.n1==v2.n2 and v1.val!=-v2.val:
                raise ValueError('Circuit error: no solution')

    n = len(nodes)-1
    K = len(vlist)
    A = np.zeros((n,n))
    B = np.zeros(n)

    # should try recursive
    # def build_matrix(circuit):
    n = len(nodes)-1
    size = n+K
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
        # if visited[i]:
        #     return
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
                B[r]+=-val
            else:   
                p = vsource_dict[comp.name].ind
                updated+=1
                if n1==vsource_dict[comp.name].n1:
                    A[r][n+p]+=1
                else:
                    A[r][n+p]-=1
                    
                print(visited)
                if visited_sources[comp.name]>=2:
                    break
                visited_sources[comp.name]+=1
                if visited[n2]==0:
                    # update(n2,r) 
                    print('yes')
                    t = [n1,n2,val]
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
    print(A,B)

    node_voltage = np.linalg.solve(A,B)
    node_voltage = np.insert(node_voltage,0,0)
    print('solution:',node_voltage)
    
    if not np.linalg.det(A):
        raise ValueError('Circuit error: no solution')

    # output = [{'GND':0}]
    output = {}
    for i in range(len(nodes)):
        output[nodes[i]]=node_voltage[i]
    print(output)

    print(vsource_dict)
    vsource_current = {}
    print(n,K,size)
    for i in range(n,size):
        vsource_current[vlist[i-n]] = node_voltage[i+1]
    print(output,vsource_current)
    # print(A,B)
        # print(A,B)
    return(output,vsource_current)

filename = r"D:\sem3\APL\A2\testcases\tc7.txt"
evalSpice(filename)