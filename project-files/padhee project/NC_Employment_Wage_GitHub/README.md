# North Carolina Employment and Wage Trends (2015–2025)
**Jack Burdge and Justin Dietzel | Data Analytics Final Project**

## Business question
How do employment levels and average weekly wages differ across industries and counties in North Carolina, and how have they changed over time?

## Research questions
1. Which North Carolina counties have the highest and lowest employment levels?
2. Which industries have the highest average weekly wages in North Carolina?
3. Is there a relationship between average weekly wages and employment levels across North Carolina industries and counties?

## Source and data
U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages (QCEW): https://www.bls.gov/cew/downloadable-data-files.htm

The original proposal describes 22,223 observations across 102 geographic areas and 21 industry groups, covering 2015–2025. **The source workbook is not included in the supplied materials and those counts have not been independently verified.** The BLS data are public; download annual QCEW CSVs by area for each year, then filter for North Carolina and all-ownership records. Refer to `data/DATA_INSTRUCTIONS.md` and `analysis/analyze.py`.

## Project contents
- `report/`: original proposal and business case report (draft with findings clearly pending)
- `presentation/`: presentation slides (results placeholders, not verified findings)
- `analysis/`: Python script for cleaning, chart generation, and regression
- `visualizations/`: generated chart images go here
- `data/`: source and processing instructions; no source dataset currently provided

## Methodology
Use annual average employment and average weekly wages, filter to North Carolina, avoid overlapping total and subindustry categories, compare comparable annual county totals and statewide industry sectors, and run an exploratory regression of employment against wages. Correlation does not establish causation. Exclude suppressed or nonnumeric values; do not replace them with zero. Report sample sizes, coefficients, R-squared and p-values.

## Reproduce the analysis
1. Download annual by-area CSV files from BLS for 2015–2025, and extract the CSVs.
2. Place the extracted CSV files in `data/raw/`.
3. Install dependencies: `pip install pandas matplotlib scipy statsmodels`.
4. Run `python analysis/analyze.py` from the repository root.
5. Review generated files in `visualizations/` and `data/processed/`, and transfer verified values into the report and presentation.

## Status / academic integrity
**This repository is a structured submission draft, not a finished empirical analysis.** No real dataset or computed findings were supplied. Charts and statistics must be generated and verified before submission. Do not present placeholders as findings.

## Data limitations
QCEW excludes most self-employed workers; disclosure suppression can produce missing values. Annual averages are not year-end employment, and geographic/industry aggregation must be kept consistent. Industry totals must not be summed alongside subcategories.
