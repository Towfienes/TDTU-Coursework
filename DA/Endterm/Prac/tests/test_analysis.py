"""Boundary checks beyond the real-data assertions embedded in the notebook."""
import contextlib
import io
import unittest

import numpy as np
import pandas as pd

from src.analysis import BANDS, comprehensive_report, normalize_within_group, performance_bands


class AnalysisTests(unittest.TestCase):
    def test_band_boundaries_and_invalid_values(self):
        values = pd.Series([0, 9, 10, 14, 15, 20])
        self.assertEqual(performance_bands(values).tolist(), [BANDS[0]] * 2 + [BANDS[1]] * 2 + [BANDS[2]] * 2)
        for invalid in [pd.Series([-1]), pd.Series([21]), pd.Series([np.nan])]:
            with self.assertRaises(ValueError):
                performance_bands(invalid)

    def test_group_alignment_and_constant_groups(self):
        frame = pd.DataFrame({"school": ["A", "B", "A", "B", "C"], "G3": [10, 4, 20, 4, 7]}, index=[8, 2, 9, 1, 20])
        result = normalize_within_group(frame)
        pd.testing.assert_series_equal(result, pd.Series([0., 0., 1., 0., 0.], index=frame.index, name="G3"))
        self.assertTrue(np.isfinite(result).all())
        with self.assertRaises(ValueError):
            normalize_within_group(pd.DataFrame({"school": ["A"], "G3": [np.inf]}))

    def test_summary_empty_and_zero_count_categories(self):
        for values in [[], [10, 14]]:
            frame = pd.DataFrame({name: values for name in ["G1", "G2", "G3"]})
            frame["performance_band"] = performance_bands(frame["G3"])
            with contextlib.redirect_stdout(io.StringIO()):
                summary = comprehensive_report(frame)
            distribution = summary["performance_distribution"]
            self.assertEqual(sum(x["count"] for x in distribution.values()), len(values))
            self.assertAlmostEqual(sum(x["percent"] for x in distribution.values()), 100.0 if values else 0.0)
            self.assertEqual(distribution[BANDS[2]]["count"], 0)


if __name__ == "__main__":
    unittest.main()
