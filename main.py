import os
import shutil

# make.fun entry — cutest-picture-01 ("Make the cutest picture")
# Writes the competition's entry image to /output/entry.png.
# The image is bundled in this repository (entry.png): a cream kitten
# in a strawberry beanie hugging a smiling plush bunny, drawn with
# numpy soft-ball shading + PIL fur strokes at 2x supersampling.
# Huge glossy amber eyes, blep tongue, rosy blush, whiskers, pink
# toe beans, knit texture and strawberry seeds on the beanie, warm
# apricot glow background. Deterministic (fixed seeds), no network.
# generate.py holds the full generator.
# Entry for make.fun cutest-picture-01 bounty ($250 USDC on Solana)

here = os.path.dirname(os.path.abspath(__file__))
src = os.path.join(here, "entry.png")

os.makedirs("/output", exist_ok=True)
shutil.copyfile(src, "/output/entry.png")
print("wrote /output/entry.png")
