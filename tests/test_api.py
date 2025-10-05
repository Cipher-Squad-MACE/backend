
import requests
import json

BASE_URL = "http://127.0.0.1:5000"
RESPONSES_DIR = "responses"

def save_response(name, data):
    with open(f"{RESPONSES_DIR}/{name}.json", "w") as f:
        json.dump(data, f, indent=2)

def test_get_species():
    response = requests.get(f"{BASE_URL}/species")
    assert response.status_code == 200
    save_response("species", response.json())

def test_get_phenophases():
    response = requests.get(f"{BASE_URL}/phenophases")
    assert response.status_code == 200
    save_response("phenophases", response.json())

def test_get_stations():
    response = requests.get(f"{BASE_URL}/stations")
    assert response.status_code == 200
    save_response("stations", response.json())

def test_load_data():
    response = requests.post(f"{BASE_URL}/load-data")
    assert response.status_code == 200
    save_response("load_data", response.json())

if __name__ == "__main__":
    test_get_species()
    test_get_phenophases()
    test_get_stations()
    test_load_data()
