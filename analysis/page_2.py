import os
import matplotlib.pyplot as plt


def plot_top_stations(current_df):
    """
    Generate a horizontal bar chart showing the
    Top 10 stations by bike availability percentage.
    Stations with zero capacity are excluded because
    bike availability percentage is undefined.
    """

    # Exclude stations with zero capacity
    top_stations = current_df[
        current_df["capacity"] > 0
    ].copy()

    if top_stations.empty:
        return None

    top_stations["availability_ratio"] = (
        top_stations["num_bikes_available"]
        / top_stations["capacity"]
    ) * 100

    top_stations = (
        top_stations
        .sort_values(
            by="availability_ratio",
            ascending=False
        )
        .head(10)
        .copy()
    )

    top_stations["display_name"] = (
        top_stations["name"]
        .str.slice(0, 35)
    )

    os.makedirs(
        "reports/charts",
        exist_ok=True
    )

    chart_path = (
        "reports/charts/top10_availability_ratio.png"
    )

    plt.figure(figsize=(10, 6))

    plt.barh(
        top_stations["display_name"],
        top_stations["availability_ratio"]
    )

    plt.gca().invert_yaxis()

    plt.title(
        "Top 10 Stations by Bike Availability (%)"
    )

    plt.xlabel("Bike Availability (%)")

    plt.ylabel("Station")

    max_ratio = top_stations["availability_ratio"].max()

    plt.xlim(
        0,
        max(100, max_ratio + 5)
    )

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path


def plot_bike_distribution(current_df):
    """
    Generate a histogram showing the distribution
    of bike availability percentages across stations.
    Stations with zero capacity are excluded because
    bike availability percentage is undefined.
    """

    distribution_df = current_df[
        current_df["capacity"] > 0
    ].copy()

    if distribution_df.empty:
        return None

    distribution_df["availability_ratio"] = (
        distribution_df["num_bikes_available"]
        / distribution_df["capacity"]
    ) * 100

    os.makedirs(
        "reports/charts",
        exist_ok=True
    )

    chart_path = (
        "reports/charts/bike_availability_distribution.png"
    )

    plt.figure(figsize=(8, 6))

    plt.hist(
        distribution_df["availability_ratio"],
        bins=10,
        edgecolor="black"
    )

    plt.title(
        "Distribution of Bike Availability (%)"
    )

    plt.xlabel("Bike Availability (%)")

    plt.ylabel("Number of Stations")

    max_ratio = distribution_df["availability_ratio"].max()

    plt.xlim(
        0,
        max(100, max_ratio + 5)
    )

    plt.tight_layout()

    plt.savefig(
        chart_path,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    return chart_path


def get_page2_data(current_df):
    """
    Generate all charts required for Page 2.
    Note:
    Stations with zero capacity are excluded only from
    percentage-based calculations because bike
    availability percentage cannot be computed.
    """

    top_station_chart = plot_top_stations(
        current_df
    )

    distribution_chart = plot_bike_distribution(
        current_df
    )

    return {
        "top_station_chart": top_station_chart,
        "distribution_chart": distribution_chart,
        "excluded_zero_capacity": int(
            (current_df["capacity"] == 0).sum()
        )
    }