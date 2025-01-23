import os, json

save_dir = "member_id"
os.makedirs(save_dir, exist_ok=True)


context = {
     
      "@context": {
       "id": "@id",
       "type": "@type",

      "@base":"https://espri-mod.github.io/mip-cmor-tables/variant_label/",
      "variant_label":"https://espri-mod.github.io/mip-cmor-tables/variant_label"
    
        }
    }
file_path = os.path.join(save_dir, "000_context.jsonld")

with open(file_path, 'w') as f:
    json.dump(context, f, indent=4)


data = {
    "@context": "000_context.jsonld",
    "id": "ripf",
    "type":"variant_label"
}

file_path = os.path.join(save_dir, "ripf.json")

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)


