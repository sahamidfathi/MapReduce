import sys
from collections import Counter

part_num = sys.argv[2]
filename = sys.argv[3]
user_name = sys.argv[4]

path = '/home/' + user_name + '/Documents/' + filename + '_part' + part_num + '.txt'

# Mapping.
with open(path, 'r') as f:
	# Removing punctuation marks.
	data = f.read().translate({ord(i): None for i in ',.?!"—-@#$%^&*()_=+'}).split()

# Combining (Preliminary reducing).
count=Counter(data)

# Sorting.
count_sorted = {key: value for key, value in sorted(count.items())}
#print(count_sorted)

# Save into file.
f = open('/home/' + user_name + '/Documents/' + 'MappedCombined_' + filename + '_part' + part_num + '.txt', "w")
for key in count_sorted:
	f.write("<" + key + ", " + str(count_sorted[key]) + ">" + '\n')
