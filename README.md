# Wellington residential CV-to-LV rates comparison

Open `index.html` directly or serve it with GitHub Pages. It is a standalone, mobile-responsive file with 77,355 accounts and no external scripts, fonts, API calls or build-time requirement for visitors.

## Model scope

2026/27 council consultation scenario, GST included. Only the general rate switches from CV to LV; base sector rates remain on CV. Water/Tiaki Wai, Greater Wellington and sludge are excluded. The scenario retains the 51:49 residential/commercial funding split. It is not an adopted future bill.

The general residential coefficients in `model.json` are **inferred from council results**, not officially published full-precision coefficients. Source valuations come from the canonical 2025/26 property workbook, while the council tool uses information dated 30 June 2026. Changes in assessments or valuations can cause differences. The page clearly distinguishes estimates from individually checked council amounts and links directly to each council result.

Rural, farmland and vacant/derelict categories do not receive a standard formula estimate. Commercial and mixed-use records are outside the residential dataset. Some accounts represent multiple dwellings.

Annual saving = rounded annual CV amount minus rounded annual LV amount. Weekly saving = annual saving / 52. Negative savings are labelled increases. Every annual scenario, yearly difference and weekly difference is precomputed by the builder. Search displays saved results immediately; a unique match opens automatically. Multiple results show the annual and weekly differences directly in the list.

## Evidence and validation

Sources accessed 29 October 2026:
- https://www.letstalk.wellington.govt.nz/rating-policies-review
- Consultation document, particularly pp. 13–14: https://www.letstalk.wellington.govt.nz/download_file/5273/1334
- https://digital.wellington.govt.nz/services/cv-lv-rates-consultation
- Each sampled result: append `/results/{id}` to the preceding URL.

`calibration.json` records 17 successful official comparisons, including the vacant-land exception; 14 standard-category samples were used for the least-squares coefficient fit. Rural and TWD checks were additional comparisons. Eight separate holdout accounts in `validation.json` had annual-saving errors of at most $0.01; this is sample validation, not a guarantee for every property. Official displayed amounts override estimates for individually checked eligible accounts.

Browser checks cover address/account search, savings, increases, special-category exclusions, exact house-number/suffix matching and 375px phone layout. Searches do not transmit addresses; opening a council link navigates to that public account page.

## Rebuild

Install `openpyxl`, then run:

```sh
python build.py '/path/to/WCC Property Database 2025-2026 Jesse Richardson (CANONICAL).xlsx' index.html
```

Keep `build.py`, `template.html` and `model.json` together. The workbook itself is not included. Do not pass the old citywide CSV: its rates/savings use the superseded calculation. A data refresh needs new council validation as well as new valuations; do not silently reuse these fitted coefficients for another year.

## Hosting

Use GitHub Pages with the `main` branch and repository root. Only `index.html` is required at runtime. All datasets embedded in the HTML are downloadable by visitors. No owner/contact information is included.

## Search regression checks

Run `node test-search.cjs` and `node test-lookup.cjs`. The latter checks every precomputed annual/weekly difference and automatic display behavior. Fifteen cases cover 8 versus 81 versus 8A, 8A versus 81A/8AB, unit numbers and street abbreviations.

## Expanded council audit — 29 October 2026

Compared the exact published HTML (SHA-256 `027cf024d5c1fc954f486e6b27feca01add3ec94c1dab36c2e78862c424d9d7a`) against 99 official account results. The reproducible sample includes random citywide and Newtown accounts, letter suffixes, unit addresses, large savings/increases, near-zero changes, and excluded categories.

Of 92 accounts with calculated figures, 90 matched current, proposed and annual differences within $0.02. One large account differed by $0.03 in the annual difference. One material discrepancy was found at 100 Darlington Road (1113351): the council shows $3,214.46 current and $3,702.08 proposed, a $487.62 annual increase or $9.38 per week. The original lookup showed a $675.45 annual increase. The cause is unconfirmed: council amounts are consistent with a different capital value, but public GIS still matches the older workbook valuation. Seven special-category accounts were correctly excluded from estimates.

All 92 calculated audit accounts now use the council's displayed amounts, with annual/weekly differences precomputed. All 20 randomly sampled Newtown accounts initially matched within $0.02. This verifies sampled addresses only, not every record in the database. Other accounts still use the documented estimate. `council-audit.json` and `council-audit.csv` retain the original discrepancies and corrected figures alongside direct official links.

## Further independent sample — 29 October 2026

A further 250 previously unchecked accounts were selected: 150 random citywide, 40 random Newtown, 30 letter-suffix and 30 unit addresses. Of these, 249 matched current, proposed and annual difference within $0.02. One material error was found at 10 Te Ara Kohuhu, Tawa (1999522): the council shows $3,966.79 current and $3,259.64 proposed, a **$707.15 yearly saving ($13.60/week)**. The old-source estimate showed a $1,296.28 yearly increase. The cause remains unconfirmed; the official displayed amounts now override the estimate.

Combined audit: **349 distinct accounts**, including 342 calculated accounts and seven excluded special categories. Original results: 339 within $0.02, one differed by $0.03, two material discrepancies. All 342 calculated accounts now use council amounts exactly; every saved yearly and weekly difference has been rechecked. Sixty accounts were specifically selected as random Newtown samples across both rounds. The combined `council-audit.csv` / `.json` retains both rounds, original errors, corrections and source URLs; `council-audit-round2` contains only the second round.

These checks do not certify unchecked addresses. In particular, the two material discrepancies show that an estimate based on the older source file can differ significantly and can reverse the direction of the change. Council-checked records are labelled separately in the lookup.
