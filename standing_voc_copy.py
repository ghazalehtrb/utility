import shutil
from os import listdir
import os
path = r'C:\Users\ghazaleh\Desktop\new_rgb_images'
path1 = r'C:\Users\ghazaleh\Desktop\new-rgb-images'
dir = listdir(path)

for d in dir:
    #if d.split('_')[0] == 'standing' and d.split('_')[1].isdigit():
    print(d)
    annots = listdir(os.path.join(path, d))
    for frame, i in enumerate(annots):
        if '.xml' in i:
            if os.path.splitext(i)[0].split('_')[-1] == '00001':
                src_file = '%s/%s/%s' % (path,d,i)

            else:
                dest_dir = '%s/%s/%s' % (path,d,i)
                shutil.copy(src_file,dest_dir)
