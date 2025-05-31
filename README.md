# Example Site:
https://gpx-plotly.pages.dev

# Why:
Finally, I can enjoy all of my hiking track export GPX files, from various sources. These can come from your Garmin watch, your Strava account, or many other sources. My personal favorite is the HiiKER app on Android, which is free and includes free file export and local download.

Use this gpx-plotly Python tool to see your multiple GPX tracks all at once. You can enjoy high detail by setting coincident starting points to easily compare different hikes, by using the '--align' flag. 

Use default no flag to show tracks in dispersed literal space.

Plots are scaled for maximum detail.

HTML export can be embedded into web apps.

# Steps for success:
- Add your GPX files to the import directory.
- Run the software to generate an HTML file export.
```
git clone https://github.com/claytonsrobot/gpx-plotly/
poetry install
poetry run python .\plot_gpx_multi_trail_export.py --align
#or
poetry run python .\plot_gpx_multi_trail_export.py
```