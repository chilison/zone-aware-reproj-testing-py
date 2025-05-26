import math
import pandas as pd
import numpy as np
from .projection import geod
from .simulation import generate_latlon_points, update_all_points


def compute_errors(points):
    """
    Calculates all pairwise Euclidean and geodesic distances, stores their differences as error values.

    Args:
        points (list[]): all generated points.

    Returns:
        errors (list[]): all generated points.
    """
    errors = {"eqdc": [], "tmerc": []}
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            p1, p2 = points[i], points[j]
            _, _, dist_geo = geod.inv(p1["original_lon"], p1["original_lat"], p2["original_lon"], p2["original_lat"])

            dist_eqdc = math.hypot(p2["eqdc_x"] - p1["eqdc_x"], p2["eqdc_y"] - p1["eqdc_y"])
            abs_err_eqdc = abs(dist_geo - dist_eqdc)
            rel_err_eqdc = abs_err_eqdc / dist_geo * 100 if dist_geo else 0
            errors["eqdc"].append((abs_err_eqdc, rel_err_eqdc))

            dist_tmerc = math.hypot(p2["tmerc_x"] - p1["tmerc_x"], p2["tmerc_y"] - p1["tmerc_y"])
            abs_err_tmerc = abs(dist_geo - dist_tmerc)
            rel_err_tmerc = abs_err_tmerc / dist_geo * 100 if dist_geo else 0
            errors["tmerc"].append((abs_err_tmerc, rel_err_tmerc))

    return errors


def run_simulation_until_max_distance(target_max_distance_km, center_lat=35, center_lon=35):
    """
    Calculates the maximum distance between points, decides whether to generate a new batch and reproject.

    Args:
        target_max_distance_km (float): reference maximum distance.
        center_lat (float): latitude of the initial coordinate.
        center_lon (float): longitude of the initial coordinate.
    """
    points = [{"original_lat": center_lat, "original_lon": center_lon}]
    max_distance_m = 0

    while max_distance_m <= target_max_distance_km * 1000:
        last_point = points[-1]
        new_points = generate_latlon_points(last_point["original_lat"], last_point["original_lon"], 1)
        points.extend(new_points)
        update_all_points(points)

        current_max = 0
        for i in range(len(points)):
            for j in range(i + 1, len(points)):
                p1, p2 = points[i], points[j]
                _, _, dist_geo = geod.inv(p1["original_lon"], p1["original_lat"], p2["original_lon"], p2["original_lat"])
                current_max = max(current_max, dist_geo)
        max_distance_m = current_max

    errors = compute_errors(points)

    return {
        "num_points": len(points),
        "max_distance_m": max_distance_m,
        "errors": errors
    }


def run_multiple_simulations_by_max_distance(start_km=100, stop_km=1000, step_km=100, n_runs_per_setting=100):
    """
    Initiates the simulation run, organizes and saves statistics from the results.

    Args:
        start_km (float): initial reference maximal distance.
        stop_km (float): last reference maximal distance.
        step (float): incremental step between start and end values.
        n_runs_per_setting (int): number of runs per reference maximal distance.

    Returns:
        pandas.DataFrame: statistics summary.
    """
    summary_rows = []
    detailed_rows = []

    for target_max_distance_km in range(start_km, stop_km + 1, step_km):
        print(f"\nProcessing target max distance {target_max_distance_km} km...")

        center_lat = 75

        for run_idx in range(n_runs_per_setting):
            if run_idx % 10 == 0:
                print(f"  ➔ Run #{run_idx+1}")

            stats = run_simulation_until_max_distance(target_max_distance_km, center_lat)

            eqdc_abs_errors = [x[0] for x in stats["errors"]["eqdc"]]
            eqdc_rel_errors = [x[1] for x in stats["errors"]["eqdc"]]
            tmerc_abs_errors = [x[0] for x in stats["errors"]["tmerc"]]
            tmerc_rel_errors = [x[1] for x in stats["errors"]["tmerc"]]

            detailed_rows.append({
                "target_max_distance_km": target_max_distance_km,
                "run": run_idx + 1,
                "center_lat": center_lat,
                "max_distance_m": stats["max_distance_m"],
                "avg_eqdc_error_m": np.mean(eqdc_abs_errors),
                "max_eqdc_error_m": np.max(eqdc_abs_errors),
                "avg_eqdc_rel_error_%": np.mean(eqdc_rel_errors),
                "max_eqdc_rel_error_%": np.max(eqdc_rel_errors),
                "avg_tmerc_error_m": np.mean(tmerc_abs_errors),
                "max_tmerc_error_m": np.max(tmerc_abs_errors),
                "avg_tmerc_rel_error_%": np.mean(tmerc_rel_errors),
                "max_tmerc_rel_error_%": np.max(tmerc_rel_errors),
            })

            center_lat -= 0.2

        df = pd.DataFrame([r for r in detailed_rows if r["target_max_distance_km"] == target_max_distance_km])
        summary_rows.append({
            "target_max_distance_km": target_max_distance_km,
            "avg_max_distance_m": df["max_distance_m"].mean(),
            "avg_eqdc_error_m": df["avg_eqdc_error_m"].mean(),
            "std_eqdc_error_m": df["avg_eqdc_error_m"].std(),
            "max_eqdc_error_m": df["max_eqdc_error_m"].max(),
            "avg_eqdc_rel_error_%": df["avg_eqdc_rel_error_%"].mean(),
            "std_eqdc_rel_error_%": df["avg_eqdc_rel_error_%"].std(),
            "max_eqdc_rel_error_%": df["max_eqdc_rel_error_%"].max(),
            "avg_tmerc_error_m": df["avg_tmerc_error_m"].mean(),
            "std_tmerc_error_m": df["avg_tmerc_error_m"].std(),
            "max_tmerc_error_m": df["max_tmerc_error_m"].max(),
            "avg_tmerc_rel_error_%": df["avg_tmerc_rel_error_%"].mean(),
            "std_tmerc_rel_error_%": df["avg_tmerc_rel_error_%"].std(),
            "max_tmerc_rel_error_%": df["max_tmerc_rel_error_%"].max(),
        })

    pd.DataFrame(detailed_rows).to_csv("all_runs.csv", index=False)
    return pd.DataFrame(summary_rows)
