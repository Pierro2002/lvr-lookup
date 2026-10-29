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
