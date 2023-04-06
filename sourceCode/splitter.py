import sys

# number of files should be equal to the number of servers
file_name = sys.argv[1]
number_of_files = int(sys.argv[2])

with open(file_name) as infp:
    files = [open(file_name.replace(".txt","_part") + '%d.txt' % (i+1), 'w') for i in range(number_of_files)]
    for i, line in enumerate(infp):
        files[i % number_of_files].write(line)
    for f in files:
        f.close()
