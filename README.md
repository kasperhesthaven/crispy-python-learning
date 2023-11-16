# Bacteria Analysis

A Python-based program for analyzing growth rates of different bacteria at varying temperatures.

## Usage

Run the main script to start the interactive program:

```bash
python main.py
```

Follow the on-screen prompts and choose inputs using numbers to load data, filter data, display statistics, generate plots, or quit the program.

## Data Format

Data should be provided in a space-separated format with columns for Temperature, Growth rate, and Bacteria.

- The Temperature must be a number between 10 and 60.
- The Growth rate must be a positive number.
- The Bacteria must be a number between 1 and 4 corresponding to one of the four mentioned in the list above.

For example:

```python
23 0.02 1
12 0.73 2
48 0.84 2
23 0.34 3
17 0.42 4
60 0.52 3
48 0.96 3
12 1.31 3
...
```

**Bacteria codes:**

1. Salmonella enterica
2. Bacillus cereus
3. Listeria
4. Brochothrix thermosphacta
