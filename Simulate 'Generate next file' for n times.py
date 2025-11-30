import time
import pyautogui
import pyttsx3

def auto_type_and_press(n, interval=20, buffer_time=10):
    """
    Simulates typing "Next batch" and pressing Enter.
    Repeats n times with a given interval (in seconds).
    buffer_time = time given to switch to the target window.
    """

    total_time = n * interval
    print(f"\nThis simulation process will run for approx {total_time} seconds.\n")
    print(f"Starting automation: {n} cycles, {interval} seconds interval.")
    print(f"You have {buffer_time} seconds to switch to the target window...\n")

    # Countdown for dynamic buffer time
    for i in range(buffer_time, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("\nAutomation started!\n")

    prompt = "Next batch"

    for i in range(1, n + 1):
        pyautogui.typewrite(prompt)
        pyautogui.press("enter")
        print(f"Cycle {i}/{n} completed.")

        if i < n:
            time.sleep(interval)

    print("Automation task completed.")


def speak(status="success"):
    engine = pyttsx3.init()
    messages = {
        "success": "Your Python script has executed successfully",
        "error": "An error occurred in your Python script",
        "warning": "Warning. Please check the output"
    }
    engine.say(messages.get(status, "Task finished"))
    engine.runAndWait()


if __name__ == "__main__":
    # ================
    # USER INPUT AREA
    # ================
    n_times = 14              # Number of repetitions
    interval_seconds = 15    # Interval between repetitions (in seconds)
    buffer_seconds = 10      # ✅ Time to switch tabs/windows

    try:
        auto_type_and_press(n_times, interval_seconds, buffer_seconds)
        speak("success")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("error")
