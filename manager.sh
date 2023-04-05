#!/bin/bash -x

# Splitting input file into multiple files.
file_name=$(ls inputFile)
servers_count=3 #Number of servers
python3 ./sourceCode/splitter.py inputFile/${file_name} ${servers_count}

# Transfer file chunks to servers.
#PASS ARGS TO BASH
vm_usr_name="sfathi4"
vm_passwrd="****"

for i in {1..3}
do
	echo $ #transferFile should take three args: file source path, usr pass

done
