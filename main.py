import csv
import os
import cv2
import numpy as np

dir_src = 'images'
dir_dest = 'detected_stars'
dir_log='logs'
filename = 'ST_db2.png'
path1 = os.path.join(os.getcwd(), dir_dest)
path2 = os.path.join(os.getcwd(), dir_log)
try:
    os.mkdir(path1)
    os.mkdir(path2)
except:
    pass
cv2.namedWindow('Detected Stars', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Detected Stars', 800, 600)

def makeCsv(l, folder='logs', csvname=filename.split('.')[0]):
    path = os.path.join(os.getcwd(), folder)
    try:
        os.mkdir(path)
    except:
        pass
    f = open(f'{folder}/{csvname}.csv', 'w', newline='')
    writer = csv.writer(f)
    writer.writerows(l)
    f.close()
    print(f'{csvname} saved.')

img = cv2.imread(f'{dir_src}\{filename}')
img_copy = img.copy()  # Make a copy of the original image
print(f"copy: {type(img_copy[0])}, len is {len(img_copy)} on {len(img_copy[0])}")
gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
print(f"grayscale: {type(gray[0])}, {len(gray)} on {len(gray[0])}")
blur = cv2.GaussianBlur(gray, (3, 3), 0)
avg=np.mean(gray)
print(f"avg: {np.mean(gray)}")

_, thresh = cv2.threshold(blur, avg*1.5, 255, cv2.THRESH_BINARY)

cv2.imshow('Detected Stars', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.namedWindow('Detected Stars', cv2.WINDOW_NORMAL)
cv2.resizeWindow('Detected Stars', 800, 600)

num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)

#print(f"There are {num_labels} stars")
#print(len(labels[666]))
#print("***************")
#print((stats[0]))
stars=[['x','y','r','b']]
print(f"loop is: {num_labels}")
for i in range(1, num_labels):
    mask = (labels == i).astype(np.uint8)
    x, y = centroids[i]
    min_radius = 2  # or any other minimum value you choose
    r = int((stats[i, cv2.CC_STAT_WIDTH] + stats[i, cv2.CC_STAT_HEIGHT]) / 4)
    if r >= min_radius:
        b = cv2.mean(gray, cv2.UMat(mask))[0]
        stars.append((x, y, r, b))
        cv2.circle(img_copy, (int(x), int(y)), r + 5, (0, 255, 0), 2)
makeCsv(stars)
cv2.imwrite(f'{dir_dest}\detected_{filename}', img_copy)
cv2.imshow('Detected Stars', img_copy)
cv2.waitKey(0)
cv2.destroyAllWindows()