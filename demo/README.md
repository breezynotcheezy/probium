# Probium Anti-Virus Demo

This directory contains simple example programs that demonstrate how to use the
[Probium](../readme.md) API for basic file scanning tasks. These examples are
for educational purposes and not intended to be a complete security solution.

## Contents

- `simple_antivirus.py` – scans a folder and prints the detected file types.
- `drive_monitor.py` – periodically checks for new mounted drives and performs a
  naive scan when they appear.

## Running the examples

```
python simple_antivirus.py /path/to/folder
```

```
python drive_monitor.py
```

Both scripts require the `psutil` package. Install it with `pip install psutil`
if it is not already available.
