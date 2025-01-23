import os, json

save_dir = "mip_era"
os.makedirs(save_dir, exist_ok=True)


context = {
     
      "@context": {
        "id":"@id",
        "type":"@type",
      "@base":"https://espri-mod.github.io/mip-cmor-tables/mip_era/",
      "mip_era":"https://espri-mod.github.io/mip-cmor-tables/mip_era",

    }
    }
file_path = os.path.join(save_dir, "000_context.jsonld")

with open(file_path, 'w') as f:
    json.dump(context, f, indent=4)


data = {
    "@context": "000_context.jsonld",
    "id": "cmip6plus",
    "type":"mip_era"
}

file_path = os.path.join(save_dir, "ripf.json")

with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)


