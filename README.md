# Battery Charging Analysis

This repository contains Python scripts for lithium-ion battery charging analysis.

## Scope

The project focuses on:

- parsing measurement data from NGU201 and DAS60
- extracting HPPC-related parameters
- plotting Δt(Q)-based charging comparison results
- supporting reproducible battery test analysis

## Data source

The scripts are designed for:

- NGU201 CSV logs
- DAS60 exported CSV files

## Current contents

- **scripts/plot_delta_tq.py**  
  Generates Δt(Q) curves for charging comparison from CSV charging data.

## Requirements

Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

Run the script with:

```bash
python scripts/plot_delta_tq.py
```

## Project structure

```text
battery-charging-analysis/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── scripts/
│   └── plot_delta_tq.py
├── docs/
│   └── method_notes.md
├── data/
│   ├── raw/
│   └── processed/
└── results/
    ├── figures/
    └── tables/
```
## Notes

Raw experimental data are not included in this repository.  
Users should prepare CSV files according to the expected input format.
