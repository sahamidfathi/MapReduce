

# splitting
import sys

# number of files should be equal to the number of servers
number_of_files = 3
file_name = sys.argv[1]
with open(file_name) as infp:
    files = [open(file_name.replace(".txt","_part") + '%d.txt' % i, 'w') for i in range(number_of_files)]
    for i, line in enumerate(infp):
        files[i % number_of_files].write(line)
    for f in files:
        f.close()
        
        
# send files to vms

# send script to vm for mapper

# combiner should not be in mapper, should be in shuffle 
import hashlib
filename = 'MappedCombined_mayoclinic_part2.txt'
path = '/home/hamid/Desktop/ScalableAndReliableDistributedSystems/assignment3/toShareOnGitHub/' + filename
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

