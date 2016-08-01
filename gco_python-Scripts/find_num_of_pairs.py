import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from copy import deepcopy
color_set = {
str((128,64,128)) : 0, 
str((128,0,0)) : 1, 
str((192,192,128)) : 2, 
str((128,128,128)) : 3, 
str((60,40,222)) : 4, 
str((128,128,0)) : 5, 
str((192,128,128)) : 6, 
str((64,64,128)) : 7, 
str((64,0,128)) : 8,
str((64,64,0)) : 9, 
str((0, 128, 192)) : 10, 
str((11, 11, 11)):11
}

pairs = [[0.0 for y in range(0, len(color_set))] for x in range(0, len(color_set))]

for i in range(0,367):
    print i
    img = Image.open("gt_train/" + str(i) + ".png" )
    img_px = img.load()
    (width, height) = img.size
    for w in range(0, width):
	for h in range(0, height):
	    gt_color = img_px[w,h][:3]
	    if w-1 >= 0:
		    pairs[color_set[str(img_px[w-1, h][:3])]][color_set[str(gt_color)]] += 1.
            if w+1 < width:
		    pairs[color_set[str(img_px[w+1, h][:3])]][color_set[str(gt_color)]] += 1.
            if h-1 >= 0:
		    pairs[color_set[str(img_px[w, h-1][:3])]][color_set[str(gt_color)]] += 1.
            if h+1 < height:
		    pairs[color_set[str(img_px[w, h+1][:3])]][color_set[str(gt_color)]] += 1.
print "===== original ========="
for row in pairs:
    print row

pair_horiz = deepcopy(pairs)

for h in range(0, len(pairs)-1):
    for w in range (0, len(pairs[h])-1):
        if h == w:
            base = pairs[h][w]
            if base == 0. : 
                base = 1.
    for w in range (0, len(pairs[h])-1):
        pair_horiz[h][w] = pairs[h][w]/base

print "====== horiz ========"
for row in pair_horiz:
    print row
    
pair_vert = deepcopy(pairs)

for w in range(0, len(pairs[0])-1):
    for h in range (0, len(pairs)-1):
        if h == w:
            base = pairs[h][w]
            if base == 0. : 
                base = 1.
    for h in range (0, len(pairs[h])-1):
        pair_vert[h][w] = pairs[h][w]/base

print "====== vert ========"
for row in pair_vert:
    print row


for h in range(0, len(pairs)-1):
    for w in range (0, len(pairs[h])-1):
        pairs[h][w] = (pair_vert[h][w] + pair_horiz[h][w])/2.

print "======= final ======="
for row in pairs:
    print row
