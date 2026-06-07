# AI Eye-Controlled Interface

A prototype hands-free computer-control system that tracks **eye/iris movement** to trigger
actions — built as an accessibility experiment during an internship. The goal: explore whether
gaze and blink gestures alone can drive basic computer interaction for users who can't rely on a
mouse or keyboard. The prototype was demonstrated running on an **Intel trainer kit**.

<!-- Optional: add a short screen-recording GIF -->
<!-- ![demo](assets/demo.gif) -->

## Screenshots

![Prototype running on an Intel trainer kit](assets/setup.jpg)
![FaceMesh iris tracking](assets/facemesh.jpg)

## What It Does

Using a webcam, the app tracks the right iris with MediaPipe FaceMesh and classifies gaze
direction (left / right / up / down / centre). Each direction is mapped to an action, and a
double-blink triggers a separate command:

| Gesture | Action |
|---------|--------|
| Look **left** | Open Notepad |
| Look **right** | Open Google |
| Look **up** | Open YouTube |
| Look **down** | Open Control Panel |
| **Double blink** | Close current tab (Ctrl + W) |

A 2-second cooldown prevents repeated triggers, and an on-screen label shows the detected gaze
direction in real time. Press **Esc** to quit.

## How It Works

- **Iris tracking:** MediaPipe FaceMesh with `refine_landmarks=True` exposes iris landmarks.
  Horizontal gaze is estimated from the iris position relative to the eye corners; vertical gaze
  from the iris position relative to the eyelids.
- **Blink detection:** the vertical eye-aperture (eye-aspect ratio) dropping below a threshold
  registers a blink; two blinks within 2.5 s count as a double-blink.
- **Action mapping:** gaze direction and blinks are debounced, then routed to OS/browser
  actions via `pyautogui`, `webbrowser`, and `os.system`.

## Tech Stack

`Python` · `OpenCV` · `MediaPipe` · `PyAutoGUI`

## Setup

> Requires Python 3.9+, a webcam, and **Windows** (the action commands use `notepad` and
> `control`).

```bash
git clone https://github.com/IkmalAzis/ai-eye-control.git
cd ai-eye-control
pip install -r requirements.txt
python main.py
```

Look around to trigger actions; press **Esc** to exit.

## Status & Limitations

This is an **early-stage prototype**, functional in controlled lighting conditions. Known
limitations and lessons learned:

- Gaze thresholds are hard-coded and sensitive to lighting, head pose, and camera angle — a
  calibration step would make it far more reliable.
- Action mapping is Windows-specific (`notepad`, `control`).
- Single-eye tracking only; no smoothing/Kalman filter on the gaze estimate.
- Reinforced the importance of UI simplification for gaze-based input — fewer, larger targets
  work better than fine-grained control.

## Future Work

Per-user calibration, gaze smoothing, configurable action mappings, dwell-to-click, and a
cross-platform action layer.

## License

See `LICENSE` for details.
