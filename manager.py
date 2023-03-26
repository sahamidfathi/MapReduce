import hashlib
filename = 'MappedCombined_mayoclinic.txt'
path = '/home/hamid/Desktop/ScalableAndReliableDistributedSystems/assignment3/mapper/' + filename
# Number of reducer servers:
reducers_count = 3

# Convert file back into a dictionary..translate({ord(i): None for i in ',><'})
dictionary = {}
with open(path) as f:
	for line in f:
		(key, val) = line.translate({ord(i): None for i in ',><'}).split()
		dictionary[key] = int(val)

print(dictionary)
	
# Hashing keys in the dictionary using SHA-1 and modulo calculating.
# A list of server (reducer) number, word, number of occurrence
mod_hashed_list = []
for the_key, the_value in dictionary.items():

	hashed_key = int(hashlib.sha1(the_key.encode()).hexdigest(), 16)
	mod_hashed_key = hashed_key % reducers_count
	
	mod_hashed_list.append((mod_hashed_key, the_key, the_value))

print(mod_hashed_list)

	

