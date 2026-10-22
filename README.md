# Hand-gesture-mouse-control
A computer-vision application that uses your webcam and MediaPipe hand tracking to recognize hand gestures in real time, allowing you to control system mouse operations naturally without touching physical hardware.
Key Features
Real-Time Hand Detection: Tracks hand movement with low latency using an standard webcam feed.

Landmark Visualization: Overlays spatial hand skeletons and tracking points directly on the camera frame.

Pinch Gesture Detection: Measures dynamic distance between the thumb and index finger tip.

Gesture-Based Clicking: Triggers left-click mouse actions automatically when a pinch is detected.

🛠️ Tech Stack
Language: Python 3.x

Computer Vision: OpenCV (opencv-python)

Tracking Framework: MediaPipe

OS Automation: PyAutoGUI

📋 Prerequisites
Ensure you have Python installed on your system along with a working webcam.

Bash
python --version
⚡ Quick Start
1. Clone the Repository
Bash
git clone https://github.com/your-username/hand-gesture-mouse-control.git
cd hand-gesture-mouse-control
2. Install Dependencies
Bash
pip install opencv-python mediapipe pyautogui
3. Run the Application
Bash
python main.py
Press q on the webcam window to exit the application.

Controls

- Index finger →  Move cursor
- Thumb + index finger pinch →  Click
- Two quick pinches →  Double click
- Open hand →  Scroll mode
- Hand position →  Scroll up/down
- Press `Q`  → Exit
