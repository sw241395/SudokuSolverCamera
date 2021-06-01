# Improvement from camera1
# same basis but we are trying to just extract the digit from the split image
# so the grid lines are removed

import cv2
# How to add functions and classes from the ./classes folder
import sys
sys.path.append("./classes")
import ImageProcessing
import OCR
import TempFolder
import GUI
import SudokuSolver

# Set up static variables
# Square position
x_axis = 85  # 85 pixels right form top left
y_axis = 15  # 15 pixels down from top left
axis_length = 454
split_image_width = int(((y_axis + axis_length - 1) - (y_axis + 3)) / 9)

# Set up temp folder to save image whilst processing
TempFolder.create_temp_folder()

# Start the webcam
key = cv2.waitKey(1)
webcam = cv2.VideoCapture(0)

# Loop to keep the webcam running
while True:
    try:
        # Display the webcam and also a square for where to put the sudoku grid
        check, frame = webcam.read()

        # create 9x9 grid to get the sudoku grid lined up
        for column in range(10):
            cv2.line(frame, ((x_axis + (split_image_width * column)), y_axis), ((x_axis + (split_image_width * column)), (y_axis + (split_image_width * 9))), (0, 255, 0), 1)
        for row in range(10):
            cv2.line(frame, (x_axis, (y_axis + (split_image_width * row))), ((x_axis + (split_image_width * 9)), (y_axis + (split_image_width * row))), (0, 255, 0), 1)

        cv2.imshow("Capturing ('s' to take photo, 'q' to quit)", frame)
        key = cv2.waitKey(1)

        if key == ord('s'):
            # Need to save the image first before processing
            cv2.imwrite(filename=TempFolder.full_image_file_name, img=frame)

            # Release hardware and software resources
            ImageProcessing.stop_webcam(webcam)

            # get cropped image of just the sudoku grid (in greyscale)
            img_new = cv2.imread(TempFolder.full_image_file_name, cv2.IMREAD_GRAYSCALE)
            crop = img_new.copy()[y_axis + 3:y_axis + axis_length - 1, x_axis + 3:x_axis + axis_length - 1]

            # split the image into 81 equal sized images to process the numbers
            grid = []
            for y in range(9):
                for x in range(9):
                    # Get the cell and resize it as a 28x28 pixel image to work with the CNN
                    split_image_array = crop.copy()[split_image_width * y:split_image_width * (y + 1), split_image_width * x:split_image_width * (x + 1)]

                    # Apply gaussian blur, threshold, and inverse
                    thresh = ImageProcessing.blur_threshold_inverse(split_image_array)

                    # Save image
                    split_image_file_name = str(y) + "," + str(x) + ".jpg"
                    split_image = TempFolder.save_image(thresh, split_image_file_name)

                    # Check to see if the cell is blank
                    if ImageProcessing.white_pixel_counter(split_image):
                        # Crop to get just the digit
                        contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                        digit_image_array = ImageProcessing.extract_digit(contours, split_image)

                        # Save digit image
                        digit_image_file_name = str(y) + "," + str(x) + "digit.jpg"
                        digit_image = TempFolder.save_image(digit_image_array, digit_image_file_name)

                        # Using OCR to predict the digit
                        digit = OCR.number_recognition(digit_image)
                    else:
                        digit = 0

                    grid.append(digit)

            SudokuSolver.set_up_boxes()

            # Check to see if the grid is correct (tkinter gui)
            GUI.start_gui(grid)

            # Get values from the tkinter gui
            corrected_grid = GUI.new_grid

            # Solve grid
            solution = SudokuSolver.solve_grid(corrected_grid)

            # Output solution
            GUI.solution_gui(solution)
            break
        elif key == ord('q'):
            ImageProcessing.stop_webcam(webcam)
            break

    except KeyboardInterrupt:
        ImageProcessing.stop_webcam(webcam)
        break

# Delete temp folder
TempFolder.remove_temp_folder()

