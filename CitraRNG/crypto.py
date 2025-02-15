import struct
from util import uint

blockPosition = [0, 1, 2, 3,
                 0, 1, 3, 2,
                 0, 2, 1, 3,
                 0, 3, 1, 2,
                 0, 2, 3, 1,
                 0, 3, 2, 1,
                 1, 0, 2, 3,
                 1, 0, 3, 2,
                 2, 0, 1, 3,
                 3, 0, 1, 2,
                 2, 0, 3, 1,
                 3, 0, 2, 1,
                 1, 2, 0, 3,
                 1, 3, 0, 2,
                 2, 1, 0, 3,
                 3, 1, 0, 2,
                 2, 3, 0, 1,
                 3, 2, 0, 1,
                 1, 2, 3, 0,
                 1, 3, 2, 0,
                 2, 1, 3, 0,
                 3, 1, 2, 0,
                 2, 3, 1, 0,
                 3, 2, 1, 0,

                 # duplicates of 0-7 to eliminate modulus
                 0, 1, 2, 3,
                 0, 1, 3, 2,
                 0, 2, 1, 3,
                 0, 3, 1, 2,
                 0, 2, 3, 1,
                 0, 3, 2, 1,
                 1, 0, 2, 3,
                 1, 0, 3, 2]


def decryptArray(encryptedData: bytes):
    pv = struct.unpack("<I", encryptedData[0x0:0x4])[0]
    sv = (pv >> 13) & 31

    data = cryptArray(encryptedData, pv, 8, 232)
    data = shuffleArray(data, sv)
    data = encryptedData[0:8] + data

    return data


def cryptArray(data: bytes, seed: int, start: int, end: int):
    result = bytes()

    step = seed
    for i in range(start, end, 2):
        step = uint(step * 0x41C64E6D + 0x6073)
        result += crypt(data[i:i+2], step >> 16)

    step = seed
    if (len(data) > end):
        for i in range(end, len(data), 2):
            step = uint(step * 0x41C64E6D + 0x6073)
            result += crypt(data[i:i+2], step >> 16)

    return result


def crypt(data: bytes, seed: int):
    value = data[0]
    value ^= (seed & 0xFF)
    result = struct.pack("B", value)

    value = data[1]
    value ^= (seed >> 8)
    result += struct.pack("B", value)

    return result


def shuffleArray(data: bytes, sv: int):
    index = sv * 4
    result = bytes()

    for block in range(4):
        start = 56 * blockPosition[block + index]
        end = start + 56
        result += data[start:end]

    result += data[224:]
    return result
