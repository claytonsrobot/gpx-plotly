import argparse
import xml.etree.ElementTree as ET
import plotly.graph_objs as go

def parse_gpx(filepath):
    """Parse lat/lon/elevation from GPX file."""
    tree = ET.parse(filepath)
    root = tree.getroot()
    ns = {'default': 'http://www.topografix.com/GPX/1/1'}

    lats, lons, elevs = [], [], []
    for trkpt in root.findall(".//default:trkpt", ns):
        try:
            lat = float(trkpt.attrib['lat'])
            lon = float(trkpt.attrib['lon'])
            ele_elem = trkpt.find("default:ele", ns)
            if ele_elem is None:
                continue
            ele = float(ele_elem.text)
            lats.append(lat)
            lons.append(lon)
            elevs.append(ele)
        except (ValueError, KeyError):
            continue  # Skip malformed points
    return lats, lons, elevs

def plot_3d_trail(lons, lats, elevs, title="3D GPX Trail"):
    fig = go.Figure(data=[go.Scatter3d(
        x=lons,
        y=lats,
        z=elevs,
        mode='lines+markers',
        line=dict(color='royalblue', width=3),
        marker=dict(size=3)
    )])

    fig.update_layout(
        scene=dict(
            xaxis_title='Longitude',
            yaxis_title='Latitude',
            zaxis_title='Elevation (m)'
        ),
        title=title,
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig.show()

def main():
    parser = argparse.ArgumentParser(description="Plot a 3D trail from a GPX file")
    parser.add_argument(
        "filename",
        nargs="?",
        default="default.gpx",
        help="GPX file to read (default: default.gpx)"
    )
    args = parser.parse_args()
    try:
        lats, lons, elevs = parse_gpx(args.filename)
        if not lats:
            print("No valid track points found in the file.")
            return
        plot_3d_trail(lons, lats, elevs, title=f"3D GPX Trail: {args.filename}")
    except FileNotFoundError:
        print(f"File not found: {args.filename}")
    except ET.ParseError:
        print(f"Invalid GPX file format: {args.filename}")

if __name__ == "__main__":
    main()
