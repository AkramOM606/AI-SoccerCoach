import json
import asyncio


async def send_chunked_json(
    file_path="transformed_file.json", send_function=lambda x: print(x)
):
    """
    This function reads a JSON file, splits it into 10-second chunks based on timestamps,
    and sends each chunk with a 10-second delay using the provided send_function.

    Args:
        file_path: Path to the JSON file.
        send_function: A function that takes a JSON string as input and sends it.
    """
    # Open the JSON file and load its content
    with open(file_path, "r") as f:
        data = json.load(f)

    # Sort the data by timestamps to ensure chronological order
    data.sort(key=lambda x: x["timestamp"])

    start_time = None  # Variable to store the starting timestamp of each chunk
    chunk = []  # List to accumulate items for the current chunk

    for item in data:
        # Extract and convert the timestamp to seconds
        timestamp = item["timestamp"]
        hours, minutes, seconds = timestamp.split(":")
        seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

        if start_time is None:
            # Initialize the start time for the first chunk
            start_time = seconds
        elif seconds - start_time >= 10:
            # If the current item's timestamp is 10 or more seconds after the start time,
            # send the current chunk and reset the variables
            send_function(
                json.dumps(chunk)
            )  # Send the chunk using the provided send_function
            await asyncio.sleep(
                10
            )  # Wait for 10 seconds before processing the next chunk

            start_time = (
                seconds  # Update the start time to the current item's timestamp
            )
            chunk = []  # Reset the chunk list for the next set of items

        chunk.append(item)  # Add the current item to the chunk

    # After the loop, send any remaining items in the last chunk
    if chunk:
        send_function(json.dumps(chunk))


# Function to be called when sending data
def send_data(data):
    print(f"Sending chunk: {data}")


# Define the file path and call the function to start sending data in chunks
file_path = "transformed_file.json"
send_chunked_json(file_path, send_data)
