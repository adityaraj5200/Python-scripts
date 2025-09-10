"""
Quick test script to verify the key combination and space fixes.
"""

import json
import os

def test_recorded_actions():
    """Test the recorded actions to see if they're properly formatted"""
    if not os.path.exists("actions.json"):
        print("No actions.json found. Please record some actions first.")
        return
    
    with open("actions.json", "r") as f:
        data = json.load(f)
    
    actions = data.get("actions", [])
    print(f"Found {len(actions)} recorded actions")
    
    # Look for combo actions
    combo_actions = [a for a in actions if a.get("type") == "combo"]
    print(f"Found {len(combo_actions)} combo actions:")
    for combo in combo_actions:
        print(f"  - {combo.get('keys', 'N/A')} at time {combo.get('t', 'N/A')}")
    
    # Look for text actions (should include spaces)
    text_actions = [a for a in actions if a.get("type") == "text"]
    print(f"Found {len(text_actions)} text actions:")
    for text in text_actions:
        content = text.get('text', '')
        # Show spaces as [SPACE] for visibility
        display_text = content.replace(' ', '[SPACE]')
        print(f"  - '{display_text}' at time {text.get('t', 'N/A')}")
    
    # Look for individual key actions
    key_actions = [a for a in actions if a.get("type") in ["keyDown", "keyUp"]]
    print(f"Found {len(key_actions)} individual key actions")
    
    # Check for space key actions specifically
    space_actions = [a for a in key_actions if a.get("key") == "SPACE"]
    print(f"Found {len(space_actions)} space key actions")

if __name__ == "__main__":
    print("Testing recorded actions format...")
    test_recorded_actions()
