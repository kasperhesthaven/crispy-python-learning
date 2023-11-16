"""Module for generating plots based on bacteria data."""

# Import necessary libraries
import numpy as np  # For numerical operations
import matplotlib.pyplot as plt  # For plotting data

# Names of bacteria corresponding to their codes
BACTERIA_NAMES = {
    1: "Salmonella enterica",
    2: "Bacillus cereus",
    3: "Listeria",
    4: "Brochothrix thermosphacta",
}

COLOR_MAPPING = {
    "Salmonella enterica": "blue",
    "Bacillus cereus": "orange",
    "Listeria": "green",
    "Brochothrix thermosphacta": "red",
}


def plot_bacteria_counts(data: np.ndarray) -> None:
    """Generate a bar plot showing the count of each bacteria type."""

    # Count the occurrences of each bacteria type in the data
    unique_bacteria, counts = np.unique(data[:, 2], return_counts=True)

    # Create a bar plot for each bacteria type
    plt.bar(
        unique_bacteria,
        counts,
        tick_label=[BACTERIA_NAMES[bacteria_code] for bacteria_code in unique_bacteria],
    )

    # Set the title and labels for the plot
    plt.title("Number of Bacteria")
    plt.ylabel("Count")

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=15)

    # Adjust layout for better display
    plt.tight_layout()


def plot_growth_rate_vs_temperature(data: np.ndarray) -> None:
    """Generate a plot showing the growth rate vs temperature for each bacteria type."""

    # For each bacteria type, plot its growth rate against temperature
    for bacteria_code, bacteria_name in BACTERIA_NAMES.items():
        # Filter data for the current bacteria type
        filtered_data = data[data[:, 2] == bacteria_code]

        # Sort filtered data by temperature
        filtered_data = filtered_data[filtered_data[:, 0].argsort()]

        # Plot the filtered data
        color = COLOR_MAPPING[bacteria_name]
        if len(filtered_data) > 0:
            plt.scatter(
                filtered_data[:, 0],
                filtered_data[:, 1],
                label=bacteria_name,
                color=color,
            )

            # Compute the coefficients for a linear fit
            coefficient = np.polyfit(filtered_data[:, 0], filtered_data[:, 1], 1)
            trendline = np.poly1d(coefficient)
            plt.plot(
                filtered_data[:, 0],
                trendline(filtered_data[:, 0]),
                linestyle="--",
                color=color,
            )

    # Set the title, labels, and legend for the plot
    plt.title("Growth Rate by Temperature")
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Growth Rate")
    plt.legend(frameon=False)

    # Add grid lines for reference
    plt.grid(True, which="both", linestyle="--", linewidth=0.75)

    # Set the y-axis to start from 0 and x-axis limits as per given range
    plt.ylim(0)
    plt.xlim([10, 60])

    # Adjust layout for better display
    plt.tight_layout()


def dataPlot(data: np.ndarray) -> None:
    """Generate and displays the two required plots based on the given bacteria data.

    Parameters:
    - data (np.ndarray): An N x 3 matrix containing rows of data.

    Produces:
    - A bar plot showing the number of each bacteria type.
    - A plot displaying growth rate by temperature for each bacteria type.
    """

    plt.style.use("fast")

    # Display the bacteria counts plot
    plt.figure(figsize=(8, 6))
    plot_bacteria_counts(data)
    plt.show()

    # Display the growth rate vs temperature plot
    plt.figure(figsize=(10, 7))
    plot_growth_rate_vs_temperature(data)
    plt.show()
