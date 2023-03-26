from collections import Counter

filename = 'mayoclinic.txt'
path = '/home/hamid/Desktop/ScalableAndReliableDistributedSystems/assignment3/mapper/mapperInput/' + filename

# Mapping.
with open(path, 'r') as f:
	# Removing punctuation marks.
	data = f.read().translate({ord(i): None for i in ',.?!"—-@#$%^&*()_=+'}).split()


# Combining (Preliminary reducing).
count=Counter(data)


# Sorting.
#count_sorted = dict(sorted(count.items(), key=lambda x: (x[1], x[0]), reverse=True))
count_sorted = {key: value for key, value in sorted(count.items())}
print(count_sorted)

# Save into file.
f = open("MappedCombined_" + filename, "w")
for key in count_sorted:
	f.write("<" + key + ", " + str(count_sorted[key]) + ">" + '\n')
