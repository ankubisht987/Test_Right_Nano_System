import os
import tempfile

from cleaning import clean_sensor_readings
from summarize import aggregate_by_device, filter_hot_devices, read_telemetry

if __name__ == "__main__":
    # Test 1: mixed input
    assert clean_sensor_readings([10, "25.5", None, "abc", -3, 700, " 40 "]) == [10.0, 25.5, 500.0, 40.0]
    # Test 2: empty list
    assert clean_sensor_readings([]) == []
    # Test 3: all invalid
    assert clean_sensor_readings([None, "abc", -5, float("nan")]) == []
    # Test 4: bad input type
    assert clean_sensor_readings(None) == []

    print("All tests passed!")

def make_rows():
    return [
        # DEV_A: normal device
        {"device_id": "DEV_A", "status": "ACTIVE", "temperature": "40"},
        {"device_id": "DEV_A", "status": "ERROR", "temperature": "60"},
        # DEV_B: too hot
        {"device_id": "DEV_B", "status": "ERROR", "temperature": "90"},
        # DEV_C: no valid temperatures at all
        {"device_id": "DEV_C", "status": "ACTIVE", "temperature": ""},
        {"device_id": "DEV_C", "status": "ACTIVE", "temperature": "abc"},
        {"device_id": "DEV_C", "status": "ACTIVE", "temperature": "-5"},
        # DEV_D: bad temp row still counts as a record and as an error
        {"device_id": "DEV_D", "status": "ACTIVE", "temperature": "70"},
        {"device_id": "DEV_D", "status": "ERROR", "temperature": "abc"},
        # DEV_E: value above 500 gets capped
        {"device_id": "DEV_E", "status": "ACTIVE", "temperature": "700"},
        # DEV_F: average exactly 80.0 (boundary)
        {"device_id": "DEV_F", "status": "ACTIVE", "temperature": "80"},
        # Messy status text and spacing
        {"device_id": " DEV_G ", "status": " error ", "temperature": " 30 "},
        # Missing device_id: must be skipped
        {"device_id": "", "status": "ACTIVE", "temperature": "30"},
        # Short row (None values): must not crash
        {"device_id": "DEV_H", "status": None, "temperature": None},
    ]


def test_aggregation():
    summary = aggregate_by_device(make_rows())

    assert summary["DEV_A"] == {"count": 2, "avg_temp": 50.0, "error_count": 1}
    assert summary["DEV_B"] == {"count": 1, "avg_temp": 90.0, "error_count": 1}
    assert summary["DEV_C"] == {"count": 3, "avg_temp": None, "error_count": 0}
    assert summary["DEV_D"] == {"count": 2, "avg_temp": 70.0, "error_count": 1}
    assert summary["DEV_E"]["avg_temp"] == 500.0
    assert summary["DEV_G"] == {"count": 1, "avg_temp": 30.0, "error_count": 1}
    assert summary["DEV_H"] == {"count": 1, "avg_temp": None, "error_count": 0}
    assert "" not in summary


def test_filtering():
    summary = aggregate_by_device(make_rows())
    filtered = filter_hot_devices(summary, 80.0)

    assert "DEV_A" in filtered          # 50.0, kept
    assert "DEV_D" in filtered          # 70.0, kept
    assert "DEV_F" in filtered          # exactly 80.0, kept
    assert "DEV_B" not in filtered      # 90.0, too hot
    assert "DEV_E" not in filtered      # 500.0, too hot
    assert "DEV_C" not in filtered      # no valid temps, excluded


def test_empty_and_all_filtered():
    assert aggregate_by_device([]) == {}
    assert filter_hot_devices({}, 80.0) == {}
    hot_only = aggregate_by_device(
        [{"device_id": "DEV_X", "status": "ACTIVE", "temperature": "99"}]
    )
    assert filter_hot_devices(hot_only, 80.0) == {}


def test_read_telemetry():
    # Missing file
    assert read_telemetry("this_file_does_not_exist.csv") is None

    with tempfile.TemporaryDirectory() as folder:
        # Header only
        header_only = os.path.join(folder, "header_only.csv")
        with open(header_only, "w", encoding="utf-8") as f:
            f.write("device_id,status,temperature\n")
        assert read_telemetry(header_only) == []

        # Missing a required column
        bad_header = os.path.join(folder, "bad_header.csv")
        with open(bad_header, "w", encoding="utf-8") as f:
            f.write("device_id,status\nDEV_A,ACTIVE\n")
        assert read_telemetry(bad_header) is None

        # Completely empty file
        empty = os.path.join(folder, "empty.csv")
        open(empty, "w").close()
        assert read_telemetry(empty) is None

        # Valid file
        good = os.path.join(folder, "good.csv")
        with open(good, "w", encoding="utf-8") as f:
            f.write("device_id,status,temperature\nDEV_A,ACTIVE,45.2\n")
        assert len(read_telemetry(good)) == 1


if __name__ == "__main__":
    test_aggregation()
    test_filtering()
    test_empty_and_all_filtered()
    test_read_telemetry()
    print("All tests passed!")