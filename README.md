# UK ISA allowance

PolicyEngine analysis of how people use the £20,000 Individual Savings Account (ISA) allowance, and whom a £12,000 cash ISA limit would bind.

## Questions

1. How many people pay the full allowance into cash ISAs, stocks and shares ISAs, or both?
2. What salary would a single person need to pay in the full allowance?
3. What share of the adult population pays in the full allowance?
4. How many people would a £12,000 annual cash ISA limit bind from April 2027?

## Data

- HMRC, [Individual Savings Account (ISA) tables, September 2026](https://www.gov.uk/government/statistics/annual-savings-statistics-2026). These count individuals subscribing in the 2023-24 tax year, by income, size of subscription and ISA type (Table 9.7), by age and type (Table 9.8), and by region (Tables 9.9 and 9.12). Crown copyright; information may be used provided that the source is acknowledged.
- HMRC, [Cash ISA limit reduction: tax information and impact note](https://www.gov.uk/government/publications/reduction-in-the-cash-individual-savings-account-isa-limit/cash-individual-savings-account-isa-limit-reduction), 17 September 2026.
- The [PolicyEngine UK](https://github.com/PolicyEngine/policyengine-uk) household calculator, for income tax and National Insurance on a given salary.

This repository uses only published HMRC statistics and the household calculator. It holds no survey microdata.

## Method

The method from HMRC's tables, and what they can't show, is set out in the repository's first issue.

PolicyEngine's population model can't answer these questions yet. Its data holds ISA balances, not what people pay in each year, and the model has no ISA subscription limits.

## Running

```bash
uv run python scripts/hmrc_isa_tables.py
```

```bash
uv run python scripts/salary_floor.py --year 2026 --spending 15000
```

`hmrc_isa_tables.py` downloads HMRC's tables to `data/` and checks them against a pinned SHA-256 before reading any cell. `salary_floor.py` finds the smallest salary that leaves the allowance (plus any yearly spending) after income tax and employee National Insurance, outside Scotland and in Scotland.

## Status

Draft. The figures are under review and not yet published here.
