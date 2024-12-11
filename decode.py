from PIL import Image
import numpy as np

from bitstream import BitStream
from utils import decode_pixel, find_nearest_unique


def decode(
    input_path,
    decode_pattern: dict[tuple[int]] = None,
) -> str:
    """
        Note that encode_pattern values must be sorted for user's convinience
        because if one change ordering it cause that some bit index
        will be changed earlier. It'll cause that bits from bitstream
        will be in different order. Actually, if one preserve encode pattern
        the same when encoding and decoding thing will be alright.
    """

    if decode_pattern is None:
        decode_pattern = {
            0: (0,),
            1: (0,),
            2: (0,),
        }

    with Image.open(input_path) as im:
        pixels = np.asarray(im.convert("RGBA")).astype(np.uint8).reshape((-1, 4))

    changed_pixels_count = int(pixels[0][1]) + int(pixels[0][2])*int(pixels[0][0])

    bs = BitStream()
    for pixel in pixels[1:changed_pixels_count + 1]:
        decode_pixel(pixel, decode_pattern, bs)

    return bytes(bs.data).decode("utf8", errors="replace")


if __name__ == "__main__":
    print(decode("sten.png"))
