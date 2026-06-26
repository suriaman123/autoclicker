
import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QTimer

from engine import AutomationEngine

UI_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "autoclicker.ui")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(UI_FILE, self)

        screen = QApplication.primaryScreen().size()
        self.engine = AutomationEngine(
            log_callback=self.log,
            on_stop_callback=self.on_engine_stopped,
            screen_size=(screen.width(), screen.height()),
        )

        self.countdown_value = 0
        self.countdown_timer = QTimer(self)
        self.countdown_timer.timeout.connect(self._tick_countdown)

        self.startButton.clicked.connect(self.begin_countdown)
        self.stopButton.clicked.connect(self.stop_now)


    def log(self, message):
        QTimer.singleShot(0, lambda: self._append_log(message))

    def _append_log(self, message):
        self.logText.append(message)

    #countdown
    def begin_countdown(self):
        settings = self._read_settings()
        if settings is None:
            return                                  # validation failed

        self._pending_settings = settings
        self.countdown_value = 3
        self.countdownLabel.setText(str(self.countdown_value))
        self.startButton.setEnabled(False)
        self.statusLabel.setText("Get ready...")
        self.countdown_timer.start(1000)

    def _tick_countdown(self):
        self.countdown_value -= 1
        if self.countdown_value <= 0:
            self.countdown_timer.stop()
            self.countdownLabel.setText("")
            self._start_engine()
        else:
            self.countdownLabel.setText(str(self.countdown_value))

    def _start_engine(self):
        self.logText.clear()
        self.engine.start(self._pending_settings)
        self.stopButton.setEnabled(True)
        self.statusLabel.setText("Running...")

    # settings 
    def _read_settings(self):
        key_enabled = self.checkKeyEnabled.isChecked()
        move_enabled = self.checkMoveEnabled.isChecked()
        click_enabled = self.checkClickEnabled.isChecked()

        if not (key_enabled or move_enabled or click_enabled):
            QMessageBox.warning(self, "Nothing enabled", "Enable at least one feature first.")
            return None

        if key_enabled and not (
            self.checkLetters.isChecked()
            or self.checkNumbers.isChecked()
            or self.checkSpecial.isChecked()
        ):
            QMessageBox.warning(
                self, "No character type", "Select at least one character type for the key feature."
            )
            return None

        if click_enabled:
            if self.radioLeft.isChecked():
                click_button = "Left"
            elif self.radioRight.isChecked():
                click_button = "Right"
            else:
                click_button = "Middle"
        else:
            click_button = "Left"

        return {
            "key_enabled": key_enabled,
            "key_interval": self.spinKeyInterval.value(),
            "key_charsets": {
                "letters": self.checkLetters.isChecked(),
                "numbers": self.checkNumbers.isChecked(),
                "special": self.checkSpecial.isChecked(),
            },
            "move_enabled": move_enabled,
            "move_interval": self.spinMoveInterval.value(),
            "click_enabled": click_enabled,
            "click_interval": self.spinClickInterval.value(),
            "click_button": click_button,
        }

    #stop
    def stop_now(self):
        self.engine.stop("Stopped by user (Stop button)")

    def on_engine_stopped(self):
        QTimer.singleShot(0, self._reset_ui_after_stop)

    def _reset_ui_after_stop(self):
        self.startButton.setEnabled(True)
        self.stopButton.setEnabled(False)
        self.statusLabel.setText("Idle")

    def closeEvent(self, event):
        self.engine.stop("Window closed")
        event.accept()


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
