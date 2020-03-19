import cv2 as cv
import numpy as np

im = cv.imread('abdomen.png')
im = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
w = im.shape[1]
h = im.shape[0]

mask = np.zeros([h, w], np.uint8)

threshold = 8


def mouse_callback(event, x, y, flags, params):
    if event == 1:
        print([x, y])
        print(im[y, x])
        cv.imshow('image_cut', spread((y, x)))


def spread(start_pixel):
    base_image = im.astype('int32')
    bitmap = np.zeros([h, w])
    bitmap[start_pixel] = 1
    queue = [start_pixel]

    while len(queue) != 0:
        current_pixel = queue.pop(0)
        for i, j in zip([-1, 1, 0, 0], [0, 0, -1, 1]):
            neighbour_pixel = max(0, min(w - 1, current_pixel[0] + i)), max(0, min(h - 1, current_pixel[1] + j))

            if bitmap[neighbour_pixel] == 1:
                continue

            if abs(base_image[neighbour_pixel] - base_image[current_pixel]) <= threshold:
                bitmap[neighbour_pixel] = 1
                queue.append(neighbour_pixel)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
    closing = cv.morphologyEx(bitmap, cv.MORPH_CLOSE, kernel)
    edge = cv.Canny((closing * 255).astype('uint8'), 100, 200)
    return edge


cv.imshow('image', im)
cv.setMouseCallback('image', mouse_callback)
cv.waitKey()
cv.destroyAllWindows()
