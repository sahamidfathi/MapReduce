import sys
import glob

# Reducer takes as command argument the number of server to run on.
# VM number n reduces all chunk files names beginning with (n-1)
reducer_server_number = sys.argv[2]
user_name = sys.argv[3]

path = '/home/' + user_name + '/Documents/' + str(int(reducer_server_number) - 1) + '_shuffled/' + '*'

# Each reducer reads all the files, from key values belonging to that reducer, 
# the reducer adds up the values of arrays with the same keys.

input_list = []
# Reading all tuples <key, value> from all files assigned to this server.
# and putting them all in input_list.
list_of_files = glob.glob(path)
for file_name in list_of_files:
	f_handle = open(file_name, 'r')
	
	for line in f_handle:
		stripped_line = line.translate({ord(i): None for i in ',><'}).split()
		input_list.append(stripped_line)

	f_handle.close()
	
#print(input_list)
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

#print(output_dict)

# Save into file.
f = open('/home/' + user_name + '/Documents/' + 'MappedCombinedPartitionedReducedTotal.txt', "a")
for key in output_dict:
	f.write("<" + key + ", " + str(output_dict[key]) + ">" + '\n')


