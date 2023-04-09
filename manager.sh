#!/bin/bash 
# -x

# Split input file into multiple files.
file_name=$(ls inputFile)
servers_count=3 #Number of servers
python3 ./sourceCode/splitter.py inputFile/${file_name} ${servers_count}

# Transfer file chunks to servers.
#PASS ARGS TO BASH
vm_usr_name=$1
vm_passwrd=$2

#PARALLEL FOR
for ((i=1;i<=$servers_count;i++))
do
	str_var="_part"
	file_name_part=${file_name%.*}
	file_name_part+=${str_var}
	file_name_part+=${i}
	file_name_part+='.txt'

	vm_name='cs4459-vm'
	vm_name+=${i}
	vm_name+='.gaul.csd.uwo.ca'

	
	origin_path="./inputFile/*part${i}*"
	dst_path="/home/${vm_usr_name}/Documents/${file_name%.*}_part${i}.txt"

	python3 ./sourceCode/transfer_file.py dummyarg ${origin_path} ${dst_path} \
		${vm_name} ${vm_usr_name} ${vm_passwrd}
done

# Create directory in each server to hold shuffled files, dir name will be <VMnumber-1>_shuflle
for ((i=1;i<=$servers_count;i++))
do
	vm_name="cs4459-vm${i}.gaul.csd.uwo.ca"
	sshpass -p ${vm_passwrd} ssh -o StrictHostKeyChecking=no \
		${vm_usr_name}@${vm_name} "mkdir /home/${vm_usr_name}/Documents/$((${i}-1))_shuffled"
	
done

# Run mapper on servers where files reside.
# Call partitioner to assign keys to servers (hash and mod calculation).
for ((i=1;i<=$servers_count;i++))
do
	vm_name="cs4459-vm${i}.gaul.csd.uwo.ca"
	#usr@host:portnumber
	# Run mapper:
	sshpass -p ${vm_passwrd} ssh -o StrictHostKeyChecking=no \
	       	${vm_usr_name}@${vm_name} python -u - --opt ${i} ${file_name%.*} \
		${vm_usr_name} < ./sourceCode/mapper.py 
	# COMBINE IN REDUCER

	# Run partitioner:	
	sshpass -p ${vm_passwrd} ssh -o StrictHostKeyChecking=no \
                ${vm_usr_name}@${vm_name} python -u - --opt ${i} \
		"${file_name%.*}" ${vm_usr_name} ${servers_count}< \
		./sourceCode/partitioner.py
	
	# Transfer assigned files to correponding servers.
	for ((j=1;j<=$servers_count;j++))
	do
		dst_vm_name="cs4459-vm${j}.gaul.csd.uwo.ca"
		origin_path="/home/${vm_usr_name}/Documents/$((${j}-1))_M*_part${i}*"
		dst_path="/home/${vm_usr_name}/Documents/$((${j}-1))_shuffled/$((${j}-1))_from_vm_${i}.txt"

		sshpass -p ${vm_passwrd} ssh -o StrictHostKeyChecking=no \
			${vm_usr_name}@${vm_name} python -u - --opt ${origin_path}\
			${dst_path} ${dst_vm_name} ${vm_usr_name} ${vm_passwrd}\
			< ./sourceCode/transfer_file.py
	done
done

# Run reducer on shuffled files.
for ((i=1;i<=$servers_count;i++))
do
	vm_name="cs4459-vm${i}.gaul.csd.uwo.ca"
	sshpass -p ${vm_passwrd} ssh -o StrictHostKeyChecking=no \
		${vm_usr_name}@${vm_name} python -u - --opt ${i} \
		${vm_usr_name} < ./sourceCode/reducer.py 
done

# Sort alphabetically.
for ((i=1;i<=$servers_count;i++))
do
	vm_name="cs4459-vm${i}.gaul.csd.uwo.ca"
	sshpass -p ${vm_passwrd} ssh -o StrictHostKeyChecking=no \
		${vm_usr_name}@${vm_name} python -u - --opt \
		${vm_usr_name} < ./sourceCode/sorter.py 
done

# Delete file chunks.
#echo $(ls ./inputFile/)
find ./inputFile/ -type f -not -name ${file_name} -delete

