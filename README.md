# LiDAR Localization Taxonomy

An interactive, historical taxonomy of methods used in LiDAR localization and point-cloud registration. Each paper-backed method links directly to its arXiv page.

- `taxonomy.fragment.html` is the source of truth. It contains the taxonomy data, styles, and the `renderTaxonomy()` function.
- `render.py` wraps that source in a complete standalone HTML document.
- `index.html` is the generated, shareable page and can be opened locally or hosted as a static website.

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

The renderer uses only the Python standard library. Commit both the edited source and regenerated `index.html` so GitHub Pages or any other static host can serve the result directly.
