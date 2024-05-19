import json


def transform_json(data):
    def transform_object(obj):
        if isinstance(obj, dict):
            if "id" in obj and "name" in obj:
                return obj["name"]
            else:
                return {k: transform_object(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [transform_object(item) for item in obj]
        else:
            return obj

    def apply_transformation(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, dict):
                    if "id" in value and "name" in value:
                        data[key] = value["name"]
                    else:
                        apply_transformation(value)
                elif isinstance(value, list):
                    for item in value:
                        apply_transformation(item)

    # Applying transformation
    apply_transformation(data)
    transformed_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

    return transformed_json


# Loading JSON data
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Transforming each JSON object in the list
transformed_data_list = [transform_json(obj) for obj in data]

# Create the final minified JSON array string
final_json_array = "[" + ",".join(transformed_data_list) + "]"

# Saving the transformed data
with open("transformed_file.json", "w", encoding="utf-8") as f:
    f.write(final_json_array)
