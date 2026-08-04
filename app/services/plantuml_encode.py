"""PlantUML text encoding for the public plantuml.com (and compatible) servers.

Matches the deflate + custom base64 scheme used by plantuml-encoder (JS).
"""

from __future__ import annotations

import zlib


_ALPHABET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"


def _encode6bit(b: int) -> str:
    return _ALPHABET[b & 0x3F]


def _append3bytes(b1: int, b2: int, b3: int) -> str:
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return _encode6bit(c1) + _encode6bit(c2) + _encode6bit(c3) + _encode6bit(c4)


def encode64(data: bytes) -> str:
    out = []
    i = 0
    n = len(data)
    while i < n:
        if i + 2 == n:
            out.append(_append3bytes(data[i], data[i + 1], 0)[:3])
        elif i + 1 == n:
            out.append(_append3bytes(data[i], 0, 0)[:2])
        else:
            out.append(_append3bytes(data[i], data[i + 1], data[i + 2]))
        i += 3
    return "".join(out)


def plantuml_encode(text: str) -> str:
    raw = text.strip().encode("utf-8")
    # zlib with default header; PlantUML expects raw deflate → strip zlib header/checksum
    compressed = zlib.compress(raw, 9)[2:-4]
    return encode64(compressed)


def plantuml_svg_url(text: str, server: str = "https://www.plantuml.com/plantuml/svg/") -> str:
    if not server.endswith("/"):
        server += "/"
    return f"{server}{plantuml_encode(text)}"
