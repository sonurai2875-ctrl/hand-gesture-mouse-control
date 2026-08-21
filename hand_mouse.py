from pathlib import Path
import pyautogui
import cv2
import mediapipe as mp
import math
import time

click_start_time=None
click_times=[]
click_cooldown=0.5
pinch_threshold=0.08
scroll_mode=False
freeze_mode=False





screen_width, screen_height = pyautogui.size()
print("\n hand mouse control \n")
prev_screen_x, prev_screen_y = 0, 0

MODEL_PATH = Path(__file__).with_name("hand_landmarker.task")
HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20), (0, 17),
)


def draw_hand(frame, landmarks):
    frame_height, frame_width = frame.shape[:2]
    points = [
        (int(landmark.x * frame_width), int(landmark.y * frame_height))
        for landmark in landmarks
    ]
    for start_index, end_index in HAND_CONNECTIONS:
        cv2.line(frame, points[start_index], points[end_index], (0, 255, 0), 2)
    for point in points:
        cv2.circle(frame, point, 5, (0, 0, 255), -1)


if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Missing model: {MODEL_PATH.name}. Download it into {MODEL_PATH.parent}."
    )

base_options = mp.tasks.BaseOptions(model_asset_path=str(MODEL_PATH))
options = mp.tasks.vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=1,
    min_hand_detection_confidence=0.7,
)

with mp.tasks.vision.HandLandmarker.create_from_options(options) as hand_landmarker:
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("Cannot open camera")

    try:
        while True:
            success, frame = camera.read()
            if not success:
                print("Cannot read from camera. Exiting...")
                break

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            result = hand_landmarker.detect(image)

            for hand_landmarks in result.hand_landmarks:
                draw_hand(frame, hand_landmarks)
                thumb_tip = hand_landmarks[4]
                index_tip = hand_landmarks[8]
                middle_tip = hand_landmarks[12]
                ring_tip = hand_landmarks[16]
                pinky_tip = hand_landmarks[20]

                fingers=[
                    1 if hand_landmarks[i].y < hand_landmarks[i - 2].y else 0
                    for i in [8, 12, 16, 20]
                ]
                #distcance between thumb and index finger
                distance = math.hypot(
                    index_tip.x - thumb_tip.x, index_tip.y - thumb_tip.y
                )
                if distance < pinch_threshold:
                    if not freeze_mode:
                        freeze_mode = True
                        click_times.append(time.time())

                        if len(click_times) >= 2 and (click_times[-1] - click_times[-2]) < click_cooldown:
                            pyautogui.doubleClick()
                            cv2.putText(frame, "Double Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 225, 255), 2)
                            click_times = []
                        else:
                            pyautogui.click()
                            cv2.putText(frame, "Click", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (225, 255, 0), 2)
                else:
                    if freeze_mode:
                        time.sleep(0.2)  # Add a small delay to prevent immediate unfreeze
                    freeze_mode = False
                if not freeze_mode:
                    screen_x = int(index_tip.x * screen_width)
                    screen_y = int(index_tip.y * screen_height)
                    pyautogui.moveTo(screen_x, screen_y, duration=0.1)
                    prev_screen_x, prev_screen_y = screen_x, screen_y

                if sum(fingers) == 4:
                        scroll_mode = True
                else:
                    scroll_mode = False

                if scroll_mode:
                    if index_tip.y<0.4:
                        pyautogui.scroll(40)
                        cv2.putText(frame, "Scroll Up", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    elif index_tip.y>0.6:
                        pyautogui.scroll(-40)
                        cv2.putText(frame, "Scroll Down", (50, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"Pinch: {distance:.3f} / {pinch_threshold:.3f}",
                    (50, 90),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (255, 255, 255),
                    2,
                )

                    

            cv2.imshow("Live video", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        camera.release()
        cv2.destroyAllWindows()
