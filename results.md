# Who pays in the full ISA allowance, and whom a £12,000 cash limit would bind

Figures for the 2023-24 tax year from HMRC's ISA statistics, and for 2026-27 from the PolicyEngine UK household calculator. The method is in [issue #1](https://github.com/PolicyEngine/uk-isa-allowance/issues/1), and `scripts/hmrc_isa_tables.py` and `scripts/salary_floor.py` reproduce every figure.

## Sources

- **HMRC, [Individual Savings Account (ISA) tables, September 2026](https://www.gov.uk/government/statistics/annual-savings-statistics-2026)** (released 16 September 2026; Tables 9.7, 9.8 and 9.12).
  - They count individuals in the 2023-24 tax year, from ISA managers' returns matched to HMRC's Survey of Personal Incomes.
  - Innovative Finance ISAs are excluded.
  - The column headings say "(thousands)", but the cells are counts of people.
- **HMRC, [Cash ISA limit reduction: tax information and impact note](https://www.gov.uk/government/publications/reduction-in-the-cash-individual-savings-account-isa-limit/cash-individual-savings-account-isa-limit-reduction)** (17 September 2026).
- **The [PolicyEngine UK](https://github.com/PolicyEngine/policyengine-uk) household calculator** (policyengine-uk 2.151.0), with 2026-27 rules.

## 1. How many people pay in the full £20,000

In 2023-24, **3.76 million people paid the full £20,000 into ISAs**. That is 28.8% of the 13.05 million people who paid into an ISA that year.

The £20,000 is one allowance across all ISA types. By the types each person paid into that year:

- **Cash ISAs only:** 2.59 million, 28.9% of 8.96 million cash-only subscribers.
- **Stocks and shares ISAs only:** 0.89 million, 28.5% of 3.12 million.
- **Both:** 0.28 million, 28.9% of 0.98 million. For this group the £20,000 is the combined total.

The share paying in the full allowance rises with income:
- 22.8% of subscribers with incomes up to £12,570;
- 28.2% at £40,001 to £50,270;
- 45.3% at £125,141 to £150,000;
- 62.5% above £150,000.

## 2. What share of the population does this

HMRC's Table 9.12 puts the 23.0 million ISA holders at 41.7% of UK adults aged 18 or over. That implies an adult population of about 55.2 million, from ONS estimates. On that base:

- **6.8% of UK adults paid in the full £20,000 in 2023-24.**
  - 4.7% through cash ISAs only;
  - 1.6% through stocks and shares ISAs only;
  - 0.5% across both.
- 23.6% of adults paid something into an ISA that year.
- 41.7% hold an ISA.

## 3. The salary needed to pay in £20,000

A single employee in 2026-27 keeps £20,000 after income tax and National Insurance on a gross salary of:

- **£22,890** outside Scotland;
- **£22,835** in Scotland.

At that salary all of their take-home pay would go into the ISA, so this is a floor, not a realistic minimum:

- **Living costs raise it.** Each £1 of yearly spending adds about £1.39 of gross salary in the basic-rate band, and about £1.72 in the higher-rate band, outside Scotland. Someone spending £15,000 a year needs £43,723 to save £20,000 as well (£43,953 in Scotland).
- **Other deductions raise it too.** The figures assume no pension contributions or student loan repayments.
- **Income alone doesn't decide who pays in the full allowance.**
  - 44% of those who did in 2023-24 had incomes of £30,000 or less.
  - 11% (411,000 people) had incomes of £12,570 or less.
  - Many pay in from existing savings, gifts or inheritances, or move money from other accounts.

## 4. A £12,000 cash limit

The Individual Savings Account (Amendment) (No. 2) Regulations 2026 (SI 2026/1018) set a £12,000 cash ISA limit from 6 April 2027. It would have applied to people aged 64 or under at the end of the tax year; the overall limit was to stay at £20,000. In the Budget speech on 28 October 2026 the Chancellor announced that the cut will not go ahead and the cash allowance stays at £20,000 ([BBC live, 13:03](https://www.bbc.co.uk/news/live/cq62y5xnm8dzt)).

The figures below show whom a £12,000 limit would bind if it were brought in.

- **Under-65s.** HMRC's impact note says 22% of cash ISA subscribers under 65 paid in more than £12,000 in 2022-23.
- **All ages, 2023-24.**
  - 3.46 million cash-only subscribers paid in more than £12,000, 38.6% of them. Table 9.7's bands break at exactly £12,000, so this count is exact.
  - Another 464,000 people paid into both types with a combined total above £12,000; the tables don't show how much of that was cash.
  - Both counts include people aged 65 or over, who would have kept the £20,000 cash limit.
- **A rough count of under-65s.** 7.46 million people under 66 paid into a cash ISA in 2023-24 (Table 9.8), and 22% of them is about 1.6 million. Three caveats:
  - it combines the 2022-23 share with 2023-24 counts;
  - HMRC's 63–65 age band includes 65-year-olds;
  - cash ISA accounts paid into rose by about 2.1 million in 2023-24 (HMRC commentary), so the 2023-24 share may be higher.
- **The effect over time.** That depends on what people would do with the money above £12,000:
  - moved into a stocks and shares ISA, it stays tax-free;
  - held in taxable savings, its interest becomes taxable above the personal savings allowance;
  - or it goes somewhere else.
  - HMRC's impact note leaves its Exchequer figures blank, pending scrutiny by the Office for Budget Responsibility. The Budget documents are the place to look for the cost of keeping the £20,000 cash allowance.

## Why these figures come from HMRC's tables, not the population model

PolicyEngine's UK data holds ISA balances, not payments, and "paying in the full allowance" and the £12,000 limit are about what someone pays in during one year.
- A balance of £40,000 could be two full years of payments, or fifteen years of small ones plus growth.
- The surveys behind the data record ISA values and interest, not payments.
- The model also has no ISA subscription limits.

[PolicyEngine/policyengine-uk#2710](https://github.com/PolicyEngine/policyengine-uk/issues/2710) sets out the engine changes needed. Modelling the limits directly also needs an imputation of yearly payments by type, calibrated to these same HMRC tables.
