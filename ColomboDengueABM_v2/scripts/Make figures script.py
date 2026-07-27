import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.family'] = 'DejaVu Serif'
plt.rcParams['font.size'] = 10

mc = pd.read_csv('MonteCarloResults.csv')
weather = pd.read_csv('WeatherExperimentResults.csv')
commuting = pd.read_excel('Final_Combined_ParamVar_Results.xlsx')
real_cases = pd.read_csv('colombo_dengue_weekly_2015_2025.csv')
real_cases['start.date'] = pd.to_datetime(real_cases['start.date'])

OUT = '/mnt/user-data/outputs/'

# ============================================================
# FIG 1: Baseline histogram
# ============================================================
ti = mc['TotalInfections']
fig, ax = plt.subplots(figsize=(6.5, 4.0))
ax.hist(ti, bins=8, color='#4A90D9', edgecolor='black', linewidth=0.6, alpha=0.85)
ax.axvline(ti.mean(), color='crimson', linestyle='--', linewidth=1.5, label=f'Mean = {ti.mean():.0f}')
ax.axvline(ti.median(), color='darkgreen', linestyle=':', linewidth=1.5, label=f'Median = {ti.median():.0f}')
ax.set_xlabel('Total simulated infections (agent counts)', fontsize=11)
ax.set_ylabel('Number of runs', fontsize=11)
ax.set_title('Distribution of total infections across 50 baseline\nMonte Carlo runs (commuting=37.8%, weather 2015--2025)', fontsize=10)
ax.legend(loc='upper right')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUT+'fig1_baseline_histogram.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 2: Baseline boxplot
# ============================================================
fig, ax = plt.subplots(figsize=(4.5, 4.0))
bp = ax.boxplot([ti], patch_artist=True, widths=0.4,
                boxprops=dict(facecolor='#4A90D9', edgecolor='black', linewidth=0.8),
                medianprops=dict(color='darkred', linewidth=1.5))
ax.scatter(np.random.normal(1, 0.04, len(ti)), ti, alpha=0.4, s=15, color='black', zorder=3)
ax.set_xticklabels(['Baseline\n(37.8% commuting)'])
ax.set_ylabel('Total infections (agent counts)', fontsize=10)
ax.set_title('Baseline Monte Carlo results (n=50)', fontsize=10)
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.3, linestyle='--', axis='y')
plt.tight_layout()
plt.savefig(OUT+'fig2_baseline_boxplot.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 3: Convergence
# ============================================================
fig, ax = plt.subplots(figsize=(6.5, 4.0))
running_mean = ti.expanding().mean()
running_std = ti.expanding().std()
runs = np.arange(1, len(ti)+1)
ax.plot(runs, running_mean, color='#4A90D9', linewidth=1.8, label='Running mean')
ax.fill_between(runs, running_mean - 1.96*running_std/np.sqrt(runs),
                running_mean + 1.96*running_std/np.sqrt(runs), alpha=0.25, color='#4A90D9', label='95% CI')
ax.axhline(ti.mean(), color='crimson', linestyle='--', linewidth=1, label=f'Final mean = {ti.mean():,.0f}')
ax.set_xlabel('Run number'); ax.set_ylabel('Cumulative mean total infections')
ax.set_title('Convergence across 50 Monte Carlo replications', fontsize=10)
ax.legend(loc='lower right')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUT+'fig3_convergence.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 4: Weather year comparison (boxplot side by side) - RQ2
# ============================================================
w2017 = weather[weather['WeatherYear']==2017].drop_duplicates(subset=['TotalInfections'])['TotalInfections']
w2019 = weather[weather['WeatherYear']==2019].drop_duplicates(subset=['TotalInfections'])['TotalInfections']

fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
bp = axes[0].boxplot([w2017, w2019], patch_artist=True, widths=0.5, labels=['2017\n(epidemic year)', '2019\n(typical year)'])
colors_box = ['#E74C3C', '#3498DB']
for patch, c in zip(bp['boxes'], colors_box):
    patch.set_facecolor(c); patch.set_alpha(0.7)
for i, vals in enumerate([w2017, w2019]):
    axes[0].scatter(np.random.normal(i+1, 0.04, len(vals)), vals, alpha=0.5, s=20, color='black', zorder=3)
axes[0].set_ylabel('Total simulated infections (10-yr run)')
axes[0].set_title('Model: 2017 vs 2019 weather\n(t-test p=0.065, Cohen\'s d=0.88)', fontsize=9.5)
axes[0].spines[['top','right']].set_visible(False)
axes[0].grid(True, alpha=0.3, linestyle='--', axis='y')

real_2017 = real_cases[real_cases['year']==2017]['cases'].sum()
real_2019 = real_cases[real_cases['year']==2019]['cases'].sum()
axes[1].bar(['2017\n(epidemic year)', '2019\n(typical year)'], [real_2017, real_2019],
            color=['#E74C3C','#3498DB'], alpha=0.85, edgecolor='black', width=0.5)
for i, v in enumerate([real_2017, real_2019]):
    axes[1].text(i, v+500, f'{v:,}', ha='center', fontsize=10)
axes[1].set_ylabel('Real notified dengue cases (Colombo district, annual)')
axes[1].set_title('Reality: 2017 vs 2019 real cases\n(ratio = 1.64x)', fontsize=9.5)
axes[1].spines[['top','right']].set_visible(False)
axes[1].grid(True, alpha=0.3, linestyle='--', axis='y')

plt.suptitle('Model fails to reproduce the real weather-driven difference between 2017 and 2019', fontsize=10.5, y=1.02)
plt.tight_layout()
plt.savefig(OUT+'fig4_weather_comparison.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 5: Commuting share total infections + zone CV dual axis
# ============================================================
zones = ['Colombo','Homagama','Maharagama','Padukka','Seethawaka','Kaduwela',
         'Dehiwala','Thimbirigasyaya','Ratmalana','Kolonnawa','Moratuwa',
         'Kesbewa','Sri Jayawardanapura Kotte']
shares = [0.0, 0.2, 0.378, 0.5]
zone_data = {}
for s in shares:
    sub = commuting[commuting['CommutingShare']==s].drop_duplicates(subset=['Zone'])
    zone_data[s] = dict(zip(sub['Zone'], sub['ZoneInfections']))
    zone_data[s]['Total'] = commuting[commuting['CommutingShare']==s]['TotalInfections'].iloc[0]

totals = [zone_data[s]['Total'] for s in shares]
cvs = [np.std([zone_data[s][z] for z in zones])/np.mean([zone_data[s][z] for z in zones])*100 for s in shares]

fig, ax1 = plt.subplots(figsize=(6.5, 4.5))
ax2 = ax1.twinx()
l1 = ax1.plot(shares, totals, 'o-', color='#3498DB', linewidth=2, markersize=8, label='Total infections')
l2 = ax2.plot(shares, cvs, 's--', color='#E74C3C', linewidth=2, markersize=8, label='Cross-zone CV')
ax1.set_xlabel('Commuting share', fontsize=11)
ax1.set_ylabel('Total infections (district-wide)', color='#3498DB', fontsize=11)
ax2.set_ylabel('Cross-zone coefficient of variation (%)', color='#E74C3C', fontsize=11)
ax1.tick_params(axis='y', labelcolor='#3498DB')
ax2.tick_params(axis='y', labelcolor='#E74C3C')
ax1.set_title('Total infections stay flat while spatial\ninequality (CV) falls sharply as commuting rises', fontsize=10.5)
lines = l1+l2
ax1.legend(lines, [l.get_label() for l in lines], loc='center right')
ax1.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUT+'fig5_commuting_dual.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 6: Heatmap
# ============================================================
zone_labels_short = ['Colombo','Homagama','Maharagama','Padukka','Seethawaka',
                     'Kaduwela','Dehiwala','Thimbirig.','Ratmalana',
                     'Kolonnawa','Moratuwa','Kesbewa','SJP Kotte']
matrix = np.array([[zone_data[s][z] for z in zones] for s in shares])
labels = ['0%','20%','37.8%','50%']

fig, ax = plt.subplots(figsize=(11, 3.8))
im = ax.imshow(matrix, aspect='auto', cmap='YlOrRd')
ax.set_xticks(range(len(zones))); ax.set_xticklabels(zone_labels_short, rotation=40, ha='right', fontsize=9)
ax.set_yticks(range(len(shares))); ax.set_yticklabels(labels, fontsize=9)
plt.colorbar(im, ax=ax, label='Zone infections', shrink=0.85)
ax.set_title('Zone-level infections by commuting share', fontsize=11)
for i in range(len(shares)):
    for j in range(len(zones)):
        ax.text(j, i, f'{matrix[i,j]:,}', ha='center', va='center', fontsize=7,
                color='black' if matrix[i,j]<12000 else 'white')
plt.tight_layout()
plt.savefig(OUT+'fig6_heatmap.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 7: Zone comparison bars (0%, 37.8%, 50%)
# ============================================================
fig, ax = plt.subplots(figsize=(12, 5))
x = np.arange(len(zones)); w = 0.28
ax.bar(x-w, [zone_data[0.0][z] for z in zones], w, label='0%', color='#E74C3C', alpha=0.85, edgecolor='black', linewidth=0.4)
ax.bar(x,   [zone_data[0.378][z] for z in zones], w, label='37.8% (census proxy)', color='#3498DB', alpha=0.85, edgecolor='black', linewidth=0.4)
ax.bar(x+w, [zone_data[0.5][z] for z in zones], w, label='50%', color='#27AE60', alpha=0.85, edgecolor='black', linewidth=0.4)
ax.set_xticks(x); ax.set_xticklabels(zone_labels_short, rotation=35, ha='right', fontsize=9)
ax.set_ylabel('Zone infections over 10 years')
ax.set_title('Zone-level infections under three commuting share scenarios')
ax.legend(); ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.25, linestyle='--', axis='y')
plt.tight_layout()
plt.savefig(OUT+'fig7_zone_comparison.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 8: Real weekly dengue case time series 2015-2025 (validation context)
# ============================================================
fig, ax = plt.subplots(figsize=(11, 4))
ax.plot(real_cases['start.date'], real_cases['cases'], color='#8E44AD', linewidth=0.9)
ax.fill_between(real_cases['start.date'], real_cases['cases'], alpha=0.15, color='#8E44AD')
# highlight 2017
mask17 = (real_cases['year']==2017)
ax.fill_between(real_cases.loc[mask17,'start.date'], real_cases.loc[mask17,'cases'], color='#E74C3C', alpha=0.3, label='2017 epidemic year')
mask19 = (real_cases['year']==2019)
ax.fill_between(real_cases.loc[mask19,'start.date'], real_cases.loc[mask19,'cases'], color='#3498DB', alpha=0.3, label='2019 typical year')
ax.set_xlabel('Date'); ax.set_ylabel('Notified weekly dengue cases, Colombo district')
ax.set_title('Real weekly dengue case counts, Colombo district, 2015--2025', fontsize=11)
ax.legend(loc='upper right')
ax.spines[['top','right']].set_visible(False)
ax.grid(True, alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig(OUT+'fig8_real_cases_timeseries.png', dpi=200, bbox_inches='tight')
plt.close()

# ============================================================
# FIG 9: Model vs Real scale comparison (log scale bar)
# ============================================================
model_annual_scaled = (mc['TotalInfections'].mean()/10) * 100
real_annual_mean = real_cases.groupby('year')['cases'].sum().mean()

fig, ax = plt.subplots(figsize=(5.5, 4.2))
bars = ax.bar(['Model\n(scaled x100)', 'Real MoH\nnotified cases'],
              [model_annual_scaled, real_annual_mean],
              color=['#3498DB','#E74C3C'], alpha=0.85, edgecolor='black', width=0.5)
ax.set_yscale('log')
ax.set_ylabel('Mean annual infections/cases (log scale)')
ax.set_title('Model output vs.\nreal surveillance data (annual mean)', fontsize=10.5)
for bar, v in zip(bars, [model_annual_scaled, real_annual_mean]):
    ax.text(bar.get_x()+bar.get_width()/2, v*1.15, f'{v:,.0f}', ha='center', fontsize=9)
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
plt.savefig(OUT+'fig9_scale_comparison.png', dpi=200, bbox_inches='tight')
plt.close()

print("All 9 figures generated successfully")