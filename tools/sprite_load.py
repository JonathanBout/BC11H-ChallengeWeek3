"""
This little script loads all sprites from the sprites folder and puts them in the sprites.py file.
"""

from os import listdir
from time import sleep
from os.path import abspath


def load_sprites():
    found_images = {}
    print("Generating sprites...")
    for file in listdir("../assets/sprites"):
        if file.lower().endswith(".png"):
            print("\r" + file.ljust(25), end="")
            found_images[file.removesuffix(".png")] = "assets/sprites/" + file
            # sleep just to make it look impressive :D
            sleep(0.001)
    print(f"\rFound {len(found_images)} sprites.".ljust(25))
    found_images = [
        f"""
{short_name} = load(r"{full_name}")


def get_{short_name}_sprite(
      x_center: int = 0,
      y_center: int = 0,
      top: int = None,
      left: int = None,
      target_size: tuple[int | None, int | None] = None):
    return create(
        r"{full_name}",
        x_center,
        y_center,
        top,
        left,
        target_size)
"""
        for short_name, full_name in found_images.items()
    ]

    file_content = """'''
THIS CODE IS AUTO-GENERATED BY tools/sprite_load.py.
ANY CHANGES TO THIS FILE WILL BE DISCARDED WHEN THE CODE IS REGENERATED.
'''
from util.sprite_overrides import create
from pygame.image import load

"""
    absolute_path = abspath("../game/sprites.py")
    print("writing to", absolute_path)
    file_content += "\n".join(found_images)
    with open("../game/sprites.py", "w") as file:
        file.write(file_content)

    print("Done!")


if __name__ == "__main__":
    load_sprites()
