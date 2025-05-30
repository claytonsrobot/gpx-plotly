import argparse
import xml.etree.ElementTree as ET
import plotly.graph_objs as go
import itertools


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
            continue
    return lats, lons, elevs


def align_tracks(tracks):
    """Offset all tracks so they start at the same origin (0, 0, 0)."""
    aligned = []
    for lats, lons, elevs in tracks:
        if not lats:
            continue
        lat0, lon0, elev0 = lats[0], lons[0], elevs[0]
        lats_rel = [lat - lat0 for lat in lats]
        lons_rel = [lon - lon0 for lon in lons]
        elevs_rel = [e - elev0 for e in elevs]
        aligned.append((lats_rel, lons_rel, elevs_rel))
    return aligned


def plot_3d_trails(tracks, filenames, align=False):
    colors = itertools.cycle(['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta'])
    fig = go.Figure()

    if align:
        tracks = align_tracks(tracks)

    for (lats, lons, elevs), name, color in zip(tracks, filenames, colors):
        fig.add_trace(go.Scatter3d(
            x=lons,
            y=lats,
            z=elevs,
            mode='lines+markers',
            name=name,
            line=dict(color=color, width=3),
            marker=dict(size=3)
        ))

    fig.update_layout(
        scene=dict(
            xaxis_title='Longitude' if not align else 'Relative X',
            yaxis_title='Latitude' if not align else 'Relative Y',
            zaxis_title='Elevation (m)'
        ),
        title="Overlayed 3D GPX Trails",
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig.show()


def main():
    parser = argparse.ArgumentParser(description="Overlay and plot multiple GPX tracks in 3D")
    parser.add_argument("files", nargs="+", help="GPX file paths")
    parser.add_argument("--align", action="store_true", help="Align all tracks to start at the same point")
    args = parser.parse_args()

    tracks = []
    valid_filenames = []

    for f in args.files:
        try:
            lats, lons, elevs = parse_gpx(f)
            if lats:
                tracks.append((lats, lons, elevs))
                valid_filenames.append(f)
            else:
                print(f"[WARNING] No valid points found in {f}")
        except Exception as e:
            print(f"[ERROR] Could not read {f}: {e}")

    if tracks:
        plot_3d_trails(tracks, valid_filenames, align=args.align)
    else:
        print("No valid tracks to plot.")


if __name__ == "__main__":
    main()
