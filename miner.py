'''
facerecog / agrim
'''
user = "prateek" 
print 'Hello ', user, "!"
# USAGE
# python miner.py --shape-predictor shape_predictor_68_face_landmarks.dat
# python miner.py --shape-predictor shape_predictor_68_face_landmarks.dat --alarm alarm.wav

from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
from threading import Thread
import numpy as np
import playsound
import argparse
import imutils
import time
import dlib
import cv2
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
from matplotlib import style
import os.path
import csv
import datetime as dt
import time
import pymysql

db = pymysql.connect("192.178.5.10","root","root","bharathacks")
cursor = db.cursor()
# likely that you'll have to do pip install pyobjc on mac bc the stupid sound doesn't play otherwise. 

#logo

def sound_alarm(path):
	# play an alarm sound
	playsound.playsound(path)

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
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
	help="path to facial landmark predictor")
ap.add_argument("-a", "--alarm", type=str, default="",
	help="path alarm .WAV file")
ap.add_argument("-w", "--webcam", type=int, default=0,
	help="index of webcam on system")
args = vars(ap.parse_args())
 
# define two constants, one for the eye aspect ratio to indicate
# blink and then a second constant for the number of consecutive
# frames the eye must be below the threshold for to set off the
# alarm
EYE_AR_THRESH = 0.20
EYE_AR_CONSEC_FRAMES = 13

# initialize the frame counter as well as a boolean used to
# indicate if the alarm is going off
COUNTER = 0
ALARM_ON = False

print("[WELCOME] FaceRecog Asia Live Fatigue Monitoring System")
# initialize dlib's face detector (HOG-based) and then create
# the facial landmark predictor
print("[INFO] loading facial landmark predictor...")
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(args["shape_predictor"])

# grab the indexes of the facial landmarks for the left and
# right eye, respectively
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# start the video stream thread
print("[INFO] starting video stream thread...")
vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

#plot stuff

# timestr = time.strftime("%Y%m%d-%H%M%S")
# axisdate = time.strftime("%Y-%m-%d %H:%M:%S")
# # print(axisdate)
# earfile = open(timestr + '.txt', 'w+')
style.use('fivethirtyeight')

# fig_ear = plt.figure()
# ax1 = fig_ear.add_subplot(1, 1, 1)

# xs = []
# ys = []

# def animate(i):
# 	graph_data = csv.reader(open('earfile.csv'))
# 	# lines = graph_data.split('\n')
# 	for line in graph_data:
# 			if len(line)>1:
# 					# x, y = line.split(',')
# 					xs.append(line[1])
# 					ys.append(dt.datetime.strptime(line[0],'%M:%S.%f'))
# 	ax1.clear()
# 	ax1.plot(xs, ys)
# 	fig_eat.autofmt_xdate()

# loop over frames from the video stream
while True:
	# grab the frame from the threaded video file stream, resize
	# it, and convert it to grayscale
	# channels)
	frame = vs.read()
	frame = imutils.resize(frame, width=900)
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# detect faces in the grayscale frame
	rects = detector(gray, 0)

	# loop over the face detections
	for rect in rects:
		# determine the facial landmarks for the face region, then
		# convert the facial landmark (x, y)-coordinates to a NumPy
		# array
		shape = predictor(gray, rect)
		shape = face_utils.shape_to_np(shape)

		# extract the left and right eye coordinates, then use the
		# coordinates to compute the eye aspect ratio for both eyes
		leftEye = shape[lStart:lEnd]
		rightEye = shape[rStart:rEnd]
		leftEAR = eye_aspect_ratio(leftEye)
		rightEAR = eye_aspect_ratio(rightEye)

		# average the eye aspect ratio together for both eyes
		ear = (leftEAR + rightEAR) / 2.0
		file_exists = os.path.isfile('earfile.csv')

		with open('earfile.csv', 'ab') as csvfile:
			fieldnames = ['Timestamp', 'EAR']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
		
			if not file_exists:
  				writer.writeheader()
			writer.writerow({'Timestamp': time.strftime("%Y-%m-%d %H:%M:%S"), 'EAR': ear})
			sql = "INSERT INTO "+user+" (time,ear) VALUES ('%s','%s')" % (str(int(time.time()),), str(ear))
			try:
				cursor.execute(sql)
				db.commit()
			except:
				db.rollback()
		
		# earfile.write(('%s','%s') % (axisdate, ear) + '\n')

		# compute the convex hull for the left and right eye, then
		# visualize each of the eyes
		leftEyeHull = cv2.convexHull(leftEye)
		rightEyeHull = cv2.convexHull(rightEye)
		cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
		cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

		# check to see if the eye aspect ratio is below the blink
		# threshold, and if so, increment the blink frame counter
		if ear < EYE_AR_THRESH:
			COUNTER += 1

			# if the eyes were closed for a sufficient number of
			# then sound the alarm
			if COUNTER >= EYE_AR_CONSEC_FRAMES:
				# if the alarm is not on, turn it on
				if not ALARM_ON:
					ALARM_ON = True

					# check to see if an alarm file was supplied,
					# and if so, start a thread to have the alarm
					# sound played in the background
					if args["alarm"] != "":
						t = Thread(target=sound_alarm,
							args=(args["alarm"],))
						t.deamon = True
						t.start()

				# draw an alarm on the frame
				cv2.putText(frame, "FATIGUE ALERT!", (10, 30),
					cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

		# otherwise, the eye aspect ratio is not below the blink
		# threshold, so reset the counter and alarm
		else:
			COUNTER = 0
			ALARM_ON = False

		# draw the computed eye aspect ratio on the frame to help
		# with debugging and setting the correct eye aspect ratio
		# thresholds and frame counters
		cv2.putText(frame, "EAR: {:.2f}".format(ear), (750, 30),
			cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
		
	# show the frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# # show graph
	# ani = animation.FuncAnimation(fig_ear, animate, interval=500)
	# plt.show()
 
	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# do a bit of cleanup
cv2.destroyAllWindows()
db.close()
vs.stop()
# earfile.close()