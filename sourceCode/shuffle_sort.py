import sys
from collections import defaultdict

import tqdm
import os

#reads and merges pairs for the same key
#read files from directory that has your num
def shuffle(file_path):
    #dictionary -> (key,value) -> (A,1)
    key_value_pairs = defaultdict(list)
    content,values = list(),list()
    #navigate to current dir
    os.chdir(os.getcwd()+file_path)
    files = os.listdir(os.getcwd())
    for file in files:
        f = open(file, "r")
        content.extend(f.readlines())
    for line in content:
        line = line.strip()
        key_value = line.split(",")
        value = []
        key = key_value[0]
        value.append(key_value[1])
        if key not in key_value_pairs:
            key_value_pairs[key] = value
        else:
            #add to value if already exists
            key_value_pairs[key].append(value)
    return key_value_pairs


def write_to_file(pairs):
    #specify the path to which the file should be sent
    os.chdir('..')
    with open('shuffled.txt', 'a') as f:
        for key,value in pairs.items():
            f.write(key+','+str(value)+'\n')
    f.close()


if __name__ == '__main__':
    #shuffler number
    num = sys.argv[1]
    print('shuffler'+ num+' running')
    #goes inside this folder and reads and deletes the file it uses
    #file format -> num_word_randomCharacters_partitioned.txt -> num for shuffler, if word changed the key changed
    file_path = "\\shuffle"+num+'\\'
    pairs = shuffle(file_path)
    write_to_file(pairs)



