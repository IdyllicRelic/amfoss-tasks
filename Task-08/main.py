import os

import cv2
import numpy as np
from natsort import natsorted
from PIL import Image, ImageDraw

coords = []
for file in natsorted(os.listdir("assets")):
    image = cv2.imread("assets/" + file)

    mask = np.any(image != [255, 255, 255], axis=2)
    ys, xs = np.where(mask)
    if len(xs) == 0:
        coords.append(None)
        continue

    x = int(xs.mean())
    y = int(ys.mean())
    b, g, r = image[y, x]
    coords.append(((x, y), (r, g, b)))

result = Image.new("RGB", (512, 512), "WHITE")
draw = ImageDraw.Draw(result)

for i in range(len(coords) - 1):
    current = coords[i]
    next = coords[i + 1]

    if current is None or next is None:
        continue

    draw.line(
        (current[0][0], current[0][1], next[0][0], next[0][1]), fill=current[1], width=2
    )

result.save("result.jpg")
