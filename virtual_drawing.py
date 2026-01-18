
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import collections
import math

# --- Constants ---
WEBCAM_WIDTH = 1280
WEBCAM_HEIGHT = 720
BRUSH_THICKNESS_DEFAULT = 25
ERASER_THICKNESS = 100
FONT = cv2.FONT_HERSHEY_SIMPLEX
MODEL_PATH = "hand_landmarker.task"

# --- Classes ---
class Point:
    """A simple class to represent a point with x and y coordinates."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Color:
    """A class to represent a BGR color."""
    def __init__(self, b, g, r):
        self.b = b
        self.g = g
        self.r = r

    def to_tuple(self):
        """Returns the color as a (B, G, R) tuple."""
        return (self.b, self.g, self.r)

# --- Global Variables ---

# A deque to store the points of the current drawing line

points = collections.deque()



# A list to store the history of paint windows

lines = []

undone_lines = []



# The currently selected color

current_color = Color(0, 255, 0) # Default to green

brush_thickness = BRUSH_THICKNESS_DEFAULT





# A flag to indicate if drawing is in progress

drawing_in_progress = False





# --- Functions ---

def initialize_webcam():

    """Initializes and returns the webcam capture object."""

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():

        raise IOError("Cannot open webcam")

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WEBCAM_WIDTH)

    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WEBCAM_HEIGHT)

    return cap



def initialize_hand_tracking():

    """Initializes and returns the MediaPipe Hand Landmarker."""

    base_options = python.BaseOptions(model_asset_path=MODEL_PATH)

    options = vision.HandLandmarkerOptions(base_options=base_options,

                                           num_hands=2)

    detector = vision.HandLandmarker.create_from_options(options)

    return detector



def create_color_palette(frame_width):



    """Creates the color palette and other UI buttons."""



    palette = []



    colors = [



        Color(255, 0, 0),    # Blue



        Color(0, 255, 0),    # Green



        Color(0, 0, 255),    # Red



        Color(0, 255, 255),  # Yellow



        Color(255, 0, 255),  # Magenta



        Color(255, 165, 0), # Orange



        Color(0, 0, 0),      # Eraser (Black)



    ]







    button_width = int(frame_width / (len(colors) + 5))



    for i, color in enumerate(colors):



        x1 = i * button_width



        y1 = 0



        x2 = (i + 1) * button_width



        y2 = 50



        palette.append((x1, y1, x2, y2, color))







    # Add a "Clear" button



    clear_button_x1 = len(colors) * button_width



    clear_button_y1 = 0



    clear_button_x2 = (len(colors) + 1) * button_width



    clear_button_y2 = 50



    clear_button = (clear_button_x1, clear_button_y1, clear_button_x2, clear_button_y2)







    # Add an "Undo" button



    undo_button_x1 = (len(colors) + 1) * button_width



    undo_button_y1 = 0



    undo_button_x2 = (len(colors) + 2) * button_width



    undo_button_y2 = 50



    undo_button = (undo_button_x1, undo_button_y1, undo_button_x2, undo_button_y2)







    return palette, clear_button, undo_button







def draw_ui(frame, palette, clear_button, undo_button, current_brush_thickness):



    """Draws the color palette and other UI buttons on the frame."""



    for x1, y1, x2, y2, color in palette:



        cv2.rectangle(frame, (x1, y1), (x2, y2), color.to_tuple(), -1)



        if color.to_tuple() == current_color.to_tuple():



            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2)











    # Draw the "Clear" button



    cv2.rectangle(frame, (clear_button[0], clear_button[1]), (clear_button[2], clear_button[3]), (0, 0, 255), -1)



    cv2.putText(frame, "CLEAR", (clear_button[0] + 10, clear_button[1] + 30), FONT, 0.5, (255, 255, 255), 2, cv2.LINE_AA)







    # Draw the "Undo" button



    cv2.rectangle(frame, (undo_button[0], undo_button[1]), (undo_button[2], undo_button[3]), (255, 0, 0), -1)



    cv2.putText(frame, "UNDO", (undo_button[0] + 10, undo_button[1] + 30), FONT, 0.5, (255, 255, 255), 2, cv2.LINE_AA)







    # Display Brush Size



    cv2.putText(frame, f"Brush Size: {current_brush_thickness}", (10, WEBCAM_HEIGHT - 10), FONT, 0.7, (255, 255, 255), 2, cv2.LINE_AA)











def get_distance(p1, p2):



    """Calculates the Euclidean distance between two points."""



    if p1 is None or p2 is None:



        return float('inf')



    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)







def handle_drawing(paint_window, index_tip, current_brush_thickness, is_drawing):



    """Handles the drawing logic based on the drawing gesture."""



    global current_color, points, lines, undone_lines, drawing_in_progress







    if is_drawing and index_tip:



        # Start of a new stroke



        if not drawing_in_progress:



            drawing_in_progress = True



            # Create a new canvas for this stroke by copying the previous state



            lines.append(lines[-1].copy())



            points.clear()



            undone_lines.clear()







        points.appendleft(index_tip)







        # Redraw the entire smoothed line for the current stroke on each frame



        if len(lines) > 1 and len(points) > 1:



            # Get the canvas state from before this stroke started



            canvas_before_stroke = lines[-2]



            



            # Create a fresh canvas for this frame's rendering of the stroke



            current_stroke_canvas = canvas_before_stroke.copy()







            # Draw the smoothed polyline



            draw_color = current_color.to_tuple()



            thickness = current_brush_thickness



            if draw_color == (0, 0, 0): # Eraser



                thickness = ERASER_THICKNESS



            



            for i in range(len(points) - 1):



                p1 = points[i]



                p2 = points[i+1]



                if p1 and p2:



                    cv2.line(current_stroke_canvas, (p1.x, p1.y), (p2.x, p2.y), draw_color, thickness)



            



            # Replace the last history state with the newly rendered stroke



            lines[-1] = current_stroke_canvas



    else:



        # End of the stroke



        if drawing_in_progress:



            drawing_in_progress = False



            points.clear()







def handle_ui_interaction(index_tip, palette, clear_button, undo_button, is_selecting):



    """Handles interactions with the UI elements based on a pinch gesture."""



    global current_color, lines, undone_lines







    if is_selecting and index_tip:



        # Check for color selection



        for x1, y1, x2, y2, color in palette:



            if x1 <= index_tip.x <= x2 and y1 <= index_tip.y <= y2:



                current_color = color



                # Add a small delay to prevent multiple rapid selections



                cv2.waitKey(200)



                break







        # Check for "Clear" button press



        if clear_button[0] <= index_tip.x <= clear_button[2] and clear_button[1] <= index_tip.y <= clear_button[3]:



            lines.clear()



            points.clear()



            undone_lines.clear()



            lines.append(np.zeros((WEBCAM_HEIGHT, WEBCAM_WIDTH, 3), dtype=np.uint8))



            cv2.waitKey(200)







        # Check for "Undo" button press



        if undo_button[0] <= index_tip.x <= undo_button[2] and undo_button[1] <= index_tip.y <= undo_button[3]:



            if len(lines) > 1:



                undone_lines.append(lines.pop())



                points.clear()



            cv2.waitKey(200)











def main():



    """The main function of the virtual drawing application."""



    global lines, brush_thickness



    cap = initialize_webcam()



    detector = initialize_hand_tracking()







    # Create a separate window for the drawing canvas



    paint_window = np.zeros((WEBCAM_HEIGHT, WEBCAM_WIDTH, 3), dtype=np.uint8)



    lines.append(paint_window)







    palette, clear_button, undo_button = create_color_palette(WEBCAM_WIDTH)







    # Initialize variables for cursor smoothing



    smoothed_index_tip = None



    smoothing_factor = 0.7  # Lower value = more smoothing, more lag







    while cap.isOpened():



        success, frame = cap.read()



        if not success:



            print("Ignoring empty camera frame.")



            continue







        # Flip the frame horizontally for a mirror effect



        frame = cv2.flip(frame, 1)



        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)



        results = detector.detect(mp_image)







        # --- Landmark Processing ---



        index_tip, thumb_tip, middle_tip, ring_tip, pinky_tip = None, None, None, None, None



        index_pip, middle_pip, ring_pip, pinky_pip = None, None, None, None



        hand_landmarks = []







        if results.hand_landmarks:



            for hand in results.hand_landmarks:



                landmarks = {}



                for i, lm in enumerate(hand):



                    landmarks[i] = Point(int(lm.x * WEBCAM_WIDTH), int(lm.y * WEBCAM_HEIGHT))



                hand_landmarks.append(landmarks)







        # --- Gesture Detection & Logic ---



        is_drawing_gesture = False



        is_selection_gesture = False







        # If two hands are detected, use them to control brush size



        if len(hand_landmarks) == 2:



            index_tip1 = hand_landmarks[0].get(8)



            index_tip2 = hand_landmarks[1].get(8)



            if index_tip1 and index_tip2:



                distance = get_distance(index_tip1, index_tip2)



                # Map distance to brush size (e.g., dist 20-250 -> size 5-100)



                brush_thickness = int(np.interp(distance, [20, 250], [5, 100]))



                # Clamp the brush size to a reasonable range



                brush_thickness = max(5, min(brush_thickness, 100))











        # Use the first detected hand for drawing and UI interaction



        if len(hand_landmarks) > 0:



            primary_hand = hand_landmarks[0]



            index_tip = primary_hand.get(8)



            thumb_tip = primary_hand.get(4)



            middle_tip = primary_hand.get(12)



            ring_tip = primary_hand.get(16)



            pinky_tip = primary_hand.get(20)



            index_pip = primary_hand.get(6)



            middle_pip = primary_hand.get(10)



            ring_pip = primary_hand.get(14)



            pinky_pip = primary_hand.get(18)







            # Apply smoothing to the index tip for the visual cursor



            if index_tip:



                if smoothed_index_tip is None:



                    smoothed_index_tip = index_tip



                else:



                    smoothed_index_tip.x = int(smoothing_factor * index_tip.x + (1 - smoothing_factor) * smoothed_index_tip.x)



                    smoothed_index_tip.y = int(smoothing_factor * index_tip.y + (1 - smoothing_factor) * smoothed_index_tip.y)







            # Check for gestures if all necessary landmarks are available



            if all([index_tip, thumb_tip, middle_tip, ring_tip, pinky_tip,



                    index_pip, middle_pip, ring_pip, pinky_pip]):







                # Define finger states (up or down)



                index_finger_up = index_tip.y < index_pip.y



                middle_finger_up = middle_tip.y < middle_pip.y



                ring_finger_up = ring_tip.y < ring_pip.y



                pinky_finger_up = pinky_tip.y < pinky_pip.y







                # Selection Gesture: Thumb-Index pinch.



                if get_distance(index_tip, thumb_tip) < 45:



                    is_selection_gesture = True







                # Drawing Gesture: Index finger pointing up, other fingers down.



                if index_finger_up and not middle_finger_up and not ring_finger_up and not pinky_finger_up:



                    is_drawing_gesture = True







        current_brush_thickness = brush_thickness



        if current_color.to_tuple() == (0,0,0):



             current_brush_thickness = ERASER_THICKNESS







        draw_ui(frame, palette, clear_button, undo_button, brush_thickness)







        # Handle gestures (using the raw, unsmoothed index_tip for responsiveness)



        handle_ui_interaction(index_tip, palette, clear_button, undo_button, is_selection_gesture)



        if lines:



            handle_drawing(lines[-1], index_tip, current_brush_thickness, is_drawing_gesture)







        # --- Display Logic ---



        display_frame = frame.copy()







        # Draw the smoothed, circular cursor



        if smoothed_index_tip:



            radius = int(current_brush_thickness / 2) if current_brush_thickness > 0 else 1



            cv2.circle(display_frame, (smoothed_index_tip.x, smoothed_index_tip.y), radius, (0, 255, 255), 2)











        if lines:



            display_frame = cv2.addWeighted(display_frame, 1, lines[-1], 0.5, 0)







        cv2.imshow('Virtual Drawing', display_frame)







        if cv2.waitKey(5) & 0xFF == ord('q'):



            break







    cap.release()



    cv2.destroyAllWindows()





if __name__ == '__main__':

    main()


