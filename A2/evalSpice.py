import numpy as np
from collections import defaultdict
import os

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
    
    # print('Node list : ',nodes) #Debugging print statement 1
    # print('label dict :', label) #Debugging print statement 2      
    # print(circuit[0][0][0],circuit[0][0][1].name) # Debugging print statement 3
    
    def print_circuit_graph(circuit): # function to print the circuit
        for i in range(len(circuit)):
            print(i,end="  ")
            for el in circuit[i]:
                print(f'[{el[0]} ({el[1].type}, {el[1].name}, {el[1].value})]', end = "  ")
            print()

    # print_circuit_graph(circuit) # Debugging print statement 4

    n = len(nodes)-1 # no. of nodes excluding GND
    K = len(vlist)  #no. of voltage sources

    n = len(nodes)-1
    size = n+K  # no.of equations = n+K
    
    # Initialize conductance matrix
    A = np.zeros((size,size))
    B = np.zeros(size)

    # Array to keep track of visited nodes
    visited = np.zeros(n+1,dtype=bool)
    
    # print(visited) # Debugging print statement 5

    # Brings the voltage sources to the first using two pointers technique
    for i in range(0,n+1):
        p = 0
        q = 0
        for el in circuit[i]:
            if(el[1].type=='V'):
                circuit[i][p], circuit[i][q] = circuit[i][q],circuit[i][p]
                p+=1
            q+=1

    # print_circuit_graph(circuit) # Debugging print statement 6
    
    # List to store voltage equations of voltage sources
    voltage_equations = []
    
    # Function to write equation for node i
    def update(i,r):
        '''
        Function to write equation for node no. i
        Modifies matrices A and B
        returns r, the next empty row in conductance matrix
        '''
        
        # Mark node as visited
        visited[i] = 1 
        
        #variable to track update in matrix
        updated = 0
        
        #iterate through the nodes connected to node i
        for el in circuit[i]:
            n1 = i
            n2 = el[0]  # connected node
            
            # print(n1,n2)
            # print(A,B,r) # Debugging print statement 7
            
            # The component connected between the nodes
            comp = el[1]
            val = comp.value
            
            if comp.type == 'R':
                '''
                If component is resistor, add the current
                V1/R - V2/R
                to the equations
                
                if V1 or V2 is not GND
                '''
                updated+=1
                if n1:
                    A[r][n1-1]+=1/val
                if n2:
                    A[r][n2-1]+=-1/val
                    
            elif comp.type == 'I':
                '''
                If the component is current source, just add the current to the equations
                '''
                updated+=1
                B[r]+=-val
                
            else:   
                '''
                If the component is voltage source,
                1) add the current variable corresponding to the voltage source
                2) Add the voltage equation V1 - V2 = Vsource if set {n1,n2} is not already explored
                '''
                p = vsource_dict[comp.name].ind # voltage source index
                updated+=1
                
                # Check terminal of voltage source and add current  
                if n1==vsource_dict[comp.name].n1:
                    A[r][n+p]+=1
                else:
                    A[r][n+p]-=1
                    
                # print(visited) # Debugging print statement 8
                
                # If the the n2 was not already visited, add the votlage equation to the list
                if visited[n2]==0:
                    t = [n1,n2,val]
                    voltage_equations.append(t)
                    # print('voltage_equations APPENDED',n1,n2) # Debugging print statement 9
                
        #if there are no updates (no components) don't increment r
        if updated:
            r+=1
            
        return r
            
    
    #iterate to each node and write the equations in the matrix        
    r = 0 
    for i in range(1,n+1):
        r = update(i,r)
        
    # print('voltage_equations: ',voltage_equations) # Debugging print statement 10
    # print(A) # Debugging print statement 11
    
    # add the voltage equations to the conductance matrix from the back
    for i,row in enumerate(voltage_equations):
        for k in range(len(A[-1-i])):
            A[-1-i]=0
        B[-1-i]=0
        
        if row[0]:
            A[-1-i][row[0]-1]=1
        if row[1]:
            A[-1-i][row[1]-1]=-1
        B[-1-i]+= row[2]
            
    # print(A,B) # Debugging print statement 12
    
    '''
    If the obtained conductance matrix is singular then it means one of the following conditions
    1) Loop with only voltage sourcees
    2) Node with current source in each branch or each brance is connected to such a node
    Raise value Error in that case
    '''
    if not np.linalg.det(A):
        raise ValueError('Circuit error: no solution')

    # Solve the linear equations using the numpy function
    node_voltage = np.linalg.solve(A,B)
    
    # Add the voltage of GND as zero in the solution list
    node_voltage = np.insert(node_voltage,0,0)
    
    # print('solution:',node_voltage) # Debugging print statement 13
    
    # output dict with voltages for each node
    output = {}
    for i in range(len(nodes)):
        output[nodes[i]]=node_voltage[i]
    # print(output) # Debugging print statement 14

    # dict to store the current to each voltage source
    vsource_current = {}
    for i in range(n,size):
        vsource_current[vlist[i-n]] = node_voltage[i+1]
    # print(output,vsource_current) # Debugging print statement 15
    
    # Return the answer!!
    return (output,vsource_current)