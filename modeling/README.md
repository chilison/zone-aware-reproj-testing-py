# Experiment: Evaluation of Map Projection Distance Errors

## Objective

This experiment compares the accuracy of two map projections — **Equidistant Conic** and **Transverse Mercator** — in terms of distance preservation across different latitudes and reference distances.

## Structure

- `projection.py`: Coordinate transformation functions (UTM, EQDC, TMERC, etc.)
- `simulation.py`: Point generation and reprojection update logic
- `analysis.py`: Error computation and statistical aggregation
- `plotting.py`: Visualization of absolute and relative error plots
- `run.py`: Execution script
- `main.py`: Entry point

## How It Works 🧐

For a range of target maximum reference distances (e.g., 100 km to 1000 km), the experiment:

1. Generates a growing set of points from a central latitude.
2. Converts each point using multiple projections.
3. Calculates geodesic distances and compares them to projected distances.
4. Collects absolute and relative errors for each projection.
5. Repeats the simulation multiple times per setting for statistical stability.
6. Saves a detailed CSV and generates summary plots.

## Installation

Install required dependencies:

```bash
pip install -r requirements.txt
