"""
Full statistical analysis and figure generation for Assignment 8.
Colombo Dengue ABM - Group 6
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'DejaVu Serif'
plt.rcParams['font.size'] = 10

# ============================================================
# 1. LOAD ALL DATA
# ============================================================
mc = pd.read_csv('MonteCarloResults.csv')
weather = pd.read_csv('WeatherExperimentResults.csv')
commuting = pd.read_excel('Final_Combined_ParamVar_Results.xlsx')
real_cases = pd.read_csv('colombo_dengue_weekly_2015_2025.csv')

print("="*70)
print("1. BASELINE MONTE CARLO ANALYSIS")
print("="*70)
ti = mc['TotalInfections']
sem = stats.sem(ti)
ci = stats.t.interval(0.95, len(ti)-1, loc=ti.mean(), scale=sem)
print(f"n={len(ti)}, mean={ti.mean():.1f}, sd={ti.std():.1f}, median={ti.median():.1f}")
print(f"95% CI: [{ci[0]:.1f}, {ci[1]:.1f}]")
print(f"CV: {ti.std()/ti.mean()*100:.2f}%")
print(f"min={ti.min()}, max={ti.max()}")

# ============================================================
# 2. WEATHER EXPERIMENT (2017 vs 2019) - RESEARCH QUESTION 2
# ============================================================
print("\n"+"="*70)
print("2. WEATHER EXPERIMENT: 2017 vs 2019")
print("="*70)

w2017 = weather[weather['WeatherYear']==2017].drop_duplicates(subset=['TotalInfections'])['TotalInfections']
w2019 = weather[weather['WeatherYear']==2019].drop_duplicates(subset=['TotalInfections'])['TotalInfections']

print(f"\n2017: n={len(w2017)}, mean={w2017.mean():.1f}, sd={w2017.std():.1f}")
print(f"2019: n={len(w2019)}, mean={w2019.mean():.1f}, sd={w2019.std():.1f}")

# Independent samples t-test
t_stat, p_val = stats.ttest_ind(w2017, w2019)
print(f"\nIndependent t-test: t={t_stat:.3f}, p={p_val:.4f}")

# Effect size (Cohen's d)
pooled_sd = np.sqrt(((len(w2017)-1)*w2017.std()**2 + (len(w2019)-1)*w2019.std()**2) / (len(w2017)+len(w2019)-2))
cohens_d = (w2017.mean() - w2019.mean()) / pooled_sd
print(f"Cohen's d: {cohens_d:.3f}")

diff = w2017.mean() - w2019.mean()
pct_diff = diff / w2019.mean() * 100
print(f"Difference: {diff:.1f} ({pct_diff:+.2f}%)")

# Real data comparison
real_2017 = real_cases[real_cases['year']==2017]['cases'].sum()
real_2019 = real_cases[real_cases['year']==2019]['cases'].sum()
real_ratio = real_2017/real_2019
print(f"\nReal MoH data: 2017={real_2017}, 2019={real_2019}, ratio={real_ratio:.2f}x")
print(f"Model ratio 2017/2019: {w2017.mean()/w2019.mean():.4f}x  <-- KEY DISCREPANCY")

# ============================================================
# 3. COMMUTING SHARE EXPERIMENT - RESEARCH QUESTION 1
# ============================================================
print("\n"+"="*70)
print("3. COMMUTING SHARE EXPERIMENT")
print("="*70)

zones = ['Colombo','Homagama','Maharagama','Padukka','Seethawaka','Kaduwela',
         'Dehiwala','Thimbirigasyaya','Ratmalana','Kolonnawa','Moratuwa',
         'Kesbewa','Sri Jayawardanapura Kotte']
shares = [0.0, 0.2, 0.378, 0.5]

zone_data = {}
for s in shares:
    sub = commuting[commuting['CommutingShare']==s].drop_duplicates(subset=['Zone'])
    zone_data[s] = dict(zip(sub['Zone'], sub['ZoneInfections']))
    total = commuting[commuting['CommutingShare']==s]['TotalInfections'].iloc[0]
    zone_data[s]['TotalInfections'] = total

for s in shares:
    vals = [zone_data[s][z] for z in zones]
    cv = np.std(vals)/np.mean(vals)*100
    print(f"CommutingShare={s}: total={zone_data[s]['TotalInfections']}, CV={cv:.1f}%")

# Correlation: commuting share vs zone CV (test the "equalization" hypothesis)
cvs = []
for s in shares:
    vals = [zone_data[s][z] for z in zones]
    cvs.append(np.std(vals)/np.mean(vals)*100)
corr, p_corr = stats.pearsonr(shares, cvs)
print(f"\nCorrelation (commuting share vs zone CV): r={corr:.4f}, p={p_corr:.4f}")

# Correlation: commuting share vs Padukka infections (smallest zone)
padukka_vals = [zone_data[s]['Padukka'] for s in shares]
corr_p, p_p = stats.pearsonr(shares, padukka_vals)
print(f"Correlation (commuting share vs Padukka infections): r={corr_p:.4f}, p={p_p:.4f}")

# Correlation: commuting share vs Colombo infections (largest zone)
colombo_vals = [zone_data[s]['Colombo'] for s in shares]
corr_c, p_c = stats.pearsonr(shares, colombo_vals)
print(f"Correlation (commuting share vs Colombo infections): r={corr_c:.4f}, p={p_c:.4f}")

padukka_change = (zone_data[0.5]['Padukka']-zone_data[0.0]['Padukka'])/zone_data[0.0]['Padukka']*100
colombo_change = (zone_data[0.5]['Colombo']-zone_data[0.0]['Colombo'])/zone_data[0.0]['Colombo']*100
print(f"\nPadukka change 0%->50%: {padukka_change:+.1f}%")
print(f"Colombo change 0%->50%: {colombo_change:+.1f}%")

# ============================================================
# 4. VALIDATION AGAINST REAL DATA - RMSE
# ============================================================
print("\n"+"="*70)
print("4. VALIDATION: RMSE AGAINST REAL WEEKLY CASES")
print("="*70)

# Model produces total infections over 10 years; convert to comparable weekly scale
# Real weekly mean cases (district level, notified)
real_weekly_mean_2017 = real_cases[real_cases['year']==2017]['cases'].mean()
real_weekly_mean_2019 = real_cases[real_cases['year']==2019]['cases'].mean()
real_weekly_mean_all = real_cases['cases'].mean()

print(f"Real weekly mean cases (all years 2015-2025): {real_weekly_mean_all:.1f}")
print(f"Real weekly mean cases (2017): {real_weekly_mean_2017:.1f}")
print(f"Real weekly mean cases (2019): {real_weekly_mean_2019:.1f}")

# Model annual mean infections (baseline, scaled)
model_annual_mean = ti.mean()/10  # per year, unscaled agent counts
model_weekly_mean = model_annual_mean/52
print(f"\nModel weekly mean infections (unscaled agent count, baseline): {model_weekly_mean:.1f}")
print(f"Model weekly mean infections (scaled x100): {model_weekly_mean*100:.1f}")

# Overshoot factor
overshoot = (model_weekly_mean*100) / real_weekly_mean_all
print(f"Overshoot factor vs real (scaled): {overshoot:.1f}x")

# RMSE on the ratio comparison (2017 vs 2019 only, since that's what we have per-scenario)
# Normalize both to relative scale (ratio to their own 2019 baseline) for shape comparison
model_2017_norm = w2017.mean()/w2019.mean()
real_2017_norm = real_2017/real_2019
rmse_ratio = np.sqrt((model_2017_norm - real_2017_norm)**2)
print(f"\nModel 2017:2019 ratio = {model_2017_norm:.3f}")
print(f"Real  2017:2019 ratio = {real_2017_norm:.3f}")
print(f"Absolute error in ratio = {abs(model_2017_norm-real_2017_norm):.3f}")

print("\n"+"="*70)
print("ANALYSIS COMPLETE - GENERATING FIGURES")
print("="*70)