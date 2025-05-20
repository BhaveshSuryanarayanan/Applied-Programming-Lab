import matplotlib.pyplot as plt
import numpy as np

# Define the keyboard layout as a list of rows with keys
keyboard_layout = [
    ['ESC', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'PRTSC', 'SCRLK', 'PAUSE'],
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'BACKSPACE'],
    ['TAB', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'],
    ['CAPS', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', '\'', 'ENTER'],
    ['SHIFT', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'SHIFT'],
    ['CTRL', 'WIN', 'ALT', 'SPACE', 'ALT', 'FN', 'CTRL']
]

# Key width multiplier for larger keys
key_size = {
    'BACKSPACE': 2,
    'TAB': 1.5,
    'CAPS': 1.75,
    'ENTER': 2.25,
    'SHIFT': 2.25,
    'SPACE': 6,
    'CTRL': 1.5,
    'WIN': 1.5,
    'ALT': 1.5,
    'FN': 1.2,
}

# Function to draw keyboard layout
def draw_keyboard_layout():
    fig, ax = plt.subplots(figsize=(12, 6))

    x_start = 0
    y_start = 5  # Start higher to leave space for top row (e.g., ESC and function keys)

    # Iterate over each row in the keyboard layout
    for row in keyboard_layout:
        x_pos = x_start
        for key in row:
            width = key_size.get(key, 1)  # Get key width, default is 1 unit

            # Create a rectangle for each key
            rect = plt.Rectangle((x_pos, y_start), width, 1, edgecolor='black', facecolor='lightgray')
            ax.add_patch(rect)
            
            # Add text to the center of the key
            ax.text(x_pos + width / 2, y_start + 0.5, key, ha='center', va='center', fontsize=10)
            
            # Increment x position by the width of the key
            x_pos += width + 0.1  # Add small gap between keys

        # Decrease y position for the next row
        y_start -= 1.1  # Move down for the next row

    # Set limits and hide axes
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 6)
    ax.set_aspect('equal')
    ax.axis('off')  # Hide axes

    plt.title('Keyboard Layout')
    plt.show()

draw_keyboard_layout()
draw_keyboard_layout()