import cv2
import pyautogui
import numpy as np

# Specify the screen resolution
screen_width, screen_height = pyautogui.size()

# Define the codec and create a VideoWriter object with MP4 format
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('screen_recording.mp4', fourcc, 20.0, (screen_width, screen_height))

try:
    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to a NumPy array
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Write the frame to the video file
        out.write(frame)

except KeyboardInterrupt:
    # Release the VideoWriter and close the recording
    out.release()
    cv2.destroyAllWindows()
