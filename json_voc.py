import os
import xml.etree.cElementTree as ET
from PIL import Image
import json

ANNOTATIONS_DIR_PREFIX = "new_output"

DESTINATION_DIR = "new_rgb_images"

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


def create_file(file_prefix, width, height, voc_labels,dst,frame):
    root = create_root(file_prefix, width, height)
    root = create_object_annotation(root, voc_labels)
    tree = ET.ElementTree(root)
    # '{:05d}.txt'.format(im_ind)
    tree.write("{}/{}/{}_{:05d}.xml".format(DESTINATION_DIR,file_prefix,file_prefix,frame+1))


def read_file(file_path,dst):
    file_prefix = file_path.split(".json")[0]
    print(file_prefix)
    # print(file_prefix)
    #image_file_name = "{}.jpg".format(file_prefix)
    #img = Image.open("{}/{}".format("data", image_file_name))
    #w, h = img.size
    w = 1440
    h = 720
    with open(os.path.join(ANNOTATIONS_DIR_PREFIX,file_path),'r') as file:
        lines = json.load(file)
        frame_num = len(list(lines.keys()))
        for frame in lines.keys():
            voc_labels = []
            this_frame = lines[frame]
            worker_num = len(list(this_frame.keys()))
            for id in this_frame.keys():
                voc = []
                worker_loc = this_frame[id]['worker_location']
                voc.append("NA")
                voc.append(int(id))
                previous_accurate_frame_number = frame
                while len(worker_loc) == 0:
                    previous_accurate_frame_number = int(previous_accurate_frame_number)-1
                    worker_loc = lines[str(previous_accurate_frame_number)][id]['worker_location']
                voc.append(round(float(worker_loc[0])))
                voc.append(round(float(worker_loc[1])))
                voc.append(round(float(worker_loc[2])))
                voc.append(round(float(worker_loc[3])))
                voc_labels.append(voc)
            create_file(file_prefix, w, h, voc_labels,dst,int(frame))
        print("Processing complete for file: {}".format(file_path))


def start():
    if not os.path.exists(DESTINATION_DIR):
        os.makedirs(DESTINATION_DIR)
    for d in os.listdir(ANNOTATIONS_DIR_PREFIX):
        if d.endswith('.json'):
            if not os.path.exists(os.path.join(DESTINATION_DIR,os.path.splitext(d)[0])):
                os.makedirs(os.path.join(DESTINATION_DIR,os.path.splitext(d)[0]))
            # for file_name in os.listdir(os.path.join(ANNOTATIONS_DIR_PREFIX,d)):
            #     if file_name.endswith('json'):
            read_file(os.path.join(d),os.path.join(DESTINATION_DIR,d))


if __name__ == "__main__":
    start()
