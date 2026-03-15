# Battery Charging Analysis

Python tools for analysing lithium-ion battery charging experiments.

This repository contains scripts and documentation for analysing battery charging behaviour using experimental data exported from measurement systems such as NGU201 and DAS60.

---

# Project Overview

The goal of this repository is to provide a structured and reproducible workflow for analysing lithium-ion battery charging experiments.

Current focus:

- Δt(Q)-based charging comparison
- CSV-based battery test data analysis
- reproducible experimental data processing
- structured research workflow for battery experiments

The project is designed as a research-oriented codebase and will be expanded with additional scripts for battery parameter extraction and data analysis.

---

# Methodological Background

The analysis approach implemented in this repository is based on comparing charging processes using **state-equivalent criteria** rather than purely voltage-based events.

Key idea:

Instead of comparing charging processes only by time to reach a voltage threshold, the comparison can be performed using **Δt(Q)** curves, which describe the time difference required to reach the same transferred charge.

This allows a more consistent comparison of charging behaviour under different charging conditions.

---

# Repository Structure

```
battery-charging-analysis/
│
├── scripts/
│   └── plot_delta_tq.py
│
├── docs/
│   └── method_notes.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── results/
│   ├── figures/
│   └── tables/
│
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

# Scripts

## plot_delta_tq.py

Generates Δt(Q) curves for comparing different battery charging conditions.

Main functionality:

- load CSV charging data
- compute charge-related time alignment
- generate Δt(Q) comparison plots

---

# Data Structure

The repository separates raw data, processed data and generated results.

```
data/raw
```

Raw experimental CSV files exported from measurement systems.

```
data/processed
```

Intermediate processed data used for analysis.

```
results/figures
```

Generated plots.

```
results/tables
```

Exported numerical results.

---

# Installation

Install required Python packages:

```bash
pip install -r requirements.txt
```

---

# Usage

Example usage:

```bash
python scripts/plot_delta_tq.py
```

The script reads charging data and generates comparison plots in the results directory.

---

# Status

This repository is under active development and currently focuses on battery charging experiment analysis.

Future extensions may include:

- automated data parsing for NGU201 and DAS60
- HPPC parameter extraction
- extended battery charging comparison methods

---

# Author

Jiaxing Lu

MSc research project on lithium-ion battery charging analysis.
