
import threading
import random
import string
import time

from pynput.keyboard import Controller as KeyController, Key, Listener as KeyListener
from pynput.mouse import Controller as MouseController, Button, Listener as MouseListener


class AutomationEngine:
    BUTTON_MAP = { "Left": Button.left, "Right": Button.right, "Middle": Button.middle, }

    def __init__(self, log_callback=None, on_stop_callback=None, screen_size=(1920, 1080)):
        self.keyboard = KeyController()
        self.mouse = MouseController()
        self.log = log_callback or (lambda msg: None)
        self.on_stop_callback = on_stop_callback or (lambda: None)
        self.screen_size = screen_size

        self.running = False
        self.threads = []

        self.key_listener = None
        self.mouse_listener = None

        self._last_commanded_pos = None
        self._ignore_until = 0.0

    # ---- public control --------------------------------------------------
    def start(self, settings):
        if self.running:
            return
        self.running = True
        self.settings = settings

        if settings["key_enabled"]:
            t = threading.Thread(target=self._key_loop, daemon=True)
            self.threads.append(t)
            t.start()

        if settings["move_enabled"]:
            t = threading.Thread(target=self._move_loop, daemon=True)
            self.threads.append(t)
            t.start()

        if settings["click_enabled"]:
            t = threading.Thread(target=self._click_loop, daemon=True)
            self.threads.append(t)
            t.start()

        self.key_listener = KeyListener(on_press=self._on_key_press)
        self.key_listener.start()

        self.mouse_listener = MouseListener(on_move=self._on_mouse_move)
        self.mouse_listener.start()

        self.log("Started. Press ESC or move the mouse yourself to stop.")

    def stop(self, reason="Stopped by user"):
        if not self.running:
            return
        self.running = False
        self.threads = []
        if self.key_listener:
            self.key_listener.stop()
            self.key_listener = None
        if self.mouse_listener:
            self.mouse_listener.stop()
            self.mouse_listener = None
        self.log(reason)
        self.on_stop_callback()

    def _on_key_press(self, key):
        if key == Key.esc:
            self.stop("Stopped: ESC pressed")

    def _on_mouse_move(self, x, y):
        if not self.running:
            return
        now = time.time()
        if now < self._ignore_until:
            return                                   # caused by us, ignore
        if self._last_commanded_pos is not None:
            cx, cy = self._last_commanded_pos
            if abs(x - cx) > 2 or abs(y - cy) > 2:
                self.stop("Stopped: manual mouse movement detected")
        else:
            self.stop("Stopped: manual mouse movement detected")

    def _sleep_interval(self, seconds):
        end = time.time() + seconds
        while self.running and time.time() < end:
            time.sleep(min(0.05, end - time.time()))

    def _key_loop(self):
        charset = self._build_charset(self.settings["key_charsets"])
        if not charset:
            self.log("Key feature: no character set selected, skipping.")
            return
        interval = self.settings["key_interval"]
        while self.running:
            char = random.choice(charset)
            try:
                self.keyboard.press(char)
                self.keyboard.release(char)
                self.log(f"Pressed key: {char!r}")
            except Exception as e:
                self.log(f"Key press error: {e}")
            self._sleep_interval(interval)

    def _move_loop(self):
        interval = self.settings["move_interval"]
        screen_w, screen_h = self.screen_size
        while self.running:
            x = random.randint(0, max(0, screen_w - 1))
            y = random.randint(0, max(0, screen_h - 1))
            self._ignore_until = time.time() + 0.3
            self.mouse.position = (x, y)
            self._last_commanded_pos = (x, y)
            self.log(f"Moved mouse to ({x}, {y})")
            self._sleep_interval(interval)

    def _click_loop(self):
        button = self.BUTTON_MAP[self.settings["click_button"]]
        interval = self.settings["click_interval"]
        while self.running:
            self.mouse.click(button)
            self.log(f"Clicked: {self.settings['click_button']}")
            self._sleep_interval(interval)

    #helper
    @staticmethod
    def _build_charset(options):
        charset = ""
        if options.get("letters"):
            charset += string.ascii_letters
        if options.get("numbers"):
            charset += string.digits
        if options.get("special"):
            charset += "!@#$%^&*()-_=+[]{};:,.<>/?"
        return charset
