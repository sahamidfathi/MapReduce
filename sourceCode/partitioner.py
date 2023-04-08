import sys
import hashlib

part_num = sys.argv[2]
file_name = sys.argv[3]
user_name = sys.argv[4]
reducers_count = sys.argv[5]

path = '/home/' + user_name + '/Documents/' + 'MappedCombined_' + file_name + '_part' + part_num + '.txt'

# Convert file back into a dictionary.
dictionary = {}
with open(path) as f:
	for line in f:
		(key, val) = line.translate({ord(i): None for i in ',><'}).split()
		dictionary[key] = int(val)

# Hashing keys in the dictionary using SHA-1 and modulo calculating.
# A list of server (reducer) number, word, number of occurrence
for the_key, the_value in dictionary.items():

	hashed_key = int(hashlib.sha1(the_key.encode()).hexdigest(), 16)
	mod_hashed_key = hashed_key % int(reducers_count)

	f = open('/home/' + user_name + '/Documents/' + str(mod_hashed_key) + 
             '_MappedCombinedPartitioned_' + file_name + '_part' + part_num + '.txt', "a")
	f.write("<" + the_key + ', ' + str(the_value) + ">" + '\n')
	f.close()

