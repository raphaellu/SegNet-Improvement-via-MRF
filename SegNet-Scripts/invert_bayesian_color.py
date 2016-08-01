import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from PIL import Image
from sets import Set

#colors = Set([])
color_matches = {
(222, 40, 60, 255) : (60, 40, 222, 255),
(0, 128, 128, 255) : (128, 128, 0, 255),
(128, 64, 64, 255) : (64, 64, 128, 255),
(128, 128, 192, 255) : (192, 128, 128, 255),
(0, 0, 128, 255) : (128, 0, 0, 255),
(0, 64, 64, 255) : (64, 64, 0, 255),
(128, 64, 128, 255) : (128, 64, 128, 255),
(192, 128, 0, 255) : (0, 128, 192, 255),
(128, 128, 128, 255) : (128, 128, 128, 255),
(128, 0, 64, 255) : (64, 0, 128, 255),
(128, 192, 192, 255) : (192, 192, 128, 255)
}

for i in range (0,233):
    img = Image.open("predictions/" + str(i) + ".png")
    img_px = img.load()
    (width, height) = img.size
    for w in range(0, width):
        for h in range(0, height):
            color = img_px[w,h]
	    img.putpixel((w,h), color_matches[color])

    img.save("predictions_inverted/" + str(i) + ".png")
