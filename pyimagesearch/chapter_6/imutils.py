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


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    """
    Resize an image to a given height or width while preserving its
    aspect ratio.
    :param image: The image to resize.
    :param width: The desired width of the returned image.
    :param height: The desired height of the returned image.
    :param inter: The interpolation method to use.
    :return: Return the resized image.
    """
    # Initialize the dimensions of the image to be resized and grab
    # the image size
    dim = None
    (h, w) = image.shape[:2]

    # If both the width and height are None, then return the original
    # image
    if width is None and height is None:
        return image

    # Check to see if the width is None
    if width is None:
        # Calculate the ratio of the height and construct the dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # Otherwise the height is None
    else:
        # Calculate the ratio of the width and construct the dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # Resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # Return the resized image
    return resized
