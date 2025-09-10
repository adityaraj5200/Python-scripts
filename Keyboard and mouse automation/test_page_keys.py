"""
Test script to verify Page Up and Page Down key support.
"""

import subprocess
import sys
import json
import os

def test_page_keys():
    """Test if Page Up and Page Down keys are properly recorded and replayed"""
    print("Testing Page Up and Page Down key support...")
    print("This will test recording and replaying Page Up/Page Down keys.")
    print("\nInstructions:")
    print("1. The recorder will start in 3 seconds")
    print("2. Switch to a window where you can use Page Up/Page Down (like a document or web page)")
    print("3. Press Page Up and Page Down keys several times")
    print("4. Press ESC to stop recording")
    print("5. We'll then check if the keys are properly recorded")
    
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
    
    # Check for Page Up/Page Down actions
    page_actions = [a for a in actions if a.get("key") in ["PAGEUP", "PAGEDOWN"]]
    print(f"Found {len(page_actions)} Page Up/Page Down actions:")
    
    for page_action in page_actions:
        key = page_action.get('key', 'unknown')
        action_type = page_action.get('type', 'unknown')
        timestamp = page_action.get('t', 'N/A')
        print(f"  - {action_type}: {key} at time {timestamp}")
    
    if len(page_actions) > 0:
        print("✅ SUCCESS: Page Up/Page Down keys are properly recorded!")
        
        # Test replay
        print("\nTesting replay...")
        print("Instructions:")
        print("1. The replayer will start in 3 seconds")
        print("2. Switch to a window where you can see Page Up/Page Down effects")
        print("3. Watch as the recorded Page Up/Page Down actions are replayed")
        
        input("\nPress Enter when ready to start replaying...")
        
        try:
            subprocess.run([sys.executable, "replay_actions.py"], check=True)
            print("Replay completed!")
            print("✅ SUCCESS: Page Up/Page Down keys are properly replayed!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Replay failed: {e}")
            return False
        except KeyboardInterrupt:
            print("Replay interrupted by user")
            return False
    else:
        print("❌ ISSUE: No Page Up/Page Down events found - did you press those keys?")
        return False

def test_all_navigation_keys():
    """Test all navigation keys"""
    print("\nTesting all navigation keys...")
    print("This will test: Page Up, Page Down, Home, End, Insert, Delete, Arrow keys")
    
    if not os.path.exists("actions.json"):
        print("No actions.json found! Please record some actions first.")
        return False
    
    with open("actions.json", "r") as f:
        data = json.load(f)
    
    actions = data.get("actions", [])
    
    # Check for various navigation keys
    nav_keys = ["PAGEUP", "PAGEDOWN", "HOME", "END", "INSERT", "DELETE", "UP", "DOWN", "LEFT", "RIGHT"]
    found_keys = {}
    
    for action in actions:
        key = action.get("key", "")
        if key in nav_keys:
            if key not in found_keys:
                found_keys[key] = 0
            found_keys[key] += 1
    
    print(f"Found navigation keys:")
    for key, count in found_keys.items():
        print(f"  - {key}: {count} events")
    
    if found_keys:
        print("✅ SUCCESS: Navigation keys are properly recorded!")
        return True
    else:
        print("❌ No navigation keys found in recorded actions")
        return False

def main():
    print("Page Up/Page Down Key Support Test")
    print("This script will test the Page Up and Page Down key functionality")
    
    # Check if required files exist
    if not os.path.exists("record_actions.py"):
        print("Error: record_actions.py not found!")
        return
    
    if not os.path.exists("replay_actions.py"):
        print("Error: replay_actions.py not found!")
        return
    
    while True:
        print("\nChoose an option:")
        print("1. Test Page Up/Page Down recording and replay")
        print("2. Check recorded navigation keys")
        print("3. View recorded actions.json")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            test_page_keys()
        elif choice == "2":
            test_all_navigation_keys()
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
