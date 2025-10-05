
import json

class SpeciesFilter:
    def filter_angiosperms(self, species_data):
        """Filters a list of species for angiosperms."""
        return [s for s in species_data if s.get('class_common_name') == "Flowering Plants"]

    def save_to_json(self, data, filename):
        """Saves data to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
