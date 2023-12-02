import pygame
import requests
import io

pygame.init()
screen = pygame.display.set_mode((800, 600))

# Request the image over HTTP
url = 'https://static.wikia.nocookie.net/mariokart/images/6/62/MK8_Rainbow_Road_map.png/revision/latest/scale-to-width-down/165?cb=20161002152721'
image_request = requests.get(url)

# Make sure the request was successful
if image_request.status_code == 200:
    image_file = io.BytesIO(image_request.content)
    try:
        # Load the image
        image = pygame.image.load(image_file)
        # Scale the image down to an appropriate size
        image = pygame.transform.scale(image, (800, 600))  # Scale to 800x600 pixels
        image_rect = image.get_rect()
    except pygame.error as e:
        print(f"Unable to load the image from the URL: {e}")

    angle = 0
    initial_verts = [
        (-image_rect.width // 2, -image_rect.height // 2),  # Top-Left edge
        (-image_rect.width // 2, image_rect.height // 2),   # Bottom-Left edge
        (image_rect.width // 2, image_rect.height // 2),    # Bottom-Right edge
        (image_rect.width // 2, -image_rect.height // 2),   # Top-Right edge
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Rotate the image
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=image_rect.center)

        # Create polygon hitbox (quadrilateral centered at image center)
        hitbox_verts = [pygame.Vector2(v).rotate(angle) + image_rect.center for v in initial_verts]

        screen.fill((255, 255, 255))
        screen.blit(rotated_image, rotated_rect)

        # Draw the polygon hitbox
        pygame.draw.polygon(screen, (255, 0, 0), hitbox_verts, 1)  # 1 for thin line (2 for thicker line, etc.)

        pygame.display.flip()
        # Increase the angle for the next frame
        angle += 1

else:
    print(f"Unable to download image: {url}")

pygame.quit()