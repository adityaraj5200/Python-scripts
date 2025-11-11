import pyautogui
import time
import random

pyautogui.FAILSAFE = True  # Move mouse to top-left to stop

def biased_delay(low=0.1, high=0.5):
    # Generate random delay biased toward low values
    # Adjust 'scale' to control how strong the bias is
    delay = random.expovariate(10)  # Mean around 0.1
    return min(high, max(low, delay))

try:
    print("Starting in 3 seconds... (Switch to the target window)")
    time.sleep(3)

    while True:
        pyautogui.hotkey('ctrl', 'z')
        time.sleep(biased_delay())

except pyautogui.FailSafeException:
    print("Stopped by moving mouse to top-left corner.")
except KeyboardInterrupt:
    print("Stopped manually with Ctrl+C.")
