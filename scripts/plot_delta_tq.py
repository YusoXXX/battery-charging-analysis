"""
plot_delta_tq.py

Generate Δt(Q) curves for lithium-ion battery charging experiments.

Purpose
-------
This script generates Δt(Q) curves to compare charging behaviour
under different charging conditions.

Instead of comparing charging processes only by voltage thresholds,
the comparison is performed using state-equivalent charge values.

Input
-----
CSV files exported from battery test equipment such as:

- Rohde & Schwarz NGU201
- Sefram DAS60

The CSV file should contain time and voltage/current measurements.

Output
------
The script generates plots showing Δt(Q) differences between
charging conditions.

Plots are saved in:

results/figures/

Author
------
Jiaxing Lu
"""
