#!/usr/bin/env python3
"""
Keyboard Logger
Logs keystrokes to analyze typing patterns and generate heatmaps.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import threading

try:
    from pynput import keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("Error: pynput not installed. Install with: pip install pynput --break-system-packages")

class KeyboardLogger:
    def __init__(self, log_file='keyboard_log.json'):
        self.log_file = log_file
        self.key_counts = defaultdict(int)
        self.total_keys = 0
        self.session_start = datetime.now()
        self.running = False
        self.listener = None
        
        # Load existing data if available
        self.load_data()
    
    def load_data(self):
        """Load existing keyboard data from file."""
        if Path(self.log_file).exists():
            try:
                with open(self.log_file, 'r') as f:
                    data = json.load(f)
                    self.key_counts = defaultdict(int, data.get('key_counts', {}))
                    self.total_keys = data.get('total_keys', 0)
                    print(f"✓ Loaded {self.total_keys} existing keystrokes from {self.log_file}")
            except Exception as e:
                print(f"Warning: Could not load existing data: {e}")
    
    def save_data(self):
        """Save keyboard data to file."""
        data = {
            'key_counts': dict(self.key_counts),
            'total_keys': self.total_keys,
            'last_updated': datetime.now().isoformat(),
            'session_start': self.session_start.isoformat()
        }
        
        try:
            with open(self.log_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def normalize_key(self, key):
        """
        Normalize key representation for consistent counting.
        Returns a string representation of the key.
        """
        try:
            # Handle character keys
            if hasattr(key, 'char') and key.char is not None:
                return key.char.lower()
            
            # Handle special keys
            key_name = str(key).replace('Key.', '')
            
            # Group similar keys
            if key_name in ['shift', 'shift_l', 'shift_r']:
                return 'shift'
            elif key_name in ['ctrl', 'ctrl_l', 'ctrl_r']:
                return 'ctrl'
            elif key_name in ['alt', 'alt_l', 'alt_r', 'alt_gr']:
                return 'alt'
            elif key_name in ['cmd', 'cmd_l', 'cmd_r']:
                return 'cmd'
            else:
                return key_name
                
        except Exception:
            return 'unknown'
    
    def on_press(self, key):
        """Callback for key press events."""
        try:
            normalized_key = self.normalize_key(key)
            
            # Ignore unknown keys
            if normalized_key == 'unknown':
                return
            
            self.key_counts[normalized_key] += 1
            self.total_keys += 1
            
            # Auto-save every 100 keystrokes
            if self.total_keys % 100 == 0:
                self.save_data()
                
        except Exception as e:
            print(f"Error logging key: {e}")
    
    def start(self):
        """Start logging keystrokes."""
        if not PYNPUT_AVAILABLE:
            print("Cannot start: pynput not available")
            return False
        
        print("\n" + "="*60)
        print("Keyboard Logger Started")
        print("="*60)
        print(f"Session start: {self.session_start.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Log file: {self.log_file}")
        print(f"Total keystrokes so far: {self.total_keys}")
        print("\nLogging keystrokes... Press Ctrl+C to stop")
        print("="*60 + "\n")
        
        self.running = True
        
        # Start the keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        
        # Status update thread
        def status_updater():
            last_count = self.total_keys
            while self.running:
                time.sleep(10)  # Update every 10 seconds
                if self.running:
                    new_keys = self.total_keys - last_count
                    if new_keys > 0:
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] Total: {self.total_keys} keys (+{new_keys} in last 10s)")
                    last_count = self.total_keys
        
        status_thread = threading.Thread(target=status_updater, daemon=True)
        status_thread.start()
        
        try:
            # Keep the main thread alive
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()
        
        return True
    
    def stop(self):
        """Stop logging and save data."""
        print("\n\n" + "="*60)
        print("Stopping Keyboard Logger...")
        print("="*60)
        
        self.running = False
        
        if self.listener:
            self.listener.stop()
        
        self.save_data()
        
        duration = datetime.now() - self.session_start
        hours = duration.total_seconds() / 3600
        
        print(f"\n✓ Session completed")
        print(f"  Duration: {duration}")
        print(f"  Total keystrokes: {self.total_keys}")
        if hours > 0:
            print(f"  Average: {self.total_keys / hours:.1f} keys/hour")
        print(f"  Data saved to: {self.log_file}")
        print(f"\nRun 'python3 keyboard_visualizer.py' to generate your heatmap!")
        print("="*60 + "\n")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Log keyboard usage to generate heatmaps',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 keyboard_logger.py                    # Start logging
  python3 keyboard_logger.py --log mydata.json  # Use custom log file
  
After collecting data, run:
  python3 keyboard_visualizer.py                # Generate heatmap
        """
    )
    parser.add_argument('--log', default='keyboard_log.json', 
                       help='Log file path (default: keyboard_log.json)')
    
    args = parser.parse_args()
    
    if not PYNPUT_AVAILABLE:
        print("\n" + "="*60)
        print("ERROR: Required package 'pynput' not installed")
        print("="*60)
        print("\nInstall it with:")
        print("  pip install pynput --break-system-packages")
        print("\nNote: On Linux, you may need additional permissions:")
        print("  sudo usermod -a -G input $USER")
        print("  (then log out and back in)")
        print("="*60 + "\n")
        return
    
    logger = KeyboardLogger(args.log)
    logger.start()

if __name__ == '__main__':
    main()
