# --- Wireless Sound Control by Hand Gestures using OpenCV and MediaPipe ---

# Importing Libraries
import cv2
import mediapipe as mp
import math
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# --- Configuration and Initialization ---
# Get the audio endpoint and volume interface for system audio control
try:
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    vol_range = volume.GetVolumeRange()
    min_vol = vol_range[0]
    max_vol = vol_range[1]
except Exception as e:
    print(f"Error initializing Pycaw: {e}")
    print("This project is designed for Windows. Please ensure the pycaw library is correctly installed.")
    exit()

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mp_drawing = mp.solutions.drawing_utils

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Set up volume bar visualization parameters
bar_height = 400
bar_width = 30
vol_bar_x = 50
vol_bar_y = 150

# --- Helper Function ---
def findDistance(x1, y1, x2, y2):
    """
    Calculates the Euclidean distance between two points.
    
    Args:
        x1, y1: Coordinates of the first point.
        x2, y2: Coordinates of the second point.
        
    Returns:
        The Euclidean distance between the two points.
    """
    return math.hypot(x2 - x1, y2 - y1)

# --- Main Program Loop ---
while True:
    success, img = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Flip the image horizontally for a natural, mirror-like view
    img = cv2.flip(img, 1)
    
    # Convert the BGR image to RGB for MediaPipe processing
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Process the image to detect hands
    results = hands.process(img_rgb)
    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Draw landmarks on the image
            mp_drawing.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            # Extract landmark coordinates for the thumb tip (4) and index finger tip (8)
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            
            h, w, c = img.shape
            x1, y1 = int(thumb_tip.x * w), int(thumb_tip.y * h)
            x2, y2 = int(index_tip.x * w), int(index_tip.y * h)
            
            # Draw circles at the tips and a line connecting them
            cv2.circle(img, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            
            # Calculate the distance between the two finger tips
            length = findDistance(x1, y1, x2, y2)
            
            # Map the finger distance to the system volume range
            # The range for the finger distance is estimated (e.g., 20 to 200 pixels)
            vol_level = np.interp(length, [20, 200], [min_vol, max_vol])
            vol_percentage = np.interp(length, [20, 200], [0, 100])
            
            # Set the system volume
            volume.SetMasterVolumeLevel(vol_level, None)
            
            # --- Volume Bar Visualization ---
            vol_bar_height = np.interp(vol_percentage, [0, 100], [0, bar_height])
            
            # Draw the static volume bar background
            cv2.rectangle(img, (vol_bar_x, vol_bar_y), 
                          (vol_bar_x + bar_width, vol_bar_y + bar_height), 
                          (255, 255, 255), 2)
            
            # Draw the dynamic volume level rectangle
            cv2.rectangle(img, (vol_bar_x, vol_bar_y + bar_height - int(vol_bar_height)), 
                          (vol_bar_x + bar_width, vol_bar_y + bar_height), 
                          (0, 255, 0), cv2.FILLED)
            
            # Display the volume percentage
            cv2.putText(img, f'{int(vol_percentage)}%', (vol_bar_x, vol_bar_y + bar_height + 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

    # Display the final image with annotations
    cv2.imshow('Wireless Sound Control', img)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- Cleanup ---
cap.release()
cv2.destroyAllWindows()