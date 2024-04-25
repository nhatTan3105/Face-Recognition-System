import os
import glob
import time
import cv2
import numpy as np
from tqdm import tqdm
import pickle
COSINE_THRESHOLD = 0.5


def match(recognizer, feature1, dictionary):
    max_score = 0.0
    sim_user_id = ""
    for user_id, feature2 in zip(dictionary.keys(), dictionary.values()):
        score = recognizer.match(
            feature1, feature2, cv2.FaceRecognizerSF_FR_COSINE)
        if score >= max_score:
            max_score = score
            sim_user_id = user_id
    if max_score < COSINE_THRESHOLD:
        return False, ("", 0.0)
    return True, (sim_user_id, max_score)

def recognize_face(image, face_detector, face_recognizer, file_name=None):
    channels = 1 if len(image.shape) == 2 else image.shape[2]
    if channels == 1:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    if channels == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    if image.shape[0] > 1000:
        image = cv2.resize(image, (0, 0),
                           fx=500 / image.shape[0], fy=500 / image.shape[0])

    height, width, _ = image.shape
    face_detector.setInputSize((width, height))
    try:
        dts = time.time()
        _, faces = face_detector.detect(image)
        if file_name is not None:
            assert len(faces) > 0, f'the file {file_name} has no face'

        faces = faces if faces is not None else []
        features = []
        #print(f'time detection  = {time.time() - dts}')
        for face in faces:
            rts = time.time()

            aligned_face = face_recognizer.alignCrop(image, face)
            feat = face_recognizer.feature(aligned_face)
            #print(f'time recognition  = {time.time() - rts}')

            features.append(feat)
        return features, faces
    except Exception as e:
        print(e)
        print(file_name)
        return None, None
    
def train(directory):
    
    # Init models face detection & recognition
    weights = os.path.join(directory, "models",
                           "face_detection_yunet_2022mar.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    face_detector.setScoreThreshold(0.87)

    weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

    # Get registered photos and return as npy files
    # File name = id name, embeddings of a photo is the representative for the id
    # If many files have the same name, an average embedding is used
    dictionary = {}
    # the tuple of file types, please ADD MORE if you want
    types = ('*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG', '*.JPEG')
    files = []
    for a_type in types:
        files.extend(glob.glob(os.path.join(directory, 'images', a_type)))

    files = list(set(files))
    print(files)
    for file in tqdm(files):

        image = cv2.imread(file)

        feats, faces = recognize_face(
             image, face_detector, face_recognizer, file)
        if faces is None:
             continue
        user_id = os.path.splitext(os.path.basename(file))[0]
        
        dictionary[user_id] = feats[0]

    print(f'there are {len(dictionary)} ids')
    # Lưu dữ liệu embeddings vào file
    with open('data_embeddings.pkl', 'wb') as f:
        pickle.dump(dictionary, f)


def pretrain(directory):
    # Init models face detection & recognition
    weights = os.path.join(directory, "models",
                           "face_detection_yunet_2022mar.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    face_detector.setScoreThreshold(0.87)

    weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")

    with open('data_embeddings.pkl', 'rb') as f:
        dictionary = pickle.load(f)

    # Thêm ảnh mới vào file pickle
    files = []
    types = ('*.jpg', '*.png', '*.jpeg', '*.JPG', '*.PNG', '*.JPEG')
    for a_type in types:
        files.extend(glob.glob(os.path.join(directory, 'images', a_type)))

    files = list(set(files))
    for file in tqdm(files):
        image = cv2.imread(file)
        feats, _ = recognize_face(image, face_detector, face_recognizer)
        if feats is None:
            continue
        user_id = os.path.splitext(os.path.basename(file))[0]
        dictionary[user_id] = feats[0]

    print(f'Pretraining completed. Total {len(dictionary)} ids.')

    # Lưu dữ liệu embeddings vào file
    with open('data_embeddings.pkl', 'wb') as f:
        pickle.dump(dictionary, f)

def detect_and_draw_labels(dictionary, image, face_detector, face_recognizer):
    
    fetures, faces = recognize_face(image, face_detector, face_recognizer)

    for idx, (face, feature) in enumerate(zip(faces, fetures)):
        result, user = match(face_recognizer, feature, dictionary)
        box = list(map(int, face[:4]))
        color = (0, 255, 0) if result else (0, 0, 255)
        thickness = 2
        cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

        id_name, score = user if result else (f"unknown_{idx}", 0.0)
        text = "{0} ({1:.2f})".format(id_name, score)
        position = (box[0], box[1] - 10)
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.6
        cv2.putText(image, text, position, font, scale,
                    color, thickness, cv2.LINE_AA)
        return image, user[0]

    return image, None

def detect_and_draw_labels_target(label, dictionary, image, face_detector, face_recognizer):
    
    fetures, faces = recognize_face(image, face_detector, face_recognizer)

    for idx, (face, feature) in enumerate(zip(faces, fetures)):
        result, user = match(face_recognizer, feature, dictionary)
        if label == user[0]:
            box = list(map(int, face[:4]))
            color = (0, 255, 0) if result else (0, 0, 255)
            thickness = 2
            cv2.rectangle(image, box, color, thickness, cv2.LINE_AA)

            id_name, score = user if result else (f"unknown_{idx}", 0.0)
            text = "{0} ({1:.2f})".format(id_name, score)
            position = (box[0], box[1] - 10)
            font = cv2.FONT_HERSHEY_SIMPLEX
            scale = 0.6
            cv2.putText(image, text, position, font, scale,
                        color, thickness, cv2.LINE_AA)
    return image

def recognize_image(image_url, dictionary, face_detector, face_recognizer):
    image = cv2.imread(image_url)
    features, faces = recognize_face(image, face_detector, face_recognizer)
    
    for face, feature in zip(faces, features):
        user = match(face_recognizer, feature, dictionary)
        return user[1][0]


if __name__ == '__main__':
    directory = 'data'
    with open('data_embeddings.pkl', 'rb') as f:
        dictionary = pickle.load(f)
    # Init models face detection & recognition
    weights = os.path.join(directory, "models",
                           "face_detection_yunet_2022mar.onnx")
    face_detector = cv2.FaceDetectorYN_create(weights, "", (0, 0))
    face_detector.setScoreThreshold(0.87)

    weights = os.path.join(directory, "models", "face_recognizer_fast.onnx")
    face_recognizer = cv2.FaceRecognizerSF_create(weights, "")
    train(directory)
    #img = recognize_image('D:\Download\\b.jpg', dictionary, face_detector, face_recognizer)
    # capture = cv2.VideoCapture(0)
    # if not capture.isOpened():
    #     sys.exit()
    # with open('data_embeddings.pkl', 'rb') as f:
    #         dictionary = pickle.load(f)
    # while True:
    #     result, image = capture.read()
    #     if result is False:
    #         cv2.waitKey(0)
    #         break
    #     image = detect_and_draw_labels(dictionary, image, face_detector, face_recognizer)
    #     cv2.imshow("face recognition", image)