from sklearn.neighbors import KDTree
import cv2
import math
from sklearn import neighbors
import os
import os.path
import pickle
from PIL import Image, ImageDraw
import face_recognition
from face_recognition.face_recognition_cli import image_files_in_folder
import numpy as np
import os
import re
from face_recognition import load_image_file, face_locations, face_encodings
from sklearn.neighbors import KDTree
import numpy as np
import pickle

def train(train_dir, model_save_path=None, leaf_size=30, verbose=False):
    X = []
    y = []

    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        print(class_dir)
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            if "resize" in img_path:
                continue  # Skip images with "resize" in their names

            image = load_image_file(img_path)
            face_bounding_boxes = face_locations(image)

            if len(face_bounding_boxes) != 1:
                # If there are no people (or too many people) in a training image, skip the image.
                if verbose:
                    print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
            else:
                # Add face encoding for current image to the training set
                X.append(face_encodings(image, known_face_locations=face_bounding_boxes)[0])
                y.append(class_dir)

    # Create and train the KDTree
    kdtree = KDTree(np.array(X), leaf_size=leaf_size)

    # Save the trained KDTree
    if model_save_path is not None:
        with open(model_save_path, 'wb') as f:
            pickle.dump((kdtree, y), f)

    return kdtree


#def predict(X_frame, kdtree=None, model_path=None, distance_threshold=0.5, k=5):

    if kdtree is None and model_path is None:
        raise Exception("Must supply KDTree either through kdtree or model_path")

    # Load a trained KDTree model (if one was passed in)
    if kdtree is None:
        with open(model_path, 'rb') as f:
            kdtree = pickle.load(f)
    print(kdtree);
    X_face_locations = face_recognition.face_locations(X_frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

    # Use the KDTree to find the best matches for the test face
    distances, indices = kdtree.query(faces_encodings, k=k)

    # Predict classes based on indices and distances
    predictions = []
    for i, (idx, dist) in enumerate(zip(indices, distances)):
        # Check if any of the distances is less than the threshold
        if any(d <= distance_threshold for d in dist):
            # Get the closest index
            closest_index = idx[np.argmin(dist)]
            # Use the index to get the class label
            class_label = kdtree.data[closest_index]
            # Append prediction with class label and face location
            predictions.append((class_label, X_face_locations[i]))
    
    return predictions
def predict(X_frame, kdtree=None, labels=None, model_path=None, distance_threshold=0.5, k=2):

    if (kdtree is None or labels is None) and model_path is None:
        raise Exception("Must supply KDTree and labels either through kdtree, labels or model_path")

    # Load a trained KDTree model and labels (if not provided)
    if kdtree is None or labels is None:
        with open(model_path, 'rb') as f:
            kdtree, labels = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

    # Use the KDTree to find the best matches for the test face
    distances, indices = kdtree.query(faces_encodings, k=k)

    # Predict classes based on indices and distances
    predictions = []
    for i, (idx, dist) in enumerate(zip(indices, distances)):
        # Check if any of the distances is less than the threshold
        if any(d <= distance_threshold for d in dist):
            # Get the closest index
            closest_index = idx[np.argmin(dist)]
            # Use the index to get the class label
            class_label = labels[closest_index]
            # Append prediction with class label and face location
            predictions.append((class_label, X_face_locations[i]))
    
    return predictions

def show_prediction_labels_on_image(frame, predictions):
    pil_image = Image.fromarray(frame)
    draw = ImageDraw.Draw(pil_image)

    for name, (top, right, bottom, left) in predictions:
        # Enlarge the predictions for the full-sized image.
        top *= 1.25
        right *= 1.25
        bottom *= 1.25
        left *= 1.25
        # Draw a box around the face using the Pillow module
        draw.rectangle(((left, top), (right, bottom)), outline=(0, 0, 255))
        # Draw a label with a name below the face
        text_height = 10
        draw.rectangle(((left, bottom - text_height - 10), (right, bottom)), fill=(0, 0, 255), outline=(0, 0, 255))
        draw.text((left + 6, bottom - text_height - 5), name, fill=(255, 255, 255, 255))

    # Remove the drawing library from memory as per the Pillow docs.
    del draw
    # Convert the PIL image to a numpy array for OpenCV compatibility
    opencvimage = np.array(pil_image)

    return opencvimage
def pretrain_model(model_path, new_data_dir, leaf_size=30, verbose=False):
    # Load the trained KDTree model and labels
    with open(model_path, 'rb') as f:
        kdtree, labels = pickle.load(f)

    # Initialize lists to store new data
    X_new = []
    y_new = []
    print(labels)

    # Loop through each image in the new data directory
    for img_path in image_files_in_folder(new_data_dir):
        print(new_data_dir)
        image = face_recognition.load_image_file(img_path)
        face_bounding_boxes = face_recognition.face_locations(image)

        if len(face_bounding_boxes) != 1:
            # If there are no people (or too many people) in an image, skip it.
            if verbose:
                print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
        else:
            # Add face encoding for the current image to the new data
            X_new.append(face_recognition.face_encodings(image, known_face_locations=face_bounding_boxes)[0])
            parts = new_data_dir.split('/')
            y_new.append(parts[-1])

    # Combine labels with y_new
    labels += y_new

    # Concatenate new data with existing data
    X_combined = np.concatenate([np.array(kdtree.data), np.array(X_new)])

    # Re-train the KDTree with the combined data
    kdtree = KDTree(X_combined, leaf_size=leaf_size)

    # Save the updated KDTree and labels
    with open(model_path, 'wb') as f:
        pickle.dump((kdtree, labels), f)

    return kdtree


def predict_target(X_frame, target_label, kdtree=None, labels=None, model_path=None, distance_threshold=0.5, k=3):

    if (kdtree is None or labels is None) and model_path is None:
        raise Exception("Must supply KDTree and labels either through kdtree, labels or model_path")

    # Load a trained KDTree model and labels (if not provided)
    if kdtree is None or labels is None:
        with open(model_path, 'rb') as f:
            kdtree, labels = pickle.load(f)

    X_face_locations = face_recognition.face_locations(X_frame)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test image
    faces_encodings = face_recognition.face_encodings(X_frame, known_face_locations=X_face_locations)

    # Use the KDTree to find the best matches for the test face
    distances, indices = kdtree.query(faces_encodings, k=k)

    # Predict classes based on indices and distances
    predictions = []
    for i, (idx, dist) in enumerate(zip(indices, distances)):
        # Check if any of the distances is less than the threshold
        if any(d <= distance_threshold for d in dist):
            # Get the closest index
            closest_index = idx[np.argmin(dist)]
            # Use the index to get the class label
            class_label = labels[closest_index]
            # Append prediction with class label and face location
            if class_label == target_label:
                predictions.append((class_label, X_face_locations[i]))
    
    return predictions

def recognize_image(image_path):
    # Đọc tấm ảnh từ đường dẫn
    image = cv2.imread(image_path)
    model_path = 'trained_model.pkl'

    # Nhận diện nhãn từ tấm ảnh
    predictions = predict(image, model_path=model_path)

    # In ra nhãn đã nhận diện
    if predictions:
        label = predictions[0][0]  # Lấy nhãn của dự đoán đầu tiên
        print("Thông tin nhận diện:", label)
        return label
    else:
        print("Không thể nhận diện")
        return "unknown"
if __name__ == "__main__":
    print("Training KD...")
    train_dir = "images"
    newtrain_dir = "images/52000132"
    model_save_path = "trained_model.pkl"
    leaf_size = 30  # Optional parameter, default value is 30
    verbose = True  # Optional parameter, default value is False

    # Call the train function
    #trained_model = train(train_dir, model_save_path=model_save_path, leaf_size=leaf_size, verbose=verbose)
    #pretrain
    #pretrain = pretrain_model(model_path=model_save_path, new_data_dir=newtrain_dir, leaf_size=leaf_size, verbose=verbose)
    
    process_this_frame = 29
    print('Setting cameras up...')
    # # multiple cameras can be used with the format url = 'http://username:password@camera_ip:port'
    url = 'http://nhattan:nhattan@192.168.1.8:4747/video'
    cap = cv2.VideoCapture(url)

    while True:
        ret, frame = cap.read()
        if ret:
            # Different resizing options can be chosen based on desired program runtime.
            # Image resizing for more stable streaming
            img = cv2.resize(frame, (0, 0), fx=1, fy=1)
            process_this_frame += 1
            if process_this_frame % 30 == 0:
                predictions = predict(img, model_path="trained_model.pkl")
            frame = show_prediction_labels_on_image(frame, predictions)
            cv2.imshow('camera', frame)
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break

    # #Target
    # while True:
    #     ret, frame = cap.read()
    #     if ret:
    #         # Different resizing options can be chosen based on desired program runtime.
    #         # Image resizing for more stable streaming
    #         img = cv2.resize(frame, (0, 0), fx=1, fy=1)
    #         process_this_frame += 1
    #         if process_this_frame % 30 == 0:
    #             target_label = "tien"  # Đặt nhãn của đối tượng bạn muốn nhận dạng
    #             predictions = predict_target(img, target_label, model_path="trained_model.pkl")
    #         frame = show_prediction_labels_on_image(frame, predictions)
    #         cv2.imshow('camera', frame)
    #         if cv2.waitKey(10) & 0xFF == ord('q'):
    #             break

    # cap.release()
    # cv2.destroyAllWindows()


    
