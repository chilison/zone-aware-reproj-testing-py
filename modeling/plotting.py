import matplotlib.pyplot as plt
import seaborn as sns


def plot_error_trends(df):
    """
    Plots the graph of absolute error versus reference distance.
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))

    sns.lineplot(data=df, x="target_max_distance_km", y="avg_eqdc_error_m", label="Equidistant Conic Projection, Mean Absolute Error (m)", marker="o", color="blue")
    sns.lineplot(data=df, x="target_max_distance_km", y="avg_tmerc_error_m", label="Transverse Mercator Projection, Mean Absolute Error (m)", marker="o", color="green")

    sns.lineplot(data=df, x="target_max_distance_km", y="max_eqdc_error_m", label="Equidistant Conic Projection, Max Absolute Error (m)", linestyle="--", marker="x", color="blue")
    sns.lineplot(data=df, x="target_max_distance_km", y="max_tmerc_error_m", label="Transverse Mercator Projection, Max Absolute Error (m)", linestyle="--", marker="x", color="green")

    plt.title("Absolute Error (Mean and Max) VS Reference Distance")
    plt.xlabel("Reference Distance (km)")
    plt.ylabel("Absolute Error (m)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("absolute_error_plot.png")
    plt.show()


def plot_relative_error_trends(df):
    """
    Plots the graph of relative error versus reference distance.
    """
    sns.set(style="whitegrid")
    plt.figure(figsize=(14, 8))

    sns.lineplot(data=df, x="target_max_distance_km", y="avg_eqdc_rel_error_%", label="Equidistant Conic Projection, Mean Relative Error (%)", marker="o", color="blue")
    sns.lineplot(data=df, x="target_max_distance_km", y="avg_tmerc_rel_error_%", label="Transverse Mercator Projection, Mean Relative Error (%)", marker="o", color="green")

    sns.lineplot(data=df, x="target_max_distance_km", y="max_eqdc_rel_error_%", label="Equidistant Conic Projection, Max Relative Error (%)", linestyle="--", marker="x", color="blue")
    sns.lineplot(data=df, x="target_max_distance_km", y="max_tmerc_rel_error_%", label="Transverse Mercator Projection, Max Relative Error (%)", linestyle="--", marker="x", color="green")

    plt.title("Relative Error (Mean and Max) VS Reference Distance")
    plt.xlabel("Reference Distance (km)")
    plt.ylabel("Relative Error (%)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("relative_error_plot.png")
    plt.show()
