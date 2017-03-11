from image_helper import rgb_image, rgb_to_gray
import cv2
import glob
import numpy as np
import pickle


def calibrate():
    # List of images to be used for calibration
    images_glob = glob.glob("camera_cal/calibration*.jpg")

    # Shape of the calibration images
    image_shape = rgb_image(images_glob[0]).shape[1::-1]

    # Number of columns and rows for the chessboard
    chessboard_shape = (9, 6)

    # Where to save the calibration data
    output_file = "./calibration.pkl"

    objpoints = []
    imgpoints = []

    for filepath in images_glob:
        # Load image
        img = rgb_image(filepath)

        # Convert image to grayscale
        gray = rgb_to_gray(img)

        # Find chessboard corners for image
        pattern_was_found, corners = cv2.findChessboardCorners(gray, chessboard_shape, None)

        # Create an object points array
        cols, rows = chessboard_shape
        objp = np.zeros((cols * rows, 3), np.float32)
        objp[:,:2] = np.mgrid[0:cols, 0:rows].T.reshape(-1, 2)

        if pattern_was_found:
            objpoints.append(objp)
            imgpoints.append(corners)

    # Use the object points and image points to calibrate a camera
    _, mtx, dist, _, _ = cv2.calibrateCamera(objpoints, imgpoints, image_shape, None, None)

    # Save the calibration data for use later
    save_calibration_data(output_file, mtx, dist)

def load_calibration_data(filepath):
    with open(filepath, "rb") as f:
        data = pickle.load(f)
        mtx, dist = data["mtx"], data["dist"]
        return mtx, dist

def save_calibration_data(filepath, mtx, dist):
    with open(filepath, "wb") as f:
        data = {}
        data["mtx"] = mtx
        data["dist"] = dist
        pickle.dump(data, f)

if __name__ == "__main__":
    calibrate()
