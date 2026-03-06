# Data Analyst Project: Sales Performance Analysis

This repository is a portfolio-ready **data analyst project** with a realistic sample dataset and a reusable analysis workflow.

## What You Can Show in Interviews

- Data cleaning/type-casting from raw CSV
- KPI computation (revenue, profit, margin, average order value)
- Dimensional analysis by region/category/channel
- Monthly trend analysis
- Exporting transformed datasets for dashboard tools (Power BI/Tableau)
- Basic automated tests for data workflow reliability

## Project Structure

- `data/sample_sales_data.csv` — synthetic sales transactions dataset (120 records).
- `src/data_analysis.py` — analysis CLI script.
- `reports/summary_report.md` — generated Markdown business report.
- `reports/revenue_by_region.csv` — generated export for downstream visuals.
- `reports/profit_by_category.csv` — generated export for downstream visuals.
- `reports/monthly_performance.csv` — generated monthly trend dataset.
- `tests/test_data_analysis.py` — unit tests for core analysis logic.
- `requirements.txt` — no third-party dependencies required.

## Dataset Columns

- `order_id`
- `order_date`
- `region`
- `category`
- `channel`
- `units_sold`
- `unit_price`
- `discount_rate`
- `revenue`
- `profit`

## Run Analysis

```bash
python src/data_analysis.py
```

### Optional CLI parameters

```bash
python src/data_analysis.py \
  --input data/sample_sales_data.csv \
  --report reports/summary_report.md \
  --exports-dir reports
```

## Run Tests

```bash
python -m unittest discover -s tests
```

## Ideas for Extension

- Add SQL-based analysis with SQLite and analytic queries
- Add visualization notebook (matplotlib/seaborn/plotly)
- Build a Power BI or Tableau dashboard from the CSV exports
- Add simple forecasting for next-quarter revenue and margin
