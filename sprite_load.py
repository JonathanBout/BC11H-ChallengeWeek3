from os import listdir


def load_sprites():
    found_images = []
    for file in listdir("sprites"):
        if file.lower().endswith(".png"):
            found_images.append(file)

    found_images = [
        f"""def {file.rstrip(".png")}(x_center: int = 0, y_center: int = 0, top: int = None, left: int = None):
    return ImageSprite("{file}", x_center, y_center, top, left)
"""
        for file in found_images
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
