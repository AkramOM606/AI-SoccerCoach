import json
from time import sleep
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
    with open(file_path, "r") as f:
        data = json.load(f)

    # Sort data by timestamps
    data.sort(key=lambda x: x["timestamp"])

    start_time = None
    chunk = []
    for item in data:
        timestamp = item["timestamp"]
        # Convert timestamp string to seconds
        hours, minutes, seconds = timestamp.split(":")
        seconds = int(hours) * 3600 + int(minutes) * 60 + float(seconds)

        if start_time is None:
            # Initialize start time for the first chunk
            start_time = seconds
        elif seconds - start_time >= 10:
            # Send the chunk and reset variables
            send_function(json.dumps(chunk))
            await asyncio.sleep(10)

            start_time = seconds
            chunk = []

        chunk.append(item)

    # Send the last chunk if any
    if chunk:
        send_function(json.dumps(chunk))


# Example usage (replace send_data with your actual sending function)
def send_data(data):
    # Implement your logic to send data here
    print(f"Sending chunk: {data}")


file_path = "transformed_file.json"
send_chunked_json(file_path, send_data)
