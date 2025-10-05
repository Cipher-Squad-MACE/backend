import requests

class NPNDataFetcher:
    def __init__(self, base_url="https://services.usanpn.org/npn_portal"):
        self.base_url = base_url

    def get_species(self):
        url = f"{self.base_url}/species/getSpecies.json"
        try:
            resp = requests.get(url)
            resp.raise_for_status()  # Raise an exception for bad status codes
            return resp.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching species data: {e}")
            return None