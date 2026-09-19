# ThermaCompute AI - Trust Sandbox Telemetry Generator

This repository contains a high-fidelity synthetic data generator used to validate the **ThermaCompute AI** extraction process. The goal is to prove that our audit engine strictly adheres to hardware-metric isolation and does not ingest proprietary workload data.

## Overview

`mock_dcgm_telemetry.py` simulates NVIDIA DCGM (Data Center GPU Manager) logs for large-scale clusters. It produces synthetic telemetry including power consumption, thermal metrics, and clock throttling events.

## Installation & Usage

The script is designed for maximum portability and has **zero external dependencies**. It utilizes only the Python standard library.

### Execution

Run the script using Python 3.x:

```bash
python mock_dcgm_telemetry.py --gpu-count 512 --gpu-type H100 --hours 24
```

### CLI Arguments

| Argument | Description | Options | Default |
| :--- | :--- | :--- | :--- |
| `--gpu-count` | Total number of GPUs in the simulated cluster | Integer | `512` |
| `--gpu-type` | Target GPU architecture for power profiling | `H100`, `B200` | `H100` |
| `--hours` | Simulation time window | Integer | `24` |

### Output Specification

The script generates a file named `synthetic_dcgm_logs.csv` with the following schema:

- `timestamp`: ISO 8601 formatted UTC time.
- `gpu_id`: Unique identifier for the GPU instance.
- `gpu_type`: The architecture simulated (H100/B200).
- `power_draw_w`: Instantaneous power draw in Watts.
- `temp_c`: Core temperature in Celsius.
- `throttle_duration_ms`: Duration of thermal throttling in milliseconds (triggered when `temp_c` > 85°C).

## Why We Built This

At ThermaCompute AI, we operate on a **Zero-Trust, Privacy-First Architecture**. 

Data center founders are understandably protective of their proprietary workloads. To earn trust, we provide a "Trust Sandbox" where clients can run our extraction engine against synthetic data. This proves that our pipeline is architecturally incapable of reading memory dumps, process lists, or network packets—extracting only the telemetry required for thermal optimization.

**Privacy Guarantee:**
- No PII (Personally Identifiable Information)
- No Workload Metadata
- No Client IP addresses
- No Security Credentials
