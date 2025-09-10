"""
replay_actions.py
- Reads actions.json and replays actions.
- 3s buffer before starting so you can switch to the target window/tab.
- Preserves recorded time gaps between actions.
- Moves mouse instantly to recorded click coordinates and clicks.
"""
import time, json, logging
import pyautogui

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

IN_FILE="actions.json"
# small default char-interval while typing (keeps typing fast)
CHAR_INTERVAL=0.01

# Scroll intensity multiplier - adjust this to make scrolling more/less noticeable
SCROLL_MULTIPLIER = 5

# map recorded tokens back to pyautogui names
REPLAY_KEY_MAP={
    'TAB':'tab','ENTER':'enter','BACKSPACE':'backspace','SPACE':'space',
    'SHIFT':'shift','CTRL':'ctrl','ALT':'alt','CTRL_L':'ctrl','CTRL_R':'ctrl',
    'ALT_L':'alt','ALT_R':'alt','SHIFT_L':'shift','SHIFT_R':'shift',
    'PAGEUP':'pageup','PAGEDOWN':'pagedown','UP':'up','DOWN':'down',
    'LEFT':'left','RIGHT':'right','HOME':'home','END':'end',
    'INSERT':'insert','DELETE':'delete'
}

# fail-safe: moving mouse to top-left aborts pyautogui actions
pyautogui.FAILSAFE=True
pyautogui.PAUSE=0  # no built-in pause between pyautogui calls

class Replayer:
    def __init__(self,in_path=IN_FILE):
        with open(in_path,"r",encoding="utf-8") as f:
            data=json.load(f)
        self.actions=data.get("actions",[])
        logging.info("Loaded %d actions from %s", len(self.actions), in_path)

    def run(self):
        if not self.actions:
            logging.info("No actions to replay. Exiting.")
            return
        logging.info("Switch to target window/tab. Replay starts in 3 seconds...")
        time.sleep(3.0)
        logging.info("Starting replay. DO NOT move mouse or type if you want deterministic results.")
        prev_t=0.0
        try:
            for act in self.actions:
                act_t = act.get("t", 0.0)
                gap = act_t - prev_t
                if gap > 0:
                    time.sleep(gap)   # preserve recorded gap

                typ = act.get("type")
                if typ=="text":
                    txt = act.get("text","")
                    logging.info("Typing text: %r", txt)
                    pyautogui.typewrite(txt, interval=CHAR_INTERVAL)
                elif typ=="key":
                    token = act.get("key","")
                    keyname = REPLAY_KEY_MAP.get(token, token.lower())
                    logging.info("Pressing key: %s", keyname)
                    try:
                        pyautogui.press(keyname)
                    except Exception as e:
                        logging.warning("pyautogui.press failed for %s: %s", keyname, e)
                elif typ=="combo":
                    keys_str = act.get("keys","")
                    logging.info("Pressing key combination: %s", keys_str)
                    try:
                        # Parse combo string like "CTRL+A" into individual keys
                        keys = keys_str.split('+')
                        # Convert to pyautogui format
                        pyautogui_keys = []
                        for key in keys:
                            pyautogui_key = REPLAY_KEY_MAP.get(key, key.lower())
                            pyautogui_keys.append(pyautogui_key)
                        # Press all keys simultaneously
                        pyautogui.hotkey(*pyautogui_keys)
                    except Exception as e:
                        logging.warning("pyautogui.hotkey failed for %s: %s", keys_str, e)
                elif typ=="click":
                    x=int(act.get("x",0)); y=int(act.get("y",0)); btn=act.get("button","left")
                    logging.info("Moving to (%d,%d) and clicking (%s)", x, y, btn)
                    pyautogui.moveTo(x,y,duration=0)  # instant jump
                    pyautogui.click(button=btn)
                elif typ=="scroll":
                    x=int(act.get("x",0)); y=int(act.get("y",0))
                    dx=int(act.get("dx",0)); dy=int(act.get("dy",0))
                    direction=act.get("direction","down")
                    
                    # Apply scroll multiplier for better visibility
                    # pyautogui.scroll() needs larger values than pynput records
                    enhanced_dy = dy * SCROLL_MULTIPLIER
                    
                    logging.info("Moving to (%d,%d) and scrolling %s (original dy=%d, enhanced dy=%d)", 
                                x, y, direction, dy, enhanced_dy)
                    pyautogui.moveTo(x,y,duration=0)  # instant jump
                    pyautogui.scroll(enhanced_dy)  # Use enhanced scroll value
                elif typ=="keyDown":
                    # Handle individual key down events
                    key = act.get("key","")
                    keyname = REPLAY_KEY_MAP.get(key, key.lower())
                    logging.info("Key down: %s", keyname)
                    try:
                        pyautogui.keyDown(keyname)
                    except Exception as e:
                        logging.warning("pyautogui.keyDown failed for %s: %s", keyname, e)
                elif typ=="keyUp":
                    # Handle individual key up events
                    key = act.get("key","")
                    keyname = REPLAY_KEY_MAP.get(key, key.lower())
                    logging.info("Key up: %s", keyname)
                    try:
                        pyautogui.keyUp(keyname)
                    except Exception as e:
                        logging.warning("pyautogui.keyUp failed for %s: %s", keyname, e)
                else:
                    logging.warning("Unknown action type: %s", typ)

                prev_t = act_t
        except pyautogui.FailSafeException:
            logging.warning("PyAutoGUI failsafe triggered (mouse moved to corner). Aborting replay.")
        logging.info("Replay finished.")

if __name__=="__main__":
    num_times_to_run = 1
    for _ in range(num_times_to_run):
        Replayer().run()
        time.sleep(1.0)
