"""Who pays in the full ISA allowance, and who pays more than £12,000 into cash.

Reads HMRC's Individual Savings Account tables (September 2026), which count
individuals subscribing in the 2023-24 tax year. The download is checked
against a pinned SHA-256 before any cell is read.

Usage::

    uv run python scripts/hmrc_isa_tables.py
"""

from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path

import pandas as pd

URL = (
    "https://assets.publishing.service.gov.uk/media/6aa26b174e17456e2cdf529c/"
    "Individual_Savings_Account_Tables_2026.ods"
)
SHA256 = "a0eaf90801fadc293c1187e8bcd66983b37a0fe81028d9a04b3e6dd71bd10e3b"
PATH = Path(__file__).resolve().parents[1] / "data" / "Individual_Savings_Account_Tables_2026.ods"

# Table 9.7 subscription bands above £12,000. The bands break at £12,000, so
# these columns are exactly the subscribers who paid in more than £12,000.
ABOVE_12K = [
    "£12,001-£14,000",
    "£14,001-£16,000",
    "£16,001-£18,000",
    "£18,001-£19,999",
    "£20,000",
]
FULL = "£20,000"
# Table 9.8 age bands from 66 up. HMRC's 63-65 band includes 65-year-olds,
# so "under 66" is the closest cut to the under-65 rule the tables allow.
AGE_66_PLUS = ["66-68", "69-71", "72-74", "75-77", "78-80", "81 and over"]


def fetch() -> Path:
    if not PATH.exists():
        PATH.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(URL, PATH)
    digest = hashlib.sha256(PATH.read_bytes()).hexdigest()
    if digest != SHA256:
        raise ValueError(f"{PATH} has SHA-256 {digest}, expected {SHA256}")
    return PATH


def subscription_blocks(sheet: pd.DataFrame) -> dict[str, dict[str, dict[str, float]]]:
    """Table 9.7's four blocks (all, cash only, stocks and shares only, both),
    each mapping income band to subscription band to individuals.

    The column headings say "(thousands)" but the cells are counts of people:
    only that reading matches HMRC's commentary (13.05 million subscribers).
    """
    blocks: dict[str, dict[str, dict[str, float]]] = {}
    name = header = None
    for _, row in sheet.iterrows():
        label = row.iloc[0]
        if isinstance(label, str) and label.startswith("Range of Income of "):
            name = label.removeprefix("Range of Income of ").split(" Subscribers")[0].strip()
            header = [str(h).split("\n")[0] for h in row.iloc[1:]]
            blocks[name] = {}
        elif name and isinstance(label, str) and pd.notna(row.iloc[1]):
            blocks[name][label.strip()] = dict(zip(header, map(float, row.iloc[1:])))
    return blocks


def adult_population(sheet: pd.DataFrame) -> float:
    """UK adults aged 18 or over implied by Table 9.12's UK holders and their
    share of the adult population (ONS estimates, rounded to 0.1 points)."""
    header = sheet.iloc[8].tolist()
    uk = dict(zip(header, sheet[sheet.iloc[:, 0] == "K02000001"].iloc[0].tolist()))
    holders = float(next(v for k, v in uk.items() if str(k).startswith("Total")))
    share = float(uk["Percentage of All Adults (%)"])
    return holders / share


def main() -> None:
    sheets = pd.read_excel(fetch(), sheet_name=None, header=None, engine="odf")
    blocks = subscription_blocks(sheets["9_7_ISA_subs_by_income"])
    adults = adult_population(sheets["9_12ISA_market_values_by_region"])
    print(f"UK adults aged 18+ implied by Table 9.12: {adults / 1e6:.1f}m\n")

    for group, rows in blocks.items():
        total = rows["All ranges"]
        subscribers = total["All Subscriptions"]
        full = total[FULL]
        above = sum(total[band] for band in ABOVE_12K)
        print(
            f"{group}: {subscribers:,.0f} subscribers; "
            f"{full:,.0f} paid in £20,000 ({full / subscribers:.1%} of them, "
            f"{full / adults:.1%} of adults); "
            f"{above:,.0f} paid in more than £12,000 ({above / subscribers:.1%})"
        )

    print("\nPeople paying in the full £20,000, by income band (all ISA types):")
    everyone = blocks["All ISA"]
    full_total = everyone["All ranges"][FULL]
    cumulative = 0.0
    for band, row in everyone.items():
        if band == "All ranges":
            continue
        cumulative += row[FULL]
        print(
            f"  {band}: {row[FULL]:,.0f} ({row[FULL] / row['All Subscriptions']:.1%} of the "
            f"band's subscribers; cumulative {cumulative / full_total:.1%} of all full payers)"
        )

    ages = sheets["9_8_ISA_subs_by_age_sex"]
    ages = ages[ages.iloc[:, 1].apply(lambda v: isinstance(v, (int, float)) and pd.notna(v))]
    ages = ages.set_index(0)
    # The person-level rows (no sex prefix) follow the male and female blocks.
    persons = ages.loc[[i for i in ages.index if not str(i).startswith(("Male", "Female"))]]
    cash_only, both = persons.iloc[:, 0].astype(float), persons.iloc[:, 2].astype(float)
    under_66 = [i for i in persons.index if i not in AGE_66_PLUS and i != "Total"]
    any_cash = cash_only[under_66].sum() + both[under_66].sum()
    print(f"\nPeople under 66 paying into a cash ISA (cash only or both): {any_cash:,.0f}")


if __name__ == "__main__":
    main()
