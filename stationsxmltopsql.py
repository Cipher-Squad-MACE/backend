import xml.etree.ElementTree as ET
import psycopg2

# Load XML file (make sure it has a single root <stations>)
try:
    tree = ET.parse("stations.xml")
    root = tree.getroot()
except ET.ParseError as e:
    print(f"Failed to parse XML: {e}")
    exit(1)
except FileNotFoundError:
    print("stations.xml file not found.")
    exit(1)

# Connect to PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    dbname="vegetation data",
    user="postgres",
    password="root"
)
cur = conn.cursor()

# Iterate over each <site> element
for site in root.findall('site'):
    try:
        station_id = int(site.get('station_id'))
        station_name = site.get('station_name', 'Unknown')
        latitude = float(site.get('latitude', 0))
        longitude = float(site.get('longitude', 0))

        # Insert into table
        cur.execute("""
            INSERT INTO stations (station_id, station_name, latitude, longitude)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (station_id) DO NOTHING
        """, (station_id, station_name, latitude, longitude))
    except Exception as e:
        print(f"Skipping site due to error: {e}, data: {site.attrib}")

# Commit and close
conn.commit()
cur.close()
conn.close()

print("Stations inserted successfully!")
