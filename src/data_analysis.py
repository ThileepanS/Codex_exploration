import argparse
import csv
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from statistics import mean


def load_data(path: str | Path) -> list[dict]:
    """Load dataset rows from CSV and cast numeric fields."""
    rows: list[dict] = []
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(
                {
                    "order_id": int(row["order_id"]),
                    "order_date": datetime.strptime(row["order_date"], "%Y-%m-%d"),
                    "region": row["region"],
                    "category": row["category"],
                    "channel": row["channel"],
                    "units_sold": int(row["units_sold"]),
                    "unit_price": float(row["unit_price"]),
                    "discount_rate": float(row["discount_rate"]),
                    "revenue": float(row["revenue"]),
                    "profit": float(row["profit"]),
                }
            )
    return rows


def summarize_sales(rows: list[dict]) -> dict:
    total_orders = len({row["order_id"] for row in rows})
    total_revenue = sum(row["revenue"] for row in rows)
    total_profit = sum(row["profit"] for row in rows)
    avg_order_value = mean(row["revenue"] for row in rows) if rows else 0
    margin = (total_profit / total_revenue) * 100 if total_revenue else 0

    return {
        "total_orders": total_orders,
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "avg_order_value": round(avg_order_value, 2),
        "profit_margin_pct": round(margin, 2),
    }


def aggregate_metric(rows: list[dict], key: str, metric: str) -> list[tuple[str, float]]:
    grouped = defaultdict(float)
    for row in rows:
        grouped[row[key]] += row[metric]
    return sorted(grouped.items(), key=lambda x: x[1], reverse=True)


def monthly_performance(rows: list[dict]) -> list[tuple[str, float, float]]:
    grouped: dict[str, dict[str, float]] = defaultdict(lambda: {"revenue": 0.0, "profit": 0.0})
    for row in rows:
        month = row["order_date"].strftime("%Y-%m")
        grouped[month]["revenue"] += row["revenue"]
        grouped[month]["profit"] += row["profit"]
    return [
        (month, round(values["revenue"], 2), round(values["profit"], 2))
        for month, values in sorted(grouped.items())
    ]


def markdown_table(headers: list[str], data: list[tuple]) -> str:
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body_rows = ["| " + " | ".join(str(item) for item in row) + " |" for row in data]
    return "\n".join([header, separator] + body_rows)


def write_csv(path: Path, headers: list[str], rows: list[tuple]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)


def generate_report(rows: list[dict], report_path: Path, exports_dir: Path) -> None:
    exports_dir.mkdir(parents=True, exist_ok=True)

    kpis = summarize_sales(rows)
    by_region_raw = aggregate_metric(rows, "region", "revenue")
    by_category_raw = aggregate_metric(rows, "category", "profit")
    by_channel_raw = aggregate_metric(rows, "channel", "revenue")
    by_month_raw = monthly_performance(rows)

    write_csv(exports_dir / "revenue_by_region.csv", ["region", "revenue"], by_region_raw)
    write_csv(exports_dir / "profit_by_category.csv", ["category", "profit"], by_category_raw)
    write_csv(exports_dir / "monthly_performance.csv", ["month", "revenue", "profit"], by_month_raw)

    by_region = [(region, f"${value:,.2f}") for region, value in by_region_raw]
    by_category = [(category, f"${value:,.2f}") for category, value in by_category_raw]
    by_channel = [(channel, f"${value:,.2f}") for channel, value in by_channel_raw]
    by_month = [(month, f"${revenue:,.2f}", f"${profit:,.2f}") for month, revenue, profit in by_month_raw]

    lines = [
        "# Sales Performance Summary",
        "",
        "## KPIs",
        "",
        f"- Total orders: **{kpis['total_orders']}**",
        f"- Total revenue: **${kpis['total_revenue']:,.2f}**",
        f"- Total profit: **${kpis['total_profit']:,.2f}**",
        f"- Average order value: **${kpis['avg_order_value']:,.2f}**",
        f"- Profit margin: **{kpis['profit_margin_pct']}%**",
        "",
        "## Revenue by Region",
        "",
        markdown_table(["Region", "Revenue"], by_region),
        "",
        "## Profit by Category",
        "",
        markdown_table(["Category", "Profit"], by_category),
        "",
        "## Revenue by Channel",
        "",
        markdown_table(["Channel", "Revenue"], by_channel),
        "",
        "## Monthly Revenue and Profit",
        "",
        markdown_table(["Month", "Revenue", "Profit"], by_month),
        "",
        "## Data Exports",
        "",
        "- `reports/revenue_by_region.csv`",
        "- `reports/profit_by_category.csv`",
        "- `reports/monthly_performance.csv`",
    ]

    report_path.write_text("\n".join(lines), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a sales analysis report from CSV data.")
    parser.add_argument("--input", default="data/sample_sales_data.csv", help="Path to input CSV file")
    parser.add_argument("--report", default="reports/summary_report.md", help="Path to output markdown report")
    parser.add_argument("--exports-dir", default="reports", help="Directory for CSV exports")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    base_dir = Path(__file__).resolve().parents[1]

    data_path = (base_dir / args.input).resolve()
    report_path = (base_dir / args.report).resolve()
    exports_dir = (base_dir / args.exports_dir).resolve()

    rows = load_data(data_path)
    generate_report(rows, report_path, exports_dir)
    print(f"Report generated at {report_path}")


if __name__ == "__main__":
    main()
