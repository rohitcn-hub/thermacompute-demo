import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_logs(output_path: str):
    """
    Generates synthetic DCGM telemetry logs for 8x H100 GPUs over 24 hours.
    """
    num_gpus = 8
    duration_hours = 24
    interval_seconds = 10

    start_time = datetime.now().replace(minute=0, second=0, microsecond=0)
    total_steps = (duration_hours * 3600) // interval_seconds

    data = []

    for gpu_id in range(num_gpus):
        # Base parameters
        temp = 70.0
        clock = 1980
        power = 650

        for step in range(total_steps):
            timestamp = start_time + timedelta(seconds=step * interval_seconds)

            # Simulate thermal spikes for GPU 2 and 5
            if gpu_id in [2, 5]:
                # Every few hours, simulate a spike for 30 minutes
                if (step // 180) % 6 == 0: # 180 steps = 30 mins; %6 = every 3 hours
                    temp = np.random.uniform(84, 87)
                    clock = np.random.uniform(1300, 1380)
                    power = np.random.uniform(300, 400)
                else:
                    temp = np.random.uniform(68, 72)
                    clock = np.random.uniform(1950, 2000)
                    power = np.random.uniform(630, 670)
            else:
                # Normal operation
                temp = np.random.uniform(68, 72)
                clock = np.random.uniform(1950, 2000)
                power = np.random.uniform(630, 670)

            data.append({
                'timestamp': timestamp,
                'gpu_id': gpu_id,
                'gpu_temp': temp,
                'sm_clock': clock,
                'power_draw': power,
                'throttle_reason': 'thermal' if temp > 80 else 'none'
            })

    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    print(f"Sample logs generated at: {output_path}")

if __name__ == "__main__":
    generate_logs("sample_dcgm_logs.csv")
