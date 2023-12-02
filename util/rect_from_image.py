import cv2
import numpy as np
import pygame


# Create a function to merge close rects
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


def load_rect(image_path: str) -> list[pygame.Rect]:
    # Load image
    image = cv2.imread(image_path, 0)

    # Get size of image
    size = pygame.image.load(image_path).get_size()

    # Apply Gaussian blur to the image
    blurred = cv2.GaussianBlur(image, (15, 15), 0)

    # Perform Canny edge detection
    edges = cv2.Canny(blurred, 10, 30)

    # Find contours in the edges
    contours, _ = cv2.findContours(
        edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # For every contour, get bounding rect and scale it according to new screen size
    scale_x = (size[0] / image.shape[1]) * 2
    scale_y = (size[1] / image.shape[0]) * 1.5
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


    return merged_rects
