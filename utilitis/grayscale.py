import cv2
# import numpy as np
# from numpy import uint8

def grayscaling(image):
    # H, W = image.shape[:2]
    # gray = np.zeros((H, W), dtype=uint8)
    # for i in range(H):
    #     for j in range(W):
    #         gray[i, j] = np.clip(0.299 * image[i, j, 0] +
    #                              0.587 * image[i, j, 1] +
    #                              0.114 * image[i, j, 2], 0, 255)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    return gray