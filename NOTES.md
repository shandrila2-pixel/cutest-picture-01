# NOTES — how `generate.py` builds the artwork

## The concept

A cream kitten in a strawberry beanie hugging a plush bunny, drawn
entirely in code into one `float64` RGB array and saved as `entry.png`.
It sits front-on, round head over a chubby body, both front paws around
the bunny held low so its face stays visible, on a warm cream /
strawberry / apricot palette, painted at 2x and downscaled with LANCZOS.

## numpy soft-ball shading

The core primitive is `ball(c, cx, cy, rx, ry, base, ...)`. Each pixel
computes an elliptical term `q = (x/rx)**2 + (y/ry)**2`, turns it into a
feathered anti-aliased mask, and blends a brighter "lit" colour with a
warm red-shifted shadow (`base * [0.80, 0.71, 0.66]`) via a falloff
raised to 1.7 and modulated by a directional `nx*lx + ny*ly` term, so
every blob reads as a lit volume; `rot` turns limbs and ears.

## Fur strokes

`fluff(...)` scatters short lines over an ellipse using `sqrt(rand)` so
hairs spread evenly rather than clumping. Each strand picks a random
angle, a light or dark cream colour, a low alpha (16-42) and jitter; a
third poke past the silhouette as stray fluff, and the layer is then
Gaussian-blurred so it reads as soft fuzz rather than clean lines.

## Glossy amber eyes

`eye(cx, cy, r)` stacks a cream white, a dark `(40, 24, 22)` pupil, and
a radial iris gradient from amber `(255, 202, 98)` to brown `(116, 52,
22)` with 30 thin radial fibres. The gloss is pure white shapework: a
large upper-left catchlight, a smaller lower-right reflection, and a
tiny plus-shaped star sparkle. The catchlights make the eye look wet.

## Strawberry beanie

The dome is a red `ball` (`218, 64, 68`). Knit texture is a lattice of
paired white and dark-red "V" stitches, offset row by row; nine pale
seeds sit on the upper arc, each with a white specular dot. A five-leaf
`calyx` of tapered polygons, a short green stem and a flattened rolled
brim with stitch marks finish the hat.

## Blep, blush, whiskers and toe beans

The blep is a pink rounded rectangle under a two-arc mouth and small
pink nose; blush is a soft elliptical field on both cheeks; whiskers are
thin white jittered strokes. Each hind foot carries one big pink pad and
three toe pads, and the front paws on the bunny get finger creases.

## The plush bunny

The bunny has its own body and head, one upright ear and one floppy ear
(each with a pink inner), two dark dot eyes with highlights, a small
stitched mouth, rosy cheeks, and a pink bow of two loops and a knot.

## Background, floor and vignette

The backdrop is built in the numpy array: a radial distance from a point
above centre maps through per-channel gradients from bright to warm
(`** 1.35`), so the centre glows apricot and the corners fall to tan. A
soft halo, a wavy fluffy floor band, a faint contact shadow and a smooth
vignette complete the frame and focus it on the kitten.

## Determinism

Nothing is random per run: the fur uses `np.random.RandomState(9)` and
the beanie seeds, iris fibres and whisker jitter use `RandomState(3)`,
while `ball`, gradient, halo, floor, shadow and vignette are closed-form
functions of the pixel grid. With no network, clock or environment
input, `python generate.py` reproduces the exact same byte-for-byte
`entry.png` every time.

## Design walkthrough

`generate.py` paints a single `float64` RGB array, layer by layer, and
only converts to an image at the end. It runs the whole pipeline at 2x
supersampling (`S = 2`, a 2048x2048 canvas) and downscales to 1024x1024
with LANCZOS at the finish, which keeps fur and edges crisp.

The background is pure numpy: a radial distance from a point above
centre drives three per-channel gradients from bright `(255, 251, ...)`
to warm tan, with a `** 1.35` curve so the middle glows apricot and the
corners darken. A soft in-radius halo `(30, 20, 6)` is added behind the
kitten to lift it off the backdrop.

The fluffy floor is a wavy mask: two sine terms make the top edge
irregular, and a clipped ramp `(ys - edge) / height` to the 1.4 power
paints a cream band across the bottom using `paste_mask`.

The creature itself is built from `ball()` calls, soft-shaded ellipses.
The tail is two rotated balls, the body is a large cream ball with a
lighter belly ball over it, and the head is a big ball with a slightly
flattened vertical radius. Each ball gets a lit side and a warm shadow.

Fur is added as strokes: `fluff()` scatters thousands of short lines
around the head and body with `sqrt(rand)` placement, alternating light
and dark cream with low alpha and jitter, about a third longer to poke
past the silhouette. The whole layer is then Gaussian-blurred so it
reads as soft fuzz.

The strawberry beanie is a red dome ball. Knit texture is a lattice of
paired white and dark-red "V" stitches drawn row by row and offset each
row. Nine pale seed ellipses, each with a white specular dot, sit in the
upper arc, placed by a separate `RandomState(3)`. A five-leaf calyx of
tapered polygons, a short green stem, and a flattened rolled brim with
vertical stitch marks complete the hat.

The eyes are the focal point. Each stacks a cream eye white, a dark
pupil disc, and a radial iris gradient from amber `(255, 202, 98)` to
brown `(116, 52, 22)`, plus 30 thin radial iris streaks for fibre
texture. The gloss is pure white: a large upper-left catchlight, a
smaller lower-right reflection, and a tiny plus-shaped star sparkle. The
catchlights are what make the eyes look wet and alive.

The face adds a small pink triangular nose, a two-arc "w" mouth, a pink
rounded-rectangle blep tongue with a darker inner shade, soft blush
fields painted on both cheeks, and three thin white whisker strokes per
side with jittered ends.

The plush bunny is held low so its face stays visible: its own body and
head balls, one upright ear and one floppy ear each with a pink inner,
two dark dot eyes with highlights, a small stitched mouth, rosy cheeks,
and a pink bow drawn as two loops plus a central knot.

The kitten's front paws are two cream balls resting on the bunny, with
finger creases; the hind feet are flattened balls, and on top each gets
one large pink pad plus three pink toe beans in a row.

Finally, a faint contact shadow grounds the feet, and a smooth vignette
multiplies the frame to focus the apricot glow on the kitten before the
2x image is downscaled to its final 1024x1024.

## Verification

Run `python generate.py`; it writes `entry.png` next to the script at
1024x1024 and about 509 KiB, well under the 1 MiB cap. Two fresh runs
produced the identical sha256
`f388531ac51d0bec4ada5dea6cdebccfb2432f8ec2fa1520744f680e4d1423c0`,
matching the committed `entry.png` byte for byte.
