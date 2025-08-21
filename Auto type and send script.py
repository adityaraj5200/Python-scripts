import pyautogui
import time

time.sleep(3)  # Give yourself 10 sec to click into the WhatsApp chat

friend_name = "Ishita"

# Send the intro message
pyautogui.typewrite(f"Hey {friend_name}, today I have a lot of time. So today I will send you 'hello' 1000 times 😂")
pyautogui.press("enter")

# Spam hello 1000 times
for i in range(100):
    pyautogui.typewrite(f"hello {i+1}")
    pyautogui.press("enter")
    time.sleep(0.00)  # small delay so it doesn’t overload