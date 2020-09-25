import glob
from os import listdir
import os
import numpy as np
from numpy.core.records import fromarrays
from scipy.io import savemat, loadmat
import pandas as pd

path = r'C:\Users\ghazaleh\Desktop\M.Sc. thesis\codes\YOWO\datasets\jhmdb21\rgb-images'
labels = r'C:\Users\ghazaleh\Desktop\M.Sc. thesis\codes\YOWO\datasets\jhmdb21\labels'


def bb_intersection_over_union(boxA, boxB):
    # determine the (x, y)-coordinates of the intersection rectangle
    xA = max(int(boxA[0]), int(boxB[0]))
    yA = max(int(boxA[1]), int(boxB[1]))
    xB = min(int(boxA[2]), int(boxB[2]))
    yB = min(int(boxA[3]), int(boxB[3]))
    # print(boxA,boxB)
    # print(xA,yA,xB,yB)
    # compute the area of intersection rectangle
    interArea = max(0, int(xB) - int(xA) + 1) * max(0, int(yB) - int(yA) + 1)
    # print(interArea)
    # compute the area of both the prediction and ground-truth
    # rectangles
    boxAArea = (int(boxA[2]) - int(boxA[0]) + 1) * (int(boxA[3]) - int(boxA[1]) + 1)
    boxBArea = (int(boxB[2]) - int(boxB[0]) + 1) * (int(boxB[3]) - int(boxB[1]) + 1)
    # print(boxAArea,boxBArea)
    # compute the intersection over union by taking the intersection
    # area and dividing it by the sum of prediction + ground-truth
    # areas - the interesection area
    iou = interArea / float(boxAArea + boxBArea - interArea)
    # return the intersection over union value
    return iou


name = listdir(path)
num_imgs = []
tubes = []
for n in name:
    im = []
    images = listdir(os.path.join(path, n))
    # print(images)
    for i in images:
        if '.jpg' in i:
            im.append(i)
    num_imgs.append(len(im))

for i, n in enumerate(name):
    # print(n)
    ef = []
    sf = []
    cl = []
    boxes = []
    sub_box = []
    num = num_imgs[i]
    actors = {}

    for j in range(num):
        if n == 'placing_fixing_standing_walking_26':
            continue
        boxes_path = os.path.join(labels, n + '_' + n + '_' + '{:05d}.txt'.format(j + 1))
        boxes_txt = open(boxes_path, 'r')

        for b in boxes_txt:
            text = b.strip().split(' ')
            # print(j,text)
            cls = text[0]
            tmp = 0
            # if n == 'placing_fixing_walking_28' and j < 20:
            #     print(actors)
            if j == 0:
                # if n == 'placing_fixing_walking_28':
                #     print('here')
                actors['{}'.format(len(actors.keys()) + 1)] = [text + [j + 1]]
            else:
                for k in actors.keys():
                    # if len(actors[k]) > 0:
                    if actors[k][-1][-1]-1 < j:
                        # print(actors[k][-1][-1])
                        prev_actor = actors[k][-1]
                        if prev_actor[0] == cls:
                            IoU = bb_intersection_over_union(text[1:5], prev_actor[1:5])
                            if IoU > 0.3:

                                text.append(j+1)
                                actors[k].append(text)
                                # if n == 'placing_fixing_walking_28':
                                #     print(IoU)
                                #     print('updated',text,j)
                                tmp = 0
                                break
                            else:
                                tmp = 1
                                # if n == 'placing_fixing_walking_28':
                                #     print('huh', j)
                                #     print(IoU)

                        else:
                            # if n == 'placing_fixing_walking_28':
                            # # actors['{}'.format(len(actors.keys()) + 1)] = [text + [j + 1]]
                            #     print('aa',j)
                            tmp = 1

                if tmp == 1:
                    # if n == 'placing_fixing_walking_28':
                    #     print('new here',j,text)
                    actors['{}'.format(len(actors.keys()) + 1)] = [text + [j + 1]]


    image_box = []
    if len(actors.keys()) > 4:
        print(n)
    # print(actors)
    for k in actors.keys():
        xmin = []
        ymin = []
        xmax = []
        ymax = []
        m = []
        # print(actors[k])
        actor_box = []
        ef.append(actors[k][-1][5])
        sf.append(actors[k][0][5])
        if actors[k][-1][5] - actors[k][0][5] + 1 != len(actors[k]):
            "fuckkkk"
        cl.append(actors[k][0][0])
        for i in range(len(actors[k])):
            # m.append(actors[k][i][1:5])
            xmin.append(actors[k][i][1])
            ymin.append(actors[k][i][2])
            xmax.append(actors[k][i][3])
            ymax.append(actors[k][i][4])

        # a = np.array(m)
        # b = np.asmatrix(a)
        shape = (len(actors[k]),4)
        a = np.zeros(shape)
        a[:,0] = xmin
        a[:,1] = ymin
        a[:,2] = xmax
        a[:,3] = ymax
        # print(fromarrays([xmin,ymin,xmax,ymax],names=['1', '2', '3', '4']).shape)
        # df = pd.DataFrame([xmin,ymin,xmax,ymax]).T
        savemat('b.mat', {'my': a})
        mat_contents = loadmat('b.mat')
        image_box.append(mat_contents)
        # savemat('b.mat', {'my{}.format ':})
        # print(df)

        # image_box.append(a)

        # print(fromarrays([xmin,ymin,xmax,ymax]))

    # print(len(image_box))
    # print(image_box)
    # print(np.array(sf).shape)
    # print(len(ef))
    # print(len(cl))
    # print(ef)

    # print({'ef' : ef , 'sf' : sf, 'class' : cl, 'boxes' : image_box})
    # d = fromarrays([ef,sf,cl,image_box], names=['ef', 'sf', 'class', 'boxes'])
    # print(fromarrays([ef,sf,cl], names=['ef', 'sf', 'class']))

    # print(fromarrays([ef,image_box]))
    # print(fromarrays([ef,sf,cl]).shape)
    # np.concatenate(np.array(ef),np.array(ef), axis=0)

    tubes.append(fromarrays([ef,sf,cl,image_box], names=['ef', 'sf', 'class','boxes']))
    # print(len(tubes))
    # tubes.append({'ef' : ef , 'sf' : sf, 'class' : cl, 'boxes' : image_box})
    # print(fromarrays([ef,sf,cl], names=['ef', 'sf', 'class']))
# print(len(tubes))
# print(len(num_imgs))
# print(len(name))
# print(np.array(tubes).shape)

myrec = fromarrays([num_imgs, name, tubes], names=['num_img', 'name', 'tubes'])
# print(tubes)
savemat('final_annotation_workers.mat', {'final_annotation_workers': myrec})
