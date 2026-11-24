"""QCEW analysis; run from repository root after downloading annual CSV files."""
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

raw=Path('data/raw'); out=Path('visualizations'); proc=Path('data/processed')
out.mkdir(exist_ok=True);proc.mkdir(exist_ok=True)
files=list(raw.rglob('*.csv'))
if not files:
    raise SystemExit('Missing QCEW annual CSV files. See data/DATA_INSTRUCTIONS.md')
frames=[]
for f in files:
    try:
        d=pd.read_csv(f,low_memory=False,dtype={'area_fips':str,'industry_code':str,'own_code':str})
        required={'year','area_fips','industry_code','own_code','annual_avg_emplvl','avg_annual_pay'}
        if not required.issubset(d.columns):continue
        frames.append(d)
    except Exception as e:print('Skipped',f,e)
if not frames:raise SystemExit('No compatible BLS annual CSVs found')
df=pd.concat(frames,ignore_index=True)
df['area_fips']=df.area_fips.astype(str).str.zfill(5)
df['industry_code']=df.industry_code.astype(str).str.strip()
df['own_code']=df.own_code.astype(str).str.strip()
df['year']=pd.to_numeric(df.year,errors='coerce')
for c in ['annual_avg_emplvl','avg_annual_pay','annual_avg_wkly_wage']:
    if c in df:df[c]=pd.to_numeric(df[c],errors='coerce')
if 'annual_avg_wkly_wage' not in df:df['annual_avg_wkly_wage']=df['avg_annual_pay']/52
nc=df[(df.area_fips.str.startswith('37')) & (df.own_code=='0') & (df.year.between(2015,2025))].copy()
county=nc[(nc.area_fips!='37000')&(nc.industry_code=='10')].copy()
county=county[county.annual_avg_emplvl.notna()]
if county.empty:raise SystemExit('No county total-employment records found; inspect BLS codes')
county=county.drop_duplicates(['year','area_fips'])
county.to_csv(proc/'county_total_employment.csv',index=False)
latest=int(county.year.max()); current=county[county.year==latest].sort_values('annual_avg_emplvl',ascending=False)
current.head(10).sort_values('annual_avg_emplvl').plot.barh(x='area_title',y='annual_avg_emplvl',legend=False,figsize=(10,6),color='#2277aa')
plt.title(f'Largest NC county workforces ({latest})');plt.xlabel('Annual average covered employment');plt.tight_layout();plt.savefig(out/'top_counties.png',dpi=180);plt.close()
trend=county.groupby('year',as_index=False)['annual_avg_emplvl'].sum()
trend.plot(x='year',y='annual_avg_emplvl',legend=False,marker='o',figsize=(9,5),color='#2277aa')
plt.title('NC county covered employment, annual average');plt.ylabel('Sum of county employment');plt.tight_layout();plt.savefig(out/'employment_trend.png',dpi=180);plt.close()
# Statewide, sector-level industries only: two-digit NAICS codes, excluding aggregates.
# Use explicitly listed two-digit NAICS sectors; grouped manufacturing and retail categories may be unavailable at this level.
sectors=['11','21','22','23','42','51','52','53','54','55','56','61','62','71','72','81','92']
state=nc[(nc.area_fips=='37000') & nc.industry_code.isin(sectors)].copy()
state=state.drop_duplicates(['year','industry_code'])
state.to_csv(proc/'state_industry_sectors.csv',index=False)
if not state.empty:
    newest=int(state.year.max()); top=state[state.year==newest].dropna(subset=['annual_avg_wkly_wage']).nlargest(10,'annual_avg_wkly_wage')
    top.sort_values('annual_avg_wkly_wage').plot.barh(x='industry_title',y='annual_avg_wkly_wage',legend=False,figsize=(11,6),color='#2277aa')
    plt.title(f'Highest-paying available NC industry sectors ({newest})');plt.xlabel('Average weekly wages ($)');plt.tight_layout();plt.savefig(out/'industry_wages.png',dpi=180);plt.close()
# County-year aggregate relationship; this is exploratory, not causal.
reg=county[['year','area_fips','annual_avg_emplvl','annual_avg_wkly_wage']].dropna()
reg=reg[(reg.annual_avg_emplvl>0)&(reg.annual_avg_wkly_wage>0)]
if len(reg)>=10:
    X=sm.add_constant(reg['annual_avg_wkly_wage']);y=reg['annual_avg_emplvl'];model=sm.OLS(y,X).fit(cov_type='HC3')
    reg.to_csv(proc/'regression_sample.csv',index=False)
    with open(proc/'regression_results.txt','w') as f:f.write(str(model.summary())+'\nObservations are county-year totals; repeated counties across years may violate independence.\n')
    plt.figure(figsize=(8,5));plt.scatter(reg.annual_avg_wkly_wage,reg.annual_avg_emplvl,alpha=.4)
    plt.xlabel('Average weekly wages ($)');plt.ylabel('Annual average employment');plt.title('County-year wages vs. employment (exploratory)')
    plt.tight_layout();plt.savefig(out/'wage_employment_scatter.png',dpi=180);plt.close()
print('Finished. Review outputs; do not treat correlations as causal.')
