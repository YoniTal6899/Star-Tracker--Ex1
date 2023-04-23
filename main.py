import csv
import os
from itertools import combinations

import cv2
import numpy as np

from Edge import Edge
from Point import Point
from Triangle import Triangle

font = cv2.FONT_HERSHEY_SIMPLEX
font_scale = 1
# Primary colors
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Secondary colors
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Tertiary colors
ORANGE = (255, 165, 0)
LIME = (0, 255, 128)
TEAL = (0, 128, 128)
VIOLET = (238, 130, 238)
BROWN = (165, 42, 42)
PINK = (255, 192, 203)

# Grayscale colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (192, 192, 192)
DARK_GRAY = (64, 64, 64)

# Other colors
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
PURPLE = (128, 0, 128)
OLIVE = (128, 128, 0)
AQUA = (0, 255, 255)
MAROON = (128, 0, 0)
NAVY = (0, 0, 128)
FUCHSIA = (255, 0, 255)
BEIGE = (245, 245, 220)
KHAKI = (240, 230, 140)
TAN = (210, 180, 140)
colors = [RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA, ORANGE, LIME, TEAL, VIOLET, BROWN, PINK, BLACK, WHITE, GRAY,
          LIGHT_GRAY, DARK_GRAY, GOLD, SILVER, PURPLE, OLIVE, AQUA, MAROON, NAVY, FUCHSIA, BEIGE, KHAKI, TAN]

dir_src = 'images'
dir_dest = 'detected_stars'
dir_log = 'logs'
file1name = './images/ST_db1.png'
file2name = './images/ST_db2.png'
identified_jpg = os.path.join(os.getcwd(), dir_dest)
logs = os.path.join(os.getcwd(), dir_log)
try:
    os.mkdir(identified_jpg)
    os.mkdir(logs)
except:
    pass


def makeCsv(l, filename, folder='logs'):
    csvname = filename.split('.')[0]
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


def fix_img(path):
    img = cv2.imread(path)
    img_copy = img.copy()  # Make a copy of the original image
    img_copy2 = img.copy()
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (3, 3), 0)
    avg = np.mean(gray)
    _, thresh = cv2.threshold(blur, avg * 1.5, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh)
    return [num_labels, labels, centroids, stats, gray, img_copy, img_copy2]


def show(img_copy):
    cv2.namedWindow('Detected Stars', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Detected Stars', 800, 600)
    cv2.imshow('Detected Stars', img_copy)
    cv2.waitKey(0)


def getStars(num_labels, labels, centroids, stats, gray, img_copy, filename):
    stars = [['id', 'x', 'y', 'r', 'b']]
    id_counter = 0
    for i in range(1, num_labels):
        mask = (labels == i).astype(np.uint8)
        x, y = centroids[i]
        min_radius = 10  # or any other minimum value you choose
        r = int((stats[i, cv2.CC_STAT_WIDTH] + stats[i, cv2.CC_STAT_HEIGHT]) / 4)
        if r >= min_radius:
            b = cv2.mean(gray, cv2.UMat(mask))[0]
            stars.append((id_counter, x, y, r, b))
            cv2.circle(img_copy, (int(x), int(y)), r + 5, (0, 255, 0), 2)
            cv2.putText(img_copy, str(id_counter), ((int(x) + 30, int(y))), font, font_scale, colors[20], 2)
            id_counter += 1

    makeCsv(stars, filename.split('/')[2].split('.')[0])
    stars.remove(stars[0])
    stars = sorted(stars, key=lambda x: x[4], reverse=True)
    show(img_copy)
    return stars


def avgBrightness(gray):
    return np.mean(gray)


def get_combinations(lst):
    return list(set(combinations(lst, 3)))


def starsToTriangles(stars):
    triangles = {}
    triangle_counter = 0
    combinations = get_combinations(stars)
    for com in combinations:
        p1 = Point(com[0][0], com[0][1], com[0][2])
        p2 = Point(com[1][0], com[1][1], com[1][2])
        p3 = Point(com[2][0], com[2][1], com[2][2])
        e1 = Edge(p1, p2)
        e2 = Edge(p2, p3)
        e3 = Edge(p3, p1)
        t = Triangle(e1, e2, e3)
        triangles.update({triangle_counter: t})
        triangle_counter += 1
    # for i in range(len(stars) - 2):
    #     for j in range(i + 1, len(stars) - 1):
    #         p1 = Point(stars[i][0], stars[i][1], stars[i][2])
    #         p2 = Point(stars[j][0], stars[j][1], stars[j][2])
    #         p3 = Point(stars[j + 1][0], stars[j + 1][1], stars[j + 1][2])
    #         e1 = Edge(p1, p2)
    #         e2 = Edge(p2, p3)
    #         e3 = Edge(p3, p1)
    #         t = Triangle(e1, e2, e3)
    #         triangles.update({triangle_counter: t})
    #         triangle_counter += 1

    print(f"{triangle_counter} triangles:")
    for i in triangles.keys():
        print(f"{i}: {triangles.get(i).get_v()}")
        if triangles.get(i).get_v().__contains__('9') and triangles.get(i).get_v().__contains__('8') and triangles.get(
                i).get_v().__contains__('10'):
            print("*****************************************************************************")
            print("*****************************************************************************")
            print("*****************************************************************************")
            print("*****************************************************************************")
            print("*****************************************************************************")
            print("*****************************************************************************")
    return triangles


if __name__ == '__main__':
    img1Data = fix_img(file1name)
    img2Data = fix_img(file2name)
    stars1 = getStars(img1Data[0], img1Data[1], img1Data[2], img1Data[3], img1Data[4], img1Data[5], file1name)
    stars2 = getStars(img2Data[0], img2Data[1], img2Data[2], img2Data[3], img2Data[4], img2Data[5], file2name)
    tri1 = starsToTriangles(stars1)
    tri2 = starsToTriangles(stars2)
    print(f"Triangle 1: {tri1[1509].get_v()}")
    print(f"Triangle 2: {tri2[1127].get_v()}")
    similarity = {}
    for key1 in range(len(tri1)):
        similarity.update({key1: []})

    for key1, first in tri1.items():
        for key2, second in tri2.items():

            if first.isSimilar(second)[0]:
                similarity.get(key1).append(key2)
    matches = []
    for first, arr in similarity.items():
        t1 = tri1.get(first)
        edges1 = t1.getEdges()
        for index in arr:
            t2 = tri2.get(index)
            edges2 = t2.getEdges()
            p11 = t1.get_common_point(edges1[0], edges1[1])
            p12 = t2.get_common_point(edges2[0], edges2[1])
            p21 = t1.get_common_point(edges1[0], edges1[2])
            p22 = t2.get_common_point(edges2[0], edges2[2])
            p31 = t1.get_common_point(edges1[2], edges1[1])
            p32 = t2.get_common_point(edges2[2], edges2[1])
            matches.append((p11.id, p12.id))
            matches.append((p21.id, p22.id))
            matches.append((p31.id, p32.id))
    avgBr1 = avgBrightness(img1Data[4])
    avgBr2 = avgBrightness(img2Data[4])

    sus_matches = {}
    rev_sus_matches = {}
    for star in stars1:
        sus_matches.update({star[0]: {}})

    for star in stars2:
        rev_sus_matches.update({star[0]: {}})

    for match in matches:
        diff = abs(stars1[match[0]][4] / avgBr1 - stars2[match[1]][4] / avgBr2)
        if match[0] == 3 and match[1] == 8:
            print(f"dif: {diff}")
        sus_matches.get(match[0]).update({match[1]: diff})
        rev_sus_matches.get(match[1]).update({match[0]: diff})
    print(sus_matches)
    print(rev_sus_matches)
    final_matches = []
    for firstIndex, potentialMatches in sus_matches.items():
        if len(potentialMatches) > 0:
            min_key = min(potentialMatches, key=lambda k: potentialMatches[k])
            curr_dif=potentialMatches.get(min_key)
            temp_rev = rev_sus_matches.get(min_key)
            rev_dif = min(rev_sus_matches.get(min_key).values())
            if curr_dif == rev_dif:
                final_matches.append((firstIndex, min_key))
                print(f"First: {firstIndex} , second: {min_key}")

    print(final_matches)
    cv2.destroyAllWindows()

    counter = 0
    for match in final_matches:
        cv2.circle(img1Data[6], (int(stars1[match[0]][1]), int(stars1[match[0]][2])),
                   stars1[match[0]][3] + 5, colors[counter], 2)
        cv2.putText(img1Data[6], str(stars1[match[0]][0]), (int(stars1[match[0]][1]) + 30, int(stars1[match[0]][2])), font,
                    font_scale, colors[counter], 2)
        cv2.circle(img2Data[6], (int(stars2[match[1]][1]), int(stars2[match[1]][2])),
                   stars2[match[1]][3] + 5, colors[counter], 2)
        cv2.putText(img2Data[6], str(stars2[match[1]][0]), (int(stars2[match[1]][1]) + 30, int(stars2[match[1]][2])), font,
                    font_scale, colors[counter], 2)
        counter += 1
    show(img1Data[6])
    show(img2Data[6])
    makeCsv(final_matches, "matches.logs")
