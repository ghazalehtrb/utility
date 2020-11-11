import xml.etree.ElementTree as ET
from os import getcwd
import glob
from os import listdir
import os

ANNOTATIONS_DIR_PREFIX = "new-rgb-images"

def create_root(file_prefix, width, height):
    root = ET.Element("annotation")
    ET.SubElement(root, "folder").text = "converted_labels"
    ET.SubElement(root, "filename").text = "{}.jpg".format(file_prefix)
    ET.SubElement(root, "path").text = "D:\PycharmProjects\convert\converted_labels\{}.jpg".format(file_prefix)
    source = ET.SubElement(root, "source")
    ET.SubElement(source, "database").text = "Unknown"
    size = ET.SubElement(root, "size")
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"
    ET.SubElement(root, "segmented").text = "0"
    return root

def create_object_annotation(root, voc_labels):
    for voc_label in voc_labels:
        obj = ET.SubElement(root, "object")
        ET.SubElement(obj, "name").text=str(voc_label[0])
        ET.SubElement(obj, "id").text=str(voc_label[1])
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[2])
        ET.SubElement(bbox, "ymin").text = str(voc_label[3])
        ET.SubElement(bbox, "xmax").text = str(voc_label[4])
        ET.SubElement(bbox, "ymax").text = str(voc_label[5])
    return root

def create_file(file_prefix, width, height, voc_labels,frame):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    print("{}/{}_{:05d}.xml".format(ANNOTATIONS_DIR_PREFIX,file_prefix,frame))
    tree.write("{}/{}/{}_{:05d}.xml".format(ANNOTATIONS_DIR_PREFIX,file_prefix,file_prefix,frame))


def convert_annotation(d, i,id_class,num_workers):
    w = 1440
    h = 720
    voc_labels = []
    in_file = open(r'C:\Users\ghazaleh\Desktop\new-rgb-images\%s\%s'%(d, i))
    tree=ET.parse(in_file)
    root = tree.getroot()
    len_workers = len(list(enumerate(root.iter('object'))))
    # if len_workers != num_workers:
    #     print('worker is gone %s' % (d))
    #     return

    for obj in root.iter('object'):
        id = obj.find('id').text
        if id not in id_class.keys():
            continue
        else:
            xmlbox = obj.find('bndbox')
            b = [int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text)]
            voc = []
            voc.append(id_class[id])
            voc.append(int(id))
            voc.append(b[0])
            voc.append(b[1])
            voc.append(b[2])
            voc.append(b[3])
            voc_labels.append(voc)

    create_file(d, w, h, voc_labels,int(frame))

wd = getcwd()
path = r'C:\Users\ghazaleh\Desktop\new-rgb-images'
#DESTINATION_DIR = r'C:\Users\ghazaleh\Desktop\tracked-labels'
dir = listdir(path)
for d in dir:
    # print(d)
    annots = listdir(os.path.join(path, d))
    for frame, i in enumerate(annots):
        if '.xml' in i:
            if frame == 0:
                # print(i)
                list_file = open('%s/%s/%s' % (path,d,i), 'r')
                tree=ET.parse(list_file)
                root = tree.getroot()
                id_class = {}
                num_workers = len(list(enumerate(root.iter('object'))))

                for obj in root.iter('object'):
                    cls = obj.find('name').text
                    id = obj.find('id').text
                    id_class[str(id)] = cls
            else:
                # if not os.path.exists(os.path.join(DESTINATION_DIR,d)):
                #     os.makedirs(os.path.join(DESTINATION_DIR,d))
                #list_file = open('%s\%s\%s' % (DESTINATION_DIR,d,i), 'r')
                convert_annotation(d, i,id_class,num_workers)
            # except:
            #     print("oh")
            list_file.close()

