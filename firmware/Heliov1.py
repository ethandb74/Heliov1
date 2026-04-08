import pyfirmata2
import time
from time import sleep
from pysolar.solar import get_altitude, get_azimuth
import mediapipe as mp
import math
import cv2
import numpy
import datetime

LAT = 33.16   # your McKinney latitude
LON = -96.74  # your McKinney longitude (negative = west)


#TODO If mistakes check numpy may cause compatability error ASK to DOWNGRADE currentnumpy version: 2.0.2

##PYfirmata SETUP
###PYFIRMATA -------------------------------------------------------------------------------------------

PORT = 'COM7'  # ← your port (was COM4 in original)
xSERVO_PIN = 10  # pin # for servo
yServo_PIN = 11

# Setup Arduino + iterator (required for reliable operation)
board = pyfirmata2.Arduino(PORT)
it = pyfirmata2.util.Iterator(board)
it.start()

sleep(1.5)  # give time for Firmata to initialize

X_servo = board.get_pin(f'd:{xSERVO_PIN}:s')
Y_servo = board.get_pin(f'd:{yServo_PIN}:s')
##--------------------------------------------------------------------------------------------------------
def normalize(val, vmin, vmax):
    return max(0.0, min(1.0, (val - vmin) / (vmax - vmin)))

######----------------######---------------------------######-----------------------------######------------------
def get_solar_servo_angles():

    now = datetime.datetime.now(datetime.timezone.utc)  # current time in UTC (pysolar requires this)
    altitude = get_altitude(LAT, LON, now)
    azimuth = get_azimuth(LAT, LON, now)

    tilt_angle = int(round(max(0, min(180, altitude))))
    pan_angle = int(round(max(0,azimuth/2)))

    tilt_angle = float(tilt_angle)
    pan_angle = float(pan_angle)

    return pan_angle, tilt_angle, altitude, azimuth
####--------------------------------------------------------------------

mode = "sun"
print("🚀 Helio v1 🪐")
print("Commands: s = Sun mode | h = Hand mode | q = Quit")

##############-----------MEDIAPIPE SETUP------------------------------------------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 600)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 500)

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hand = mp_hands.Hands(max_num_hands=1)

##info for this specific frame Width and Height
##for single point (pointer finger at landmark 8
# x (Min - .01   ,   Max- 1)
# y (Min - 0.03  ,   Max- 0.7)
# z (Min - -0.01 ,  Max- -0.5)
###--------------------------------------------------------------------------

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            time.sleep(0.1)
            continue

        #cv2.imshow('Helio v1', frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q') or key == ord('Q'):
            break
        elif key == ord('s') or key == ord('S'):
            mode = "sun"
            print("→ Switched to SUN mode")
        elif key == ord('h') or key == ord('H'):
            mode = "hand"
            print("→ Switched to HAND mode")

        if mode == "sun":
            current_time = time.time()


            if 'last_sun_update' not in globals() or (current_time - globals()['last_sun_update']) >= 5:
                pan_angle, tilt_angle, alt, az = get_solar_servo_angles()

                #serv
                X_servo.write(pan_angle)  # pan (azimuth mapped)
                Y_servo.write(tilt_angle)  # tilt (altitude)


                print("pan angle: ", pan_angle)
                print("tilt angle: ", tilt_angle)

                globals()['last_sun_update'] = current_time

            cv2.imshow('Helio v1', frame)

            #time.sleep(30)  # continuous tracking — sun moves slowly

        else:
            #cv2.destroyWindow("Helio v1")


            success, frame = cap.read()
            if success:
                RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                result = hand.process(RGB_frame)
                if result.multi_hand_landmarks:
                    for hand_landmarks in result.multi_hand_landmarks:
                        index = hand_landmarks.landmark[8]
                        thumbTip = hand_landmarks.landmark[4]
                        middleTip = hand_landmarks.landmark[12]
                        distance = math.sqrt((thumbTip.x - middleTip.x) ** 2 + (thumbTip.y - middleTip.y) ** 2)

                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                        ## change the arguments to make more or less sensitive  ex. I change x Vmax to lower value ot make it more sensitive
                        ## vmin and vmax arguments are the values that you get rn and want to map to 0-180

                        X_servo_angle = round(normalize(index.x, 0.01, 0.70), 2) * 180
                        Y_servo_angle = round(normalize(index.y, 0.03, 0.70), 2) * 180
                        Z_servo_angle = round(normalize(distance, 0.02, 0.4)) * 180

                        ## added open close hand and = 0 - 180 on servo (only open and only close may need to fix Prob in normalize distance
                        ## servo.write
                        print("x value:  " + str(X_servo_angle))
                        print("y value:  " + str(Y_servo_angle))

                        X_servo.write(X_servo_angle)
                        Y_servo.write(Y_servo_angle)
                        sleep(.001)
                     # TEXT OVERLAY - HAND MODE
                cv2.putText(frame, "MANUAL OVERRIDE", (10, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
                cv2.imshow('Helio v1', frame)



except KeyboardInterrupt:
    print("\n  🛑 tracking stopped  🛑")
    board.exit()
except Exception as e:   # extra safety so it doesn't crash on other errors
    print("Error:", e)
    board.exit()

# Clean shutdown
print("Helio v1 shutting down...")
board.exit()







