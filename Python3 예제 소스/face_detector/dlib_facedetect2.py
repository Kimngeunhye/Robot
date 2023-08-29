import cv2, dlib, sys
import numpy as np



# initialize face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


W_View_size = 320
#H_View_size = int(W_View_size / 1.777)
H_View_size = int(W_View_size / 1.333)

# load video
cap = cv2.VideoCapture(0)
cap.set(3, W_View_size)
cap.set(4, H_View_size)
    


face_roi = []
face_sizes = []

scaler = 1

# loop
while True:
  # read frame buffer from video
  ret, img = cap.read()
  if not ret:
    break

  # resize frame
  img = cv2.resize(img, (int(img.shape[1] * scaler), int(img.shape[0] * scaler)))
  ori = img.copy()

  # find faces
  if len(face_roi) == 0:
    faces = detector(img, 1)
  else:
    roi_img = img[face_roi[0]:face_roi[1], face_roi[2]:face_roi[3]]
    # cv2.imshow('roi', roi_img)
    faces = detector(roi_img)

  # no faces
  if len(faces) == 0:
    print('no faces!')

  # find facial landmarks
  for face in faces:
    if len(face_roi) == 0:
      dlib_shape = predictor(img, face)
      shape_2d = np.array([[p.x, p.y] for p in dlib_shape.parts()])
    else:
      dlib_shape = predictor(roi_img, face)
      shape_2d = np.array([[p.x + face_roi[2], p.y + face_roi[0]] for p in dlib_shape.parts()])

    for s in shape_2d:
      cv2.circle(img, center=tuple(s), radius=1, color=(0, 255, 0), thickness=1, lineType=cv2.LINE_AA)

    # compute face center
    center_x, center_y = np.mean(shape_2d, axis=0).astype(np.int)

    # compute face boundaries
    min_coords = np.min(shape_2d, axis=0)
    max_coords = np.max(shape_2d, axis=0)

    # draw min, max coords
    cv2.circle(img, center=tuple(min_coords), radius=1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)
    cv2.circle(img, center=tuple(max_coords), radius=1, color=(255, 0, 0), thickness=2, lineType=cv2.LINE_AA)

    # compute face size
    face_size = max(max_coords - min_coords)
    face_sizes.append(face_size)
    if len(face_sizes) > 10:
      del face_sizes[0]
    mean_face_size = int(np.mean(face_sizes) * 1.8)

    # compute face roi
    face_roi = np.array([int(min_coords[1] - face_size / 2), int(max_coords[1] + face_size / 2), int(min_coords[0] - face_size / 2), int(max_coords[0] + face_size / 2)])
    face_roi = np.clip(face_roi, 0, 10000)

   

  # visualize
  #cv2.imshow('original', ori)
  cv2.imshow('dlib_facedetect2', img)
  #cv2.imshow('result', result)
  if 0xFF & cv2.waitKey(1) == 27:  # ESC  Key
    sys.exit(1)
