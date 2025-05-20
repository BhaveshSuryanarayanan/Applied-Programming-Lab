import numpy as np
import os

nodes = ['GND']
def evalSpice(filename):
    
    #raise error file path is invalid
    if not os.path.exists(filename):
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")
    
    file = open(filename,'r')

    # Class to store the components of the circuit
    class Component():
        def __init__(self,type,name,value):
            self.type = type
            self.name = name
            self.value = value

    # Class to store the Voltage sources of the circuit
    class Vsource():
        def __init__(self,name,value,node1,node2,ind):
            self.name = name
            self.val = value
            self.n1 = node1
            self.n2 = node2
            self.ind = ind

    # List of the nodes in the circuit and dict to access the index of the nodes with ease
    nodes = []
    label = {}
    
    # Assuming GND is always one of the nodes, assign index zero to it
    nodes.append('GND')
    label['GND'] = 0
    
    #dictionary and list to source voltage sources
    vsource_dict = {}
    vlist = []
    
    # adjacency list to store the circuit connections (initialised for gnd)
    circuit = [[]]
    
    start = 0
    malform_check = 0
    
    #read lines from the file
    lines = file.readlines()
    for line in lines:
        
        # Start only after encountering .circuit
        if '.circuit' in line:
            start = 1
            if malform_check%2:
                raise ValueError('Malformed circuit file')
            malform_check+=1
            continue
        
        # End after encountering .end
        if '.end' in line:
            start = 0
            if not malform_check%2:
                raise ValueError('Malformed circuit file')
            malform_check+=1
            continue
        
        # Take input only if circuit has started
        if not start:
            continue
        
        # parse the uncommented portion of the line   
        line = line.split('#')[0].strip()
        words = line.strip().split()
        
        #ignore if number of words is less than 3
        if not len(words):
            continue
        
        # Raise value error in case of invalid element name
        if words[0][0]!='V' and words[0][0]!='R' and words[0][0]!='I':
            raise ValueError('Only V, I, R elements are permitted')
        
        # Read the nodes
        n1, n2 = words[1], words[2]
        
        # Add nodes to the list if it isn't already present
        if n1 not in nodes:
            nodes.append(n1)
            label[n1] = len(nodes)-1 # assign label
            circuit.append([])      # add empty list to the circuit
            
        if n2 not in nodes:
            nodes.append(n2)
            label[n2] = len(nodes)-1
            circuit.append([])
        
        # create an object with component data
        component1  = Component(words[0][0],words[0],float(words[-1]))
        
        # add the node along with the component to the circuit
        circuit[label[n1]].append([label[n2],component1])
        
        # Add voltage source component to the voltage source list and dict 
        if words[0][0].upper() == 'V':
            if len(words)<5:
                raise ValueError('Malformed circuit file')
            if words[3].lower() != 'dc':
                raise ValueError('Only V, I, R elements are permitted')
                
            vsource_dict[words[0]] = Vsource(words[0][0],float(words[-1]),label[n1],label[n2],len(vlist))
            vlist.append(words[0])
        
        # create resistor component
        if words[0][0].upper()=='R':
            if len(words)<4:
                raise ValueError('Malformed circuit file')
            component2  = Component(words[0][0],words[0],float(words[-1]))
            
        else :
            if len(words)<5:
                raise ValueError('Malformed circuit file')
            if words[3].lower() != 'dc':
                raise ValueError('Only V, I, R elements are permitted')
            component2  = Component(words[0][0],words[0],-float(words[-1]))
            
        circuit[label[n2]].append([label[n1],component2])
    
    # raise error incase there is no .circuit or .end in the file
    if malform_check <2:
        raise ValueError('Malformed circuit file')
    
        
    def print_circuit_graph(circuit):
        for i in range(len(circuit)):
            print(i,end="  ")
            for el in circuit[i]:
                print(f'[{el[0]} ({el[1].type}, {el[1].name}, {el[1].value})]', end = "  ")
            print()
    print(label)
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
        updated = 0
        for el in circuit[i]:
            n1 = i
            n2 = el[0]
            print(n1,n2)
            print(A,B,r)
            comp = el[1]
            val = comp.value
            if comp.type == 'R':
                updated+=1
                if n1:
                    A[r][n1-1]+=1/val
                if n2:
                    A[r][n2-1]+=-1/val
            elif comp.type == 'I':
                updated+=1
                B[r]+=-val
            elif comp.type=='V':   
                print(visited)
                if visited_sources[comp.name]>=2:
                    break
                visited_sources[comp.name]+=1
                
                #recursive call
                if visited[n2]==0:
                    update(n2,r) 
                    t = [n1,n2,val]
                    stack.append(t)
        
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

    if not np.linalg.det(A):
        raise ValueError('Circuit error: no solution')
    
    node_voltage = np.linalg.solve(A,B)
    
    # Add the voltage of GND as zero in the solution list
    node_voltage = np.insert(node_voltage,0,0)
    print(node_voltage)
    # print('solution:',node_voltage) # Debugging print statement 13
    
    # output dict with voltages for each node
    output = {}
    for i in range(len(nodes)):
        output[nodes[i]]=node_voltage[i]
    # print(output) # Debugging print statement 14
    
    def find_current(v):
        visited_sources[v]=1
        n1 = vsource_dict[vlist[v]].n1
        current = 0
        updated = 0
        for el in circuit[n1]:
            n2 = el[0]
            print(n1,n2,current)
            
            comp = el[1]
            val = comp.value
            
            
            if comp.type == 'R':
                # if vpresent:
                #     break
                updated+=1
                current += (output[nodes[n1]]-output[nodes[n2]])/val
                print("//",n1, n2,val,current)
                
            elif comp.type == 'I':
                # if vpresent:
                #     break
                updated+=1
                print("//",n1, n2,val)
                current+=val
            else:   
                if vsource_dict[comp.name].ind == v:
                    continue
                if visited_sources[vsource_dict[comp.name].ind]:
                    raise ValueError("Circuit error: no solution")
                current += find_current(vsource_dict[comp.name].ind)
        return current
    
    vsource_current = {}
    for i in range(len(vlist)):
        visited_sources = defaultdict(int)
        vsource_current[vlist[i]] = -find_current(i) 
    print(vsource_current)   
    
    return (output,vsource_current)