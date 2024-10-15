import torch
import cv2

# Load the YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Option 1: Use a raw string to handle the path correctly
img = cv2.imread(r"C:\Users\DELL\OneDrive\Desktop\Waste_detection\cans-2.png")

# Option 2: Use forward slashes
# img = cv2.imread(""C:\Users\DELL\OneDrive\Desktop\cans.png"")

# Perform object detection
results = model(img)

# Display the image with detected objects
results.show()

# Get the image with detected objects
output_img = results.render()[0]  # Render the results on the image

# Save the output image
cv2.imwrite(r"C:\Users\DELL\OneDrive\Desktop\GLASS-OUTPUT.png", output_img)

print(results.xyxy[0])  # Print detection results to the console
