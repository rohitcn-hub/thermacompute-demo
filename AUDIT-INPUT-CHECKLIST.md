# ThermaCompute AI: $80 GPU Efficiency Audit

Understand what your hardware telemetry supports before buying more capacity or changing production settings.

## Start without sharing your logs

Email **vivaan.thermacompute@gmail.com** with the subject **GPU audit enquiry** and:

- GPU model and approximate count.
- Whether you own the hardware or rent it.
- The question you want answered: temperature, reported throttling, power usage, or electricity cost.
- Your available CSV column names and observation period. Send column headers first; do not attach private data at this stage.

We confirm data suitability, deliverables, delivery timing and the agreed transfer method before payment. The audit price is **$80**. A future subscription is separate and optional.

## What you receive

- A review of temperature, power and reported throttling where those fields are available.
- GPU-level findings and prioritized checks for your engineers.
- Electricity-cost estimates where timestamps, power coverage and your tariff support them.
- A PDF documenting evidence, assumptions, missing measurements and recommended next steps.

Hardware telemetry alone cannot prove lost tokens, recoverable revenue or application performance gains. Those require workload measurements and controlled comparisons. Estimates are not guaranteed savings.

## Prepare hardware telemetry safely

Retain timestamps with timezone, stable anonymized GPU IDs, units and sampling interval. Useful fields include GPU model, temperature in degrees Celsius, power in watts, throttle reason, and measured throttle duration with its unit. Clock measurements are optional. Tell us whether duration fields are interval measurements or cumulative counters.

Do not fabricate absent metrics or replace missing clocks with zero. Tell us about gaps, restarts, duplicates and changes in sampling frequency. We will agree on a compatible schema before ingestion; arbitrary DCGM exports may require mapping.

Remove hostnames, customer identifiers and workload metadata you do not want shared. Do not send passwords, API keys, SSH credentials, model weights, prompts, training data or customer records. Never post customer telemetry in a public GitHub issue.

The audit reviews your exported file and makes no changes to your servers. Sharing a CSV for review is a data transfer; this is not an air-gapped deployment. Confirm the transfer, access and deletion arrangements with us before sending it. Submitted logs and reports are not for public marketing or redistribution.

## Try the free example first

Read [GPU efficiency explained](GPU-EFFICIENCY-EXPLAINED.md): a reproducible fictional example showing why lower watts can still mean higher energy per token. The numbers are educational, not customer results.

## What is still in development

Thermal-aware scheduling, GPU power and clock policies, and inference configuration benchmarking are planned capabilities. They are not included as production control in this passive audit. No subscription purchase is required to order the audit.

**Next step:** email [vivaan.thermacompute@gmail.com](mailto:vivaan.thermacompute@gmail.com?subject=GPU%20audit%20enquiry) with your GPU model, count and CSV column names. No discovery call required.
