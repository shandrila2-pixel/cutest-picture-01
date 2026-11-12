import os
import shutil

# Writes the competition's entry image to /output/entry.png.
# The image is bundled in this repository (entry.png): a kawaii
# kitten in a teal beanie, drawn procedurally with PIL.
# generate.py holds the full generator for reference.

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")

os.makedirs("/output", exist_ok=True)
shutil.copyfile(src, "/output/entry.png")
print("wrote /output/entry.png")
