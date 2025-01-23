import os, json

save_dir = "time_range"
os.makedirs(save_dir, exist_ok=True)


context = {
     
      "@context": {
      "id":"@id",
      "type":"@type",
      "@base":"https://espri-mod.github.io/mip-cmor-tables/time_range/",
      "time_range":"https://espri-mod.github.io/mip-cmor-tables/time_range"
     }
    }
file_path = os.path.join(save_dir, "000_context.jsonld")

with open(file_path, 'w') as f:
    json.dump(context, f, indent=4)

ids = ["hourly","daily","monthly",]

for id in ids :
    data = {
        "@context": "000_context.jsonld",
        "id": id,
        "type":"time_range"

    }

    file_path = os.path.join(save_dir, f"{data["id"]}.json")

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)


