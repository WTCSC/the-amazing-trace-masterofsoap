import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Function to execute traceroute
def execute_traceroute(destination):
    try:
        command = ["tracert", destination] if subprocess.os.name == "nt" else ["traceroute", "-I", destination]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

# Function to parse traceroute output
def parse_traceroute(traceroute_output):
    hops = []
    for line in traceroute_output.split("\n"):
        match = re.match(r"\s*(\d+)\s+([\d\.]+|\*)\s+(\S+)?\s+([\d\.]+ ms)?\s+([\d\.]+ ms)?\s+([\d\.]+ ms)?", line)
        if match:
            hop = int(match.group(1))
            ip = match.group(2) if match.group(2) != "*" else None
            hostname = match.group(3) if match.group(3) != ip else None
            rtts = [float(x.split()[0]) if x else None for x in match.groups()[3:]]
            hops.append({"hop": hop, "ip": ip, "hostname": hostname, "rtt": rtts})
    return hops

# Function to update the table with parsed data
def update_table(tree, data):
    tree.delete(*tree.get_children())  # Clear previous data
    for hop in data:
        rtt_avg = round(sum(filter(None, hop["rtt"])) / len(hop["rtt"]), 2) if any(hop["rtt"]) else "N/A"
        tree.insert("", "end", values=(hop["hop"], hop["ip"], hop["hostname"], rtt_avg))

# Function to plot RTT graph
def plot_graph(frame, data, title="Traceroute RTT Analysis", color="cyan"):
    x = [hop["hop"] for hop in data]
    y = [round(sum(filter(None, hop["rtt"])) / len(hop["rtt"]), 2) if any(hop["rtt"]) else 0 for hop in data]

    fig, ax = plt.subplots(facecolor="#1e1e1e")
    ax.plot(x, y, marker="o", linestyle="-", color=color, label=title)
    ax.set_xlabel("Hop Number", color="white")
    ax.set_ylabel("Average RTT (ms)", color="white")
    ax.set_title(title, color="white")
    ax.legend()
    ax.tick_params(colors="white")
    ax.set_facecolor("#2b2b2b")

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Function to plot combined graph
def plot_combined_graph(frame, all_data):
    fig, ax = plt.subplots(facecolor="#1e1e1e")
    colors = ["cyan", "lime", "magenta"]

    for i, data in enumerate(all_data):
        if not data:
            continue  # Skip empty data
        x = [hop["hop"] for hop in data]
        y = [round(sum(filter(None, hop["rtt"])) / len(hop["rtt"]), 2) if any(hop["rtt"]) else 0 for hop in data]
        ax.plot(x, y, marker="o", linestyle="-", color=colors[i], label=f"Trace {i+1}")

    ax.set_xlabel("Hop Number", color="white")
    ax.set_ylabel("Average RTT (ms)", color="white")
    ax.set_title("Combined Traceroute Analysis", color="white")
    ax.legend()
    ax.tick_params(colors="white")
    ax.set_facecolor("#2b2b2b")

    for widget in frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Function to run traceroute and update UI
def run_traceroute(destination, tree, graph_frame, status_label, results_storage, combined_graph_frame):
    status_label.config(text=f"Tracing {destination}...", foreground="cyan")
    raw_output = execute_traceroute(destination)

    if "Error" in raw_output:
        messagebox.showerror("Traceroute Error", raw_output)
        status_label.config(text=f"Failed to trace {destination}", foreground="red")
        return

    parsed_data = parse_traceroute(raw_output)

    # Update UI safely from the main thread
    root.after(0, lambda: update_table(tree, parsed_data))
    root.after(0, lambda: plot_graph(graph_frame, parsed_data, title=f"RTT for {destination}"))

    # Store the data for the combined graph
    results_storage.append(parsed_data)
    if len(results_storage) > 3:  # Keep only the latest 3 results
        results_storage.pop(0)

    root.after(0, lambda: plot_combined_graph(combined_graph_frame, results_storage))

    status_label.config(text=f"Trace complete: {destination}", foreground="lime")

# Function to start traceroute in a thread
def start_traceroute(destination, tree, graph_frame, status_label, results_storage, combined_graph_frame):
    threading.Thread(target=lambda: run_traceroute(destination, tree, graph_frame, status_label, results_storage, combined_graph_frame), daemon=True).start()

# GUI Setup
root = tk.Tk()
root.title("Traceroute Analyzer")
root.geometry("900x600")
root.configure(bg="#1e1e1e")

# Apply dark theme
style = ttk.Style()
style.theme_use("clam")
style.configure("Dark.TFrame", background="#1e1e1e")
style.configure("Treeview", background="#2b2b2b", foreground="white", fieldbackground="#2b2b2b")
style.configure("Treeview.Heading", background="#1e1e1e", foreground="white")
style.configure("TLabel", background="#1e1e1e", foreground="white")
style.configure("TButton", background="#444", foreground="white", padding=5)
style.map("TButton", background=[("active", "#666")])

notebook = ttk.Notebook(root)

# Define destinations and data storage
destinations = ["bbc.co.uk", "amazon.com", "google.com"]
tables = []
graph_frames = []
status_labels = []
results_storage = [[] for _ in range(3)]

frames = [ttk.Frame(notebook, style="Dark.TFrame") for _ in range(4)]

# Create 3 tabs for individual traces
for i, frame in enumerate(frames[:3]):
    notebook.add(frame, text=destinations[i])

    status_label = ttk.Label(frame, text="Waiting to start...", style="TLabel")
    status_label.pack(pady=5)
    status_labels.append(status_label)

    table = ttk.Treeview(frame, columns=("Hop", "IP", "Hostname", "Avg RTT"), show="headings", style="Treeview")
    for col in ("Hop", "IP", "Hostname", "Avg RTT"):
        table.heading(col, text=col)
        table.column(col, anchor="center")
    table.pack(fill=tk.BOTH, expand=True)
    tables.append(table)

    graph_frame = ttk.Frame(frame, style="Dark.TFrame")
    graph_frame.pack(fill=tk.BOTH, expand=True)
    graph_frames.append(graph_frame)

    start_button = ttk.Button(frame, text="Start Trace", command=lambda i=i: start_traceroute(destinations[i], tables[i], graph_frames[i], status_labels[i], results_storage, frames[3]))
    start_button.pack(pady=5)

# Combined Graph Tab
notebook.add(frames[3], text="Combined Graph")
combined_graph_frame = ttk.Frame(frames[3], style="Dark.TFrame")
combined_graph_frame.pack(fill=tk.BOTH, expand=True)

notebook.pack(expand=True, fill="both")
root.mainloop()
