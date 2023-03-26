import hashlib
filename = 'MappedCombined_mayoclinic_part2.txt'
path = '/home/hamid/Desktop/ScalableAndReliableDistributedSystems/assignment3/managerSplitterMapperReducer/' + filename
# Number of reducer servers:
reducers_count = 3

# Convert file back into a dictionary.
dictionary = {}
with open(path) as f:
	for line in f:
		(key, val) = line.translate({ord(i): None for i in ',><'}).split()
		dictionary[key] = int(val)

	
# Hashing keys in the dictionary using SHA-1 and modulo calculating.
# A list of server (reducer) number, word, number of occurrence
mod_hashed_list = []
for the_key, the_value in dictionary.items():

	hashed_key = int(hashlib.sha1(the_key.encode()).hexdigest(), 16)
	mod_hashed_key = hashed_key % reducers_count
	
	mod_hashed_list.append((mod_hashed_key, the_key, the_value))

print(mod_hashed_list)

# Save to file.
with open("MappedCombinedPartitioned_" + filename, "w") as f:
    for line in mod_hashed_list:
        f.write(f"{line}\n")

