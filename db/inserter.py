
import json
import xml.etree.ElementTree as ET
from pymongo import MongoClient

class MongoInserter:
    def __init__(self, db_params):
        self.client = MongoClient(db_params['uri'])
        self.db = self.client[db_params['db_name']]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.client.close()

class SpeciesInserter(MongoInserter):
    def insert_species(self, species_data):
        species_collection = self.db['species']
        for sp in species_data:
            species_collection.update_one({'species_id': sp.get('species_id')}, {'$set': sp}, upsert=True)

class PhenophaseInserter(MongoInserter):
    def insert_phenophases(self, phenophases_data):
        phenophases_collection = self.db['phenophases']
        for ph in phenophases_data:
            phenophases_collection.update_one({'phenophase_id': ph.get('phenophase_id')}, {'$set': ph}, upsert=True)

class StationInserter(MongoInserter):
    def insert_stations_from_xml(self, xml_file):
        stations_collection = self.db['stations']
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
        except ET.ParseError as e:
            print(f"Failed to parse XML: {e}")
            return
        except FileNotFoundError:
            print(f"{xml_file} file not found.")
            return

        for site in root.findall('site'):
            try:
                station_id = int(site.get('station_id'))
                station_name = site.get('station_name', 'Unknown')
                latitude = float(site.get('latitude', 0))
                longitude = float(site.get('longitude', 0))

                station_doc = {
                    'station_id': station_id,
                    'station_name': station_name,
                    'latitude': latitude,
                    'longitude': longitude
                }
                stations_collection.update_one({'station_id': station_id}, {'$set': station_doc}, upsert=True)
            except Exception as e:
                print(f"Skipping site due to error: {e}, data: {site.attrib}")
