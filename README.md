# Colombo Dengue ABM

An agent-based model of dengue transmission driven by human commuter mobility
across the 13 Divisional Secretariat (DS) zones of Colombo District, Sri Lanka.

Built for AM 4086 / AM 4039 / FM 4054 (Agent-Based Modeling), Semester I 2026,
Group 6, University of Colombo.

## Research Questions

1. Does representing daily commuting produce a materially different spatial
   pattern of dengue transmission compared to a model where everyone stays
   in their home zone?
2. Do weather conditions alone explain the difference in outbreak size
   between an epidemic year (2017) and a typical year (2019)?

## Repository Structure

```
.
├── anylogic_model/
│   └── ColomboDengueABM_v2.alp        # AnyLogic 8.9.9 model file
├── data/
│   ├── population.csv                  # 2024 census population per DS zone
│   ├── weather_cleaned.csv             # ERA5-derived daily temp/rainfall, 2015-2025
│   ├── colombo_ds.shp (+ .dbf/.shx/.prj) # DS zone boundary shapefile
│   └── colombo_dengue_weekly_2015_2025.csv  # Real MoH weekly case counts (validation)
├── results/
│   ├── MonteCarloResults.csv           # Baseline experiment output (50 reps)
│   ├── WeatherExperimentResults.csv    # 2017 vs 2019 weather sweep (10 reps each)
│   └── Final_Combined_ParamVar_Results.xlsx  # Commuting share sweep (0/20/37.8/50%)
├── scripts/
│   ├── analysis.py                     # Statistical analysis (t-tests, correlations, CIs)
│   └── make_figures.py                 # Generates all 9 figures used in the report
├── figures/
│   └── fig1_baseline_histogram.png ... fig9_scale_comparison.png
├── report/
│   └── Group06_Assignment8_SIURO.tex   # Final report (SIURO journal template)
│   └── Group06_Assignment8_SIURO.pdf
└── README.md
```

## How to Reproduce the Results

### 1. Run the AnyLogic model

- Requires AnyLogic 8.9.9 Personal Learning Edition (free): https://www.anylogic.com/downloads/
- Open `anylogic_model/ColomboDengueABM_v2.alp`
- Ensure `data/population.csv`, `data/weather_cleaned.csv`, and the shapefile
  files are in the same folder as the `.alp` file
- Run the `MonteCarlo_Baseline`, `ParamVar_CommutingShare`, and
  `ParamVar_Weather` experiments from the Projects panel
- Export each experiment's output table to CSV/XLSX into the `results/` folder

### 2. Run the statistical analysis

```bash
pip install pandas numpy matplotlib scipy openpyxl
python scripts/analysis.py       # prints all statistics used in the report
python scripts/make_figures.py   # regenerates all 9 figures into figures/
```

### 3. Compile the report

The report uses the SIAM SIURO journal template. Open `report/Group06_Assignment8_SIURO.tex`
in Overleaf (or compile locally with `pdflatex`, run twice), with all files
from `figures/` in the same directory as the `.tex` file.

## Key Findings

- **Baseline stability:** 50 Monte Carlo replications, CV = 0.77%, confirming
  the model's stochastic behaviour is stable and well-behaved.
- **RQ1 (commuting):** Supported. Cross-zone coefficient of variation in
  infections falls from 44.1% (0% commuting) to 15.2% (50% commuting),
  r = -0.998, p = 0.002.
- **RQ2 (weather):** Not supported. Model shows only a 0.61% difference
  between 2017 and 2019 weather (t = 1.965, p = 0.065), versus a real
  64% difference in Ministry of Health surveillance data.

## Known Limitations

- The commuting-share experiment's 10 nominal replications per scenario
  produced identical results (SD = 0), indicating the AnyLogic random seed
  was not configured for independent draws in that specific sweep. The
  weather-year sweep did not have this issue.
- Model output exceeds real case counts by approximately 100-fold, reflecting
  both the inclusion of subclinical infections and unrecalibrated importation/
  waning-immunity parameters.
- The 37.8% commuting rate is a proxy from census employment-migration data,
  not a direct daily-commuting statistic.

See the report's Discussion and Limitations sections for full details.

## Data Sources

- Population: 2024 Sri Lanka Population and Housing Census, Department of
  Census and Statistics
- Weather: Copernicus Climate Change Service, ERA5 reanalysis
- Zone boundaries: Humanitarian Data Exchange (HDX), COD administrative
  boundaries for Sri Lanka
- Dengue case validation data: Ministry of Health Weekly Epidemiological
  Reports, Sri Lanka

## Authors

Nishara Laksara (s16836), Nanduni Sathsara (s16962),
Tharushi Madushika (s16950), Madhubhashini Jayasinghe (s16985)

Department of Mathematics, University of Colombo

## License

This repository is shared for academic evaluation purposes as part of a
university course assignment.
