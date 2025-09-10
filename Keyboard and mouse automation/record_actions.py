
"""
record_actions.py
- Saves to actions.json (in same folder).
- 3s buffer before starting so you can switch windows.
- Press ESC to stop and save.
"""
import time, json, logging, threading
from pynput import keyboard, mouse

logging.basicConfig(format='[%(asctime)s] %(message)s', level=logging.INFO)

OUT_FILE="actions.json"
TEXT_GAP_THRESHOLD=0.5   # seconds: group printable chars into one "text" action
CLICK_DEBOUNCE=0.05      # seconds: ignore very-fast duplicate clicks

KEY_NAME_MAP={
    'space':'SPACE','tab':'TAB','enter':'ENTER','backspace':'BACKSPACE',
    'shift':'SHIFT','ctrl_l':'CTRL','ctrl_r':'CTRL','alt_l':'ALT','alt_r':'ALT',
    'esc':'ESC','page_up':'PAGEUP','page_down':'PAGEDOWN',
    'up':'UP','down':'DOWN','left':'LEFT','right':'RIGHT',
    'home':'HOME','end':'END','insert':'INSERT','delete':'DELETE'
}

def is_printable(key):
    # Check if key has a character and it's printable
    if hasattr(key, 'char') and key.char is not None:
        return True
    # Also treat space as printable (it's a special case)
    if hasattr(key, 'name') and key.name == 'space':
        return True
    return False

def key_name(key):
    # Return readable name for special keys or the char for printable keys
    if is_printable(key):
        # Special case for space key
        if hasattr(key, 'name') and key.name == 'space':
            return ' '
        return key.char
    return getattr(key, 'name', str(key))

def normalize_key_name(key_name):
    """Normalize key names for consistent handling"""
    # Handle control characters (Ctrl+A becomes 'a', Ctrl+C becomes 'c', etc.)
    if len(key_name) == 1 and ord(key_name) < 32:
        # Control character - convert to corresponding letter
        return chr(ord(key_name) + 96)  # \u0001 -> 'a', \u0002 -> 'b', etc.
    return key_name

class Recorder:
    def __init__(self, out_path=OUT_FILE):
        self.out_path=out_path
        self.actions=[]
        self.text_buffer=[]  # list of (char, timestamp)
        self.lock=threading.Lock()
        self.start_time=None
        self.last_click_time=0.0
        self.pressed_keys=set()  # track currently pressed keys for combo detection
        self.combo_buffer=[]  # buffer for potential key combinations

    def _now(self):
        return time.time()

    def _flush_text(self):
        if not self.text_buffer:
            return
        text=''.join(ch for ch,_ in self.text_buffer)
        ts=self.text_buffer[0][1]-self.start_time
        self.actions.append({"type":"text","text":text,"t":round(ts,3)})
        logging.info("Recorded text: %r", text)
        self.text_buffer.clear()

    def _record_special_key(self, name):
        self._flush_text()
        ts=self._now()-self.start_time
        token=KEY_NAME_MAP.get(name,name.upper())
        self.actions.append({"type":"key","key":token,"t":round(ts,3)})
        logging.info("Recorded key: %s", token)

    def _is_modifier_key(self, key_name):
        """Check if a key is a modifier (Ctrl, Alt, Shift, etc.)"""
        modifiers = {'ctrl_l', 'ctrl_r', 'alt_l', 'alt_r', 'shift_l', 'shift_r', 'cmd', 'cmd_l', 'cmd_r'}
        return key_name in modifiers

    def _check_for_combo(self, key_name, timestamp):
        """Check if the current key press forms a combination with pressed modifiers"""
        if len(self.pressed_keys) >= 2:  # At least one modifier + current key
            modifiers = [k for k in self.pressed_keys if self._is_modifier_key(k)]
            if modifiers and not self._is_modifier_key(key_name):
                # We have a key combination
                normalized_key = normalize_key_name(key_name)
                combo_keys = sorted(modifiers) + [normalized_key]
                combo_str = '+'.join(KEY_NAME_MAP.get(k, k.upper()) for k in combo_keys)
                ts = timestamp - self.start_time
                self.actions.append({"type":"combo","keys":combo_str,"t":round(ts,3)})
                logging.info("Recorded combo: %s", combo_str)
                return True
        return False

    def on_press(self, key):
        if key==keyboard.Key.esc:
            logging.info("ESC pressed -> stopping recorder.")
            return False

        ts=self._now()
        name=key_name(key)

        with self.lock:
            # Add key to pressed keys set
            self.pressed_keys.add(name)
            
            if is_printable(key):
                # Get the character (handle space specially)
                if hasattr(key, 'name') and key.name == 'space':
                    ch = ' '
                else:
                    ch = key.char
                # Check if this forms a combo with modifiers
                if self._check_for_combo(name, ts):
                    # Combo was recorded, don't add to text buffer
                    pass
                else:
                    # Normal text handling with gap threshold
                    if self.text_buffer and (ts - self.text_buffer[-1][1]) <= TEXT_GAP_THRESHOLD:
                        self.text_buffer.append((ch, ts))
                    else:
                        self._flush_text()
                        self.text_buffer.append((ch, ts))
            else:
                self._flush_text()
                # Check if this forms a combo with modifiers
                if not self._check_for_combo(name, ts):
                    # Only record individual key if it's not part of a combo
                    normalized_name = normalize_key_name(name)
                    self.actions.append({"type":"keyDown","key":normalized_name.upper(),"t":round(ts-self.start_time,3)})
                    logging.info("Recorded keyDown: %s", normalized_name)

    def on_release(self, key):
        """Handle key release events"""
        name = key_name(key)
        with self.lock:
            # Remove key from pressed keys set
            self.pressed_keys.discard(name)
            
            # Only record keyUp for non-combo keys
            if not self._is_modifier_key(name):
                ts = self._now()
                normalized_name = normalize_key_name(name)
                self.actions.append({"type":"keyUp","key":normalized_name.upper(),"t":round(ts-self.start_time,3)})
                logging.info("Recorded keyUp: %s", normalized_name)
        
        if key == keyboard.Key.esc:
            return False

    def on_click(self, x, y, button, pressed):
        if not pressed:
            return
        ts = self._now()
        if ts - self.last_click_time < CLICK_DEBOUNCE:
            return
        self.last_click_time = ts
        with self.lock:
            self._flush_text()
            rel_t = ts - self.start_time if self.start_time else 0.0
            act={"type":"click","x":int(x),"y":int(y),"button":str(button).split('.')[-1],"t":round(rel_t,3)}
            self.actions.append(act)
            logging.info("Recorded click @(%d,%d) button=%s",int(x),int(y),act["button"])

    def on_scroll(self, x, y, dx, dy):
        """Handle mouse wheel scroll events"""
        ts = self._now()
        with self.lock:
            self._flush_text()
            rel_t = ts - self.start_time if self.start_time else 0.0
            # Determine scroll direction
            direction = "up" if dy > 0 else "down"
            act = {
                "type": "scroll",
                "x": int(x),
                "y": int(y),
                "dx": int(dx),
                "dy": int(dy),
                "direction": direction,
                "t": round(rel_t, 3)
            }
            self.actions.append(act)
            logging.info("Recorded scroll @(%d,%d) direction=%s dx=%d dy=%d", 
                        int(x), int(y), direction, int(dx), int(dy))

    def run(self):
        logging.info("Switch to target window/tab. Recording starts in 3 seconds...")
        time.sleep(3.0)
        self.start_time=self._now()
        logging.info("Recording started. Press ESC to stop and save.")

        kb_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        ms_listener = mouse.Listener(on_click=self.on_click, on_scroll=self.on_scroll)
        kb_listener.start()
        ms_listener.start()

        # block until keyboard listener stops (ESC)
        kb_listener.join()
        # ensure mouse listener stops too
        try:
            ms_listener.stop()
            ms_listener.join(timeout=0.5)
        except Exception:
            pass

        # finalise and write JSON
        with self.lock:
            self._flush_text()
            out = {"meta":{"recorded_at":round(time.time(),3),"start_time":round(self.start_time,3)},"actions":self.actions}
            with open(self.out_path,"w",encoding="utf-8") as f:
                json.dump(out,f,indent=2)
        logging.info("Saved %d actions to %s", len(self.actions), self.out_path)
        logging.info("Done.")

if __name__=="__main__":
    Recorder().run()
