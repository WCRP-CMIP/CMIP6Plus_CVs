import os,glob
import json
import importlib.util
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyld import jsonld
from jsonschema import validate
import jsonschema

def validate_json(data, schema, name = ''):
    try:
        validate(instance=data, schema=schema)
        # print(f"Validation succeeded: {name}")
        return None
    except jsonschema.exceptions.ValidationError as err:
        # print("Validation error:", err.message)
        return name, err.message

def find_files(root_dir, file_name):
    """
    Recursively finds all instances of file_name in the directory tree starting at root_dir.
    """
    for dirpath, _, filenames in os.walk(root_dir):
        if file_name in filenames:
            yield dirpath, os.path.join(dirpath, file_name)

def load_custom_validator(dir_path):
    """
    Dynamically loads the custom validator function from validator.py in the given directory.
    """
    
    print(dir_path)
    # validator_path = os.path.join(dir_path, 'validator.py')
    # if not os.path.isfile(validator_path):
    #     raise FileNotFoundError(f"No validator.py found in directory {dir_path}")
    
    # spec = importlib.util.spec_from_file_location("validator", validator_path)
    # validator_module = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(validator_module)
    
    # if not hasattr(validator_module, 'validate'):
    #     raise AttributeError(f"No validate function found in {validator_path}")
    
    # return validator_module.validate
    
    return dir_path

# def validate_jsonld(file_path, validate_function):
#     """
#     Reads and validates the JSON-LD file using the provided validate_function.
#     """
#     try:
#         with open(file_path, 'r', encoding='utf-8') as file:
#             jsonld_content = json.load(file)
        
#         # Validate the JSON-LD content using the custom validate function
#         validate_function(jsonld_content)
#         return f"Validation successful for {file_path}"
#     except Exception as e:
#         return f"Error in {file_path}: {str(e)}"

def main(root_dir):
    
    jsonld_files = list(find_files(root_dir, 'graph.jsonld'))
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_file = {}
        for dir_path, file_path in jsonld_files:
            try:
                schema = json.load(open(f"{dir_path}/schema.jsonld", 'r'))
                
                
                # jsonld.expand(json.load(open(f"{dir_path}/graph.jsonld", 'r')))
                # validate_function = load_custom_validator(dir_path)
                # future = executor.submit(validate_jsonld, file_path, validate_function)
                # future_to_file[future] = file_path
                
                files = glob.glob(f"{dir_path}/*.json")
                failed = []
                for i in files: 
                    content = json.load(open(i, 'r'))
                    
                    # check this is valid jsonld
                    jsonld.expand(content)
                    # also maybe try to run frame here
                    
                    # check content against schema
                    output = validate_json(content, schema, i)
                    if output:
                        print('FAIL',output, i)
                        failed.append(i)
                        
                    
                
            except Exception as e:
                print(f"Failed to load validator for {dir_path}: {str(e)}")
        
        for future in as_completed(future_to_file):
            file_path = future_to_file[future]
            try:
                result = future.result()
                print(result)
            except Exception as exc:
                print(f"{file_path} generated an exception: {exc}")

if __name__ == "__main__":
    main("../")
