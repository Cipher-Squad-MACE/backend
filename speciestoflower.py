import json

# Load the full species JSON
with open("species.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter only angiosperms by 'class_common_name'
angios = [s for s in data if s.get('class_common_name') == "Flowering Plants"]

# Save filtered JSON
with open("angiospecies.json", "w", encoding="utf-8") as f:
    json.dump(angios, f, indent=2)

print(f"Saved {len(angios)} angiosperm species to angiospecies.json")
