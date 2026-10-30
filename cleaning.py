import math

MAX_READING = 500.0


def clean_sensor_readings(readings):
    """
    Convert a list of mixed sensor inputs into a list of valid floats.

    - Values that can't be converted to float (None, "abc") are dropped.
    - NaN and negative values are dropped.
    - Values above 500.0 are capped at 500.0.
    - Empty or invalid input returns an empty list.
    """
    if not readings:
        return []

    cleaned_readings = []
    for item in readings:
        try:
            value = float(item)
        except (ValueError, TypeError):
            continue  # not convertible, skip

        if math.isnan(value) or value < 0:
            continue  # NaN or negative error flag, skip

        cleaned_readings.append(min(value, MAX_READING))

    return cleaned_readings


