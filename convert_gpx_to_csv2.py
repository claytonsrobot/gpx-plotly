import xml.etree.ElementTree as ET
import csv
from datetime import datetime, timezone

# ======== SETTINGS ========
INPUT_FILE = "Hawk's Cave Hike 10-05-2025 01_58 PM.gpx"
OUTPUT_FILE = "output2.csv"
EXCEL_EPOCH = datetime(1899, 12, 30, tzinfo=timezone.utc)
# ==========================

def iso_to_excel(iso_timestamp):
    """Convert ISO 8601 time (UTC) to Excel serial date."""
    dt = datetime.fromisoformat(iso_timestamp.replace("Z", "+00:00"))
    delta = dt - EXCEL_EPOCH
    return delta.total_seconds() / 86400  # seconds in a day

def convert_gpx_to_csv(input_path, output_path):
    ns = {'default': 'http://www.topografix.com/GPX/1/1'}
    tree = ET.parse(input_path)
    root = tree.getroot()

    points = []
    for trkpt in root.findall('.//default:trkpt', ns):
        lat = float(trkpt.get('lat'))
        lon = float(trkpt.get('lon'))
        ele_elem = trkpt.find('default:ele', ns)
        time_elem = trkpt.find('default:time', ns)

        ele = float(ele_elem.text) if ele_elem is not None else None
        time_str = time_elem.text if time_elem is not None else None

        excel_serial = iso_to_excel(time_str) if time_str else None

        points.append([lat, lon, ele, time_str, excel_serial])

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'latitude_decimal',
            'longitude_decimal',
            'elevation_meters',
            'time_utc',
            'time_excel'
        ])
        writer.writerows(points)

    print(f"✅ Data written to {output_path}. Rows: {len(points)}")

if __name__ == "__main__":
    convert_gpx_to_csv(INPUT_FILE, OUTPUT_FILE)
