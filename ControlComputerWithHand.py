# Date Created: 03/29/2024
# Coded By: Jacob Graham
# Purpose: To use your hand as a mouse and control the laptop using gestures.

# Imports
import cv2        # For video capture and image processing
import mediapipe  # For hand tracking
import pyautogui  # For controlling the mouse and performing clicks

# Initializations
capture_hands = mediapipe.solutions.hands.Hands()
drawing_option = mediapipe.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()
camera = cv2.VideoCapture(0)

# Variables to store hand landmark positions
x1 = y1 = x2 = y2 = 0

# Main loop to process video frames
while True:
    # Capture a frame from the camera
    _, image = camera.read()
    image_height, image_width, _ = image.shape

    # Flip the image horizontally to make it more intuitive
    image = cv2.flip(image, 1)

    # Convert the image from BGR to RGB for Mediapipe processing
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image to detect hands and landmarks
    output_hands = capture_hands.process(rgb_image)

    # Extract detected hands and landmarks
    all_hands = output_hands.multi_hand_landmarks

    # Check if any hands are detected
    if all_hands:
        for hand in all_hands:
            # Draw hand landmarks on the image (more so to help while creating the program)
            drawing_option.draw_landmarks(image, hand)
            
            # Access the landmarks of the detected hand
            one_hand_landmarks = hand.landmark

            # Iterate through the landmarks of the hand
            for id, lm in enumerate(one_hand_landmarks):
                # Converts the landmark positions to pixel coordinates on the computer
                x = int(lm.x * image_width)
                y = int(lm.y * image_height)

                # Check for specific landmark IDs for control logic
                if id == 8:  # The top of the index finger
                    # Moves the mouse based on the index finger's position
                    mouse_x = int(screen_width / image_width * x)
                    mouse_y = int(screen_height / image_height * y)
                    cv2.circle(image, (x, y), 10, (0, 255, 255))
                    pyautogui.moveTo(mouse_x, mouse_y)
                    x1, y1 = x, y  # Stores the coordinates 
                # The top of the thumb
                if id == 4: 
                    x2, y2 = x, y  # Stores the coordinates
                    cv2.circle(image, (x, y), 10, (0, 255, 255))
                # The top of the middle finger
                if id == 12: 
                    x3, y3 = x, y  # Stores the coordinates
                    cv2.circle(image, (x, y), 10, (0, 255, 255))
                # The top of the ring finger
                if id == 16: 
                    x4, y4 = x, y  # Stores the coordinates
                    cv2.circle(image, (x, y), 10, (0, 255, 255))
                # The top of the pinky finger
                if id == 20:  
                    x5, y5 = x, y  # Stores the coordinates
                    cv2.circle(image, (x, y), 10, (0, 255, 255))

        # This calculates the distances between the thumb and other fingers for gestures
        dist = y2 - y1   # The Distance between thumb and index finger
        dist2 = y2 - y3  # The Distance between thumb and middle finger
        dist3 = y2 - y4  # The Distance between thumb and ring finger
        dist4 = y2 - y5  # The Distance between thumb and pinky finger

        # If the pointer finger is touching the thumb
        if dist < 31:  
            pyautogui.click()  # Left clicks
            print("clicked")
            
        # If the middle finger is touching the thumb
        if dist2 < 20:  
            pyautogui.rightClick()  # Right clicks
            print("Right clicked")

        # If the ring finger is touching the thumb
        if dist3 < 20:  
            pyautogui.scroll(150)  # Scrolls up
            print("scrolled up")
            
        # If the pinky finger touches the thumb
        if dist4 < 20:  
            pyautogui.scroll(-150)  # Scrolls down
            print("scrolled down")

    # Display the video feed with landmarks
    cv2.imshow("Hand movement video capture", image)

    # Break the loop if the ESC key is pressed
    key = cv2.waitKey(100)
    if key == 27:
        break

# Release the camera and close all OpenCV windows
camera.release()
cv2.destroyAllWindows()
