# ThermaCompute Incident Lens

**Evidence before assumptions.** Free, offline GPU-job log triage. Version 0.1.0 — experimental preview, not production-validated.

Incident Lens extracts supported failure signatures from existing text logs and produces a readable HTML report plus Markdown and JSON. No account, API key, GPU, third-party Python dependency or network connection is required to run it.

## Try the synthetic demonstration

Install Python 3.10 or newer, download this repository, then open a terminal in `incident-lens`:

```sh
python incident_lens.py examples/synthetic.log --out my-demo-report
```

Open `my-demo-report/report.html` in your browser. The example contains **invented events**, not measurements from a customer or a reproduced GPU failure. A committed [sample Markdown report](examples/sample-report/report.md) lets you inspect the output without running code.

To review your own selected files:

```sh
python incident_lens.py worker0.log worker1.log --out private-report
```

The output directory must not already exist. Inputs are never modified. Reports can contain sensitive information: review before sharing and keep them out of public repositories.

## What the report tells you

- Which of six supported error signatures occurred, with input number and line number.
- How often each signature occurred. These are line matches, not unique incidents.
- UTC event order only when every matched event has a full timezone-aware ISO timestamp. Otherwise the report preserves input order and warns that chronology is unavailable.
- A suggested next investigation step for each signature.
- Explicit limitations and an `insufficient_evidence` result for unrecognized input.

Supported signatures: CUDA allocation failure, kernel host OOM, NCCL collective timeout, Python missing module, NVIDIA Xid event, and worker/engine exit. Multiple signatures can match a line. A matching phrase is evidence that text was present, not proof an event occurred; quoted examples and negations can produce matches.

## What it cannot do yet

No root-cause inference, diagnosis confidence score, generic traceback parsing, multi-line context extraction, automatic fix, version-specific workaround, telemetry CSV import, persistent fleet history, hardware certification or GPU control. It does not calculate lost revenue, recoverable GPU-hours or savings. It cannot verify that clocks are synchronized or logs complete. It does not collapse duplicate tracebacks; counts group signature occurrences while retaining evidence lines.

This preview is tested on synthetic fixtures only. Real sanitized incident validation remains outstanding. Do not use it to decide hardware replacement or production changes without independent investigation.

## Privacy and operating boundaries

Python standard library only. No subprocesses, external AI service, telemetry, shell execution or network requests. It reads only file paths you supply and writes to a new directory you choose. Combined input limit: 20 MiB; UTF-8 text only. Common labelled credentials, bearer strings and emails receive best-effort masking. Hostnames, paths, unlabeled credentials and proprietary text can remain. HTML escapes log text and disables scripts and external resources. Markdown should still be reviewed in a trusted viewer.

Use a non-privileged account and a private output directory. This tool does not need production SSH or root. A local run is not a security certification.

## Development

From this directory:

```sh
python -m unittest discover -s tests -v
```

Files: `incident_lens.py` (CLI/parser/renderers), `tests/test_lens.py` (regression tests), `examples/` (synthetic fixture and reports), `SECURITY.md`, `CONTRIBUTING.md`, `ARCHITECTURE.md`, `CHANGELOG.md`, `LICENSE`.

## Why this exists

Engineers often need to locate a relevant error among repeated failure messages. This utility is a small starting point for that task; it is not a replacement for DCGM, PyTorch Flight Recorder or vLLM diagnostics.

References for investigation, not automatic authoritative mappings:
- [PyTorch Flight Recorder](https://pytorch.org/blog/flight-recorder-a-new-lens-for-understanding-nccl-watchdog-timeouts/)
- [NVIDIA Xid documentation](https://docs.nvidia.com/deploy/xid-errors/index.html)
- [vLLM troubleshooting](https://docs.vllm.ai/en/latest/usage/troubleshooting/)
- [NVIDIA DCGM diagnostics](https://docs.nvidia.com/datacenter/dcgm/latest/user-guide/dcgm-diagnostics.html)

## Free means useful without payment

This directory is MIT licensed. No audit purchase is required. ThermaCompute's separate $80 telemetry audit is described in the repository's [audit checklist](../AUDIT-INPUT-CHECKLIST.md). Fleet subscriptions and automated optimization remain future work, not functionality provided by this release.

Built by Vivaan with AI coding assistance. Contact: vivaan.thermacompute@gmail.com. Please send only a description initially; do not email private logs without agreed handling arrangements.
