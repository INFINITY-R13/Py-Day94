"""
Google Dinosaur Game Auto-Player
Uses PyAutoGUI for screenshot capture and keyboard control
Uses PIL for image processing to detect obstacles
"""

import pyautogui
import time
from PIL import ImageGrab
import numpy as np

class DinoGameBot:
    def __init__(self):
        # Disable PyAutoGUI failsafe
        pyautogui.FAILSAFE = False
        
        # Game region coordinates
        self.game_region = None
        self.obstacle_region = None
        
        # Detection threshold
        self.jump_cooldown = 0
        
    def get_screen_region(self):
        """
        Automatically detect game region or use manual calibration
        """
        print("\nCalibration Options:")
        print("1. Auto-detect (recommended - works if game is visible)")
        print("2. Manual calibration")
        
        choice = input("\nEnter choice (1 or 2): ").strip()
        
        if choice == "1":
            return self.auto_calibrate()
        else:
            return self.manual_calibrate()
    
    def auto_calibrate(self):
        """
        Use a fixed region approach - user positions game in center of screen
        """
        print("\n=== AUTO CALIBRATION ===")
        print("1. Open Chrome Dino game (chrome://dino)")
        print("2. Press F11 to go fullscreen OR maximize the window")
        print("3. Make sure the game is visible and centered")
        print("\nPress Enter when ready...")
        input()
        
        # Get screen size
        screen_width, screen_height = pyautogui.size()
        
        # Use center portion of screen for game detection
        # Chrome dino game is typically in the center
        margin = 100
        self.game_region = (margin, margin, screen_width - margin, screen_height - margin)
        
        # Obstacle detection region (right side where obstacles appear)
        width = screen_width - 2 * margin
        height = screen_height - 2 * margin
        
        # Detection zone: middle-right area where obstacles first appear
        self.obstacle_region = (
            margin + width // 3,
            margin + height // 3,
            margin + 2 * width // 3,
            margin + 2 * height // 3
        )
        
        print(f"\nScreen size: {screen_width}x{screen_height}")
        print(f"Detection region: {self.obstacle_region}")
        return True
    
    def manual_calibrate(self):
        """
        Manual calibration by clicking corners
        """
        print("\n=== MANUAL CALIBRATION ===")
        print("You will click two corners of the game area")
        
        print("\nMove mouse to TOP-LEFT corner of game and press Enter...")
        input()
        x1, y1 = pyautogui.position()
        print(f"Top-left: ({x1}, {y1})")
        
        print("\nMove mouse to BOTTOM-RIGHT corner of game and press Enter...")
        input()
        x2, y2 = pyautogui.position()
        print(f"Bottom-right: ({x2}, {y2})")
        
        width = x2 - x1
        height = y2 - y1
        
        if width < 200 or height < 100:
            print(f"\n❌ Region too small: {width}x{height}")
            print("Please select a larger area!")
            return False
        
        self.game_region = (x1, y1, x2, y2)
        
        # Detection region
        self.obstacle_region = (
            x1 + width // 3,
            y1 + height // 3,
            x1 + 2 * width // 3,
            y1 + 2 * height // 3
        )
        
        print(f"\n✓ Calibrated: {width}x{height}")
        return True
        
    def detect_obstacle(self):
        """
        Detect obstacles by checking for dark pixels
        """
        try:
            # Capture detection region
            screenshot = ImageGrab.grab(bbox=self.obstacle_region)
            
            # Convert to grayscale numpy array
            gray = np.array(screenshot.convert('L'))
            
            # Chrome dino: background is light (240-250), obstacles are dark (50-100)
            # Count dark pixels
            dark_threshold = 150
            dark_pixels = np.sum(gray < dark_threshold)
            
            # Calculate percentage of dark pixels
            total_pixels = gray.size
            dark_percentage = (dark_pixels / total_pixels) * 100
            
            # If more than 1% of pixels are dark, obstacle detected
            return dark_percentage > 1.0
            
        except Exception as e:
            print(f"Detection error: {e}")
            return False
        
    def jump(self):
        """Make the dino jump"""
        pyautogui.press('space')
        
    def play(self):
        """Main game loop"""
        if not self.game_region:
            print("❌ Calibration required!")
            return
        
        print("\n" + "="*50)
        print("Starting in 3 seconds...")
        print("Make sure Chrome window is active!")
        print("Press Ctrl+C to stop")
        print("="*50)
        
        time.sleep(3)
        
        # Start the game
        pyautogui.press('space')
        time.sleep(0.5)
        
        print("\n🎮 Bot is playing! Watch the magic...\n")
        
        jump_count = 0
        last_jump_time = 0
        
        try:
            while True:
                current_time = time.time()
                
                # Check for obstacles
                if self.detect_obstacle():
                    # Cooldown to prevent double jumps
                    if current_time - last_jump_time > 0.3:
                        self.jump()
                        jump_count += 1
                        last_jump_time = current_time
                        print(f"Jump #{jump_count}", end="\r")
                
                time.sleep(0.03)  # ~30 FPS check rate
                
        except KeyboardInterrupt:
            print(f"\n\n✓ Stopped! Total jumps: {jump_count}")

def main():
    print("=" * 50)
    print("🦖 Google Dinosaur Game Auto-Player")
    print("=" * 50)
    
    bot = DinoGameBot()
    
    # Calibrate
    while not bot.get_screen_region():
        print("\n❌ Calibration failed. Retrying...\n")
    
    # Play
    bot.play()

if __name__ == "__main__":
    main()
