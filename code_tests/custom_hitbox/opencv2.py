import cv2
import numpy as np
import pygame


def merge_rects(rects, threshold):
    merged_rects = []
    while rects:
        main_rect = rects.pop(0)
        close_rects = [
            rect
            for rect in rects
            if np.linalg.norm(np.array(main_rect.center) - np.array(rect.center))
            < threshold
        ]
        for rect in close_rects:
            rects.remove(rect)
        x_values = [r.x for r in close_rects + [main_rect]]
        y_values = [r.y for r in close_rects + [main_rect]]
        last_values_x = [r.x + r.width for r in close_rects + [main_rect]]
        last_values_y = [r.y + r.height for r in close_rects + [main_rect]]
        x_min = min(x_values)
        y_min = min(y_values)
        width = max(last_values_x) - x_min
        height = max(last_values_y) - y_min
        merged_rects.append(pygame.Rect(x_min, y_min, width, height))
    return merged_rects


# Load image
image = cv2.imread("../../assets/sprites/rainbow_road_map_old.png", 0)

# Apply Gaussian blur to the image
blurred = cv2.GaussianBlur(image, (15, 15), 0)

# Perform Canny edge detection
edges = cv2.Canny(blurred, 10, 30)

# Find contours in the edges
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Initialize pygame and create a window and a surface to draw onto
pygame.init()
window = pygame.display.set_mode((1280, 720))
surface = pygame.Surface(window.get_size())

# For every contour, get bounding rect and scale it according to new screen size
scale_x = window.get_width() / image.shape[1]
scale_y = window.get_height() / image.shape[0]
rects = [
    pygame.Rect(
        cv2.boundingRect(contour)[0] * scale_x,
        cv2.boundingRect(contour)[1] * scale_y,
        cv2.boundingRect(contour)[2] * scale_x,
        cv2.boundingRect(contour)[3] * scale_y,
    )
    for contour in contours
]

# Merge rects
threshold_distance = 50
merged_rects = merge_rects(rects, threshold_distance)

# Draw the merged rects on the surface
for rect in merged_rects:
    pygame.draw.rect(surface, (255, 255, 255), rect)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    window.fill((0, 0, 0))
    window.blit(surface, (0, 0))
    pygame.display.flip()
pygame.quit()
