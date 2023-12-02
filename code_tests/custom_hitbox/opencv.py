import cv2
import numpy as np

# Load image
image = cv2.imread('../../assets/sprites/rainbow_road_map_old.png', 0)

# Apply Gaussian blur to the image
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Perform Canny edge detection
edges = cv2.Canny(blurred, 10, 30)

# Display edges
cv2.imshow('Edges', edges)
cv2.waitKey(0)
cv2.destroyAllWindows()