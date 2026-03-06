from pathlib import Path
import tempfile
import unittest

from src.data_analysis import generate_report, load_data, summarize_sales


class DataAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.base_dir = Path(__file__).resolve().parents[1]
        self.data_path = self.base_dir / "data" / "sample_sales_data.csv"
        self.rows = load_data(self.data_path)

    def test_load_data_has_expected_shape(self) -> None:
        self.assertEqual(len(self.rows), 120)
        self.assertIn("revenue", self.rows[0])

    def test_kpis_are_positive(self) -> None:
        kpis = summarize_sales(self.rows)
        self.assertGreater(kpis["total_revenue"], 0)
        self.assertGreater(kpis["total_profit"], 0)
        self.assertGreaterEqual(kpis["profit_margin_pct"], 0)

    def test_generate_report_creates_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            report = tmp_path / "summary_report.md"
            generate_report(self.rows, report, tmp_path)

            self.assertTrue(report.exists())
            self.assertTrue((tmp_path / "monthly_performance.csv").exists())
            self.assertTrue((tmp_path / "revenue_by_region.csv").exists())
            self.assertTrue((tmp_path / "profit_by_category.csv").exists())


if __name__ == "__main__":
    unittest.main()
