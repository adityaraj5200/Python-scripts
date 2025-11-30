import pyautogui
import time
import keyboard
import random

# === Configuration ===
num_clicks = 16          # total number of clicks
base_delay = 2.0      # base delay between clicks (seconds)
delay_jitter = 0.05   # +/- jitter in seconds (i.e., 50ms)
buffer = 5            # wait before clicking starts
stop_key = 'esc'      # emergency stop key

pyautogui.FAILSAFE = True  # move to top-left corner to abort

print(f"Move your mouse to the desired point. Starting in {buffer} seconds...")
time.sleep(buffer)

x, y = pyautogui.position()
print(f"Clicking at ({x}, {y}) {num_clicks} times with random timing. Press '{stop_key}' to stop.\n")

click_count = 0
try:
    for i in range(num_clicks):
        if keyboard.is_pressed(stop_key):
            print(f"\nStopped manually after {click_count} clicks.")
            break

        pyautogui.click()
        click_count += 1

        # Randomized delay
        delay = base_delay + random.uniform(-delay_jitter, delay_jitter)
        time.sleep(max(0, delay))
    else:
        print(f"\nCompleted all {click_count} clicks.")
except pyautogui.FailSafeException:
    print(f"\nFail-safe triggered (mouse moved to corner) after {click_count} clicks.")
except KeyboardInterrupt:
    print(f"\nScript interrupted after {click_count} clicks.")

print("Done.")
