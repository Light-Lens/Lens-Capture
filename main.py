from win32api import GetSystemMetrics
from PIL import ImageGrab
import numpy, time, cv2

def record(filename, FPS=30, codec='XVID', window_size=(1280, 720)):
    """
    Records the screen and saves the recording to a video file.

    Parameters:
    - filename: str, name of the output file, including extension (e.g. 'my_recording.avi')
    - FPS: int, frames per second of the output video (default: 10)
    - codec: str, four character code of the codec used to encode the video (default: 'XVID')
    - window_size: tuple of int, size of the recording window (default: (1280, 720))

    Returns:
    - None
    """
    # Get system resolution
    screen_width, screen_height = GetSystemMetrics(0), GetSystemMetrics(1)

    # Set up video writer
    fourcc = cv2.VideoWriter_fourcc(*codec)

    out = cv2.VideoWriter(filename, fourcc, FPS, (screen_width, screen_height))

    # Set up recording window
    cv2.namedWindow("Lens Capture", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Lens Capture", *window_size)

    # Start recording
    print("Press 'Esc' to stop recording")
    start_time = time.time()
    while True:
        # Capture screenshot
        img = ImageGrab.grab(bbox=(0, 0, screen_width, screen_height)).convert("RGB")

        # Convert screenshot to numpy array and resize it
        frame = numpy.array(img)
        frame = cv2.resize(frame, (screen_width, screen_height))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # Convert it from BGR(Blue, Green, Red) to RGB(Red, Green, Blue)

        # Write frame to output file
        out.write(frame)

        # Display recording window
        cv2.imshow("Lens Capture", frame)

        # Check for 'Esc' key press to stop recording
        if cv2.waitKey(33) == 27:
            break

        if cv2.getWindowProperty("Lens Capture", cv2.WND_PROP_VISIBLE) < 1:
            break

    # Release resources
    out.release()
    cv2.destroyAllWindows()

    # Print recording duration
    duration = time.time() - start_time
    print(f"Recording saved to '{filename}' ({round(duration, 2)} seconds)")

# Example usage
if __name__ == '__main__':
    CurrentTime = str(time.strftime("%d-%m-%Y %H-%M-%S"))
    Filename = f"{CurrentTime}.avi"

    record(Filename)
