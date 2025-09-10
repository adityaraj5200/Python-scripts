"""
Test script to verify the scroll intensity fix.
"""

import subprocess
import sys
import json
import os

def test_scroll_intensity():
    """Test if the scroll intensity fix works"""
    print("Testing scroll intensity fix...")
    print("This will replay your recorded scroll actions with enhanced intensity.")
    print("\nThe fix:")
    print("- Original scroll values (dy: -1, 1) are too small for pyautogui")
    print("- Now applying 5x multiplier (dy: -5, 5) for better visibility")
    print("- You can adjust SCROLL_MULTIPLIER in replay_actions.py if needed")
    
    if not os.path.exists("actions.json"):
        print("No actions.json found! Please record some scroll actions first.")
        return False
    
    with open("actions.json", "r") as f:
        data = json.load(f)
    
    actions = data.get("actions", [])
    scroll_actions = [a for a in actions if a.get("type") == "scroll"]
    
    if len(scroll_actions) == 0:
        print("No scroll actions to replay!")
        return False
    
    print(f"\nFound {len(scroll_actions)} scroll actions to replay")
    print("Sample scroll values:")
    for i, scroll in enumerate(scroll_actions[:5]):  # Show first 5
        dy = scroll.get('dy', 0)
        direction = scroll.get('direction', 'unknown')
        enhanced_dy = dy * 5  # Same multiplier as in replay_actions.py
        print(f"  {i+1}. Original dy={dy} -> Enhanced dy={enhanced_dy} ({direction})")
    
    print("\nInstructions:")
    print("1. The replayer will start in 3 seconds")
    print("2. Switch to a window where you can see scrolling")
    print("3. Watch as the enhanced scroll events are replayed")
    print("4. The scrolling should now be much more noticeable!")
    
    input("\nPress Enter when ready to start replaying...")
    
    try:
        subprocess.run([sys.executable, "replay_actions.py"], check=True)
        print("Replay completed!")
        print("\nDid the scrolling feel more intense now?")
        print("If it's still too weak/strong, you can adjust SCROLL_MULTIPLIER in replay_actions.py")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Replay failed: {e}")
        return False
    except KeyboardInterrupt:
        print("Replay interrupted by user")
        return False

if __name__ == "__main__":
    test_scroll_intensity()
