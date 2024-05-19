import json

# Function to transform JSON data
def transform_json(data):

  # Nested function to transform an object
  def transform_object(obj):
    # If the object is a dictionary
    if isinstance(obj, dict):
      # If the dictionary contains "id" and "name"
      if "id" in obj and "name" in obj:
        # Return the value of "name"
        return obj["name"]
      else:
        # Otherwise, recursively transform each key-value pair in the dictionary
        return {k: transform_object(v) for k, v in obj.items()}
    # If the object is a list
    elif isinstance(obj, list):
      # Transform each item in the list
      return [transform_object(item) for item in obj]
    # If the object is neither a dictionary nor a list, return it as is
    else:
      return obj

  # Nested function to apply the transformation to the data
  def apply_transformation(data):
    # If the data is a dictionary
    if isinstance(data, dict):
      # For each key-value pair in the dictionary
      for key, value in data.items():
        # If the value is a dictionary
        if isinstance(value, dict):
          # If the dictionary contains "id" and "name"
          if "id" in value and "name" in value:
            # Replace the value with the value of "name"
            data[key] = value["name"]
          else:
            # Otherwise, recursively apply the transformation to the value
            apply_transformation(value)
        # If the value is a list
        elif isinstance(value, list):
          # Apply the transformation to each item in the list
          for item in value:
            apply_transformation(item)

  # Apply the transformation to the data
  apply_transformation(data)
  # Convert the transformed data to a JSON string
  transformed_json = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

  # Return the transformed JSON string
  return transformed_json

# Load the JSON data from a file
with open("data.json", "r", encoding="utf-8") as f:
  data = json.load(f)

# Transform each JSON object in the list
transformed_data_list = [transform_json(obj) for obj in data]

# Create the final minified JSON array string
final_json_array = "[" + ",".join(transformed_data_list) + "]"

# Save the transformed data to a file
with open("transformed_file.json", "w", encoding="utf-8") as f:
  f.write(final_json_array)
