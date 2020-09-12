import xml.etree.ElementTree as ET
from os import getcwd
import glob
from os import listdir
import os

# sets=[('2007', 'train'), ('2007', 'val'), ('2007', 'test')]
sets=[('2019-12-10_22_00_00_007', '00000')]


classes = ['placing_fixing']


def convert_annotation(d, s, i, list_file, sub_dir):
    in_file = open(r'C:/Users/ghazaleh/Desktop/im/%s/%s/%s'%(d, s, i))
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        # if cls not in classes or int(difficult) == 1:
        #     continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(str(cls_id) + ',' + ",".join([str(a) for a in b]))
        list_file.write('\n')

wd = getcwd()
path = r'C:\Users\ghazaleh\Desktop\im'
dir = listdir(path)
for d in dir:
    print(d)
    sub_dir = listdir(os.path.join(path, d))
    print(sub_dir)
    for s in sub_dir:
        print(s)
        images = listdir(os.path.join(path, d, s))
        # print(images)
        # images = [os.path.splitext(id)[0] for id in images]
        # images = images[1:]
        for i in images:
            if '.xml' in i:
                list_file = open('%s_%s.txt' % (d,os.path.splitext(i)[0]), 'w')
                # try:
                convert_annotation(d, s, i, list_file,sub_dir)
                # except:
                #     print("oh")
                list_file.close()

