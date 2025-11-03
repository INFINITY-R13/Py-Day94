# Py-Day94: Google Dinosaur Game Auto-Player 🦖

A Python bot that automatically plays the Chrome Dinosaur Game using computer vision and keyboard automation.

## Features

- Auto-calibration mode for easy setup
- Real-time obstacle detection using image processing
- Smart jump cooldown to prevent double-jumping
- Live jump counter
- Works with fullscreen or windowed mode

## Requirements

- Python 3.7+
- PyAutoGUI
- Pillow (PIL)
- NumPy

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start (Recommended)

1. Open Chrome and navigate to `chrome://dino`
2. Press F11 to go fullscreen (or maximize the window)
3. Run the script:
   ```bash
   python dino_game.py
   ```
4. Choose option 1 (Auto-detect)
5. Press Enter when the game is visible
6. Watch the bot play!
7. Press `Ctrl+C` to stop

### Manual Calibration

If auto-detect doesn't work:

1. Run the script and choose option 2
2. Move mouse to top-left corner of game area, press Enter
3. Move mouse to bottom-right corner of game area, press Enter
4. Bot starts playing automatically

## How It Works

1. **Screen Capture**: Captures the game region using PIL ImageGrab
2. **Obstacle Detection**: Analyzes pixel darkness in detection zone
   - Background pixels are light (240-250)
   - Obstacles are dark (50-100)
   - Triggers jump when >1% of pixels are dark
3. **Jump Action**: Presses spacebar with 0.3s cooldown
4. **Loop**: Checks ~30 times per second for optimal performance

## Tips

- Fullscreen mode (F11) works best for auto-calibration
- Make sure Chrome window is active when bot starts
- The bot shows jump count in real-time
- Works best with default Chrome Dinosaur Game settings

## Troubleshooting

- **Bot not jumping**: Try manual calibration, select a larger game area
- **Too many jumps**: Increase cooldown time in code (line with `0.3`)
- **Missing jumps**: Decrease sleep time in main loop (line with `0.03`)

## Limitations

- Only handles jumping (not ducking for pterodactyls)
- Requires game window to be visible
- Performance depends on CPU speed
