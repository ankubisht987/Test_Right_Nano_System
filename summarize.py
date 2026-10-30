import csv
import json
import sys

from cleaning import clean_sensor_readings

INPUT_FILE = "device_telemetry.csv"
OUTPUT_FILE = "summary.json"
MAX_AVG_TEMP = 80.0


def read_telemetry(path): # Read the file and return the rows as a list of dictionaries. Each dictionary represents a row in the CSV file, with keys corresponding to the column headers. If the file is not found or cannot be read, an error message is printed and None is returned. If the file is empty or missing required columns, an error message is printed and None is returned.
    """Read the CSV file and return the rows as a list."""
    try:
        with open(path, "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # check that the needed columns are present
            if reader.fieldnames is None:
                print("Error: the CSV file is empty")
                return None
            for column in ["device_id", "status", "temperature"]:
                if column not in reader.fieldnames:
                    print("Error: missing column:", column)
                    return None

            return list(reader)
    except FileNotFoundError:
        print("Error: file not found:", path)
        return None
    except OSError as error:
        print("Error: could not read file:", error)
        return None


def aggregate_by_device(rows): # The main Calculation function that processes the list of rows and aggregates the data by device ID. It counts the number of records, calculates the average temperature, and counts the number of error statuses for each device. The function returns a summary dictionary containing this aggregated information for each device.
    """Group rows by device and calculate count, average temp and errors."""
    devices = {}

    for row in rows:
        device_id = (row.get("device_id") or "").strip()
        status = (row.get("status") or "").strip().upper()

        # skip rows that have no device id
        if device_id == "":
            continue

        if device_id not in devices:
            devices[device_id] = {
                "count": 0,
                "total_temp": 0.0,
                "temp_count": 0,
                "error_count": 0,
            }

        devices[device_id]["count"] += 1

        if status == "ERROR":
            devices[device_id]["error_count"] += 1

        # use the cleaning function from Section 1
        temps = clean_sensor_readings([row.get("temperature")])
        if len(temps) > 0:
            devices[device_id]["total_temp"] += temps[0]
            devices[device_id]["temp_count"] += 1

    # calculate the average for each device
    summary = {}
    for device_id in devices:
        data = devices[device_id]

        if data["temp_count"] > 0:
            average = round(data["total_temp"] / data["temp_count"], 2)
        else:
            average = None

        summary[device_id] = {
            "count": data["count"],
            "avg_temp": average,
            "error_count": data["error_count"],
        }

    return summary


def filter_hot_devices(summary, max_avg): #remove hot devices from the summary dictionary based on their average temperature. It iterates through the summary and checks if the average temperature for each device is less than or equal to the specified max_avg. If it is, the device is included in the result; otherwise, it is excluded. The function returns a new dictionary containing only the devices that meet the temperature criteria.
    """Remove devices whose average temperature is above max_avg."""
    result = {}

    for device_id in summary:
        average = summary[device_id]["avg_temp"]
        if average is not None and average <= max_avg:
            result[device_id] = summary[device_id]

    return result


def save_json(summary, path): #write the result of the aggregation to a JSON file. It takes the summary dictionary and the path to the output file as arguments. The function opens the specified file in write mode and uses the json.dump() method to serialize the summary dictionary into JSON format, with an indentation of 4 spaces for readability. If the file cannot be opened or written to, an error message is printed.
    """Save the summary to a JSON file."""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(summary, file, indent=4)


def print_table(summary): #show the result of the aggregation in a tabular format. It takes the summary dictionary as an argument and prints a formatted table to the console. The table includes columns for Device ID, Records, Avg Temp, and Errors. If the summary is empty, it prints a message indicating that there are no devices to display.
    """Print the summary as a table."""
    if len(summary) == 0:
        print("No devices to display.")
        return

    print()
    print(f"{'Device ID':<15}{'Records':<10}{'Avg Temp':<12}{'Errors':<10}")
    print("-" * 47)

    for device_id in summary:
        data = summary[device_id]
        print(f"{device_id:<15}{data['count']:<10}{data['avg_temp']:<12.2f}{data['error_count']:<10}")


def main():
    # use a file given on the command line, or the default file
    if len(sys.argv) > 1:
        input_path = sys.argv[1]
    else:
        input_path = INPUT_FILE

    rows = read_telemetry(input_path)
    if rows is None:
        sys.exit(1)
    if len(rows) == 0:
        print("The CSV has no data rows.")
        sys.exit(0)

    summary = aggregate_by_device(rows)
    summary = filter_hot_devices(summary, MAX_AVG_TEMP)
    save_json(summary, OUTPUT_FILE)
    print_table(summary)


# if __name__ == "__main__":
#     main()