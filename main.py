"""Main interactive script for bacteria data analysis.

Provides options to:
- Load data
- Filter data
- Display statistics
- Generate plots
- Quit
"""

import os
import numpy as np
import colorama
from src.data_load import dataLoad
from src.data_statistics import dataStatistics, STATISTIC_OPTIONS
from src.data_plotting import dataPlot



# Initialize colorama for colored terminal text
colorama.init()

BACTERIA_NAMES = {
    1: "Salmonella enterica",
    2: "Bacillus cereus",
    3: "Listeria",
    4: "Brochothrix thermosphacta",
}


def main_menu():
    """Display the main menu and handle user choices."""
    data = None
    active_filters = dict()
    clear_terminal()

    while True:
        print(
            f"\n{colorama.Fore.BLUE}{colorama.Style.BRIGHT}MAIN MENU{colorama.Style.RESET_ALL}"
        )
        print("1: Load data")
        print("2: Filter data")
        print("3: Display statistics")
        print("4: Generate plots")
        print("5: Quit")

        # Display active filters (if any)
        if active_filters and data is not None:
            filtered_data = apply_filters(data, active_filters)
            print(
                f"\n{colorama.Fore.BLUE}{colorama.Style.BRIGHT}FILTERS{colorama.Style.RESET_ALL}"
            )

            if "bacteria" in active_filters:
                print(
                    f"Bacteria Filter: {active_filters['bacteria']} ({BACTERIA_NAMES.get(active_filters['bacteria'], 'Unknown Bacteria')})"
                )
            if "growth_rate_range" in active_filters:
                print(f"Growth Rate Filter: {active_filters['growth_rate_range']}")

            print(f"{len(filtered_data)} data rows matching out of {len(data)}")

        choice = input(
            f"\n{colorama.Style.BRIGHT}Please enter your choice [1-5]: {colorama.Style.RESET_ALL}"
        )

        # Load data
        if choice == "1":
            filename = (
                input(
                    f"\n{colorama.Style.BRIGHT}Enter the file path to your data file (or press Enter for default - 'data/random_sample_data.txt'): {colorama.Style.RESET_ALL}"
                )
                or "data/random_sample_data.txt"
            )
            clear_terminal()
            data = dataLoad(filename)
            if len(data[0]):
                print(
                    f"{colorama.Fore.GREEN}Loaded {len(data[0])} rows of valid data from {filename}.{colorama.Style.RESET_ALL}"
                )
            if data[1] > 0:
                print(f"{colorama.Fore.YELLOW}{data[1]} invalid rows were discarded.")
            data = data[0]

        # Filter data
        elif choice == "2":
            if data is None:
                clear_terminal()
                print(
                    f"\n{colorama.Fore.YELLOW}Please load data first before filtering.{colorama.Style.RESET_ALL}"
                )
                continue
            active_filters = filter_data_menu(active_filters)

        # Display statistics
        elif choice == "3":
            if data is None:
                clear_terminal()
                print(
                    f"\n{colorama.Fore.YELLOW}Please load data first before calculating statistics.{colorama.Style.RESET_ALL}"
                )
                continue

            print(
                f"\n{colorama.Style.BRIGHT}Available statistics:{colorama.Style.RESET_ALL}"
            )
            for key, value in STATISTIC_OPTIONS.items():
                print(f"{key}: {value['name']}")
            statistic_choice = input(
                f"\n{colorama.Style.BRIGHT}Please enter the statistic type number [1-7]: {colorama.Style.RESET_ALL}"
            )

            if statistic_choice in STATISTIC_OPTIONS:
                filtered_data = apply_filters(data, active_filters)
                result = dataStatistics(
                    filtered_data, STATISTIC_OPTIONS[statistic_choice]["name"]
                )
                clear_terminal()
                print(
                    f"{colorama.Fore.GREEN}{colorama.Style.BRIGHT}{STATISTIC_OPTIONS[statistic_choice]['name']}:{colorama.Style.RESET_ALL}{colorama.Fore.GREEN} {result}"
                )

        # Generate plots
        elif choice == "4":
            if data is None:
                clear_terminal()
                print(
                    f"\n{colorama.Fore.YELLOW}Please load data first before generating plots.{colorama.Style.RESET_ALL}"
                )
                continue
            clear_terminal()
            dataPlot(apply_filters(data, active_filters))

        # Exit the program
        elif choice == "5":
            clear_terminal()
            print("Goodbye 👋")
            break

        else:
            print(
                f"{colorama.Fore.YELLOW}Invalid choice. Please select a valid option.{colorama.Style.RESET_ALL}"
            )


def clear_terminal():
    """
    Clear the terminal screen
    """
    # Windows
    if os.name == "nt":
        os.system("cls")
    # macOS and Linux
    else:
        os.system("clear")


def filter_data_menu(active_filters):
    """Display the filter data menu and return selected filters."""

    print(f"\n{colorama.Style.BRIGHT}Filter options:{colorama.Style.RESET_ALL}")
    print("1: By Bacteria Type")
    print("2: By Growth Rate range")
    print("3: Clear filters")
    filter_choice = input(
        f"\n{colorama.Style.BRIGHT}Please enter your filter choice [1-3]: {colorama.Style.RESET_ALL}"
    )

    # Bacteria type filter
    if filter_choice == "1":
        print(f"\n{colorama.Style.BRIGHT}Bacteria Types:{colorama.Style.RESET_ALL}")
        for key, value in BACTERIA_NAMES.items():
            print(f"{key}: {value}")
        bacteria_choice = input(
            f"\n{colorama.Style.BRIGHT}Enter the bacteria type number [1-4] (or press Enter to skip): {colorama.Style.RESET_ALL}"
        )
        if bacteria_choice in ["1", "2", "3", "4"]:
            active_filters["bacteria"] = int(bacteria_choice)
            clear_terminal()
            print(
                f"{colorama.Fore.GREEN}Bacteria Filter set to {int(bacteria_choice)} ({BACTERIA_NAMES.get(int(bacteria_choice))})"
            )

    # Growth rate range filter
    elif filter_choice == "2":
        lower_bound = input(
            f"\n{colorama.Style.BRIGHT}Enter the lower bound for growth rate (or press Enter to skip): {colorama.Style.RESET_ALL}"
        )
        upper_bound = input(
            f"{colorama.Style.BRIGHT}Enter the upper bound for growth rate (or press Enter to skip): {colorama.Style.RESET_ALL}"
        )
        if lower_bound or upper_bound:
            active_filters["growth_rate_range"] = (
                float(lower_bound) if lower_bound else None,
                float(upper_bound) if upper_bound else None,
            )
            clear_terminal()
            print(
                f"{colorama.Fore.GREEN}Growth Rate Filter set to {float(lower_bound) if lower_bound else 0} - {float(upper_bound) if upper_bound else None}"
            )

    # Reset filters
    elif filter_choice == "3":
        clear_terminal()
        print(f"{colorama.Fore.GREEN}All filters have been reset.")
        return dict()

    return active_filters


def apply_filters(data: np.ndarray, active_filters: dict) -> np.ndarray:
    """Apply filters to the data based on the active_filters."""
    if "bacteria" in active_filters:
        data = data[data[:, 2] == active_filters["bacteria"]]
    if "growth_rate_range" in active_filters:
        lower, upper = active_filters["growth_rate_range"]
        if lower:
            data = data[data[:, 1] >= lower]
        if upper:
            data = data[data[:, 1] <= upper]
    return data


if __name__ == "__main__":
    main_menu()
