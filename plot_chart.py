import json

import matplotlib.pyplot as plt


SUMMARY_FILE = "summary.json"
OUTPUT_FILE = "avg_temperature_chart.png"


def main():
    try:
        with open(SUMMARY_FILE, "r", encoding="utf-8") as file:
            summary = json.load(file)
    except FileNotFoundError:
        print(f"Error: {SUMMARY_FILE} not found. Run summarize.py first.")
        return
    if not summary:
        print("No data to plot.")
        return

    device_ids = list(summary.keys())
    average_temperatures = [
        device_data["avg_temp"] for device_data in summary.values()
    ]

    plt.figure(figsize=(8, 5))
    plt.bar(device_ids, average_temperatures, color="steelblue")
    plt.title("Average Temperature per Device")
    plt.xlabel("Device")
    plt.ylabel("Average Temperature")
    plt.tight_layout()
    plt.savefig(OUTPUT_FILE, dpi=300)
    plt.close()

    print(f"Chart saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
