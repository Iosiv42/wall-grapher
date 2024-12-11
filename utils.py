from typing import Iterable

from bitstream import BitStream, BitStreamIter


def set_bit(v, index, x):
    """Set the index:th bit of v to 1 if x is truthy, else to 0, and return the new value."""
    mask = 1 << index   # Compute mask, an integer with just bit 'index' set.
    v |= mask           # Set the bit indicated by the mask to True.
    v ^= (not x) * mask # If x is True, do nothing (XOR with 0). If x is False, use the mask for clearing the bit indicated by the mask (XOR with 1 in the requested position).
    return v            # Return the result, we're done.


def encode_pixel(pixel, encode_pattern: dict[Iterable[int]], bs_iter: BitStreamIter):
    encoded_pixel = pixel.copy()
    for component_idx, bit_idxs in encode_pattern.items():
        for bit_idx in bit_idxs:
            try:
                bit = next(bs_iter)
            except StopIteration:
                return pixel
            encoded_pixel[component_idx] = set_bit(pixel[component_idx], bit_idx, bit)

    return encoded_pixel


def decode_pixel(pixel, decode_pattern: dict[Iterable[int]], bs: BitStream):
    for component_idx, bit_idxs in decode_pattern.items():
        for bit_idx in bit_idxs:
            bs.append((pixel[component_idx] >> bit_idx) & 1)


def find_nearest_unique(values_set, initial):
    delta = 0
    while True:
        if (initial + delta) in values_set:
            return initial + delta
        if (initial - delta) in values_set:
            return initial - delta

        delta += 1
