"""Gross salary a single employee needs to keep a given amount after income tax
and National Insurance, from the PolicyEngine UK household calculator.

The default target is the £20,000 ISA allowance with no living costs, which is
a floor: add yearly spending to the target with --spending.

Usage::

    uv run python scripts/salary_floor.py --year 2026 --spending 15000
"""

from __future__ import annotations

import argparse

from policyengine_uk import Simulation

REGIONS = ["LONDON", "SCOTLAND"]


def after_tax(salaries: list[float], year: int, region: str) -> list[float]:
    """Salary less income tax and employee National Insurance."""
    situation = {
        "people": {
            f"p{i}": {"age": {year: 35}, "employment_income": {year: s}}
            for i, s in enumerate(salaries)
        },
        "benunits": {f"b{i}": {"members": [f"p{i}"]} for i in range(len(salaries))},
        "households": {
            f"h{i}": {"members": [f"p{i}"], "region": {year: region}} for i in range(len(salaries))
        },
    }
    sim = Simulation(situation=situation)
    tax = sim.calculate("income_tax", year) + sim.calculate("national_insurance", year)
    return [s - t for s, t in zip(salaries, tax)]


def salary_for(target: float, year: int, region: str) -> int:
    """Smallest whole-pound salary whose after-tax amount reaches the target.

    Narrows a £1 grid of 101 salaries per round, so each round is one
    simulation rather than one per salary.
    """
    low, high = 0.0, 250_000.0
    while high - low > 1:
        grid = [low + (high - low) * k / 100 for k in range(101)]
        values = after_tax(grid, year, region)
        above = next(k for k, v in enumerate(values) if v >= target)
        low, high = grid[max(above - 1, 0)], grid[above]
    for salary in range(int(low), int(high) + 2):
        if after_tax([float(salary)], year, region)[0] >= target:
            return salary
    raise RuntimeError("no salary found")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--year", type=int, default=2026)
    parser.add_argument("--allowance", type=float, default=20_000)
    parser.add_argument("--spending", type=float, default=0)
    args = parser.parse_args()
    target = args.allowance + args.spending
    for region in REGIONS:
        salary = salary_for(target, args.year, region)
        print(
            f"{args.year} {region.title()}: £{salary:,} keeps £{target:,.0f} after income tax and NI"
        )


if __name__ == "__main__":
    main()
