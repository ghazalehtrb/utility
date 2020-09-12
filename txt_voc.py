import os
import xml.etree.cElementTree as ET
from PIL import Image

ANNOTATIONS_DIR_PREFIX = "data"

DESTINATION_DIR = "converted_labels"

CLASS_MAPPING = {
    '1': 'worker'
    # Add your remaining classes here.
}


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
        ET.SubElement(obj, "pose").text = "Unspecified"
        ET.SubElement(obj, "truncated").text = str(0)
        ET.SubElement(obj, "difficult").text = str(0)
        bbox = ET.SubElement(obj, "bndbox")
        ET.SubElement(bbox, "xmin").text = str(voc_label[1])
        ET.SubElement(bbox, "ymin").text = str(voc_label[2])
        ET.SubElement(bbox, "xmax").text = str(voc_label[3])
        ET.SubElement(bbox, "ymax").text = str(voc_label[4])
    return root


def create_file(file_prefix, width, height, voc_labels,dst):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    tree.write("{}/{}.xml".format(ANNOTATIONS_DIR_PREFIX, file_prefix))


def read_file(file_path,dst):
    file_prefix = file_path.split(".txt")[0]
    # print(file_prefix)
    #image_file_name = "{}.jpg".format(file_prefix)
    #img = Image.open("{}/{}".format("data", image_file_name))
    #w, h = img.size
    w = 1440
    h = 720
    with open(os.path.join(ANNOTATIONS_DIR_PREFIX,file_path), 'r') as file:
        lines = file.readlines()
        voc_labels = []
        for line in lines:
            voc = []
            line = line.strip()
            data = line.split()
            CLASS_MAPPING.get(data[0])
            a = int(data[0])
            # if a == 1:
            if 'walking' not in file_path and 'standing' not in file_path:
                voc.append("placing_fixing")
            else:
                voc.append("NA")
            # bbox_width = float(data[3]) * w
            # bbox_height = float(data[4]) * h
            # center_x = float(data[1]) * w
            # center_y = float(data[2]) * h
            # voc.append(round(center_x - (bbox_width / 2)))
            # voc.append(round(center_y - (bbox_height / 2)))
            # voc.append(round(center_x + (bbox_width / 2)))
            # voc.append(round(center_y + (bbox_height / 2)))
            voc.append(round(float(data[2])* w))
            voc.append(round(float(data[1])* h))
            voc.append(round(float(data[4])* w))
            voc.append(round(float(data[3])* h))
            voc_labels.append(voc)
        create_file(file_prefix, w, h, voc_labels,dst)
    print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for d in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if not os.path.exists(os.path.join(DESTINATION_DIR,d)):
            os.makedirs(os.path.join(DESTINATION_DIR,d))
        for file_name in os.listdir(os.path.join(ANNOTATIONS_DIR_PREFIX,d)):
            if file_name.endswith('txt'):
                read_file(os.path.join(d,file_name),os.path.join(DESTINATION_DIR,d))
            else:
                print("Skipping file: {}".format(file_name))


if __name__ == "__main__":
    start()