"""
Test script to demonstrate key combination recording and replaying.
This script will create a test file with some text, then record actions
that include key combinations like Ctrl+A, Ctrl+C, etc.
"""

import time
import os
import subprocess
import sys

def create_test_file():
    """Create a test file with some content"""
    test_content = """This is a test file for key combination testing.
Line 2: More content here.
Line 3: Even more content for testing.
Line 4: Final line of test content."""
    
    with open("test_content.txt", "w") as f:
        f.write(test_content)
    print("Created test_content.txt with sample text")

def run_recorder():
    """Run the recorder script"""
    print("\n" + "="*50)
    print("KEY COMBINATION RECORDING TEST")
    print("="*50)
    print("Instructions:")
    print("1. The recorder will start in 3 seconds")
    print("2. Switch to a text editor (like Notepad)")
    print("3. Try these key combinations:")
    print("   - Ctrl+A (select all)")
    print("   - Ctrl+C (copy)")
    print("   - Ctrl+V (paste)")
    print("   - Ctrl+Z (undo)")
    print("   - Ctrl+S (save)")
    print("4. Press ESC to stop recording")
    print("="*50)
    
    input("Press Enter when ready to start recording...")
    
    try:
        subprocess.run([sys.executable, "record_actions.py"], check=True)
        print("Recording completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Recording failed: {e}")
    except KeyboardInterrupt:
        print("Recording interrupted by user")

def run_replayer():
    """Run the replayer script"""
    print("\n" + "="*50)
    print("KEY COMBINATION REPLAY TEST")
    print("="*50)
    print("Instructions:")
    print("1. The replayer will start in 3 seconds")
    print("2. Switch to a text editor (like Notepad)")
    print("3. The recorded key combinations will be replayed")
    print("4. Watch as the same actions are performed automatically")
    print("="*50)
    
    input("Press Enter when ready to start replaying...")
    
    try:
        subprocess.run([sys.executable, "replay_actions.py"], check=True)
        print("Replay completed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"Replay failed: {e}")
    except KeyboardInterrupt:
        print("Replay interrupted by user")

def main():
    print("Key Combination Recording/Replay Test")
    print("This script will test the updated recorder and replayer")
    print("with key combinations like Ctrl+A, Ctrl+C, etc.\n")
    
    # Check if required files exist
    if not os.path.exists("record_actions.py"):
        print("Error: record_actions.py not found!")
        return
    
    if not os.path.exists("replay_actions.py"):
        print("Error: replay_actions.py not found!")
        return
    
    create_test_file()
    
    while True:
        print("\nChoose an option:")
        print("1. Record key combinations")
        print("2. Replay recorded actions")
        print("3. View recorded actions.json")
        print("4. Exit")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == "1":
            run_recorder()
        elif choice == "2":
            if not os.path.exists("actions.json"):
                print("No actions.json found! Please record some actions first.")
                continue
            run_replayer()
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
