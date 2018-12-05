import os
import uuid
import random
import numpy as np
from PIL import Image, ImageFont, ImageDraw

from config import Config

EMOJIS_FOLDER = Config.EMOJIS_FOLDER
OUTPUT_SIZE = Config.OUTPUT_IMAGE_SIZE
OUTPUT_FOLDER = Config.OUTPUT_IMAGE_FOLDER

def get_emojie(folder=EMOJIS_FOLDER):
    emojis = [f for f in os.listdir(folder) if ".png" == f[-4:]]
    emoji_path = os.path.join(folder, random.choice(emojis))
    return Image.open(emoji_path)

def get_gradient(imgsize=(OUTPUT_SIZE, OUTPUT_SIZE), innerColor=[80, 80, 255], outerColor = [0, 0, 80]):
    # source: https://stackoverflow.com/questions/30608035/plot-circular-gradients-using-pil-in-python
    image = Image.new('RGB', imgsize)
    for y in range(imgsize[1]):
        for x in range(imgsize[0]):

            #Find the distance to the center
            distanceToCenter = np.sqrt((x - imgsize[0]/2) ** 2 + (y - imgsize[1]/2) ** 2)

            #Make it on a scale from 0 to 1
            distanceToCenter = float(distanceToCenter) / (np.sqrt(2) * imgsize[0]/2)

            #Calculate r, g, and b values
            r = outerColor[0] * distanceToCenter + innerColor[0] * (1 - distanceToCenter)
            g = outerColor[1] * distanceToCenter + innerColor[1] * (1 - distanceToCenter)
            b = outerColor[2] * distanceToCenter + innerColor[2] * (1 - distanceToCenter)

            #Place the pixel        
            image.putpixel((x, y), (int(r), int(g), int(b)))

    return image

def get_most_freq_color(img, reverse=True):
    a = np.array(img)
    
    colors = a.reshape((1, a.shape[0] * a.shape[1], 4))[0]
    r = np.mean([c[0] for c in colors if c[0] != 255 and c[0] != 0])
    g = np.mean([c[1] for c in colors if c[1] != 255 and c[1] != 0])
    b = np.mean([c[2] for c in colors if c[2] != 255 and c[2] != 0])

    if reverse:
        return (255 - r, 255 - g, 255 - b)
    return (r, g, b)

def insert_image(background, img):
    b_w, b_h = background.size
    img = img.resize((b_w // 2, b_h // 2), Image.ANTIALIAS)
    i_w, i_h = img.size
    background.paste(img, ((b_w - i_w) // 2, (b_h - i_h) // 2), img)
    return background

def get_random_filename():
    return str(uuid.uuid4()) + ".png"

def generate_random_emoji_cover(filepath=None, output_folder=OUTPUT_FOLDER):
    emoji_pic = get_emojie()
    background = get_gradient(
        innerColor=get_most_freq_color(emoji_pic),
        outerColor=(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )
    )
    final = insert_image(background, emoji_pic)
    if filepath is not None:
        final.save(filepath)
        return filepath

    filepath = get_random_filename()
    if output_folder is not None:
        filepath = os.path.join(output_folder, filepath)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

    final.save(filepath)
    return filepath

