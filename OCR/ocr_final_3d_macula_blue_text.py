import cv2
import pytesseract
import numpy as np

# Load the image
image = cv2.imread('/Users/mertegemencaliskan/Downloads/WhatsApp Image 2024-04-22 at 7.34.38 PM.jpeg')

# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply threshold to create a binary image
_, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Define the lower and upper bounds of blue color in HSV
lower_blue = np.array([110, 10, 75])
upper_blue = np.array([200, 245, 250])

# Convert the image to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a mask for blue regions
blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Bitwise AND to obtain only blue regions
blue_only = cv2.bitwise_and(binary, binary, mask=blue_mask)

# Perform OCR on the masked image
text_data = pytesseract.image_to_data(blue_only, output_type=pytesseract.Output.DICT)

# Iterate over each detected text region
for i in range(len(text_data['text'])):
    # Extract bounding box coordinates
    x, y, w, h = text_data['left'][i], text_data['top'][i], text_data['width'][i], text_data['height'][i]
    # Draw bounding box on the original image
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # Add text label
    cv2.putText(image, text_data['text'][i], (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

# Display the image with text regions highlighted
cv2.imshow('Text Detection', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

