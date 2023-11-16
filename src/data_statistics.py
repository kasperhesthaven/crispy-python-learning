"""Module for computing various statistics based on loaded bacteria data."""

# Import necessary libraries
import numpy as np
import colorama


# Initialize colorama for colored terminal text
colorama.init()


def compute_mean_temperature(data: np.ndarray) -> float:
    """Compute and return the mean temperature from the provided data.

    Parameters:
    - data (np.ndarray): A matrix containing rows of data.

    Returns:
    - float: The computed mean temperature.
    """
    return float(np.mean(data[:, 0]))


def compute_mean_growth_rate(data: np.ndarray) -> float:
    """Compute and return the mean growth rate from the provided data.

    Parameters:
    - data (np.ndarray): A matrix containing rows of data.

    Returns:
    - float: The computed mean growth rate.
    """
    return float(np.mean(data[:, 1]))


def compute_filtered_mean_growth_rate(
    data: np.ndarray, temperature_threshold: float, comparison: str
) -> float | str:
    """Compute and return the mean growth rate for temperatures below or above a given threshold.

    Parameters:
    - data (np.ndarray): A matrix containing rows of data.
    - temperature_threshold (float): A float with temperature threshold on which to filter
    - comparison (str): Direction (lower / higher) on which to compare data to threshold

    Returns:
    - float: The computed mean growth rate for data with temperature corresponding to threshold.
    """
    if comparison == "below":
        filtered_data = data[data[:, 0] < temperature_threshold]
    else:
        filtered_data = data[data[:, 0] > temperature_threshold]
    if len(filtered_data) == 0:
        return f"{colorama.Fore.YELLOW}No data available with temperatures {comparison} {temperature_threshold}°C.{colorama.Style.RESET_ALL}"
    return float(np.mean(filtered_data[:, 1]))


def compute_std_temperature(data: np.ndarray) -> float:
    """Compute and return the standard deviation of temperature from the provided data.

    Parameters:
    - data (np.ndarray): A matrix containing rows of data.

    Returns:
    - float: The computed standard deviation of temperature.
    """
    return float(np.std(data[:, 0]))


def compute_std_growth_rate(data: np.ndarray) -> float:
    """Compute and return the standard deviation of growth rate from the provided data.

    Parameters:
    - data (np.ndarray): A matrix containing rows of data.

    Returns:
    - float: The computed standard deviation of growth rate.
    """
    return float(np.std(data[:, 1]))


def count_data_rows(data: np.ndarray) -> int:
    """Return the number of rows in the provided data.

    Parameters:
    - data (np.ndarray): A matrix containing rows of data.

    Returns:
    - int: The number of rows in the data.
    """
    return int(data.shape[0])


# Centralized mapping of options to their respective function calls.
STATISTIC_OPTIONS = {
    "1": {"name": "Mean Temperature", "function": compute_mean_temperature},
    "2": {"name": "Mean Growth Rate", "function": compute_mean_growth_rate},
    "3": {"name": "Std Temperature", "function": compute_std_temperature},
    "4": {"name": "Std Growth Rate", "function": compute_std_growth_rate},
    "5": {"name": "Data Rows", "function": count_data_rows},
    "6": {
        "name": "Mean Cold Growth Rate",
        "function": lambda data: compute_filtered_mean_growth_rate(data, 20, "below"),
    },
    "7": {
        "name": "Mean Hot Growth Rate",
        "function": lambda data: compute_filtered_mean_growth_rate(data, 50, "above"),
    },
}


def dataStatistics(data: np.ndarray, statistic: str) -> str:
    """Compute and return the requested statistic from the provided data.

    Parameters:
    - data (np.ndarray): A matrix containing rows of data
      (temperature, growth rate, and bacteria type).
    - statistic (str): A string specifying the statistic to compute.

    Returns:
    - str: The computed statistic.

    Raises:
    - ValueError: If the provided statistic is not valid.
    """
    # Check if the provided statistic is valid
    if statistic not in [option["name"] for option in STATISTIC_OPTIONS.values()]:
        raise ValueError(f"Invalid statistic: {statistic}")

    # Retrieve the appropriate function from the STATISTIC_OPTIONS and compute the statistic
    for key, value in STATISTIC_OPTIONS.items():
        if value["name"] == statistic:
            result = value["function"](data)
            return str(result)
    # If for some reason the statistic isn't computed, raise an error.
    # This should be unreachable due to the above validation
    raise ValueError(f"Unable to compute statistic: {statistic}")
