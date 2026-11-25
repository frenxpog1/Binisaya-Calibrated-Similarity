"""Hand-calculated example for the paired ranking evaluator.

Run from the repository root with python3 -m unittest discover -s tests.
"""
import unittest

from evaluate_rankings import metrics


class WorkedRankingExample(unittest.TestCase):
    def test_tied_cutoff_and_average_precision(self):
        rows = [
            {"label": 1, "baseline": 0.9, "corrected": 0.9},
            {"label": 0, "baseline": 0.7, "corrected": 0.6},
            {"label": 1, "baseline": 0.7, "corrected": 0.8},
            {"label": 0, "baseline": 0.1, "corrected": 0.1},
        ]
        # At k=2, one positive is certain. The second slot has a 1/2
        # chance of being positive, giving expected precision 1.5/2.
        baseline = metrics(rows, "baseline", [1, 2, 4, 5])
        self.assertEqual(baseline["precision_at"], {1: 1, 2: 0.75, 4: 0.5, 5: None})
        # Each positive contributes 1/2 of recall. Precision at its
        # score threshold is 1 for the first and 2/3 for the second.
        self.assertAlmostEqual(baseline["average_precision"], 0.5 * (1 + 2 / 3))

        corrected = metrics(rows, "corrected", [1, 2, 4, 5])
        self.assertEqual(corrected["precision_at"], {1: 1, 2: 1, 4: 0.5, 5: None})
        self.assertEqual(corrected["average_precision"], 1)
