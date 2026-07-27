"""
CORRECTED statistical analysis - commuting share experiment with proper
per-replication randomization (fixed from the original zero-variance bug).
"""
import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('/mnt/user-data/uploads/ParamVar_CommutingShare_Results.csv')

zones = ['Colombo','Homagama','Maharagama','Padukka','Seethawaka','Kaduwela',
         'Dehiwala','Thimbirigasyaya','Ratmalana','Kolonnawa','Moratuwa',
         'Kesbewa','Sri Jayawardanapura Kotte']
shares = sorted(df['CommutingShare'].unique())

print("="*70)
print("1. DESCRIPTIVE STATISTICS PER COMMUTING SHARE")
print("="*70)
for s in shares:
    sub = df[df['CommutingShare']==s]['TotalInfections']
    ci = stats.t.interval(0.95, len(sub)-1, loc=sub.mean(), scale=stats.sem(sub))
    print(f"\nCommutingShare={s}: n={len(sub)}")
    print(f"  Mean={sub.mean():.1f}, SD={sub.std():.1f}, CV={sub.std()/sub.mean()*100:.2f}%")
    print(f"  95% CI: [{ci[0]:.1f}, {ci[1]:.1f}]")
    print(f"  Min={sub.min()}, Max={sub.max()}")

print("\n"+"="*70)
print("2. ONE-WAY ANOVA: does commuting share affect total infections?")
print("="*70)
groups = [df[df['CommutingShare']==s]['TotalInfections'].values for s in shares]
f_stat, p_anova = stats.f_oneway(*groups)
print(f"F={f_stat:.4f}, p={p_anova:.4f}")

print("\n"+"="*70)
print("3. PEARSON CORRELATION: commuting share vs mean total infections")
print("="*70)
means = [df[df['CommutingShare']==s]['TotalInfections'].mean() for s in shares]
corr, p_corr = stats.pearsonr(shares, means)
print(f"r={corr:.4f}, p={p_corr:.4f}")

print("\n"+"="*70)
print("4. ZONE-LEVEL ANALYSIS: mean infections per zone per commuting share")
print("="*70)
zone_means = {}
for s in shares:
    sub = df[df['CommutingShare']==s]
    zone_means[s] = {z: sub[z].mean() for z in zones}
    vals = list(zone_means[s].values())
    cv = np.std(vals)/np.mean(vals)*100
    print(f"\nCommutingShare={s}: cross-zone CV={cv:.1f}%")
    for z in sorted(zones, key=lambda z: -zone_means[s][z]):
        print(f"  {z}: {zone_means[s][z]:.0f}")

print("\n"+"="*70)
print("5. CORRELATION: commuting share vs cross-zone CV")
print("="*70)
cvs = []
for s in shares:
    vals = list(zone_means[s].values())
    cvs.append(np.std(vals)/np.mean(vals)*100)
corr_cv, p_cv = stats.pearsonr(shares, cvs)
print(f"r={corr_cv:.4f}, p={p_cv:.4f}")
print(f"CVs: {[f'{c:.1f}%' for c in cvs]}")

print("\n"+"="*70)
print("6. PADUKKA AND COLOMBO TRENDS (with proper SD now)")
print("="*70)
padukka_means = [zone_means[s]['Padukka'] for s in shares]
colombo_means = [zone_means[s]['Colombo'] for s in shares]
corr_p, p_p = stats.pearsonr(shares, padukka_means)
corr_c, p_c = stats.pearsonr(shares, colombo_means)
print(f"Padukka: r={corr_p:.4f}, p={p_p:.4f}")
print(f"Colombo: r={corr_c:.4f}, p={p_c:.4f}")

padukka_change = (padukka_means[-1]-padukka_means[0])/padukka_means[0]*100
colombo_change = (colombo_means[-1]-colombo_means[0])/colombo_means[0]*100
print(f"\nPadukka change (0% -> 50%): {padukka_change:+.1f}%")
print(f"Colombo change (0% -> 50%): {colombo_change:+.1f}%")

print("\n"+"="*70)
print("7. PAIRWISE t-TESTS: 0% vs 50% (the two extremes)")
print("="*70)
g0 = df[df['CommutingShare']==0.0]['TotalInfections']
g50 = df[df['CommutingShare']==0.5]['TotalInfections']
t_stat, p_val = stats.ttest_ind(g0, g50)
pooled_sd = np.sqrt(((len(g0)-1)*g0.std()**2 + (len(g50)-1)*g50.std()**2)/(len(g0)+len(g50)-2))
cohens_d = (g50.mean()-g0.mean())/pooled_sd
print(f"0% vs 50%: t={t_stat:.3f}, p={p_val:.4f}, Cohen's d={cohens_d:.3f}")

print("\nANALYSIS COMPLETE")
