import cv2
import glob
import random
dir = glob.glob("*")
print(dir)
vids = []
for d in dir:
	vids += glob.glob("{}/*.avi".format(d))

print(vids)

random.shuffle(vids)
num_samples = len(vids)
num_training = int(num_samples*0.8)
with open('trainlist01.txt', 'w') as filehandle:
	filehandle.writelines("%s\n" % v for v in vids[0:num_training])

with open('testlist01.txt', 'w') as filehandle:
	filehandle.writelines("%s\n" % v for v in vids[num_training+1:num_samples-1])