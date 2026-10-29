# Wellington council-sourced rates lookup

The formula estimate fallback has been removed. Displayed annual CV/LV amounts come directly from the official council lookup, including GST. Yearly and weekly differences are precomputed. The standalone HTML needs no API connection to search.

**Full verification is in progress.** The page displays its current coverage. Accounts not yet checked show “Verification pending”, and council-unavailable accounts show no amount. Do not interpret either as a zero change.

## Scope and sources

The address list contains the 77,355 accounts in the original residential workbook. All accounts are being checked, including categories previously excluded by the formula. This verifies coverage of that file, not all newly created Wellington properties.

Official results: `https://digital.wellington.govt.nz/services/cv-lv-rates-consultation/results/{account}`. Council's consultation snapshot uses information dated 30 June 2026; retrieval began 29 October 2026. These remain council consultation estimates, not adopted future bills. Water, regional rates and sludge are excluded.

Every displayed annual amount comes from the “Including GST” section of its official current/proposed card. Account identity and card structure are checked. Redirects carrying `PROPERTY_NOT_FOUND` are recorded as council-unavailable. Technical failures and unparseable results never fall back to an estimated amount.

## Files

- `index.html`: self-contained lookup, exact house-number/suffix matching and mobile layout.
- `council-results.json`: compact source records: account, address, status, current amount, proposed amount, retrieval timestamp.
- `council-full-audit.csv`: per-account status, council amounts/differences, previous published annual difference and direct council URL. Pending rows are explicitly marked.
- `build.py` and `template.html`: rebuild the lookup from council results.
- Earlier `model.json`, `calibration.json`, `validation.json`, and sampled `council-audit*` files are historical evidence. **They are no longer used to calculate displayed amounts.**

```sh
python build.py council-results.json index.html
node test-search.cjs
node test-lookup.cjs
```

Annual difference = council current minus council proposed. Weekly difference = absolute annual difference / 52, with decimal half-up rounding to cents. Savings and increases are labelled separately. No inferred rate coefficients or source-file valuations are used.

The full audit was requested after sample checking found two material errors, including a reversal of saving/increase direction. It replaces sampled verification with account-by-account retrieval; unavailable records remain visible and clearly marked.
