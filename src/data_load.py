"""This module helps in loading and validating bacteria data from a file."""

# Importing necessary libraries
import numpy as np  # For numerical operations
import colorama  # For colored terminal text

# Initialize colorama for colored terminal text
colorama.init()

# List of valid bacteria codes
VALID_BACTERIA_CODES = [1, 2, 3, 4]


def dataLoad(filename: str):
    """Load data from the given file and validate each row.

    Parameters:
    - filename (str): The path to the data file.

    Returns:
    - np.array: A matrix containing rows of valid data.
    - int: A count of invalid data rows.

    Any errors in the data will be printed to the console.
    """

    # List to store rows of valid data
    valid_data_rows = []

    try:
        # Open and read the file
        with open(filename, "r", encoding="utf-8") as file:
            invalid_data_row_count = 0
            for line_number, line in enumerate(file, start=1):
                # Check for a header line (usually the first line)
                if not any(char.isdigit() for char in line) and line_number == 1:
                    invalid_data_row_count += 1
                    print(
                        f"{colorama.Fore.YELLOW}Error in line {line_number}:{colorama.Style.RESET_ALL} Looks like a header ({line.strip()})"
                    )
                    continue

                # Try to process and validate the data in the current line
                try:
                    temperature, growth_rate, bacteria_code = map(float, line.split())

                    # Check if the temperature is within the valid range
                    if not 10 <= temperature <= 60:
                        raise ValueError(
                            f"Invalid temperature. It must be between 10 and 60 degrees. Found: {temperature}."
                        )

                    # Check if the growth rate is a positive number
                    if growth_rate < 0:
                        raise ValueError(
                            f"Invalid growth rate. It must be a positive number. Found: {growth_rate}."
                        )

                    # Check if the bacteria code is valid
                    if bacteria_code not in VALID_BACTERIA_CODES:
                        raise ValueError(
                            f"Invalid bacteria code. It must be 1, 2, 3, or 4. Found: {bacteria_code}."
                        )

                    # If all checks pass, add the data to our list
                    valid_data_rows.append([temperature, growth_rate, bacteria_code])

                # If there's an error in validation, print it
                except ValueError as error_message:
                    invalid_data_row_count += 1
                    print(
                        f"{colorama.Fore.YELLOW}Error in line {line_number}:{colorama.Style.RESET_ALL}",
                        str(error_message),
                    )

        # Convert our list of valid data rows into a matrix and return
        return np.array(valid_data_rows), invalid_data_row_count

    except FileNotFoundError:
        print(
            f"{colorama.Fore.RED}Error: The file '{filename}' was not found.{colorama.Style.RESET_ALL}"
        )
        return np.array([]), 0  # Return an empty array and 0 invalid data rows

    except Exception as error:
        print(
            f"{colorama.Fore.RED}An unexpected error occurred while loading the data: {error}{colorama.Style.RESET_ALL}"
        )
        return np.array([]), 0  # Return an empty array and 0 invalid data rows
