# Traceroute Analyzer

## Overview
Traceroute Analyzer is a Python-based GUI application that performs network traceroute analysis and visualizes the results. It uses `tkinter` for the user interface, `subprocess` to execute traceroute commands, and `matplotlib` for graphical representation of network hops.

## Features
- Runs traceroute on three predefined destinations: `bbc.co.uk`, `amazon.com`, and `google.com`.
- Displays traceroute results in a structured table format.
- Plots the average Round-Trip Time (RTT) for each hop.
- Provides a combined graph to analyze multiple traceroute results.
- Dark-themed UI for better readability.

## Requirements
Ensure you have the following dependencies installed before running the application:

```bash
pip install matplotlib
```

## Usage
1. Run the script:
   ```bash
   python traceroute_analyzer.py
   ```
2. Click the "Start Trace" button on any tab to begin a traceroute analysis for that destination.
3. View the results in the table and graph sections.
4. Navigate to the "Combined Graph" tab to see a consolidated view of recent traceroute analyses.

## File Structure
- `traceroute_analyzer.py` - Main application script.

## Notes
- The script detects the OS and uses `tracert` on Windows and `traceroute -I` on Linux/macOS.
- Admin privileges may be required to run traceroute on some systems.

## License
This project is open-source and can be modified or distributed under the MIT License.

