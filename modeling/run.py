from analysis import run_multiple_simulations_by_max_distance
from plotting import plot_error_trends, plot_relative_error_trends


def run_experiment():
    """
    Initiates the multiple simulation run, organizes and saves statistics summary from the results, initiates plot creating.
    """
    df_summary = run_multiple_simulations_by_max_distance(
        start_km=100,
        stop_km=1000,
        step_km=100,
        n_runs_per_setting=500
    )
    df_summary.to_csv("summary.csv", index=False)
    plot_error_trends(df_summary)
    plot_relative_error_trends(df_summary)
