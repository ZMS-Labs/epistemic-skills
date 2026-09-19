# Documentation artwork

The cover and method map are original vector compositions for the project
handbook. The map groups questions for readers; it does not create new skill
triggers or prescribe an execution sequence. Nearby Markdown carries the same
information without requiring the images.

The desktop and narrow-screen covers use the same composition and palette.
All type is converted to paths, so the images need no network font service,
embedded script, or locally installed typeface. SVG titles and descriptions
provide text alternatives. The README supplies an additional image description.

## Rebuild

With Python and `fonttools` available:

```bash
python docs/assets/render_assets.py
```

The font is an unmodified copy of Archivo, distributed under the
[SIL Open Font License](fonts/OFL.txt). Source:
[Google Fonts / Archivo](https://github.com/google/fonts/tree/main/ofl/archivo).
The bundled font's SHA-256 is
`0e094a7d3c7c4c25cf1310c4b30014f1dae9332220b1c2c88f4fa996f0b05053`.
The generator and compositions use the repository's license; the font retains
its own license. No font installation is required to read the documentation.

The palette is ink (`#152c35`), paper (`#f5f3ed`), orange (`#ffac70` on ink),
and muted blue (`#b7c8cc` on ink). Diagram labels on paper use darker colors
for contrast. Native GitHub Markdown controls prose layout and theme behavior.
