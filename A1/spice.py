from collections import defaultdict
import io

d = defaultdict(int)
start=0
p=0

def circuit_count(msg):
    sfp = io.StringIO(msg)
    p=0
    for line in sfp.readlines():
        words = line.split()
        
        if '.end' in words:
            p=0
            
        if '.circuit' in words:
            p=1
            
        if p==0:
            continue
        
        if len(words)<2:
            continue
        
        comp = words[0][0]
        # cnt = int(words[1])
        
        d[comp]+=1
        
    return d

from collections import defaultdict
import io

def circuit_count(msg):
    d = defaultdict(int)  # Initialize defaultdict to count components
    sfp = io.StringIO(msg)  # Create an in-memory file-like object
    p = 0  # State variable to determine if we're inside a .circuit section
    
    for line in sfp:
        words = line.split()
        
        if '.end' in words:
            p = 0  # End of circuit section
        
        if '.circuit' in words:
            p = 1  # Start of circuit section
        
        if p == 0:
            continue  # Skip lines outside .circuit sections
        
        if len(words) < 2:
            continue  # Skip lines that don't have enough words
        
        comp = words[0][0]  # Get the first character of the first word
        d[comp] += 1  # Increment the count for this component
    
    return d  # Return the defaultdict with counts

	
	
msg = """
* Circuit with both voltage and current sources

.circuit
Vsource n1 GND 10
Isource n3 GND 1
R1 n1 n2 2
R2 n2 n3 5
L3 n2 GND 3
.end
"""
X = circuit_count(msg)
Exp = {'V': 1, 'R': 2}
for i in Exp.keys():
  if Exp[i] != X[i]:
    print("FAIL")
print("PASS")
print(X)