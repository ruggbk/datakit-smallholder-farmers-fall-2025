# Data Change Log

This file records any change made to original or canonical data files used for analysis. Each entry should be appended (newest at top) and include at minimum:

- timestamp (UTC preferred)
- author
- script/notebook or manual edit
- original file path(s)
- description of change
- rows before / rows after (if applicable)
- reason for change
- link to commit hash (if available)

Example entry:

- 2025-11-07 14:35Z | author: Jane Doe | script: `challenge_1/weather_preproc.py` | file: `data/raw/questions.parquet` | change: filtered duplicates; standardized timezone; dropped rows with missing id | rows_before: 7600321 | rows_after: 7598420 | reason: remove corrupted rows | git: abc1234

Guidelines:
- Prefer using `logs/log_writer.py` to append entries to ensure consistent formatting.
- If a change is reversible, note the backup location (e.g., `data/raw/questions.parquet.bak.20251107`).
- Keep entries concise but precise so someone can reproduce the change.

---

## Sanitization / Column Removal
- **2025-12-04 11:15Z** | author: Omar Bensatal | notebook: `challenge_1_omar_bensatal_final.ipynb` (Section 2.16) | source: `E://datakind_project//datakind_dataset.csv` → `E://datakind_project//datakind_dataset_cleaned.csv` | change: dropped high-null or PII-risk columns (`response_user_dob`, `question_user_dob`, `response_user_gender`, `question_user_gender`, `question_user_status`, `response_user_status`, `question_user_type`, `response_user_type`, `question_sent_dt`, `response_user_created_at`, `question_user_created_at`) to produce a sanitized working copy | rows_before: 20,304,843 | rows_after: 20,304,843 | reason: remove sensitive/unreliable fields prior to sharing downstream views | git: pending

## Derived Outputs / Exports
- **2025-12-04 11:05Z** | author: Omar Bensatal | notebook: `challenge_1_omar_bensatal_final.ipynb` (Section 2.13) | file: `challenge_1/top_power_users.csv` | change: exported top 20 askers and answerers (count summary only) for manual validation; no edits to raw dataset | rows_before: n/a | rows_after: 40 summary rows | reason: support community-leader review | git: b089688 (branch `bnesatal_omar`)
- **2025-11-08 10:00Z** | author: Omar Bensatal | script: `challenge_1_omar_bensatal.ipynb` | file: `challenge_1/top_power_users.csv` | change: initial export of top askers/answerers derived from EDA (no modifications to original raw data) | rows_before: - | rows_after: unknown | reason: derived artifact for manual review | git: b089688 | pushed_to: https://github.com/amrouvitch/datakit-smallholder-farmers-fall-2025.git | branch: bnesatal_omar | pr: pending

## Legacy / Reference Entries
- *(none yet — add older or superseded changes here for traceability if needed.)*

