import csv
import random
from datetime import datetime, timedelta
import argparse

def generate_telemetry():
    parser = argparse.ArgumentParser(description="Synthetic DCGM Telemetry Generator for ThermaCompute AI Trust Sandbox")
    parser.add_argument("--gpu-count", type=int, default=512, help="Number of GPUs to simulate")
    parser.add_argument("--gpu-type", choices=['H100', 'B200'], default='H100', help="GPU model to simulate")
    parser.add_argument("--hours", type=int, default=24, help="Duration of simulation in hours")

    args = parser.parse_args()

    output_file = "synthetic_dcgm_logs.csv"
    start_time = datetime.now()

    # Power draw ranges based on GPU type
    power_range = (350, 700) if args.gpu_type == 'H100' else (400, 1000)

    try:
        with open(output_file, mode='w', newline='') as csvfile:
            fieldnames = ['timestamp', 'gpu_id', 'gpu_type', 'power_draw_w', 'temp_c', 'throttle_duration_ms']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            # Generate logs for every 15 minutes for the specified duration
            for hour in range(args.hours):
                for minute in [0, 15, 30, 45]:
                    timestamp = (start_time + timedelta(hours=hour, minutes=minute)).isoformat()

                    for gpu_id in range(args.gpu_count):
                        # Simulation Logic
                        power = random.uniform(*power_range)
                        temp = random.uniform(45, 89)
                        throttle = 0

                        if temp > 85:
                            throttle = random.randint(100, 500)

                        writer.writerow({
                            'timestamp': timestamp,
                            'gpu_id': gpu_id,
                            'gpu_type': args.gpu_type,
                            'power_draw_w': round(power, 2),
                            'temp_c': round(temp, 2),
                            'throttle_duration_ms': throttle
                        })

        print("\nSynthetic DCGM Telemetry Generated.")
        print("Notice: This script generates fake hardware metrics to demonstrate the ThermaCompute AI audit process. It contains zero workload data, client IP, or security credentials.\n")

    except IOError as e:
        print(f"Error writing to file: {e}")

if __name__ == "__main__":
    generate_telemetry()
