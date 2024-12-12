import json

# Load the dataset
with open("pokedex_raw_array.json", "r") as file:
    pokemon_data = json.load(file)

# Check for unique names
pokemon_names = [pokemon["name"].lower() for pokemon in pokemon_data]
unique_names = set(pokemon_names)

if len(pokemon_names) == len(unique_names):
    print("All Pokémon names are unique.")
else:
    print("There are duplicate Pokémon names.")
    duplicates = [name for name in unique_names if pokemon_names.count(name) > 1]
    print("Duplicate names:", duplicates)