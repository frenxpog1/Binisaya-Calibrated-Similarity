"""Compare rankings on a shared set of adjudicated medicine-name pairs.

Usage: python3 evaluate_rankings.py pairs.csv --k 25 50 100
CSV header: pair_id,label,baseline,corrected
Use one unique ID per pair and final binary labels (1 = LASA, 0 = non-LASA).
Higher scores rank first. Input must already reflect the chosen label policy.
"""

import argparse
import csv
import json
import math
from collections import defaultdict


def metrics(rows, column, budgets):
    groups = defaultdict(list)
    for row in rows:
        groups[row[column]].append(row["label"])
    positives = sum(row["label"] for row in rows)
    seen = hits = 0
    ap = 0.0
    at_k = {k: 0.0 for k in budgets if k <= len(rows)}
    for score in sorted(groups, reverse=True):
        labels = groups[score]
        size, relevant = len(labels), sum(labels)
        for k in at_k:
            slots = max(0, min(size, k - seen))
            at_k[k] += slots * relevant / size / k
        seen += size
        hits += relevant
        if positives:
            ap += (relevant / positives) * (hits / seen)
    return {"average_precision": ap if positives else None,
            "precision_at": {k: at_k.get(k) for k in budgets}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file")
    parser.add_argument("--k", type=int, nargs="+", default=[25, 50, 100])
    args = parser.parse_args()
    if min(args.k) < 1:
        parser.error("Review budgets must be positive.")
    rows, ids = [], set()
    try:
        with open(args.csv_file, newline="", encoding="utf-8-sig") as handle:
            reader = csv.DictReader(handle)
            fields = {"pair_id", "label", "baseline", "corrected"}
            if not fields.issubset(reader.fieldnames or []):
                parser.error("Required columns: pair_id,label,baseline,corrected")
            for row in reader:
                pair_id = (row["pair_id"] or "").strip()
                if not pair_id or pair_id in ids or row["label"] not in ("0", "1"):
                    parser.error(f"Line {reader.line_num}: invalid ID, duplicate ID or nonbinary label.")
                ids.add(pair_id)
                scores = {}
                for key in ("baseline", "corrected"):
                    try:
                        scores[key] = float(row[key])
                    except (TypeError, ValueError):
                        parser.error(f"Line {reader.line_num}: invalid {key} score.")
                    if not math.isfinite(scores[key]):
                        parser.error(f"Line {reader.line_num}: nonfinite {key} score.")
                rows.append(dict(scores, label=int(row["label"])))
    except (OSError, csv.Error, UnicodeError) as error:
        parser.error(str(error))
    if not rows:
        parser.error("No evaluated pairs.")
    print(json.dumps({"pairs": len(rows),
                      "prevalence": sum(r["label"] for r in rows) / len(rows),
                      **{key: metrics(rows, key, args.k) for key in ("baseline", "corrected")}},
                     indent=2))


if __name__ == "__main__":
    main()
