
from flask import Flask, jsonify, request
from data.fetcher import NPNDataFetcher
from data.filter import SpeciesFilter
from db.inserter import SpeciesInserter, PhenophaseInserter, StationInserter
from pymongo import MongoClient
import json

app = Flask(__name__)

# MongoDB connection parameters
MONGO_DB_PARAMS = {
    "uri": "mongodb://localhost:27017/",
    "db_name": "vegetation_data"
}

def get_db():
    client = MongoClient(MONGO_DB_PARAMS['uri'])
    db = client[MONGO_DB_PARAMS['db_name']]
    return db

@app.route('/')
def index():
    return "Welcome to the Vegetation Data API!"

@app.route('/species', methods=['GET'])
def get_species():
    db = get_db()
    species = list(db.species.find({}, {'_id': 0}))
    return jsonify(species)

@app.route('/phenophases', methods=['GET'])
def get_phenophases():
    db = get_db()
    phenophases = list(db.phenophases.find({}, {'_id': 0}))
    return jsonify(phenophases)

@app.route('/stations', methods=['GET'])
def get_stations():
    db = get_db()
    stations = list(db.stations.find({}, {'_id': 0}))
    return jsonify(stations)

@app.route('/load-data', methods=['POST'])
def load_data():
    # 1. Fetch and filter species data
    print("Fetching species data...")
    fetcher = NPNDataFetcher()
    all_species = fetcher.get_species()
    if all_species:
        print(f"Fetched {len(all_species)} species.")
        
        # Filter for angiosperms
        print("Filtering for angiosperms...")
        s_filter = SpeciesFilter()
        angiosperms = s_filter.filter_angiosperms(all_species)
        print(f"Found {len(angiosperms)} angiosperm species.")

        # Save angiosperms to a file
        angiosperms_file = "angiospecies.json"
        print(f"Saving angiosperms to {angiosperms_file}...")
        s_filter.save_to_json(angiosperms, angiosperms_file)

        # 2. Insert species data into the database
        print("Inserting species data into the database...")
        with SpeciesInserter(MONGO_DB_PARAMS) as inserter:
            inserter.insert_species(angiosperms)
        print("Species data inserted.")

    # 3. Insert phenophase data
    print("Inserting phenophase data...")
    phenophases_file = "phenophases.json"
    with open(phenophases_file, "r", encoding="utf-8") as f:
        phenophases_data = json.load(f)
    
    with PhenophaseInserter(MONGO_DB_PARAMS) as inserter:
        inserter.insert_phenophases(phenophases_data)
    print("Phenophase data inserted.")

    # 4. Insert station data
    print("Inserting station data...")
    stations_file = "stations.xml"
    with StationInserter(MONGO_DB_PARAMS) as inserter:
        inserter.insert_stations_from_xml(stations_file)
    print("Station data inserted.")
    
    return jsonify({"message": "Data loading process completed."})

if __name__ == '__main__':
    app.run(debug=True)
