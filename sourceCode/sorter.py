import sys
import glob

user_name = sys.argv[2]

path = '/home/' + user_name + '/Documents/' + 'MappedCombinedPartitionedReducedTotal.txt'

# Convert file back into a dictionary.
dictionary = {}
with open(path) as f:
	for line in f:
		(key, val) = line.translate({ord(i): None for i in ',><'}).split()
		dictionary[key] = int(val)

# Sort dictionary.
sorted_dict = {key: value for key, value in sorted(dictionary.items())}

# Save into file.
f = open('/home/' + user_name + '/Documents/' + 'MappedCombinedPartitionedReducedTotalSorted.txt', "w")
for key in sorted_dict:
	f.write("<" + key + ", " + str(sorted_dict[key]) + ">" + '\n')


