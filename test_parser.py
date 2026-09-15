import pytest
import csv
import os
from parser import ThermaComputeParser

@pytest.fixture
def sample_log_file(tmp_path):
    """Creates a temporary CSV log file for testing."""
    log_file = tmp_path / "test_logs.csv"
    # headers: timestamp,gpu_id,junction_temp,clock_speed
    data = [
        ["2023-01-01 00:00:00", "GPU0", "70", "1500"], # OK
        ["2023-01-01 01:00:00", "GPU0", "90", "1200"], # Downclocking (1 hour)
        ["2023-01-01 02:00:00", "GPU0", "95", "1100"], # Downclocking (1 hour)
        ["2023-01-01 00:00:00", "GPU1", "75", "1500"], # OK
        ["2023-01-01 01:00:00", "GPU1", "86", "1200"], # Downclocking (1 hour)
    ]

    with open(log_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "gpu_id", "junction_temp", "clock_speed"])
        writer.writerows(data)

    return str(log_file)

def test_parse_logs_calculation(sample_log_file):
    parser = ThermaComputeParser(hourly_rate=3.50, temp_threshold=85)
    total_loss, details = parser.parse_logs(sample_log_file)

    # GPU0: 2 hours downclocking
    # GPU1: 1 hour downclocking
    # Total: 3 hours * 3.50 = 10.50
    assert total_loss == 10.50
    assert details["GPU0"] == 2.0
    assert details["GPU1"] == 1.0

def test_parse_logs_no_downclocking(tmp_path):
    log_file = tmp_path / "no_downclock.csv"
    data = [
        ["2023-01-01 00:00:00", "GPU0", "70", "1500"],
        ["2023-01-01 01:00:00", "GPU0", "80", "1500"],
    ]
    with open(log_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "gpu_id", "junction_temp", "clock_speed"])
        writer.writerows(data)

    parser = ThermaComputeParser(hourly_rate=3.50, temp_threshold=85)
    total_loss, details = parser.parse_logs(str(log_file))

    assert total_loss == 0.0
    assert details == {}

def test_parse_logs_empty_file(tmp_path):
    log_file = tmp_path / "empty.csv"
    with open(log_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "gpu_id", "junction_temp", "clock_speed"])

    parser = ThermaComputeParser()
    total_loss, details = parser.parse_logs(str(log_file))

    assert total_loss == 0.0
    assert details == {}
