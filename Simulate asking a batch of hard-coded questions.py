import time
import pyautogui
import pyttsx3

# =====================
# QUESTIONS ARRAY
# =====================
questions = [
    "How is the safety of a thread achieved?",
    "What is difference between start() and run() method of thread class?",
    "What is Thread Group? Why it's advised not to use it?",
    "How do you stop a thread in java?",
    "Can we call run() method of a Thread class?",
    "What is difference between Yield and Sleep method in Java?",
    "What is Java Thread Dump, How can we get Java Thread dump of a Program?",
    "What will happen if we don’t override Thread class run() method?",
    "What is difference between the Thread class and Runnable interface for creating a Thread?",
    "What does join() method?",
    "What is race-condition?",
    "What is Lock interface in Java Concurrency API? What is the Difference between ReentrantLock and Synchronized?",
    "What is the difference between the Runnable and Callable interface?",
    "What is the Thread's interrupt flag? How does it relate to the InterruptedException?",
    "What is Java Memory Model (JMM)? Describe its purpose and basic ideas.",
    "Describe the conditions of livelock and starvation.",
    "How do I share a variable between 2 Java threads?",
    "What are the main components of concurrency API?",
    "What is Semaphore in Java concurrency?",
    "What is Callable and Future in Java concurrency?",
    "What is blocking method in Java?",
    "What is atomic variable in Java?",
    "What is Executors Framework?",
    "What are the available implementations of ExecutorService in the standard library?",
    "What kind of thread is the Garbage collector thread?",
    "How can we pause the execution of a Thread for specific time?",
    "What is difference between Executor.submit() and Executer.execute() method?",
    "What is Phaser in Java concurrency?",
    "How to stop a Thread in Java?",
    "Why implementing Runnable is better than extending thread?",
    "Tell me about join() and wait() methods?",
    "How to implement thread-safe code without using the synchronized keyword?"
]


def auto_type_and_press(interval=20, buffer_time=10):
    """
    Types each item from the questions list and presses Enter.
    interval = wait time between each question
    buffer_time = time given to switch to the target window
    """

    total_time = len(questions) * interval
    print(f"\nThis simulation will run for approx {total_time} seconds or {total_time/60:.2f} minutes.\n")
    print(f"Typing {len(questions)} questions with {interval} seconds interval.")
    print(f"You have {buffer_time} seconds to switch to the target window...\n")

    # Countdown
    for i in range(buffer_time, 0, -1):
        print(f"Starting in {i}...", end="\r")
        time.sleep(1)

    print("\nAutomation started!\n")

    # Loop through questions
    for i, question in enumerate(questions, start=1):
        pyautogui.typewrite(question)
        pyautogui.press("enter")

        print(f"Typed question {i}/{len(questions)}")

        if i < len(questions):
            time.sleep(interval)

    print("All questions typed successfully!")


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

    # ======================
    # USER INPUT AREA
    # ======================
    interval_seconds = 30    # Interval between questions (in seconds)
    buffer_seconds = 10

    try:
        auto_type_and_press(interval_seconds, buffer_seconds)
        speak("success")
    except Exception as e:
        print(f"An error occurred: {e}")
        speak("error")
