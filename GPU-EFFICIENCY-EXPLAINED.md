# GPU watts are not GPU efficiency

ThermaCompute AI · Built by Vivaan · Educational, synthetic example

A configuration that draws less power can still use more energy per output token.

| Configuration | GPU watts | Output tokens/sec | P95 TTFT | Joules/output token |
|---|---:|---:|---:|---:|
| Baseline | 3,200 | 800 | 220 ms | 4.00 |
| Power saver | 2,800 | 600 | 240 ms | 4.67 |
| Throughput push | 3,400 | 1,100 | 310 ms | 3.09 |
| Balanced | 3,000 | 900 | 230 ms | 3.33 |

Assume a 250 ms P95 TTFT limit and equivalent traffic/output quality. Balanced improves energy per token in this fictional example. Throughput push fails the latency constraint. These values are invented for teaching; they are not measured GPU benchmarks or ThermaCompute results.

## Reproduce the comparison

```python
cases = [("baseline", 3200, 800, 220), ("power saver", 2800, 600, 240), ("throughput push", 3400, 1100, 310), ("balanced", 3000, 900, 230)]
for name, watts, tokens_per_second, p95_ttft in cases:
    print(name, round(watts / tokens_per_second, 3), "J/token", "latency pass" if p95_ttft <= 250 else "latency fail")
```

A real comparison requires repeated runs, equivalent model/precision/traffic, quality evaluation, inter-token latency constraints and consistent measurement windows. GPU board energy excludes other equipment and cooling.

## What the $80 audit provides

A scoped review of an exported hardware-metrics CSV: temperature, power and reported throttling, GPU-level findings, supported electricity-cost estimates, limitations and prioritized checks in a PDF. We confirm data suitability, deliverables and timing before payment. It does not include live GPU control or guaranteed savings.

Email **vivaan.thermacompute@gmail.com** with your GPU model/count and available metric names to request the checklist. Do not attach private logs initially or post them in public issues. We do not request SSH credentials, model weights, prompts or training data. Agree private transfer and retention terms before sharing an anonymized export.

Thermal-aware scheduling, power/clock tuning and automated performance testing are planned capabilities, separate from the current audit. Audit purchase does not commit you to subscribe.

Synthetic data can test software arithmetic, but it cannot prove production permission isolation or recoverable savings. Consult your collector's field semantics: https://docs.nvidia.com/datacenter/dcgm/latest/dcgm-api/dcgm-api-field-ids.html

Prepared with AI assistance. No customer or hardware vendor endorsement is implied.
