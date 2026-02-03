# Keyboard Heatmap Generator

Track your keyboard usage and generate beautiful heatmaps showing which keys you press most often.

## Features

- 🎹 Log all keyboard activity in the background
- 🔥 Generate visual heatmaps of key usage
- 📊 Detailed statistics and analysis
- 📈 Bar charts and pie charts for key categories
- 💾 Persistent data storage (accumulates over time)
- 🎨 Multiple color schemes available

## Requirements

Install the required Python packages:

```bash
pip install pynput numpy matplotlib --break-system-packages
```

### System-Specific Setup

**Linux:**
You may need to add your user to the `input` group for keyboard access:
```bash
sudo usermod -a -G input $USER
# Log out and back in for changes to take effect
```

**macOS:**
You may be prompted to grant accessibility permissions the first time you run the logger.

**Windows:**
Usually works without additional setup. You may need to run as administrator.

## Usage

### Step 1: Collect Keyboard Data

Start logging your keyboard usage:

```bash
python3 keyboard_logger.py
```

The logger will:
- Run in the background
- Save data every 100 keystrokes
- Display periodic status updates
- Continue until you press Ctrl+C

**Tips:**
- Run it during your normal work day
- Let it collect at least 1000+ keystrokes for meaningful results
- The longer you collect, the more accurate your heatmap
- You can stop and restart anytime - data accumulates

**Example session:**
```
============================================================
Keyboard Logger Started
============================================================
Session start: 2024-02-04 09:00:00
Log file: keyboard_log.json
Total keystrokes so far: 0

Logging keystrokes... Press Ctrl+C to stop
============================================================

[09:10:00] Total: 234 keys (+234 in last 10s)
[09:20:00] Total: 567 keys (+333 in last 10s)
[09:30:00] Total: 1023 keys (+456 in last 10s)
```

Press **Ctrl+C** when you want to stop.

### Step 2: Generate Heatmap

Create visualizations from your collected data:

```bash
python3 keyboard_visualizer.py
```

This will generate:
- A keyboard heatmap showing usage intensity
- Statistics charts with top keys
- Detailed analysis in the terminal

**Advanced options:**

```bash
# Use custom log file
python3 keyboard_visualizer.py --log mydata.json

# Use different color scheme
python3 keyboard_visualizer.py --colormap plasma

# Only show statistics (no images)
python3 keyboard_visualizer.py --stats-only

# Custom output filename
python3 keyboard_visualizer.py --output my_heatmap.png
```

### Available Color Schemes

Try different colormaps for your heatmap:
- `hot` - Red/orange/yellow (default)
- `viridis` - Purple to yellow
- `plasma` - Purple to pink to yellow
- `inferno` - Black to red to yellow
- `magma` - Black to purple to white
- `cool` - Cyan to magenta
- `autumn` - Red to yellow

Example:
```bash
python3 keyboard_visualizer.py --colormap viridis
```

## Output Files

- `keyboard_log.json` - Your keystroke data (can be backed up/shared)
- `keyboard_heatmap.png` - Visual heatmap of your keyboard
- `keyboard_stats.png` - Charts showing top keys and categories

## Understanding the Heatmap

The heatmap shows:
- **Color intensity**: Darker/brighter = more frequently pressed
- **Key labels**: Show the key name and press count
- **Percentages**: Show what % of total keystrokes each key represents
- **Statistics box**: Shows total keystrokes and top 5 keys

## Analysis Features

The visualizer provides:

1. **Overall Statistics**
   - Total keystrokes
   - Unique keys used
   
2. **Hand Usage**
   - Left vs right hand distribution (approximate)
   
3. **Top Keys**
   - Most pressed keys with counts and percentages
   
4. **Special Keys Analysis**
   - Space, Enter, Backspace, Tab usage
   
5. **Letter Frequency**
   - Most common letters you type
   
6. **Modifier Keys**
   - Shift, Ctrl, Alt, Cmd usage

## Privacy Notes

⚠️ **Important Privacy Information:**

- The logger captures ALL keystrokes including passwords
- Data is stored locally in `keyboard_log.json`
- No data is sent anywhere - it's 100% local
- Be careful who has access to your log files
- Consider excluding sensitive work sessions
- You can delete `keyboard_log.json` anytime to clear data

**Recommendations:**
- Don't run during password entry
- Don't share your log files publicly
- Review log files before sharing insights
- Use this tool responsibly

## Use Cases

- **Optimize keyboard layout**: See if ergonomic layouts might help
- **Identify repetitive strain**: Find overused keys
- **Improve typing habits**: Notice patterns in your typing
- **Ergonomics analysis**: Understand hand distribution
- **Productivity insights**: Analyze work patterns
- **Keyboard shopping**: Choose keyboards with durable keys for your most-used letters

## Example Workflow

```bash
# 1. Install dependencies
pip install pynput numpy matplotlib --break-system-packages

# 2. Start logging (leave running during work)
python3 keyboard_logger.py

# ... do your normal work for a few hours ...
# Press Ctrl+C when done

# 3. Generate visualizations
python3 keyboard_visualizer.py --colormap plasma

# 4. View your results
# Open keyboard_heatmap.png and keyboard_stats.png
```

## Troubleshooting

**"pynput not installed"**
```bash
pip install pynput --break-system-packages
```

**Linux: "Permission denied"**
```bash
sudo usermod -a -G input $USER
# Then log out and back in
```

**macOS: "Accessibility permissions"**
- Go to System Preferences → Security & Privacy → Privacy → Accessibility
- Add Terminal or your Python interpreter to the allowed apps

**Windows: Not capturing all keys**
- Try running as administrator
- Some system keys may be protected

**"No keyboard data to visualize"**
- Make sure you ran `keyboard_logger.py` first
- Check that `keyboard_log.json` exists
- Verify the file isn't empty

## Data Format

The `keyboard_log.json` file structure:

```json
{
  "key_counts": {
    "a": 342,
    "space": 892,
    "enter": 234,
    ...
  },
  "total_keys": 8234,
  "last_updated": "2024-02-04T15:30:00",
  "session_start": "2024-02-04T09:00:00"
}
```

You can manually edit counts or merge data from multiple sessions.

## Tips for Best Results

1. **Collect longer**: 5000+ keystrokes give great results
2. **Multiple days**: Combine data from several work sessions
3. **Representative usage**: Capture typical work patterns
4. **Clean data**: Delete the log and restart if you want fresh data
5. **Backup logs**: Save interesting datasets before resetting

## Limitations

- Password-protected apps may block keylogging
- Some system keys might not be captured
- Accuracy varies by operating system
- Hand usage calculation is approximate
- Virtual keyboards aren't tracked

## Advanced: Multiple Sessions

To track different contexts separately:

```bash
# Work session
python3 keyboard_logger.py --log work_keys.json

# Gaming session  
python3 keyboard_logger.py --log gaming_keys.json

# Generate separate heatmaps
python3 keyboard_visualizer.py --log work_keys.json --output work_heatmap.png
python3 keyboard_visualizer.py --log gaming_keys.json --output gaming_heatmap.png
```

## Example Analysis Output

```
============================================================
KEYBOARD USAGE ANALYSIS
============================================================

📊 Overall Statistics:
   Total Keystrokes: 8,234
   Unique Keys Used: 52

✋ Hand Usage (approximate):
   Left Hand:  3,456 (42.0%)
   Right Hand: 4,123 (50.1%)
   Other:      655 (7.9%)

🔥 Top 10 Most Pressed Keys:
    1. Space       :      892 ( 10.8%)
    2. E           :      567 (  6.9%)
    3. T           :      456 (  5.5%)
    4. O           :      421 (  5.1%)
    5. I           :      389 (  4.7%)
...
```

## License

Free to use and modify for personal use. No warranty provided.

## Safety Reminder

Always use keyboard logging ethically and legally. Only log your own keyboard activity with your explicit consent. Never use this to monitor others without their knowledge and permission.
