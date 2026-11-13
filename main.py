#!/usr/bin/env python3
# cutest-picture-01 - make.fun "Make the cutest picture" entry.
#
# The artwork: a cream kitten in a strawberry beanie hugging a plush
# bunny. It is drawn entirely in code with numpy soft-ball shading and
# PIL fur strokes, with huge glossy amber eyes, a knit strawberry beanie
# (V stitches, cream seeds, leaf calyx, rolled brim), pink toe beans and
# a warm apricot glow background.
#
# The render is deterministic: every random scatter uses fixed numpy
# seeds, and there is no network, clock or environment input, so the
# same bytes come out on every run. It runs fully offline.
#
# The finished image is committed here as entry.png, a 1024x1024 PNG
# about 509 KiB. generate.py is the full generator that produces it.
#
# This script is the entry's runner: it ships the bundled image to the
# path the grader expects, /output/entry.png, creating the directory
# first if needed. It performs no drawing and needs no third-party
# packages.
#
# License: MIT.

import os
import shutil

# entry.png lives next to this script.
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

# Where the competition expects the rendered image.
OUT_DIR = "/output"
OUT_PATH = os.path.join(OUT_DIR, "entry.png")


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    shutil.copyfile(SRC, OUT_PATH)
    print("wrote " + OUT_PATH)


if __name__ == "__main__":
    main()
