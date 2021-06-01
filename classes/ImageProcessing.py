# Class containing all functions relating to image processing
import cv2
import numpy

# Set up some static variables
# RGB threshold for to see if a pixel is white or not
rgb_thresh = 200
# need at least 500/2500 pixels to be white for it to class as having a number in the call
pixel_count_lower_bound = 500


# small function to stop the webcam to reduce some duplicated code
# Release hardware and software resources
def stop_webcam(webcam):
    webcam.release()
    cv2.destroyAllWindows()


# Function to apply gaussian blur, threshold, and inverse
def blur_threshold_inverse(image):
    blur = cv2.GaussianBlur(image, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    return thresh


# Take the file path to the single digit and then count the number of white pixels
def white_pixel_counter(image):
    white_pixel_count = 0
    for axis in image:
        for pixel in axis:
            if pixel[0] >= rgb_thresh and pixel[1] >= rgb_thresh and pixel[2] >= rgb_thresh:
                white_pixel_count += 1

    if white_pixel_count >= pixel_count_lower_bound:
        return True
    else:
        return False


# Take the image, work out the biggest contour (likely to be the contour for our digit)
# Then black out the rest of the image around the digit the reduce noise
def extract_digit(contours, image):
    # Find max area contour
    areas = []
    for c in contours:
        areas.append(cv2.contourArea(c))
    index = areas.index(max(areas))

    # Crop to get just the digit and find box around the digit
    max_x = 0
    min_x = 1000
    max_y = 0
    min_y = 1000
    for array in contours[index]:
        if array[0][0] > max_y:
            max_y = array[0][0]
        if array[0][0] < min_y:
            min_y = array[0][0]
        if array[0][1] > max_x:
            max_x = array[0][1]
        if array[0][1] < min_x:
            min_x = array[0][1]
    # Create mask to black out whats not the digit
    mask = numpy.zeros(image.shape, numpy.uint8)
    cv2.rectangle(mask, (min_y, min_x), (max_y, max_x), (255, 255, 255), -1)
    # Blacked out the whole image apart from the digit
    digit_image_array = numpy.zeros_like(image)
    digit_image_array[mask == 255] = image[mask == 255]
    return digit_image_array
