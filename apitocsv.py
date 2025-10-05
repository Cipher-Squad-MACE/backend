import requests

url = "https://services.usanpn.org/npn_portal/species/getSpecies.json"
resp = requests.get(url).json()

# Filter only angiosperms
angiosperms = [s for s in resp if s.get("functional_group") == "Angiosperm"]

print(len(angiosperms), "angiosperm species found")
