import cv2 as cv
import numpy as np
import pytesseract
from PIL import Image



image = cv.imread("/Users/mertegemencaliskan/Downloads/Screenshot 2024-04-22 at 7.36.58 PM.png")

lower = np.array([0, 200, 0])
upper = np.array([100, 255, 100])
shapeMask = cv.inRange(image, lower, upper)

cv.imwrite('/Users/mertegemencaliskan/Downloads/result.png', shapeMask)