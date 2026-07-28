# Colombo Dengue ABM

An Agent-Based Model (ABM) developed in **AnyLogic 8.9.9 Personal Learning Edition** to investigate dengue transmission across the **13 Divisional Secretariat (DS) divisions of Colombo District, Sri Lanka**.

This project evaluates how **human commuter mobility** and **historical weather conditions** influence dengue transmission using Monte Carlo simulation and parameter variation experiments.

Developed for:
**AM 4086 / AM 4039 / FM 4054 – Agent-Based Modeling**
Department of Mathematics 
University of Colombo
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
├── anylogic_model/          # AnyLogic project files
├── al_internal/             # AnyLogic internal project files
├── cache/                   # AnyLogic cache
├── data/                    # Population, weather and validation datasets
├── database/                # SQLite database used by the model
├── figures/                 # Figures generated for the report
├── results/                 # CSV/XLSX outputs from simulation experiments
├── scripts/                 # Python scripts for analysis and plotting
│
├── README.md
│
├── db_backup_*.zip          # Automatic AnyLogic database backups
└── hs_err_pid*.log          # Java crash logs (can be ignored)
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

Population of each Colombo DS Division.

```
data/population.csv
```

---

### Weather

Weekly temperature and rainfall observations.

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

Weekly reported dengue cases for Colombo District.

```
data/colombo_dengue_weekly_2015_2025.csv
```

Used for model validation.

---

# Simulation Experiments

Three simulation experiments were performed.

## 1. MonteCarlo_Baseline

Purpose:

Evaluate stochastic variability of the model using repeated Monte Carlo simulations.

Output:

```
results/MonteCarloResults.csv
```

---

## 2. ParamVar_CommutingShare

Research Question 1

Commuting share was varied across four values.

- 0%
- 20%
- 37.8%
- 50%

Ten independent replications were performed for each scenario.

Outputs include

- Total infections
- Zone-level infections
- Statistical comparisons

Output:

```
results/Final_Combined_ParamVar_Results.xlsx
```

---

## 3. ParamVar_Weather

Research Question 2

Weather conditions were fixed to either

- 2017 (major epidemic year)

or

- 2019 (typical year)

with

```
useSingleYearWeather = true
```

Ten independent replications were performed for each weather scenario.

Output:

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

- compute descriptive statistics
- calculate confidence intervals
- perform hypothesis tests
- generate publication-quality figures

Figures are saved into

```
figures/
```

---

# Results Summary

## Baseline Monte Carlo

- 50 Monte Carlo replications
- Stable stochastic behaviour
- Very small coefficient of variation

---

## Research Question 1

Human commuting significantly changes the **spatial distribution** of dengue transmission.

Increasing commuter mobility

- decreases infections in central Colombo
- increases infections in suburban zones
- redistributes transmission across DS divisions

However,

the **overall district-wide infection total remains statistically unchanged.**

---

## Research Question 2

Weather conditions alone were **not sufficient** to explain the observed difference between the 2017 and 2019 dengue outbreaks.

The model produced only a small difference between the two weather scenarios, whereas surveillance data showed a substantially larger epidemic during 2017.

This suggests additional factors such as

- viral serotype changes
- imported infections
- human behaviour
- vector ecology

likely contributed to the real outbreak.

---

# Validation

Model predictions were compared against weekly dengue surveillance data obtained from the Sri Lanka Ministry of Health.

Validation focused on

- qualitative epidemic behaviour
- relative differences between years
- spatial transmission patterns

rather than exact case counts.

The comparison showed that

- the commuting mechanism reproduced realistic spatial redistribution of infections;

- the weather-only experiment did not reproduce the magnitude of the 2017 epidemic, indicating that weather alone is insufficient to explain observed outbreak severity.

---

# Figures

The report figures are generated automatically and saved in

```
figures/
```

These include

- Baseline histogram
- Baseline boxplot
- Monte Carlo convergence
- Commuting-share comparison
- Zone heatmap
- Zone distribution
- Weather comparison
- Validation plots

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
