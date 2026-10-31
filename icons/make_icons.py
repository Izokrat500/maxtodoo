"""Rysuje ikony appki (niebieskie tło, białe kółko z ptaszkiem) i zapisuje je jako PNG.

Uruchom z folderu projektu:  py icons/make_icons.py
Nie wymaga żadnych dodatkowych bibliotek.
"""
import math
import os
import struct
import zlib

BG = (43, 99, 217)       # --accent z index.html
FG = (255, 255, 255)
SIZES = [180, 192, 512]


def seg_dist(px, py, ax, ay, bx, by):
    dx, dy = bx - ax, by - ay
    t = max(0.0, min(1.0, ((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)))
    return math.hypot(px - (ax + t * dx), py - (ay + t * dy))


def coverage(d, half):
    # Wygładzone krawędzie: 1 w środku kreski, 0 poza nią, płynne przejście na 1 px
    return max(0.0, min(1.0, half - d + 0.5))


def draw(size):
    s = size / 100.0
    cx = cy = 50 * s
    ring_r, ring_half = 30 * s, 3.6 * s
    check = [(36 * s, 51 * s), (46 * s, 61 * s), (65 * s, 41 * s)]
    check_half = 4.2 * s

    rows = []
    for y in range(size):
        row = bytearray([0])  # filtr PNG: brak
        py = y + 0.5
        for x in range(size):
            px = x + 0.5
            ring = coverage(abs(math.hypot(px - cx, py - cy) - ring_r), ring_half)
            d = min(seg_dist(px, py, *check[0], *check[1]),
                    seg_dist(px, py, *check[1], *check[2]))
            a = max(ring, coverage(d, check_half))
            row += bytes(round(BG[i] + (FG[i] - BG[i]) * a) for i in range(3))
        rows.append(bytes(row))
    return b"".join(rows)


def png(size, raw):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", size, size, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


if __name__ == "__main__":
    here = os.path.dirname(os.path.abspath(__file__))
    for size in SIZES:
        path = os.path.join(here, f"icon-{size}.png")
        with open(path, "wb") as f:
            f.write(png(size, draw(size)))
        print("zapisano", path)
