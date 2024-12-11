from typing import Iterable

Byte = int


class BitStreamIter:
    def __init__(self, data: Iterable[Byte]|bytes|bytearray):
        self.data = iter(data)
        self.bit_idx = 8    # Counted from MSB
        self.is_empty = False

    def __next__(self):
        if self.bit_idx == 8:
            self.bit_idx = 0
            try:
                self.curr_byte = next(self.data)
            except StopIteration as exc:
                self.is_empty = True
                raise exc

        res = (self.curr_byte >> (7 - self.bit_idx)) & 1
        self.bit_idx += 1
        return res

    def __iter__(self):
        return self


class BitStream:
    def __init__(self, data: Iterable[Byte]|bytes|bytearray = None):
        self.data = data
        if data is None:
            self.data = []

        self.bit_idx = 8    # Counted from MSB

    def append(self, bit):
        if self.bit_idx == 8:
            self.data.append(0)
            self.bit_idx = 0

        self.data[-1] |= bit << (7 - self.bit_idx)
        self.bit_idx += 1

    def __iter__(self):
        return BitStreamIter(self.data)
