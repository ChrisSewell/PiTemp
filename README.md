# Raspberry Pi Live Temperature Monitor

This script provides a **live, real-time graph** of your Raspberry Pi's CPU temperature and CPU load directly in the terminal. The graph scrolls dynamically as new data is collected and includes color-coded alerts for temperature thresholds.

I built this for use on my [Hackberry Pi](https://github.com/ZitaoTech/Hackberry-Pi_Zero), but others may find it useful as well. Check out their project for a great hand-held cyberdeck!

## Features

- **Real-Time Temperature Monitoring**: Continuously updates the CPU temperature in real-time.
- **Dynamic Scrolling Graph**: Displays a scrolling graph of the most recent temperature readings.
- **CPU Load Display**: Shows current CPU load percentage.
- **Color-Coded Alerts**:
  - **Green**: Safe temperature.
  - **Yellow**: Warning temperature (close to threshold).
  - **Red**: Temperature exceeds the specified threshold.
- **Pause/Resume Functionality**: Pause and resume the monitoring process.
- **Logging (Optional)**: Logs temperature readings to a file with timestamps if the `--log` argument is provided.
- **Elapsed Time**: Displays the total runtime of the script.
- **Command-Line Arguments**: Customize threshold, log file path, and number of points displayed.

## Requirements

- **Python 3**
- **Dependencies**:
  - `asciichartpy`: For plotting the graph.
  - `psutil`: For fetching CPU load data.

### Installing Dependencies

You can install the required dependencies using the `requirements.txt` file.

1. **Install via `pip`**:

   ```bash
   pip install -r requirements.txt
   ```

2. **Alternatively, Install Manually**:

   ```bash
   pip install asciichartpy psutil
   ```

## Usage

### Running the Script

```bash
python PiTemp.py [OPTIONS]
```

### Command-Line Options

| Option               | Description                                       | Default Value           |
|----------------------|---------------------------------------------------|------------------------|
| `--threshold`        | Temperature threshold for alerts (°C).            | `70.0`                 |
| `--log`              | Path to the log file (optional).                  | None                   |
| `--points`           | Number of points to display on the graph.         | `100`                  |

#### Example Command

```bash
python PiTemp.py --threshold 65.0 --log my_temp_log.txt --points 200
```

### Controls

| Key | Action        |
|-----|---------------|
| `q` | Quit the script. |
| `p` | Pause updates.   |
| `r` | Resume updates.  |

## Output Example

```
Current Temp: 55.2 °C
CPU Load: 32.1%
Threshold: 70.0 °C
Elapsed Time: 00:05:23
RUNNING

    60.0 ┤                            ╭─╮    
    57.5 ┤                       ╭────╯ ╰─╮  
    55.0 ┤                  ╭────╯       ╰╮ 
    52.5 ┤          ╭───────╯             ╰╮
    50.0 ┤      ╭───╯                      ╰
    47.5 ┤  ╭───╯                           

Commands: [q] Quit | [p] Pause | [r] Resume
```

## Logging

Temperature readings will **only be logged** if the `--log` argument is provided. Example log entries:

```
2024-06-15 12:01:23 - 55.2 °C
2024-06-15 12:01:24 - 55.6 °C
2024-06-15 12:01:25 - 56.0 °C
```

