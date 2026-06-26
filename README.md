# AutoClicker

A feature-rich **Python AutoClicker** with a modern **Qt Designer** interface that automates mouse clicks, keyboard presses, and mouse movement. Designed to prevent inactivity while giving users complete control over automation settings.

> **Disclaimer:** This project is intended for learning, testing, and personal automation purposes only. Use it responsibly and in accordance with the rules of any software or service where it is used.

---

## Features

### ⌨️ Random Keyboard Presses
* Enable or disable random key presses.
* Configure the time interval between each key press.
* Choose which type of characters to generate:
  * Letters (a-z, A-Z)
  * Numbers (0-9)
  * Special Characters (!@#$...)

### 🖱️Random Mouse Movement
* Enable or disable random mouse movement.
* Set a custom movement interval.

### 🖲️Auto Mouse Clicking
* Enable or disable automatic clicking.
* Configure the click interval.
* Select the mouse button:
  * Left Click
  * Right Click
  * Middle Click

---

## How It Works
1. Launch the application.
2. Select the automation features you want.
3. Configure the intervals and options.
4. Click **Start**.
5. A **3-second countdown** begins, giving you time to switch to another application.
6. Automation starts automatically.

---

## 🛑 Stop Conditions
The program can be stopped instantly by either:
* Pressing the **Esc** key.
* Simply **moving your mouse**.

This provides a quick and safe way to stop automation at any time.

---

## Activity Log
The bottom section of the application contains a real-time **Activity Log** that displays:
* Program status
* Countdown progress
* Keyboard actions
* Mouse movements
* Mouse clicks
* Start/Stop events
* Other runtime information

This makes it easy to monitor what the application is doing.

---

## User Interface
The graphical interface was created using **Qt Designer**, providing a clean and easy-to-use experience while keeping the application lightweight.

---

## Built With
* Python
* PyQt / Qt Designer
* ChatGPT (used to improve code readability and assist in writing this README)
