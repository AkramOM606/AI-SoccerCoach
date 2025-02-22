import json


def get_chunks(file_path="transformed_file.json", interval=60):
    """
    Load match data from a JSON file and group it into non-overlapping 1-minute chunks (60 seconds).
    Each chunk contains only the events that occurred within that specific 1-minute interval.
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    # Sort data by timestamp
    data.sort(key=lambda x: x["timestamp"])

    chunks = []
    current_chunk = []
    interval_start = None

    for item in data:
        timestamp = item["timestamp"]
        hours, minutes, secs = timestamp.split(":")
        current_seconds = int(hours) * 3600 + int(minutes) * 60 + float(secs)

        if interval_start is None:
            interval_start = (
                current_seconds // interval * interval
            )  # Align to nearest minute boundary

        # If the event falls into a new 1-minute interval
        if current_seconds >= interval_start + interval:
            if current_chunk:  # Save the previous chunk if it has data
                chunks.append(current_chunk)
            current_chunk = [item]  # Start a new chunk with the current event
            interval_start += interval  # Move to the next 1-minute boundary
        else:
            current_chunk.append(item)  # Add event to the current chunk

    # Append the final chunk if there’s remaining data
    if current_chunk:
        chunks.append(current_chunk)

    return chunks
