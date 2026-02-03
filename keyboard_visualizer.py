#!/usr/bin/env python3
"""
Keyboard Heatmap Visualizer
Creates visual heatmaps from logged keyboard data.
"""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path
from collections import defaultdict

# Standard QWERTY keyboard layout
KEYBOARD_LAYOUT = {
    'row1': ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
    'row2': ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    'row3': ['caps_lock', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter'],
    'row4': ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'shift'],
    'row5': ['ctrl', 'alt', 'cmd', 'space', 'cmd', 'alt', 'ctrl']
}

# Key widths (for visual spacing)
KEY_WIDTHS = {
    'tab': 1.5,
    'caps_lock': 1.75,
    'enter': 2.25,
    'shift': 2.25,
    'ctrl': 1.25,
    'alt': 1.25,
    'cmd': 1.25,
    'space': 6.25,
    'backspace': 2.0
}

# Key positions for heatmap (row, col)
KEY_POSITIONS = {}

def build_key_positions():
    """Build a dictionary mapping keys to their (row, col) positions."""
    positions = {}
    
    for row_idx, (row_name, keys) in enumerate(KEYBOARD_LAYOUT.items()):
        col = 0
        for key in keys:
            positions[key] = (row_idx, col)
            width = KEY_WIDTHS.get(key, 1.0)
            col += width
    
    return positions

KEY_POSITIONS = build_key_positions()

def load_keyboard_data(log_file='keyboard_log.json'):
    """Load keyboard data from JSON file."""
    if not Path(log_file).exists():
        print(f"Error: {log_file} not found.")
        print("Run keyboard_logger.py first to collect data.")
        return None
    
    with open(log_file, 'r') as f:
        data = json.load(f)
    
    return data

def create_keyboard_heatmap(data, output_file='keyboard_heatmap.png', colormap='hot'):
    """
    Create a visual heatmap of keyboard usage.
    
    Args:
        data: Keyboard usage data
        output_file: Output file path
        colormap: Matplotlib colormap to use
    """
    key_counts = data.get('key_counts', {})
    total_keys = data.get('total_keys', 0)
    
    if total_keys == 0:
        print("No keyboard data to visualize.")
        return
    
    print(f"Creating heatmap from {total_keys} keystrokes...")
    
    # Create figure
    fig, ax = plt.subplots(figsize=(18, 8))
    
    # Calculate max count for normalization
    max_count = max(key_counts.values()) if key_counts else 1
    
    # Draw keyboard
    for row_idx, (row_name, keys) in enumerate(KEYBOARD_LAYOUT.items()):
        col = 0
        
        for key in keys:
            # Get key count
            count = key_counts.get(key, 0)
            
            # Calculate color intensity (0 to 1)
            intensity = count / max_count if max_count > 0 else 0
            
            # Get key width
            width = KEY_WIDTHS.get(key, 1.0)
            height = 1.0
            
            # Choose color based on intensity
            cmap = plt.get_cmap(colormap)
            color = cmap(intensity)
            
            # Draw key rectangle
            rect = patches.Rectangle(
                (col, -row_idx), width * 0.95, height * 0.95,
                linewidth=2, edgecolor='black', facecolor=color, alpha=0.8
            )
            ax.add_patch(rect)
            
            # Add key label
            display_key = key.replace('_', ' ').title() if len(key) > 1 else key.upper()
            
            # Add count if significant
            if count > 0:
                percentage = (count / total_keys) * 100
                label = f"{display_key}\n{count}\n({percentage:.1f}%)"
                fontsize = 8 if len(display_key) > 3 else 10
            else:
                label = display_key
                fontsize = 8 if len(display_key) > 3 else 10
            
            ax.text(
                col + width * 0.5, -row_idx + height * 0.5, label,
                ha='center', va='center', fontsize=fontsize,
                fontweight='bold' if count > max_count * 0.5 else 'normal'
            )
            
            col += width
    
    # Set axis properties
    ax.set_xlim(-0.5, 20)
    ax.set_ylim(-5.5, 0.5)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # Add title
    plt.title('Keyboard Usage Heatmap', fontsize=20, fontweight='bold', pad=20)
    
    # Add statistics
    stats_text = f"Total Keystrokes: {total_keys:,}\n"
    stats_text += f"Unique Keys: {len([k for k, v in key_counts.items() if v > 0])}\n"
    
    # Find most pressed keys
    top_keys = sorted(key_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    stats_text += "\nTop 5 Keys:\n"
    for i, (key, count) in enumerate(top_keys, 1):
        pct = (count / total_keys) * 100
        display_key = key.replace('_', ' ').title() if len(key) > 1 else key.upper()
        stats_text += f"  {i}. {display_key}: {count:,} ({pct:.1f}%)\n"
    
    # Add stats box
    ax.text(
        0.02, 0.98, stats_text, transform=fig.transFigure,
        fontsize=10, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )
    
    # Add colorbar
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=0, vmax=max_count))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.01, aspect=30)
    cbar.set_label('Key Press Count', fontsize=12)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Heatmap saved to {output_file}")
    
    return fig

def create_statistics_chart(data, output_file='keyboard_stats.png'):
    """Create a bar chart of top keys and typing statistics."""
    key_counts = data.get('key_counts', {})
    total_keys = data.get('total_keys', 0)
    
    if total_keys == 0:
        return
    
    # Get top 20 keys
    top_keys = sorted(key_counts.items(), key=lambda x: x[1], reverse=True)[:20]
    
    keys = [k.replace('_', ' ').title() if len(k) > 1 else k.upper() for k, _ in top_keys]
    counts = [c for _, c in top_keys]
    
    # Create figure with subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    # Bar chart
    colors = plt.cm.viridis(np.linspace(0, 1, len(keys)))
    bars = ax1.barh(keys, counts, color=colors)
    ax1.set_xlabel('Number of Presses', fontsize=12)
    ax1.set_title('Top 20 Most Pressed Keys', fontsize=14, fontweight='bold')
    ax1.invert_yaxis()
    
    # Add value labels
    for i, (bar, count) in enumerate(zip(bars, counts)):
        percentage = (count / total_keys) * 100
        ax1.text(count, i, f' {count:,} ({percentage:.1f}%)', 
                va='center', fontsize=9)
    
    # Key categories pie chart
    categories = {
        'Letters': 0,
        'Numbers': 0,
        'Special Keys': 0,
        'Modifiers': 0,
        'Space': 0
    }
    
    for key, count in key_counts.items():
        if key == 'space':
            categories['Space'] += count
        elif key in ['shift', 'ctrl', 'alt', 'cmd', 'tab', 'caps_lock']:
            categories['Modifiers'] += count
        elif key in ['enter', 'backspace', 'delete', 'esc', 'up', 'down', 'left', 'right']:
            categories['Special Keys'] += count
        elif key.isdigit():
            categories['Numbers'] += count
        elif key.isalpha():
            categories['Letters'] += count
        else:
            categories['Special Keys'] += count
    
    # Filter out zero categories
    categories = {k: v for k, v in categories.items() if v > 0}
    
    # Pie chart
    ax2.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%',
            startangle=90, colors=plt.cm.Set3(range(len(categories))))
    ax2.set_title('Key Categories Distribution', fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✓ Statistics chart saved to {output_file}")
    
    return fig

def analyze_typing_patterns(data):
    """Analyze and print detailed typing statistics."""
    key_counts = data.get('key_counts', {})
    total_keys = data.get('total_keys', 0)
    
    print("\n" + "="*60)
    print("KEYBOARD USAGE ANALYSIS")
    print("="*60)
    
    print(f"\n📊 Overall Statistics:")
    print(f"   Total Keystrokes: {total_keys:,}")
    print(f"   Unique Keys Used: {len([k for k, v in key_counts.items() if v > 0])}")
    
    # Calculate hand usage (approximate)
    left_hand_keys = set('qwertasdfgzxcvb12345`')
    right_hand_keys = set('yuiophjklnm67890-=[]\\;\',./') 
    
    left_count = sum(count for key, count in key_counts.items() if key in left_hand_keys)
    right_count = sum(count for key, count in key_counts.items() if key in right_hand_keys)
    other_count = total_keys - left_count - right_count
    
    if total_keys > 0:
        print(f"\n✋ Hand Usage (approximate):")
        print(f"   Left Hand:  {left_count:,} ({left_count/total_keys*100:.1f}%)")
        print(f"   Right Hand: {right_count:,} ({right_count/total_keys*100:.1f}%)")
        print(f"   Other:      {other_count:,} ({other_count/total_keys*100:.1f}%)")
    
    # Top keys
    print(f"\n🔥 Top 10 Most Pressed Keys:")
    top_keys = sorted(key_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    for i, (key, count) in enumerate(top_keys, 1):
        pct = (count / total_keys) * 100
        display_key = key.replace('_', ' ').title() if len(key) > 1 else key.upper()
        print(f"   {i:2d}. {display_key:12s}: {count:8,} ({pct:5.1f}%)")
    
    # Special keys
    special_keys = ['space', 'enter', 'backspace', 'delete', 'tab']
    print(f"\n⌨️  Special Keys:")
    for key in special_keys:
        count = key_counts.get(key, 0)
        if count > 0:
            pct = (count / total_keys) * 100
            display_key = key.replace('_', ' ').title()
            print(f"   {display_key:12s}: {count:8,} ({pct:5.1f}%)")
    
    # Letter frequency
    letters = {k: v for k, v in key_counts.items() if len(k) == 1 and k.isalpha()}
    if letters:
        print(f"\n📝 Most Common Letters:")
        top_letters = sorted(letters.items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (letter, count) in enumerate(top_letters, 1):
            pct = (count / total_keys) * 100
            print(f"   {i:2d}. {letter.upper()}: {count:8,} ({pct:5.1f}%)")
    
    # Modifier keys
    modifiers = ['shift', 'ctrl', 'alt', 'cmd']
    mod_counts = {k: key_counts.get(k, 0) for k in modifiers}
    if any(mod_counts.values()):
        print(f"\n⚙️  Modifier Keys:")
        for key, count in mod_counts.items():
            if count > 0:
                pct = (count / total_keys) * 100
                print(f"   {key.upper():12s}: {count:8,} ({pct:5.1f}%)")
    
    print("\n" + "="*60 + "\n")

def main():
    """Main visualization function."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Visualize keyboard usage data',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 keyboard_visualizer.py                      # Generate all visualizations
  python3 keyboard_visualizer.py --log mydata.json    # Use custom log file
  python3 keyboard_visualizer.py --colormap plasma    # Use different color scheme
  
Available colormaps: hot, viridis, plasma, inferno, magma, cool, autumn
        """
    )
    parser.add_argument('--log', default='keyboard_log.json', 
                       help='Log file path (default: keyboard_log.json)')
    parser.add_argument('--output', default='keyboard_heatmap.png',
                       help='Output heatmap file (default: keyboard_heatmap.png)')
    parser.add_argument('--colormap', default='hot',
                       help='Colormap to use (default: hot)')
    parser.add_argument('--stats-only', action='store_true',
                       help='Only show statistics, no visualizations')
    
    args = parser.parse_args()
    
    # Load data
    data = load_keyboard_data(args.log)
    if data is None:
        return
    
    # Analyze patterns
    analyze_typing_patterns(data)
    
    if not args.stats_only:
        # Create visualizations
        create_keyboard_heatmap(data, args.output, args.colormap)
        create_statistics_chart(data, 'keyboard_stats.png')
        
        print("\n✓ Visualization complete!")
        print(f"  View your heatmap: {args.output}")
        print(f"  View statistics: keyboard_stats.png")

if __name__ == '__main__':
    main()
