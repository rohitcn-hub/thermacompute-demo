import csv
from datetime import datetime
from collections import defaultdict

class ThermaComputeParser:
    def __init__(self, hourly_rate=3.50, temp_threshold=85):
        """
        Initialize the parser.
        :param hourly_rate: Dollar loss per GPU per hour of downclocking.
        :param temp_threshold: Temperature in Celsius above which a GPU is considered downclocking.
        """
        self.hourly_rate = hourly_rate
        self.temp_threshold = temp_threshold

    def parse_logs(self, file_path):
        """
        Parses raw logs and calculates the total dollar loss.
        Expected CSV format: timestamp,gpu_id,junction_temp,clock_speed
        Timestamp format: YYYY-MM-DD HH:MM:SS
        """
        gpu_downclock_hours = defaultdict(float)

        try:
            with open(file_path, mode='r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                # We expect headers: timestamp, gpu_id, junction_temp, clock_speed
                for row in reader:
                    gpu_id = row['gpu_id']
                    temp = float(row['junction_temp'])

                    # If temperature exceeds threshold, we consider it a "downclocking" event.
                    # In a real scenario, we'd check if the clock_speed actually dropped.
                    if temp >= self.temp_threshold:
                        # Assume each log entry represents one hour of monitoring for simplicity in this init.
                        # In a production system, we would calculate the delta between timestamps.
                        gpu_downclock_hours[gpu_id] += 1.0

        except (FileNotFoundError, KeyError, ValueError) as e:
            print(f"Error parsing log file: {e}")
            return 0.0, {}

        total_loss = sum(hours * self.hourly_rate for hours in gpu_downclock_hours.values())
        return total_loss, dict(gpu_downclock_hours)

    def calculate_monthly_loss(self, total_loss):
        """
        If the logs represent a sample, this could scale it to a month.
        For this implementation, we'll assume total_loss is the loss for the period provided.
        """
        return total_loss

if __name__ == "__main__":
    # Simple CLI test
    import sys
    if len(sys.argv) > 1:
        parser = ThermaComputeParser()
        loss, details = parser.parse_logs(sys.argv[1])
        print(f"Total Monthly Loss: ${loss:.2f}")
        print(f"GPU Downclock Hours: {details}")
    else:
        print("Please provide a log file path.")
