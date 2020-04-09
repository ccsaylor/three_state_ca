import random
from matplotlib import pyplot as plt
from numpy import array_equal

# user-defined variables
rule_number = 110
length = 100
time = 100 

# create the initial string
initial_condition = []
for i in range(length):
    initial_condition.append(random.randint(0,2))
print(initial_condition)

# list of possible neighborhoods
neighborhoods = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

# convert rule number to ternary
n = rule_number
nums = []
while n:
    n, r = divmod(n, 3)
    nums.append(str(r))
in_ternary = ''.join(reversed(nums))

# pad the ternary number with zeroes
ternary_length = len(in_ternary)
if ternary_length != 9:
    padding = 9 - ternary_length
    in_ternary = '0'*padding + in_ternary
print(in_ternary)

# create a lookup table of rules
lookup_table = dict(zip(neighborhoods, reversed(in_ternary)))

for key, val in lookup_table.items():
    print(key, '-->', val)

spacetime_field = [initial_condition]
current_configuration = initial_condition.copy()

new_configuration = []
for t in range(time):
    new_configuration = []
    for i in range(len(current_configuration)):
        
        neighborhood = (current_configuration[(i-1)%length], 
                        current_configuration[i])
        
        new_configuration.append(int(lookup_table[neighborhood]))
    # update the current configuration    
    current_configuration = new_configuration # here we don't want to keep making new copies, so use '='
    # add the new configuration to the spacetime field
    spacetime_field.append(new_configuration)

plt.figure(figsize=(12,12))
plt.imshow(spacetime_field, cmap=plt.cm.Greys, interpolation='nearest')
plt.show()