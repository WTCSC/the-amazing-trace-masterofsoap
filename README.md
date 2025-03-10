# Traceroute Analysis Tool

## Overview
This project analyzes network routing using **traceroute** and Python. It helps visualize the paths that packets take to reach a destination, making it useful for troubleshooting network latency and routing issues.

## Features
- Executes a **traceroute** to a specified destination.
- Parses the raw output into a structured format.
- Generates a **visual representation** of the route.
- Supports error handling for timeouts and unreachable hosts.

## Prerequisites
Before running the project, ensure you have:
- **Python 3.8+** installed.
- **Linux** (or use Vagrant for a consistent environment).
- **Vagrant** and **VirtualBox** (if using a VM).
- `pytest` for testing (install with `pip install pytest`).

## Installation & Setup
### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/traceroute-analysis.git
cd traceroute-analysis
```

### 2️⃣ Setup Vagrant (Optional)
If running in a virtual environment:
```bash
vagrant up
vagrant ssh
cd /vagrant
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

## Usage
### Run Traceroute Analysis
```bash
python3 amazing-trace.py <destination>
```
Example:
```bash
python3 amazing-trace.py google.com
```

### Expected Output
- **Raw Traceroute Output** (printed to terminal)
- **Parsed Data** (formatted as a structured list)
- **Visualization** (saved in `output/` directory)

## Code Breakdown
### `execute_traceroute(destination)`
- Runs the `traceroute` command using Python’s `subprocess` module.
- Returns raw output.

### `parse_traceroute(traceroute_output)`
- Uses **regular expressions** to extract hop data.
- Returns a structured list of dictionaries with:
  - **Hop Number**
  - **IP Address**
  - **Hostname** (if available)
  - **Round-Trip Times (RTT)**

## Testing
Run unit tests to verify the parsing function:
```bash
pytest test_amazing_trace.py
```

## Troubleshooting
**Permission Issues?**
Try running with `sudo`:
```bash
sudo python3 amazing-trace.py google.com
```

**Traceroute Not Found?**
Install it:
```bash
sudo apt install traceroute  # Debian/Ubuntu
yum install traceroute       # CentOS/RHEL
```

## Future Improvements
- Add **GeoIP lookup** to display locations of hops.
- Implement a **web interface** for visualizations.
- Store results in a **database** for historical analysis.

---

🚀 **Happy Tracing!**

