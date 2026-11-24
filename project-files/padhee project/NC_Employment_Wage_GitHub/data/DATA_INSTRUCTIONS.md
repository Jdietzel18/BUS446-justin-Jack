# Data acquisition

Source: https://www.bls.gov/cew/downloadable-data-files.htm

Download the **annual averages by area** QCEW CSV archive for each year 2015–2025. Extract relevant CSV files into `data/raw/` (do not rename columns). BLS releases may be revised; record retrieval date. Filter NC counties using 5-digit area FIPS starting `37` (exclude statewide aggregate `37000` for county charts), ownership code `0` (total covered employment), and industry code `10` (total all industries) for county employment. For statewide industry comparisons use area `37000` and comparable high-level NAICS sector codes; avoid mixing aggregate and subindustry records. Suppressed or unavailable values must remain missing.

The 22,223-row workbook described in the proposal was not supplied, so this is a reconstruction workflow, not a claim that the exact original file is reproduced.
