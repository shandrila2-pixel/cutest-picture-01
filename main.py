import os
import shutil

# make.fun entry — cutest-picture-01 ("Make the cutest picture")
# Writes the competition's entry image to /output/entry.png.
# The image is bundled in this repository (entry.png): a kawaii
# kitten in a teal knit beanie, drawn procedurally with PIL at
# 2x supersampling. Big glossy eyes, rosy blush, cat mouth (ω),
# ribbed band, chevron knit texture, pompom, floating hearts on
# soft pastel sky. generate.py holds the full generator.

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")

os.makedirs("/output", exist_ok=True)
shutil.copyfile(src, "/output/entry.png")
print("wrote /output/entry.png")
