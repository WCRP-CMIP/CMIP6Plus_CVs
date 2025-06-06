import json
from pathlib import Path

archive_file_path = Path("../CMIP6_CVs/_archive/CMIP6_institution_id.json")
institution_id_path = Path("institution_id")

with open(archive_file_path, "r") as f:
    input_data = json.load(f)

for file in institution_id_path.iterdir():
    if file.stem != "000_context":
        with open(file, "r") as f:
            term_data = json.load(f)
        for k, desc in input_data["institution_id"].items():
            if k.lower() == term_data["id"]:
                # print(f"ADD {desc} FOR {k}")
                term_data["description"] = desc
        if "description" not in term_data:
            term_data["description"] = ""
            # print("vu")
        with open(file, "w") as f:
            json.dump(term_data, f, indent=4)
