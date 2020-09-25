import xml.etree.ElementTree as ET
from os import getcwd
import glob
from os import listdir
import os
import random
#
# path = r'C:\Users\ghazaleh\Desktop\M.Sc. thesis\codes\YOWO\datasets\workers\labels'
# files = listdir(path)
# random.shuffle(files)
# list_train = open('train_list.txt', 'a')
# for f in files[:int(0.8*len(files))]:
#     # print(f)
#     list_train.write(f)
#     list_train.write('\n')
# list_train.close()
#
# list_test = open('test_list.txt', 'a')
# for f in files[int(0.8*len(files))+1:]:
#     # print(f)
#     list_test.write(f)
#     list_test.write('\n')
# list_test.close()
#
#     # print(sub_dir)

path = r'C:\Users\ghazaleh\Desktop\M.Sc. thesis\codes\YOWO\datasets\jhmdb21___________\rgb-images'
dir = listdir(path)
text_files = []
# print(dir)
for d in dir:
    # print(d)
    images = listdir(os.path.join(path, d))
    # print(images)
    for i in images:
        # print(i)
        if '.txt' in i:
            # print(os.path.join(d, i))
            print(os.path.join(path,d, os.path.splitext(i)[0] + '.jpg'))
            if os.path.isfile(os.path.join(path, d,os.path.splitext(i)[0] + '.jpg')):
                print('here?')
                text_files.append(os.path.join(d, i))

random.shuffle(text_files)

list_train = open('train_list.txt', 'a')
for f in text_files[:int(0.8*len(text_files))]:
    # print(f)
    list_train.write(f)
    list_train.write('\n')
list_train.close()

list_test = open('test_list.txt', 'a')
for f in text_files[int(0.8*len(text_files))+1:]:
    # print(f)
    list_test.write(f)
    list_test.write('\n')
list_test.close()

