import pandas as pd
import numpy as np
from datetime import datetime

def analyze_dcgm(file_path: str) -> dict:
    """
    Analyzes DCGM logs to identify thermal throttling and calculate financial waste.

    Args:
        file_path (str): Path to the CSV log file.

    Returns:
        dict: A structured dictionary containing summary metrics and per-GPU records.
    """
    df = pd.read_csv(file_path)

    # Ensure timestamp is datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Identify throttling events
    # Throttling: sm_clock < 1400 MHz while gpu_temp > 80.0°C
    df['is_throttled'] = (df['sm_clock'] < 1400) & (df['gpu_temp'] > 80.0)

    # Calculate total cluster runtime hours
    # Time range per GPU
    time_diff = df.groupby('gpu_id')['timestamp'].agg(['min', 'max'])
    total_duration_per_gpu = (time_diff['max'] - time_diff['min']).dt.total_seconds() / 3600
    total_cluster_hours = total_duration_per_gpu.sum()

    # Calculate throttled GPU-hours
    # Assuming each row is a 10s interval as per requirements
    # We can count rows where is_throttled is True and divide by (3600/10)
    throttled_rows = df['is_throttled'].sum()
    throttled_hours = throttled_rows * (10 / 3600)

    # Total hours for the cluster (sum of durations of all GPUs)
    # This is total_cluster_hours calculated above

    # Throughput loss percentage
    throughput_loss_pct = (throttled_hours / total_cluster_hours * 100) if total_cluster_hours > 0 else 0

    # Financial waste: $2.50 / GPU / hour
    cost_per_hour = 2.50
    total_financial_waste = throttled_hours * cost_per_hour

    # Per-GPU breakdown
    gpu_ids = df['gpu_id'].unique()
    gpu_records = []

    for gpu_id in gpu_ids:
        gpu_df = df[df['gpu_id'] == gpu_id]
        throttled_gpu_df = gpu_df[gpu_df['is_throttled']]

        max_temp = gpu_df['gpu_temp'].max()
        avg_throttled_clock = throttled_gpu_df['sm_clock'].mean() if not throttled_gpu_df.empty else np.nan

        # Individual GPU throttled hours
        gpu_throttled_rows = throttled_gpu_df.shape[0]
        gpu_throttled_hours = gpu_throttled_rows * (10 / 3600)
        gpu_dollar_loss = gpu_throttled_hours * cost_per_hour

        gpu_records.append({
            'gpu_id': int(gpu_id),
            'max_temp': float(max_temp),
            'avg_throttled_clock': float(avg_throttled_clock) if not np.isnan(avg_throttled_clock) else 0.0,
            'dollar_loss': float(gpu_dollar_loss),
            'throttled_hours': float(gpu_throttled_hours)
        })

    return {
        'summary': {
            'total_cluster_hours': float(total_cluster_hours),
            'total_throttled_hours': float(throttled_hours),
            'throughput_loss_pct': float(throughput_loss_pct),
            'total_financial_waste': float(total_financial_waste),
            'gpus_affected': len([g for g in gpu_records if g['throttled_hours'] > 0])
        },
        'gpu_details': gpu_records
    }
