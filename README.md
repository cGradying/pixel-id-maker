# Pixel ID Maker

Offline, single-file tools for the AWS Student Builder Group (PUP) pixel ID cards.

- `dist/pixel-id-maker.html`: the ID designer. Front and back of a CR80 card (637 x 1012 px at 300 dpi), pixel photo fade, pixel-art QR, connect list, job description overlay, asset area, PVC and laminated 3D mockups, PNG exports. Open it in Chrome or Edge, no install needed.
- `dist/pixel-fade-tool.html`: the standalone photo-to-pixel fade tool.

Settings and uploaded images save automatically in your browser (localStorage + IndexedDB). Use **Save settings file** in the Export panel to move settings to another computer.

## Editing and rebuilding

The source of the ID maker is `src/id-maker.html` (placeholders like `__FONTCSS__` are filled at build time). The pixel-fade engine is extracted from `src/pixel-fade-tool.html`.

```
python3 build.py
```

writes `dist/pixel-id-maker.html` with every font, the background, the QR library and the engine inlined.

## Assets

- `assets/pixel-bg.png`: the purple pixel background.
- `assets/fonts/IntraNet-*.otf`: IntraNet typeface files supplied by the org. Check the font license before making this repo public.
- `assets/fonts/*.woff2`: Pixelify Sans, Silkscreen, Chakra Petch, Space Grotesk (SIL Open Font License, via Fontsource).
- `assets/vendor/qrcode.js`: qrcode-generator by Kazuhiko Arase (MIT).
