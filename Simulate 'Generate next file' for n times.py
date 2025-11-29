import time
import pyautogui

def auto_type_and_press(n, interval=20):
    """
    Simulates typing "generate next file" and pressing Enter.
    Repeats n times with a given interval (in seconds).
    """

    print(f"\nThis simulation process will end in {n * interval} seconds.\n")
    print(f"Starting automation: {n} cycles, {interval} seconds interval.")
    print("You have 5 seconds to switch to the target window...")
    time.sleep(5)

    for i in range(1, n + 1):
        pyautogui.typewrite("Generate next file")
        pyautogui.press("enter")
        print(f"Cycle {i}/{n} completed.")

        if i < n:
            time.sleep(interval)

    print("Automation task completed.")


if __name__ == "__main__":
    # ================
    # USER INPUT AREA
    # ================
    n_times = 10        # Number of repetitions
    interval_seconds = 30   # Interval between repetitions (in seconds)

    auto_type_and_press(n_times, interval_seconds)
