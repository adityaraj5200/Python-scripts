"""
Test script to verify space handling fix.
This will record a simple text with spaces and check if they're properly included in text actions.
"""

import subprocess
import sys
import json
import os

def test_space_recording():
    """Test if spaces are properly recorded in text actions"""
    print("Testing space recording fix...")
    print("This will record the text: 'Hello World'")
    print("Spaces should be included in text actions, not as separate keyDown/keyUp events.")
    print("\nInstructions:")
    print("1. The recorder will start in 3 seconds")
    print("2. Type exactly: Hello World")
    print("3. Press ESC to stop recording")
    print("4. We'll then check if spaces are properly recorded")
    
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
    
    # Check text actions
    text_actions = [a for a in actions if a.get("type") == "text"]
    print(f"Found {len(text_actions)} text actions:")
    
    all_text = ""
    for text_action in text_actions:
        text_content = text_action.get('text', '')
        all_text += text_content
        # Show spaces as [SPACE] for visibility
        display_text = text_content.replace(' ', '[SPACE]')
        print(f"  - '{display_text}' at time {text_action.get('t', 'N/A')}")
    
    print(f"\nCombined text: '{all_text}'")
    
    # Check for individual space key events
    space_key_events = [a for a in actions if a.get("key") == "SPACE"]
    print(f"Found {len(space_key_events)} individual space key events")
    
    if len(space_key_events) == 0 and ' ' in all_text:
        print("✅ SUCCESS: Spaces are properly included in text actions!")
        return True
    elif len(space_key_events) > 0:
        print("❌ ISSUE: Spaces are still being recorded as individual key events")
        return False
    else:
        print("⚠️  No spaces found in text - did you type spaces?")
        return False

if __name__ == "__main__":
    test_space_recording()
