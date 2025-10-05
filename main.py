
import json
from lib.data.fetcher import NPNDataFetcher
from lib.data.filter import SpeciesFilter
from db.inserter import SpeciesInserter, PhenophaseInserter, StationInserter

# MongoDB connection parameters
MONGO_DB_PARAMS = {
    "uri": "mongodb://localhost:27017/",
    "db_name": "vegetation_data"
}

def main():
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

if __name__ == "__main__":
    main()
