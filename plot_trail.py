import csv
import argparse
import plotly.graph_objs as go

def load_csv_data(filepath):
    lats, lons, elevs = [], [], []
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                lats.append(float(row['latitude_decimal']))
                lons.append(float(row['longitude_decimal']))
                elevs.append(float(row['elevation_meters']))
            except (KeyError, ValueError):
                continue  # skip invalid rows
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
    parser = argparse.ArgumentParser(description="Plot a 3D trail from a CSV file")
    parser.add_argument(
        "filename",
        nargs="?",
        default="output.csv",
        help="CSV file to read (default: output.csv)"
    )
    args = parser.parse_args()
    try:
        lats, lons, elevs = load_csv_data(args.filename)
        if not lats:
            print("No valid data points found in the file.")
            return
        plot_3d_trail(lons, lats, elevs, title=f"3D Trail: {args.filename}")
    except FileNotFoundError:
        print(f"File not found: {args.filename}")

if __name__ == "__main__":
    main()
