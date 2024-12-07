import curses
import subprocess
import time
import asciichartpy
import psutil
from collections import deque
import argparse
import statistics

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Live Raspberry Pi Temperature Monitor")
parser.add_argument("--threshold", type=float, default=70.0, help="Temperature threshold for alerts (default: 70.0°C)")
parser.add_argument("--log", type=str, help="Path to log file (optional)")
parser.add_argument("--points", type=int, default=100, help="Number of points to display on the graph (default: 100)")
args = parser.parse_args()
THRESHOLD = args.threshold
LOG_FILE = args.log
MAX_POINTS = args.points

# Initialize data storage
temps = deque(maxlen=MAX_POINTS)  # Store temperature readings
start_time = time.time()  # Track script start time

# Function to get the temperature
def get_temp():
    try:
        result = subprocess.run(
            ['vcgencmd', 'measure_temp'],
            capture_output=True,
            text=True,
            timeout=2
        )
        temp_str = result.stdout.strip().split('=')[1].replace("'C", "")
        return float(temp_str)
    except Exception as e:
        return None

# Function to get the CPU load
def get_cpu_load():
    return psutil.cpu_percent(interval=0.1)

# Function to log temperature to file if logging is enabled
def log_temperature(temp):
    if LOG_FILE:
        with open(LOG_FILE, "a") as log_file:
            log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {temp} °C\n")

# Function to draw the graph using asciichartpy
def draw_graph(stdscr, temps, cpu_load, paused):
    stdscr.clear()
    height, width = stdscr.getmaxyx()

    # Initialize colors
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1)   # Green for safe temps
    curses.init_pair(2, curses.COLOR_YELLOW, -1)  # Yellow for warning temps
    curses.init_pair(3, curses.COLOR_RED, -1)     # Red for high temps
    curses.init_pair(4, curses.COLOR_CYAN, -1)    # Cyan for CPU load
    curses.init_pair(5, curses.COLOR_WHITE, -1)   # White for normal text

    # Display current temp and CPU load info
    if temps:
        current_temp = temps[-1]
        elapsed_time = time.strftime("%H:%M:%S", time.gmtime(time.time() - start_time))

        # Choose color based on temperature
        if current_temp < THRESHOLD - 5:
            temp_color = curses.color_pair(1)  # Green
        elif current_temp < THRESHOLD:
            temp_color = curses.color_pair(2)  # Yellow
        else:
            temp_color = curses.color_pair(3)  # Red

        stdscr.addstr(0, 0, f"Current Temp: ", curses.color_pair(5))
        stdscr.addstr(f"{current_temp:.1f} °C", temp_color)

        stdscr.addstr(1, 0, f"CPU Load: ", curses.color_pair(5))
        stdscr.addstr(f"{cpu_load:.1f}%", curses.color_pair(4))

        stdscr.addstr(2, 0, f"Threshold: {THRESHOLD} °C", curses.color_pair(5))
        stdscr.addstr(3, 0, f"Elapsed Time: {elapsed_time}", curses.color_pair(5))
        stdscr.addstr(4, 0, f"{'PAUSED' if paused else 'RUNNING'}", curses.color_pair(5))

        # Display alert if the latest temperature exceeds the threshold
        if current_temp > THRESHOLD:
            stdscr.addstr(5, 0, "ALERT: High Temperature!", curses.color_pair(3) | curses.A_BOLD | curses.A_REVERSE)

        # Calculate dynamic min and max for the graph with buffers
        min_temp = min(temps)
        max_temp = max(temps)

        # Add buffers to min and max temperatures
        buffer = 5
        min_temp_bound = max(min_temp - buffer, 0)
        max_temp_bound = max_temp + buffer

        # Ensure a reasonable range if temps are very close
        if max_temp_bound - min_temp_bound < 10:
            max_temp_bound = min_temp_bound + 10

        # Determine the number of points to display based on terminal width
        graph_width = width - 10
        temp_slice = list(temps)[-graph_width:]

        # Plot temperatures using asciichartpy
        chart = asciichartpy.plot(temp_slice, {'height': height - 10, 'min': min_temp_bound, 'max': max_temp_bound})
        for i, line in enumerate(chart.split("\n")):
            if i + 7 < height:
                stdscr.addstr(i + 7, 0, line)

    else:
        stdscr.addstr(0, 0, "No temperature data available.", curses.color_pair(3))

    # Display command options at the bottom
    commands = "Commands: [q] Quit | [p] Pause | [r] Resume"
    stdscr.addstr(height - 2, 0, commands, curses.color_pair(4))

    stdscr.refresh()

# Main function for curses
def main(stdscr):
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(True)  # Make getch non-blocking
    stdscr.timeout(1000)  # Refresh every 1 second

    paused = False

    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = True
        elif key == ord('r'):
            paused = False

        if not paused:
            temp = get_temp()
            if temp is not None:
                temps.append(temp)
                log_temperature(temp)

            cpu_load = get_cpu_load()
        else:
            cpu_load = get_cpu_load()  # Keep updating CPU load even when paused

        draw_graph(stdscr, temps, cpu_load, paused)

# Run the curses application and display summary on exit
try:
    curses.wrapper(main)
finally:
    print("\nMonitoring stopped.")

