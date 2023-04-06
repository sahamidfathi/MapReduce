#!/bin/bash 
# -x

# Split input file into multiple files.
file_name=$(ls inputFile)
servers_count=3 #Number of servers
python3 ./sourceCode/splitter.py inputFile/${file_name} ${servers_count}

# Transfer file chunks to servers.
#PASS ARGS TO BASH
vm_usr_name="sfathi4"
vm_passwrd="*"
for i in {1..3}
do
	str_var="_part"
	file_name_part=${file_name%.*}
	file_name_part+=${str_var}
	file_name_part+=${i}
	file_name_part+='.txt'

	vm_name='cs4459-vm'
	vm_name+=${i}
	vm_name+='.gaul.csd.uwo.ca'

	python3 ./sourceCode/transfer_file.py ${file_name%.*} ${i} ${vm_name} ${vm_usr_name} ${vm_passwrd}
done

# Run mapper on servers where files reside.
for i in {1..3}
do
	vm_name='cs4459-vm'
	vm_name+=${i}
	vm_name+='.gaul.csd.uwo.ca'

	#usr@host:portnumber
	sshpass -p ${vm_passwrd} ssh -o StrictHostKeyChecking=no ${vm_usr_name}@${vm_name} python -u - --opt ${i} ${file_name%.*} ${vm_usr_name} < ./sourceCode/mapper.py 
done




# Delete file chunks.
#echo $(ls ./inputFile/)
find ./inputFile/ -type f -not -name ${file_name} -delete

