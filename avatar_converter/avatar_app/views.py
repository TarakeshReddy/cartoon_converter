from django.shortcuts import render
from .models import MyModel
import cv2
from io import BytesIO
import base64

def process_image(image_path):
    original_image = cv2.imread(image_path)
    
    
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    # Apply a median blur to reduce noise
    blurred_image = cv2.medianBlur(gray_image, 3)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(blurred_image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter to smoothen colors while preserving edges
    color_image = cv2.bilateralFilter(original_image, 3, 200, 200)

    # Create a cartoon-like image by combining edges and color image
    cartoon_image = cv2.bitwise_and(color_image, color_image, mask=edges)

    # Encode the cartoon image as base64
    _, buffer = cv2.imencode('.jpg', cartoon_image)
    image_data = base64.b64encode(buffer).decode('utf-8')
    return image_data

def upload_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        if not image:
            return render(request, 'index.html', {'error': 'Please choose an image to upload.'})
        my_model = MyModel(image=image)
        my_model.save()
        image_path = my_model.image.path

        processed_image_data = process_image(image_path)

        return render(request, 'output.html', {'image_data': processed_image_data})
    return render(request, 'index.html')
