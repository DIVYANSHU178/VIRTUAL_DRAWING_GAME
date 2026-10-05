# Virtual Gesture Drawing Canvas

> **Real-time computer vision drawing application using webcam hand tracking powered by Python, MediaPipe, and OpenCV.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-5C3EE8?style=flat-square&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand_Landmarks-0078D4?style=flat-square&logo=google&logoColor=white)](https://developers.google.com/mediapipe)

---

## 📌 Overview

An interactive, touchless computer vision application that turns the user's index finger into an on-screen digital pen using a standard webcam. Powered by **MediaPipe Hands** and **OpenCV**, the system tracks hand landmarks in real time and renders smooth, anti-aliased drawing strokes directly over the video feed.

---

## ✨ Features

* **Touchless Air-Canvas:** Draw in 2D space by tracking the tip of the index finger.
* **Interactive Toolbars:** Real-time on-screen UI buttons for color switching (Blue, Green, Red, Yellow, Magenta, Orange).
* **Canvas Actions:** Hover-based action triggers to clear the canvas or export the generated artwork as `drawing.png`.
* **Adaptive Stroke Smoothing:** Anti-aliased line rendering that minimizes jitter between captured frames.

---

## 🚀 Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone https://github.com/DIVYANSHU178/VIRTUAL_DRAWING_GAME.git
   cd VIRTUAL_DRAWING_GAME
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python virtual_drawing.py
   ```

4. **Controls:**
   * Raise your hand in front of the camera.
   * Move your index finger to sketch on screen.
   * Hover over the top color palette to select ink colors.
   * Hover over **CLEAR** to reset or **SAVE** to export your drawing.

---

## 📄 License
This project is open-source and available under the MIT License.
