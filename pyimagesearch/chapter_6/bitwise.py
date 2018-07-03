import numpy as np
import cv2

# First, lets draw a rectangle
rectangle = np.zeros((300, 300), dtype='uint8')
cv2.rectangle(rectangle, (25, 25), (275, 275), 255, -1)
cv2.imshow("Rectangle", rectangle)

# Secondly, lets draw a circle
circle = np.zeros((300, 300), dtype='uint8')
cv2.circle(circle, (150, 150), 150, 255, -1)
cv2.imshow("Circle", circle)

"""
A bitwise 'AND' is only True when both rectangle and circle have
a value that is 'ON.' Simply put, the bitwise AND function
examines every pixel in rectable and circle. If both pixels
have a value rather than zero, that pixel is turn 'ON' (i.e.
set to 255 in the output image). If both pixels are not greater
than zero, then the output pixel is left 'OFF' with a value of 0.
"""
bitwise_and = cv2.bitwise_and(rectangle, circle)
cv2.imshow("AND", bitwise_and)

"""
A bitwise 'OR' examines every pixel in rectangle and circle. If
EITHER pixel in rectangle or circle is greater than zero, then
the ouput pixel has a value of 255, otherwise it is 0.
"""
bitwise_or = cv2.bitwise_or(rectangle, circle)
cv2.imshow("OR", bitwise_or)

"""
The bitwise 'XOR' is identical to the 'OR' function, with one
exception: both rectangle and circle are not allowed to BOTH
have values greater than 0.
"""
bitwise_xor = cv2.bitwise_xor(rectangle, circle)
cv2.imshow("XOR", bitwise_xor)

"""
Finally, the bitwise 'NOT' inverts the values of the pixels. Pixels
with a value of 255 become 0, and pixels with a value of 0 become
255:
"""
bitwise_not = cv2.bitwise_not(circle)
cv2.imshow("NOT", bitwise_not)
cv2.waitKey(0)
