#!/usr/bin/env python3
"""news-image-20261126 v3 — 26 November 2026 world news in one image.

Stdlib only. Copies the pre-rendered entry.png to the output directory
given as argv[1], or MAKEFUN_OUTPUT_DIR, or ./output.

The image (1024x1024, 38 verified stories across 10 regions) is produced
by render.py at build time; this entry point only ships it.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")


def output_dir():
    if len(sys.argv) > 1 and sys.argv[1]:
        return sys.argv[1]
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        return env
    return os.path.join(os.getcwd(), "output")


def main():
    if not os.path.isfile(SOURCE):
        sys.exit("entry.png missing next to main.py")
    dest_dir = output_dir()
    os.makedirs(dest_dir, exist_ok=True)
    dest = os.path.join(dest_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    digest = hashlib.sha256(open(dest, "rb").read()).hexdigest()
    if os.path.getsize(dest) != os.path.getsize(SOURCE):
        sys.exit("copied file size mismatch")
    print("wrote %s (%d bytes, sha256 %s)"
          % (dest, os.path.getsize(dest), digest))


if __name__ == "__main__":
    main()
