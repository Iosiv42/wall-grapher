from typing import Iterable
from math import ceil, floor

from PIL import Image, ImageDraw
import numpy as np

from bitstream import BitStream
from utils import *

def encode(
    input_path,
    output_path,
    encode_data: str,
    encode_pattern: dict[tuple[int]] = None,
):
    """
        Note that encode_pattern values must be sorted for user's convinience
        because if one change ordering it cause that some bit index
        will be changed earlier. It'll cause that bits from bitstream
        will be in different order. Actually, if one preserve encode pattern
        the same when encoding and decoding thing will be alright.
    """

    if encode_pattern is None:
        encode_pattern = {
            0: (0,),
            1: (0,),
            2: (0,),
        }

    with Image.open(input_path) as im:
        pixels = np.asarray(im.convert("RGBA")).astype(np.uint8).reshape((-1, 4))
        w, h = im.width, im.height

    bs = iter(BitStream(encode_data.encode("utf8")))

    encoded_pixels = pixels.copy()
    changed_pixels_count = 0
    
    for idx, pixel in enumerate(pixels, 1):
        if bs.is_empty:
            break

        encoded_pixels[idx] = encode_pixel(pixel, encode_pattern, bs)
        changed_pixels_count += 1

    encoded_pixels[0] = (
        changed_pixels_count // 255,
        changed_pixels_count % 255,
        255,
        255
    )

    encoded_pixels = encoded_pixels.reshape((h, w, 4))

    Image.fromarray(encoded_pixels).save(output_path)


if __name__ == "__main__":
    with open("data.txt") as f:
        data = f.read()

    encode("test.jpg", "sten.png", data)
