import xml.etree.ElementTree as ET
import csv
from datetime import datetime
import pytz

# ======== SETTINGS ========
INPUT_FILE = "Hawk's Cave Hike 10-05-2025 01_58 PM.gpx"
OUTPUT_FILE = "output.csv"
CENTRAL_TZ = pytz.timezone("America/Chicago")
# ==========================

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

        if time_elem is not None:
            utc_time = datetime.fromisoformat(time_elem.text.replace("Z", "+00:00"))
            local_time = utc_time.astimezone(CENTRAL_TZ)
            time_str = local_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            time_str = None

        points.append([lat, lon, ele, time_str])

    with open(output_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['latitude_decimal', 'longitude_decimal', 'elevation_meters', 'time_centralUSA'])
        writer.writerows(points)

    print(f"✅ Data written to {output_path}. Rows: {len(points)}")

if __name__ == "__main__":
    convert_gpx_to_csv(INPUT_FILE, OUTPUT_FILE)