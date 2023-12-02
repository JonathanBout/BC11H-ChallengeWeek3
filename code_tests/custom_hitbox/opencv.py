import cv2
import numpy as np
import pygame

# Load image
image = cv2.imread('../../assets/sprites/rainbow_road_map_old.png', 0)

# Apply Gaussian blur to the image
blurred = cv2.GaussianBlur(image, (5, 5), 0)

# Perform Canny edge detection
edges = cv2.Canny(blurred, 10, 30)

# Find contours in the Canny image
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize pygame and create a window and a surface to draw onto
pygame.init()
window_width = image.shape[1]
window_height = image.shape[0]
window = pygame.display.set_mode((window_width, window_height))
surface = pygame.Surface((window_width, window_height))

# For every contour, get bounding rect and draw it on the pygame surface
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    pygame.draw.rect(surface, (255, 255, 255), pygame.Rect(x, y, w, h))

# Start the loop for displaying pygame window
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Blit the surface onto the window
    window.blit(surface, (0, 0))
    pygame.display.flip()
pygame.quit()