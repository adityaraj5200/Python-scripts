"""
Test script to verify mouse wheel scroll recording and replaying.
"""

import subprocess
import sys
import json
import os

def test_scroll_recording():
    """Test if mouse wheel scrolls are properly recorded"""
    print("Testing mouse wheel scroll recording...")
    print("This will record mouse wheel scroll events.")
    print("\nInstructions:")
    print("1. The recorder will start in 3 seconds")
    print("2. Switch to a window where you can scroll (like a web page or document)")
    print("3. Scroll up and down with your mouse wheel")
    print("4. Press ESC to stop recording")
    print("5. We'll then check if scroll events are properly recorded")
    
    input("\nPress Enter when ready to start recording...")
    
    try:
        subprocess.run([sys.executable, "record_actions.py"], check=True)
        print("Recording completed!")
    except subprocess.CalledProcessError as e:
        print(f"Recording failed: {e}")
        return False
    except KeyboardInterrupt:
        print("Recording interrupted by user")
        return False
    
    # Check the recorded actions
    if not os.path.exists("actions.json"):
        print("No actions.json found!")
        return False
    
    with open("actions.json", "r") as f:
        data = json.load(f)
    
    actions = data.get("actions", [])
    print(f"\nRecorded {len(actions)} actions")
    
    # Check scroll actions
    scroll_actions = [a for a in actions if a.get("type") == "scroll"]
    print(f"Found {len(scroll_actions)} scroll actions:")
    
    for scroll_action in scroll_actions:
        x = scroll_action.get('x', 0)
        y = scroll_action.get('y', 0)
        dx = scroll_action.get('dx', 0)
        dy = scroll_action.get('dy', 0)
        direction = scroll_action.get('direction', 'unknown')
        timestamp = scroll_action.get('t', 'N/A')
        print(f"  - Scroll {direction} @({x},{y}) dx={dx} dy={dy} at time {timestamp}")
    
    if len(scroll_actions) > 0:
        print("✅ SUCCESS: Mouse wheel scrolls are properly recorded!")
        return True
    else:
        print("❌ ISSUE: No scroll events found - did you scroll with the mouse wheel?")
        return False

def test_scroll_replay():
    """Test if recorded scroll events can be replayed"""
    if not os.path.exists("actions.json"):
        print("No actions.json found! Please record some actions first.")
        return False
    
    with open("actions.json", "r") as f:
        data = json.load(f)
    
    actions = data.get("actions", [])
    scroll_actions = [a for a in actions if a.get("type") == "scroll"]
    
    if len(scroll_actions) == 0:
        print("No scroll actions to replay!")
        return False
    
    print(f"\nTesting scroll replay with {len(scroll_actions)} scroll events...")
    print("Instructions:")
    print("1. The replayer will start in 3 seconds")
    print("2. Switch to a window where you can see scrolling (like a web page)")
    print("3. Watch as the recorded scroll events are replayed")
    
    input("\nPress Enter when ready to start replaying...")
    
    try:
        subprocess.run([sys.executable, "replay_actions.py"], check=True)
        print("Replay completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Replay failed: {e}")
        return False
    except KeyboardInterrupt:
        print("Replay interrupted by user")
        return False

def main():
    print("Mouse Wheel Scroll Recording/Replay Test")
    print("This script will test the mouse wheel scroll functionality")
    
    # Check if required files exist
    if not os.path.exists("record_actions.py"):
        print("Error: record_actions.py not found!")
        return
    
    if not os.path.exists("replay_actions.py"):
        print("Error: replay_actions.py not found!")
        return
    
    while True:
        print("\nChoose an option:")
        print("1. Record mouse wheel scrolls")
        print("2. Replay recorded scroll actions")
        print("3. View recorded actions.json")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            test_scroll_recording()
        elif choice == "2":
            test_scroll_replay()
        elif choice == "3":
            if os.path.exists("actions.json"):
                with open("actions.json", "r") as f:
                    content = f.read()
                print("\nRecorded actions:")
                print(content)
            else:
                print("No actions.json found!")
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-4.")

if __name__ == "__main__":
    main()
