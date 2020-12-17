# import the necessary packages
import cv2
import dlib
from threading import Thread
import numpy as np
from imutils import face_utils
import time
from scipy.spatial import distance as dist
import playsound


# # intializing pygame library mixer to play sound
# pygame.mixer.init()

# # code to make logs dir for logging the actions -
# today = datetime.now()
# dt = today.strftime("%Y-%m-%d")
# if not os.path.exists('logs'):
#     os.makedirs('logs')
# logging.basicConfig(level=logging.DEBUG, filename='logs\\' + dt + '-' + str(gma().replace(':', '-')) + '-copilot.log',
#                     filemode='a', format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


# function to calculate eye aspect ratio
def eye_aspect_ratio(eye):
    # compute the euclidean distances between the two sets of
    # vertical eye landmarks (x, y)-coordinates
    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])

    # compute the euclidean distance between the horizontal
    # eye landmark (x, y)-coordinates
    C = dist.euclidean(eye[0], eye[3])

    # compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)

    # return the eye aspect ratio
    return ear

# function to sound the alarm
def sound_alarm(path):
    # play an alarm sound
    playsound.playsound('Sounds/' + path)
    # sound = mixer.Sound('Sounds/' + path)
    # sound.play()
    time.sleep(0.5)

# function to return euler_angle of the face.
def get_head_pose(size, gray, shape):
    # 3d model Coordinates of few points on face like left eye corner, chin, tip of nose.
    object_pts = np.float32([[6.825897, 6.760612, 4.402142],
                             [1.330353, 7.122144, 6.903745],
                             [-1.330353, 7.122144, 6.903745],
                             [-6.825897, 6.760612, 4.402142],
                             [5.311432, 5.485328, 3.987654],
                             [1.789930, 5.393625, 4.413414],
                             [-1.789930, 5.393625, 4.413414],
                             [-5.311432, 5.485328, 3.987654],
                             [2.005628, 1.409845, 6.165652],
                             [-2.005628, 1.409845, 6.165652],
                             [2.774015, -2.080775, 5.048531],
                             [-2.774015, -2.080775, 5.048531],
                             [0.000000, -3.116408, 6.097667],
                             [0.000000, -7.415691, 4.070434]])

    # calibrated camera matrix, describes the mapping of a camera image from 3D points in the world to 2D points.
    camera_matrix = np.array([6.40334044e+03, 0.00000000e+00, 6.45556827e+02,
                              0.00000000e+00, 6.35739614e+03, 4.23570228e+02,
                              0.00000000e+00, 0.00000000e+00, 1.00000000e+00]).reshape(3, 3).astype(np.float32)

    # distortion coefficients of camera lens.
    dist_coeffs = np.array([-2.48966054e+00, 3.25709902e+02, 7.16673596e-03, -8.79248343e-04,
                            3.84944117e+00]).reshape(5, 1).astype(np.float32)
    # 2D image points taken from 68 face lanmarks predictor which are corresponding to object_pts matrix defined above.
    image_pts = np.float32([shape[17], shape[21], shape[22], shape[26], shape[36],
                            shape[39], shape[42], shape[45], shape[31], shape[35],
                            shape[48], shape[54], shape[57], shape[8]])

    # Calculate perspective and point
    _, rotation_vector, translation_vector = cv2.solvePnP(object_pts, image_pts, camera_matrix, dist_coeffs)
    rotation_matrix, _ = cv2.Rodrigues(rotation_vector)
    pose_matrix = cv2.hconcat((rotation_matrix, translation_vector))
    # Calculate Euler angles
    _, _, _, _, _, _, euler_angle = cv2.decomposeProjectionMatrix(pose_matrix)
    return euler_angle


# function to detect attentiveness of the face.
def detect_attentiveness():
    # initializing boolean flags to trigger respective tasks

    # # if log_sleep is True then write comment in logs that drive is sleeping at that time.
    # log_sleep = False
    # # if log_off_road is True then write comment in logs that drive is loooking off road at that time.
    # log_off_road = False
    # # if log_face is True then write comment in logs that drive's face is not detected that time.
    # log_face = False

    # path for 68 face lanmarks predictor file.
    # The pre-trained facial landmark detector inside the dlib library is used to estimate
    # the location of 68 (x, y)-coordinates that map to facial structures on the face.
    face_landmark_path = './model/shape_predictor_68_face_landmarks.dat'

    # grab the indexes of the facial landmarks for the left and right eye, respectively.
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    # capture the video feed from web cam and assign to camera_stream variable.
    camera_stream = cv2.VideoCapture(0)

    if not camera_stream.isOpened():
        # write comments in log file  - Unable to the camera.
        # logging.debug('Unable to connect to camera.')
        return
    # else:
    #     # write comments in log file  - connecting to the camera.
    #     logging.debug('Connecting to the camera.')

    # Creating object of frontal face detector.
    detector = dlib.get_frontal_face_detector()

    # creating object of dlip shape_predictor using 68 face landmarks predictor file.
    predictor = dlib.shape_predictor(face_landmark_path)

    # setting eye aspect ratio threshold
    EYE_AR_THRESH = 0.25

    # initializing COUNTER  and eye_counter variable to trigger the alarm once they reach to certain value.
    COUNTER = 0
    eye_counter = 0

    # initializing consecutive frames variables for eyes and head pose, to trigger the alarm eye_counter and
    # COUNTER must be above the below variables respectively.
    EYE_AR_CONSEC_FRAMES = 30
    CONSEC_FRAMES = 30

    # write comments in log file -  camera has started capturing frames.
    # logging.debug('Starting feed capture.')
    # loop over frames from the video stream while the camera is open.
    while camera_stream.isOpened():
        # grab the frame from the threaded video file stream, resize it, and convert it to grayscale channels
        ret, frame = camera_stream.read()
        if ret:
            # Converting image to greyscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # num_faces = detector.detect_faces(frame)
            num_faces: object = detector(gray, 0)

        if len(num_faces) > 0:
            for face in num_faces:
                # get shape of face using predictor(object of shape_predictor) and convert the shape to numpy array.
                try:
                    shape = predictor(frame, face)
                except:
                    detect_attentiveness()
                shape = face_utils.shape_to_np(shape)

                # code to get a position on above of face to show status of driver.
                i, j = shape[0]
                face_point = (i - 40, j - 80)

                # extract the left and right eye coordinates, then use the
                # coordinates to compute the eye aspect ratio for both eyes
                leftEye = shape[lStart:lEnd]
                rightEye = shape[rStart:rEnd]
                leftEAR = eye_aspect_ratio(leftEye)
                rightEAR = eye_aspect_ratio(rightEye)

                # Assign mean of rightEAR  and leftEAR to ear.
                ear = (rightEAR + leftEAR) / 2

                # if ear value is less than threshold, then increase the eye_counter by 1
                # and once counter become equal to EYE_AR_CONSEC_FRAMES then alarm the user of sleep.
                if ear < EYE_AR_THRESH:
                    eye_counter += 1
                    if eye_counter >= EYE_AR_CONSEC_FRAMES:
                        # Show driver sleeping status on above of driver's face.
                        cv2.putText(frame, "Sleeping", (i - 40, j - 120), cv2.FONT_HERSHEY_SIMPLEX, 0.60,
                                    (255, 255, 255),
                                    thickness=2)

                        # add comment in the log file  - Driver is sleeping when log_sleep is false
                        # if not log_sleep:
                        #     logging.debug('Driver is sleeping.')
                        #     log_sleep = True

                        # start a thread to have the alarm sound played in the background
                        t = Thread(target=sound_alarm,
                                   args=('short_message.wav',))
                        t.deamon = True
                        t.start()
                        t.join()


                # otherwise, the eye aspect ratio is not below the blink
                # threshold, so reset the counter and alarm
                else:
                    eye_counter = 0
                    # if log_sleep:
                    #     logging.debug('Driver opened eyes.')
                    #     log_sleep = False

                # get euler angle of a face from get_head_pose function
                euler_angle = get_head_pose(frame.shape, gray, shape)

                # Camera to be placed on the 30 degrees right side of the driver,
                # To use it on the left side select value in negative(-30) and for front set origin to 0
                origin = 0

                # circle the dots on face using below code
                for (x, y) in shape:
                    cv2.circle(frame, (x, y), 1, (0, 0, 255), -1)

                # evaluate horizontal position of face by taking refrence of y axis of euler angle,
                # if it is more than 15 degree right or left, then show the face inattentive.
                if ((euler_angle[1, 0] + origin) > 15) or ((euler_angle[1, 0] + origin) < -15):
                    # Increase counter by 1 if the condtion is met.
                    COUNTER += 1

                    # Once counter value becomes greater or equal to CONSEC_FRAMES then sound the alarm that driver is looking off road.
                    if COUNTER >= CONSEC_FRAMES:
                        # Code to show the driver off road on the frame.
                        cv2.putText(frame, 'Inattentive', face_point, cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0),
                                    thickness=2)

                        # if log_off_road is false then add comment in log file.
                        # if not log_off_road:
                        #     logging.debug('Driver is looking off road.')
                        #     log_off_road = True

                        t = Thread(target=sound_alarm,
                                   args=('short_message.wav',))
                        t.deamon = True
                        t.start()
                        t.join()

                    # Else show on the frame that driver is looking on road and add comment in the log file.
                    # And re-intalizing the counter variable.
                else:

                    cv2.putText(frame, 'Attentive', face_point, cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 0, 0),
                                thickness=2)
                    # if log_off_road:
                    #     logging.debug('Driver paying attention now.')
                    #     log_off_road = False
                    COUNTER = 0

                # Code to show the X, Y, Z angles of driver on the frame.
                cv2.putText(frame, "X: " + "{:7.2f}".format(euler_angle[0, 0]), (20, 20), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), thickness=2)
                cv2.putText(frame, "Y: " + "{:7.2f}".format(euler_angle[1, 0]), (20, 50), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), thickness=2)
                cv2.putText(frame, "Z: " + "{:7.2f}".format(euler_angle[2, 0]), (20, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, (0, 255, 0), thickness=2)

                # Code to show Eye aspect ratio on the frame.
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255),
                            2)

                # Condition to sound the alarm and add comment in log file in camera couldn't detect any face in the frame.
        # Code to show the frame on the screen.
        cv2.namedWindow('demo', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('demo', 1100, 780)
        cv2.imshow("demo", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera_stream.release()

# detect_attentiveness()
# if __name__ == '__main__':
#
#     # delete logs earlier than 7 days
#     if not os.path.exists('logs'):
#         path = "/logs"
#         now = time.time()
#
#         for filename in os.listdir(path):
#             if os.path.getmtime(os.path.join(path, filename)) < now - 7 * 86400:
#                 if os.path.isfile(os.path.join(path, filename)):
#                     # print(filename)
#                     logging.debug('Deleted log - ' + filename)
#                     os.remove(os.path.join(path, filename))
#
#     # Calling the function to detect drivers attentiveness.
#     # If any error occurs then added the code to write the error in the log file.
#     try:
#         detect_attentiveness()
#     except Exception as e:
#         e_type, e_obj, e_trace = sys.exc_info()
#         line_num = e_trace.tb_lineno
#         logging.debug(str(e_obj) + ' at line number - ' + str(line_num))
