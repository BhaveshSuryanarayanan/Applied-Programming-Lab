from collections import defaultdict
freq = defaultdict(int)

def letter_count(s):
    for l in s:
        freq[l]+=1
    
    return freq


	
def compare_dicts(actual, expected):
    if len(actual) != len(expected):
        return False
    return all(actual.get(k) == v for k, v in expected.items())

# Test case 2: Case with uppercase and lowercase letters
result = letter_count("Hello World")
expected = {'H': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'W': 1, 'r': 1, 'd': 1}
print(compare_dicts(result, expected))