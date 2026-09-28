# Architecture and trust boundaries

Explicit local files -> bounded UTF-8 reader -> line signature rules -> evidence masking -> conservative timestamp ordering -> JSON / Markdown / escaped static HTML.

Rule matching is deterministic and independent of any language model. Rules are intentionally simple and readable. Output schema includes version, input_count, lines_scanned, ordering, status, counts, events and warnings. Each event includes source alias, line number, optional normalized timestamp, rule ID, title, masked excerpt and next check. Excerpts are capped at 2,000 characters; inputs are capped at 20 MiB total.

No file contents become executable code. HTML escapes all rendered report text. Source paths are replaced by input-N labels in reports; operators retain their input command privately to map aliases. The CLI's OS error messages may include local paths.

Known limits: number of output events is proportional to matched lines; large reports may be unwieldy. Redaction is not anonymization. Regexes may match quoted or negated statements. Timestamps on non-event lines are not inherited. Timestamp ordering does not establish causality. Naive/date-less timestamps remain unknown. No unique-incident grouping, cross-job correlation or performance claims.

Roadmap, conditional on real user evidence: multi-line traceback grouping; supported version-aware adapters; operator-supplied timestamp offsets; selected DCGM exports; recurring node associations. Each addition needs negative cases and documented schema coverage before release.
