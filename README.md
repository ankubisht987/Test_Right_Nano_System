# Device Log Summarizer

A small Python command-line tool that reads device telemetry from a CSV file, cleans the data, summarizes it per device, saves the result as JSON, and draws a bar chart of average temperature.

## What it does

1. Cleans sensor values (drops invalid ones, caps values above 500.0).
2. Reads `device_telemetry.csv` and groups the rows by `device_id`.
3. For each device, calculates the total records, the average temperature, and the number of `ERROR` rows.
4. Removes devices whose average temperature is above 80.0.
5. Saves the result to `summary.json` and prints a table in the terminal.
6. Draws a bar chart of average temperature per device and saves it as `avg_temperature_chart.png`.

## Project files

| File | Purpose |
|---|---|
| `main.py` | Runs the whole project (summary, then chart) |
| `cleaning.py` | `clean_sensor_readings()` function with simple tests |
| `summarize.py` | Reads the CSV, aggregates, filters, saves JSON, prints the table |
| `plot_chart.py` | Creates the bar chart from `summary.json` |
| `test_summarize.py` | Tests for `summarize.py` |
| `device_telemetry.csv` | Input data |
| `summary.json` | Sample output |
| `avg_temperature_chart.png` | Sample chart |
| `PROMPT_LOG.md` | How AI tools were used for the chart |

## Setup

Python 3 is required.

```
pip install matplotlib
```

## How to run

Run everything:

```
python main.py
```

Use a different CSV file:

```
python main.py my_file.csv
```

Run only one step:

```
python summarize.py
python plot_chart.py
```

## How to run the tests

```
python cleaning.py
python test_summarize.py
```

Each should end with `All tests passed!`.
(`test_summarize.py` also prints a few "Error: ..." lines. That is expected, because it tests bad input on purpose.)

## Cleaning rules

- Values that cannot be converted to a number (`None`, `"abc"`, blank) are dropped.
- Negative values and `NaN` are dropped.
- Values above 500.0 are capped at 500.0.
- An empty or invalid list returns an empty list instead of crashing.

## Design choices

- A row with a bad temperature still counts as a record, and its `ERROR` status is still counted. It is only left out of the average.
- A device with no valid temperature at all is excluded, because its average cannot be calculated.
- A device with an average of exactly 80.0 is kept. Only averages above 80.0 are removed.
- Rows with a missing `device_id` are skipped.
- Status text is not case-sensitive and extra spaces are ignored (`" error "` counts as `ERROR`).

## Error handling

The program shows a clear message instead of crashing when:

- the CSV file is missing or empty
- a required column is missing
- temperatures are blank, text, or negative
- no devices are left after filtering
- `summary.json` is missing when plotting the chart
