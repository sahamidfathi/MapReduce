import sys
import glob

# Each reducer reads all the files, from key values belonging to that reducer, 
# the reducer adds up the values of arrays with the same keys.

# Reducer takes as command argument the number of server to run on.
reducer_server_number = sys.argv[1]


input_list = []
# Reading all triples (reducer_server, key, value) from files with the same name
# beginnings from current directory, selecting key values allocated to this reducer,
# and putting them all in a list: input_list.
list_of_files = glob.glob('./MappedCombinedPartitioned*.txt')
for file_name in list_of_files:
	f_handle = open(file_name, 'r')
	
	for line in f_handle:
		stripped_line = line.strip().replace(" ","").replace(")","").replace("(","").split(',')
		if (stripped_line[0] == reducer_server_number):
			input_list.append((stripped_line[1][1:-1], stripped_line[2]))
			
	f_handle.close()

# Reducing (adding up values) of input_list and putting into output_dict.
output_dict = {}
i = 0
while i < len(input_list):
	j = i + 1
	sum_value = int(input_list[i][1])

	while j < len(input_list):

		if input_list[i][0] == input_list[j][0]:
			sum_value += int(input_list[j][1])
			del input_list[j]
		j += 1
		
	output_dict[input_list[i][0]] = sum_value
	i += 1

print(output_dict)

# Save into file.
f = open("MappedCombinedPartitionedReduced.txt", "w")
for key in output_dict:
	f.write("<" + key + ", " + str(output_dict[key]) + ">" + '\n')


