# LiDAR Localization Taxonomy

An interactive, historical taxonomy of methods used in LiDAR localization and point-cloud registration. Each paper-backed method links directly to its arXiv page.

- `taxonomy.fragment.html` is the source of truth. It contains the taxonomy data, styles, and the `renderTaxonomy()` function.
- `render.py` wraps that source in a complete standalone HTML document.
- `index.html` is an ignored local preview. Tagged releases generate and attach `lidar-localization-taxonomy.html` without committing it.

## Add or update a method

Edit the appropriate category in `taxonomy.fragment.html`. A paper-backed method has this shape:

```javascript
{
  year: 2023,
  name: "Method name",
  note: "Why it matters in this lineage.",
  type: "learned",
  paper: "https://arxiv.org/abs/xxxx.xxxxx"
}
```

Then regenerate the public page:

```bash
python3 render.py
```

You can also choose explicit paths:

```bash
python3 render.py taxonomy.fragment.html index.html
```

## Test

Run the dependency-free test suite with:

```bash
python3 -m unittest discover -s tests -v
```

The tests validate the standalone renderer, command-line output, category controls, method record schema, paper URLs, and the explicit allowlist of classical primitives without paper links.

## Release

Push a version tag such as `v0.1.0`. GitHub Actions tests the tagged source, renders `lidar-localization-taxonomy.html`, and attaches it to the corresponding GitHub Release.

Generated HTML is ignored and should not be committed.
