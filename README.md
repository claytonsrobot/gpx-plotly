# Example Site:
https://gpx-plotly.pages.dev

# Why:
Finally, I can enjoy all of my hiking export files from the hikerr app.
See multiple tracks with coincident starting points to easily compare different hikes spatially.
HTML export can be embedded into web apps.

# Steps for success:
- Add your GPX files to the import directory.
- Run the software to generate an HTML file export.
```
poetry install
poetry run python .\plot_gpx_multi_trail_export.py --align
#or
poetry run python .\plot_gpx_multi_trail_export.py
```