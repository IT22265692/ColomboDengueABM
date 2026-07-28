# Colombo Dengue ABM

An Agent-Based Model (ABM) developed in **AnyLogic 8.9.9 Personal Learning Edition** to investigate dengue transmission across the **13 Divisional Secretariat (DS) divisions of Colombo District, Sri Lanka**.

This project evaluates how **human commuter mobility** and **historical weather conditions** influence dengue transmission using Monte Carlo simulation and parameter variation experiments, validated against real Ministry of Health surveillance data.

Developed for:
**AM 4086 / AM 4039 / FM 4054 – Agent-Based Modeling**

Department of Mathematics - University of Colombo

---

# Research Questions

This study addresses the following research questions:

### RQ1

**Does representing daily commuting produce a materially different spatial pattern of dengue transmission compared to a model where everyone remains in their home zone?**

### RQ2

**Do weather conditions alone explain the difference in outbreak size between an epidemic year (2017) and a typical year (2019)?**

---

# Repository Structure

```
ColomboDengueABM_v2/
│
├── anylogic_model/          # AnyLogic project files (.alp)
├── al_internal/              # AnyLogic internal project files
├── cache/                    # AnyLogic cache
├── data/                     # Population, weather, GIS, and validation datasets
├── database/                 # SQLite database used by the model
├── figures/                  # Figures generated for the report
├── results/                  # CSV/XLSX outputs from simulation experiments
├── scripts/                  # Python scripts for analysis and plotting
├── report/                   # Final report (LaTeX source and compiled PDF)
│
├── README.md
│
├── db_backup_*.zip           # Automatic AnyLogic database backups
└── hs_err_pid*.log           # Java crash logs (can be ignored)
```

---

# Software Requirements

The project requires:

- AnyLogic Personal Learning Edition 8.9.9
- Java (included with AnyLogic)
- Python 3.10 or later

Python packages:

```bash
pip install pandas numpy matplotlib scipy openpyxl
```

---

# Datasets

The model uses the following datasets.

### Population

Population of each Colombo DS Division, from the 2024 census.

```
data/population.csv
```

---

### Weather

Weekly temperature and rainfall observations, derived from ERA5 and rescaled to match Colombo's real climate statistics.

```
data/temperature_and_rainfall_per_zone_weekly.csv
```

---

### Administrative Boundaries

Colombo District Divisional Secretariat boundary shapefiles.

```
data/*.shp
data/*.dbf
data/*.prj
data/*.shx
```

---

### Validation Dataset

Weekly reported dengue cases for Colombo District, 2015–2025, used to validate the weather-year experiment against real surveillance data.

```
data/colombo_dengue_weekly_2015_2025.csv
```

---

# Simulation Experiments

Three simulation experiments were performed.

## 1. MonteCarlo_Baseline

**Purpose:** Evaluate stochastic variability of the model using repeated Monte Carlo simulations at default parameters.

**Design:** 50 independent replications, commuting share fixed at 37.8%, weather cycling through the full 2015–2025 series.

**Key result:** Mean total infections = 121,129, CV = 0.77%, confirming stable, well-behaved stochastic dynamics.

**Output:**

```
results/MonteCarloResults.csv
```

---

## 2. ParamVar_CommutingShare

**Research Question 1**

Commuting share was varied across four values.

- 0%
- 20%
- 37.8%
- 50%

**Design note:** The first run of this experiment used a misconfigured random seed, causing all nominal replications within each commuting-share level to produce identical results (SD = 0). This was identified during data validation, the seed configuration was corrected to draw an independent seed per replication, and the experiment was re-run, yielding 20–30 genuinely independent replications per scenario.

**Key results (corrected data):**

- District-wide total infections showed no statistically significant difference across commuting levels (one-way ANOVA, F = 0.85, p = 0.47).
- Cross-zone coefficient of variation fell from 42.5% (0% commuting) to 15.9% (50% commuting), a strong and highly significant relationship (Pearson r = −0.9999, p = 0.0001).
- Padukka's mean infections rose 87.4% (3,795 → 7,113) between 0% and 50% commuting; Colombo's fell 22.5% (14,904 → 11,545) over the same range.

**Output:**

```
results/ParamVar_CommutingShare_Results.csv
```

---

## 3. ParamVar_Weather

**Research Question 2**

Weather conditions were fixed to either

- 2017 (major epidemic year)

or

- 2019 (typical year)

with

```
useSingleYearWeather = true
```

Ten independent replications were performed for each weather scenario.

**Key results:**

- Model mean total infections: 121,664 (2017) vs. 120,929 (2019), a difference of only 0.61% (independent-samples t-test: t = 1.965, p = 0.065, Cohen's d = 0.88 — not statistically significant).
- Real Ministry of Health annual case counts: 32,882 (2017) vs. 20,069 (2019), a difference of 64% (ratio = 1.638).
- The model's 2017:2019 ratio (1.006) does not reproduce the real ratio (1.638), indicating the model's weather-response functions are not sufficiently sensitive to explain the 2017 epidemic from weather alone.

**Output:**

```
results/WeatherExperimentResults.csv
```

---

# Running the Model

Open

```
anylogic_model/
```

using

```
AnyLogic 8.9.9 Personal Learning Edition
```

Run the experiments

- MonteCarlo_Baseline
- ParamVar_CommutingShare
- ParamVar_Weather

For `ParamVar_CommutingShare` and `ParamVar_Weather`, confirm the experiment's **Randomness** setting is set to draw an independent random seed per replication before running, rather than a fixed seed, to avoid the seeding issue described above.

Export the experiment outputs into

```
results/
```

---

# Running the Analysis

Navigate to

```
scripts/
```

and execute

```bash
python analysis.py
```

or

```bash
python make_figures.py
```

The scripts automatically

- compute descriptive statistics (means, standard deviations, confidence intervals)
- perform hypothesis tests (one-way ANOVA, independent-samples t-tests)
- compute Pearson correlations and effect sizes (Cohen's d)
- generate publication-quality figures

Figures are saved into

```
figures/
```

---

# Results Summary

## Baseline Monte Carlo

- 50 Monte Carlo replications
- Mean total infections: 121,129 (95% CI: [120,864, 121,395])
- Coefficient of variation: 0.77%, confirming stable stochastic behaviour

---

## Research Question 1: Commuting Share

Human commuting significantly changes the **spatial distribution** of dengue transmission, even though it does not significantly change the **total** volume of infections.

Increasing commuter mobility

- decreases mean infections in central Colombo (−22.5% from 0% to 50% commuting)
- increases mean infections in peripheral zones such as Padukka (+87.4% over the same range)
- reduces the cross-zone coefficient of variation from 42.5% to 15.9% (r = −0.9999, p = 0.0001)

The **district-wide infection total remains statistically unchanged** across commuting scenarios (one-way ANOVA, p = 0.47).

---

## Research Question 2: Weather Year

Weather conditions alone were **not sufficient** to explain the observed difference between the 2017 and 2019 dengue outbreaks.

The model produced only a 0.61% difference between the two weather scenarios (not statistically significant, p = 0.065), whereas surveillance data showed a 64% larger epidemic during 2017.

This suggests additional factors such as

- viral serotype changes (a documented DENV-2 resurgence occurred in 2017)
- imported infections from outside Colombo district
- human behaviour
- vector ecology not captured by the model's simplified temperature-response curves

likely contributed to the real outbreak's severity.

---

# Validation

Model predictions were compared against weekly dengue surveillance data obtained from the Sri Lanka Ministry of Health.

Validation focused on

- qualitative epidemic behaviour
- relative differences between years
- spatial transmission patterns

rather than exact case counts, since the model's absolute output exceeds real surveillance data by approximately 100-fold (reflecting both the inclusion of subclinical infections and unrecalibrated importation/waning-immunity parameters).

The comparison showed that

- the commuting mechanism reproduced realistic spatial redistribution of infections, consistent with prior mobility-dengue studies in Iquitos and Singapore;
- the weather-only experiment did not reproduce the magnitude of the 2017 epidemic, indicating that weather alone is insufficient to explain observed outbreak severity in this model as currently implemented.

---

# Figures

The report figures are generated automatically and saved in

```
figures/
```

These include

- Baseline histogram and boxplot
- Monte Carlo convergence
- Commuting-share boxplot (with genuine replication variance)
- Commuting-share dual-axis summary (totals vs. cross-zone CV)
- Cross-zone CV correlation plot
- Zone heatmap and zone comparison bar chart (with error bars)
- Weather comparison (model vs. real data)
- Real weekly case time series (2015–2025)
- Model vs. real annual scale comparison

---

# Report

The final written report, following the SIAM SIURO journal template, is available at:

```
report/Group06_Assignment8_SIURO.pdf
report/Group06_Assignment8_SIURO.tex
```

The report includes the full Results, Discussion, Conclusion, and Individual Contributions sections, along with a Python code appendix.

---

# Data Sources

Population

- Department of Census and Statistics, Sri Lanka

Weather

- Copernicus Climate Change Service (ERA5)

Administrative Boundaries

- Humanitarian Data Exchange (HDX)

Validation Data

- Ministry of Health, Sri Lanka
- Weekly Epidemiological Reports

---

# Known Limitations

- The 37.8% commuting share used as the default scenario is a proxy derived from 2024 census employment-migration data, not a direct daily-commuting statistic.
- Work-zone assignment is uniform-random across zones rather than weighted by real employment density.
- Mosquito biting-rate and survival temperature-response functions are simplified bell-curve approximations rather than the exact empirical curves in the cited literature.
- Model output exceeds real surveillance data by approximately two orders of magnitude; absolute case counts should not be interpreted as calibrated predictions without further work.

See `report/Group06_Assignment8_SIURO.pdf` for full discussion of limitations and future directions.

---

# Authors

**Group 6**

Department of Mathematics

University of Colombo

- Nishara Laksara (s16836)
- Nanduni Sathsara (s16962)
- Tharushi Madushika (s16950)
- Madhubhashini Jayasinghe (s16985)

---

# License

This repository is provided solely for academic and educational purposes.
The source code, datasets, figures and report were developed as part of a University of Colombo coursework project.
