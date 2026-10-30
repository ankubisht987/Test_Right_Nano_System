# Prompt Log

## Tool used
ChatGPT (AI assistant in VS Code)

## 1. Initial prompt
> Write a Python script called plot_chart.py that loads summary.json and
> creates a bar chart of average temperature per device using matplotlib.
>
> summary.json looks like this:
> {
>     "DEV_A": {"count": 2, "avg_temp": 50.0, "error_count": 1},
>     "DEV_D": {"count": 2, "avg_temp": 70.0, "error_count": 1}
> }
>
> Save the chart as avg_temperature_chart.png.

## 2. Bug / mistake in the first attempt
No charting or layout bug was observed in the first script: it included a
title, axis labels, and `tight_layout()` to help prevent crowding. No formatting
mistake was found and corrected in this conversation.

## 3. Follow-up prompt
No follow-up prompt was used in this conversation.

## Result
The script loaded `summary.json` and generated `avg_temperature_chart.png`.
I ran it and verified that the output was a valid 2400 × 1500 PNG image.
