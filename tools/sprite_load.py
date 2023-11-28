"""
This little script loads all sprites from the sprites folder and puts them in the sprites.py file.
"""

from os import listdir


def load_sprites():
    found_images = {}
    for file in listdir("../assets/sprites"):
        if file.lower().endswith(".png"):
            found_images[file.rstrip(".png")] = "assets/sprites/" + file

    found_images = [
        f"""
{short_name} = load(r"{full_name}")


def get_{short_name}_sprite(
      x_center: int = 0,
      y_center: int = 0,
      top: int = None,
      left: int = None,
      target_size: tuple[int|None, int|None] = (None, None)):
    return ImageSprite(r"{full_name}", x_center, y_center, top, left, target_size)
"""
        for short_name, full_name in found_images.items()
    ]

    file_content = """'''
[CHALLENGEWEEK 3] THIS IS AUTO-GENERATED CODE GENERATED FOR EVERY .PNG FILE IN THE 'sprites' FOLDER.
ANY CHANGES TO THIS FILE WILL BE DISCARDED WHEN THE CODE IS REGENERATED.
'''
from util.sprite_overrides import ImageSprite
from pygame.image import load


"""

    file_content += "\n".join(found_images)
    with open("../game/sprites.py", "w") as file:
        file.write(file_content)


if __name__ == "__main__":
    load_sprites()
