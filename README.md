# Virtual Drawing App
& "C:\VS CODE\VIRTUAL DRAWING\.venv\Scripts\python.exe" "C:\VS CODE\VIRTUAL DRAWING\virtual_drawing.py"
This Python project is an interactive drawing application that uses your webcam to track your hand and allows you to draw on the screen with your index finger.

## Features

- Real-time hand tracking using MediaPipe.
- Drawing on the screen by moving your index finger.
- Multiple color options.
- A "Clear" button to erase the drawing.
- Live webcam feed as the background.
- Smooth and anti-aliased drawing strokes.

## Installation

1.  **Clone the repository or download the code.**
2.  **Install the required libraries:**

    ```bash
    pip install -r requirements.txt
    ```

## How to Run

1.  **Run the application:**

    ```bash
    python virtual_drawing.py
    ```

2.  **Use the application:**

    *   Your webcam will turn on.
    *   Raise your hand in front of the camera.
    *   Move your index finger to draw on the screen.
    *   To change colors, hover your index finger over the color palette at the top of the screen. The available colors are Blue, Green, Red, Yellow, Magenta, and Orange.
    *   To clear the screen, hover your index finger over the "CLEAR" button.
    *   To save your drawing, hover your index finger over the "SAVE" button. The drawing will be saved as `drawing.png` in the same directory.
