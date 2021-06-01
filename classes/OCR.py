# Class containing functions relating to OCR
# OCR = Object Character Recognition

import pytesseract


# Using Tesseracts to try and get the number form the image
def number_recognition(image):
    digit = pytesseract.image_to_string(image, config=("-c tessedit"
                                                       "_char_whitelist=123456789"
                                                       " --psm 10"
                                                       " -l osd")).strip()
    if digit == '':
        digit = 0
    return int(digit)
