import os
import json
# Directory where the JSON files will be saved
save_dir = 'grid_label'

# Create the directory if it doesn't exist
os.makedirs(save_dir, exist_ok=True)

#the context : 
ctx = {"@context": 
        {
        "id": "@id",
        "type": "@type",

        "@base" : "https://espri-mod.github.io/mip-cmor-tables/grid_label/",
        "grid_label":"https://espri-mod.github.io/mip-cmor-tables/grid_label"
       }

       }
file_path = os.path.join(save_dir, "000_context.jsonld")

with open(file_path, 'w') as f:
    json.dump(ctx, f, indent=4)


# TERMS : TODO ... check if it appears in CMIP6Plus

terms = ["gn","gr"]

for term in terms:
    data = {"@context":"000_context.jonld",
            "id" : term,
            "type": "grid_label"}

    file_path = os.path.join(save_dir, f"{term}.json")

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)
