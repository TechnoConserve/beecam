import numpy as np
import cv2


def rotate(image, angle, center=None, scale=1.0):
    """
    Convenience function to rotate and optionally scale an image.
    :param image: Image to be manipulated.
    :param angle: Angle to rotate the image.
    :param center: Center coordinate from which to perform the
    rotation.
    :param scale: Amount to scale the image.
    :return: Return the rotated image.
    """
    # Grab the dimensions of the image
    (h, w) = image.shape[:2]

    # If the center is None, initialize it as the center of the image
    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # Return the rotated image
    return rotated


def translate(image, x, y):
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))
    return shifted
