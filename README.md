# 🔊 Wireless Sound Control by Gestures

## 💡 About The Project

This project provides a contactless way to control your computer's system volume using hand gestures. By leveraging a webcam and computer vision techniques, you can increase or decrease the volume simply by moving your thumb and index finger closer together or farther apart. This is a fun and practical application of the OpenCV and MediaPipe libraries.

**Features:**
* **Gesture-Based Volume Control**: Adjusts system volume based on the distance between your thumb and index finger.
* **Real-time Feedback**: Displays a visual volume bar and finger tracking on the webcam feed.
* **Touchless Interface**: Offers a hygienic and modern way to interact with your computer.
* **Lightweight and Efficient**: Uses MediaPipe for fast and accurate hand landmark detection.

## ⚙️ Prerequisites and Setup

Before running the project, you need to have Python and the required libraries installed.

### 1. Requirements

* **Python 3.6+**
* **OpenCV (`cv2`)**: For video capture and image processing.
* **MediaPipe**: For robust hand landmark detection.
* **pycaw**: For programmatic control of the system's audio.
* **NumPy**: For numerical operations.

### 2. Installation

First, clone this repository to your local machine:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

Next, install all the required libraries using pip from the requirements.txt file:
```bash
pip install -r requirements.txt
```

> Note: pycaw is a Windows-specific library. This project is currently designed for Windows operating systems.

## ▶️ Usage

Ensure your webcam is connected and ready.

Run the Python script from your terminal:
```bash
python "Wireless Sound Control PYTHON File.py"
```

A window will appear showing your webcam feed.

Move your hand into the camera's view. The script will track your thumb and index finger.

- **Increase Volume**: Move your thumb and index finger far apart.
- **Decrease Volume**: Bring your thumb and index finger close together.

To exit the application, simply press the 'q' key on your keyboard.

## 🚀 How It Works

The core of the project relies on three main components:

- **Webcam Capture**: The program continuously reads frames from your webcam.
- **Hand Detection**: The MediaPipe library processes each frame to detect a hand and identify 21 key points (landmarks) on it, including the tips of each finger.
- **Distance-Based Control**: The script calculates the Euclidean distance between the tips of the thumb and the index finger. This distance is then mapped to the system's volume range (0-100%). When your fingers are close, the volume decreases; when they are far apart, it increases.

## 🤝 Contribution

Contributions are welcome! If you find a bug or have a suggestion for an improvement, feel free to open an issue or submit a pull request.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.
