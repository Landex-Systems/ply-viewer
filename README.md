# PLY viewer

View Gaussian splats and point clouds in the browser. One HTML file, no build, no upload — files are read by your
own browser and never leave your machine.

**Try it: https://landex-systems.github.io/ply-viewer/** — drag a `.ply` / `.ksplat` / `.splat` onto the page.

A `.ply` is detected automatically: if it has Gaussian fields (`f_dc_0`, `opacity`, `scale_*`) it renders as a
splat, otherwise as a plain point cloud (`x y z` + optional `red green blue`; binary little/big-endian and ASCII).
Tested on 1.3 GB splat PLYs (5 M gaussians) and 28 M-point clouds.

## Run it locally

```sh
git clone https://github.com/Landex-Systems/ply-viewer.git
cd ply-viewer
python3 serve.py          # → http://localhost:8000
```

Then either drag your file onto the page / click **open file…**, or put files in `scenes/` and list them in
`scenes.json` so they appear in the dropdown (see `scenes.example.json`):

```json
[
  { "label": "my site", "id": "site_points", "name": "point cloud", "kind": "points",
    "file": "scenes/site/points.ply",
    "camera": { "position": [-6, 1, 0.3], "lookAt": [0, 0, -0.5] } },
  { "label": "my site", "id": "site_splat", "name": "splat", "kind": "splat",
    "file": "scenes/site/splat.ply" }
]
```

`?scene=<id>` opens a listed scene directly; `?url=https://…/file.ply` opens any file on a CORS-enabled host.
Any static server works instead of `serve.py` (`npx serve`, VS Code Live Server, `python3 -m http.server`) — the
page just needs to be served over http, because browsers block `fetch()` from `file://`. Dragging a file in works
even from `file://`.

## Controls

| mode | |
|---|---|
| **orbit** (default) | drag = orbit · right-drag = pan · scroll = zoom · **click a surface** to orbit around that point (Alt-click also flies to it) · `F` = centre under cursor · `WASD` move · `E`/`Space` up · `Q` down · `Shift` = 4x |
| **fly** (tick the box) | click the view to capture the mouse (`Esc` frees it) · mouse = look · `WASD` fly · `Space` up · `Shift` down · `Ctrl` = 4x · release keys to drift to a stop |

**speed** and **look** sliders tune movement; **point size** appears for point clouds. Z is up.

## Manifest fields

- `file` — path or URL of the scene; `files` — a list of chunks fetched in order and stitched before loading
  (GitHub Pages refuses files over 100 MB: `split -b 90m -d -a 1 scene.ksplat scene.ksplat.part`).
- `kind` — `splat` or `points`; optional, the header is sniffed otherwise.
- `camera` — `{position, lookAt}`; optional, point clouds are auto-framed from their bounding box.

Big splat PLYs open much faster as `.ksplat` (4–6x smaller). Convert with GaussianSplats3D's
[`create-ksplat.js`](https://github.com/mkkellogg/GaussianSplats3D#creating-ksplat-files):
`node create-ksplat.js in.ply out.ksplat 1 5 "0,0,0" 5.0 256 1` (compression 1, alpha ≥ 5, SH degree 1).

## Built with

[three.js](https://threejs.org/) for point clouds and [GaussianSplats3D](https://github.com/mkkellogg/GaussianSplats3D)
by Mark Kellogg for splats, both loaded from jsDelivr (so the page needs internet for those two scripts; your
data does not go anywhere). MIT licence. Made by [Landex Systems](https://landexsystems.com).
