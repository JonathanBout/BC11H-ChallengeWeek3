from os import listdir
from os.path import abspath


def load_sprites():
    found_images = {}
    for file in listdir("sprites"):
        if file.lower().endswith(".png"):
            found_images[file] = abspath("sprites/" + file)

    found_images = [
        f"""def {short_name.rstrip(".png")}(x_center: int = 0, y_center: int = 0, top: int = None, left: int = None):
    return ImageSprite(r"{full_name}", x_center, y_center, top, left)
"""
        for short_name, full_name in found_images.items()
    ]

    file_content = """'''
THIS IS AUTO-GENERATED CODE GENERATED FOR EVERY .PNG FILE IN THE 'sprites' FOLDER.
ANY CHANGES TO THIS FILE WILL BE DISCARDED WHEN THE CODE IS REGENERATED.
'''
from sprite_overrides import ImageSprite


"""

    file_content += "\n\n".join(found_images)
    with open("sprites.py", "w") as file:
        file.write(file_content)


if __name__ == "__main__":
    load_sprites()
