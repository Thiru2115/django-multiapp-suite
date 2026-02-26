import os
import cv2
import numpy as np
import base64
import uuid
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import ImageUploadForm
from django.http import HttpResponse
import mimetypes

def process_image(request):
    processed_image_url = None
    original_image_url = None
    form = ImageUploadForm()

    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = request.FILES.get('image')
            camera_data = form.cleaned_data.get('camera_data')
            action = form.cleaned_data['action']
            quality = form.cleaned_data['quality']
            
            img = None
            filename = None

            if uploaded_image:
                # Handle File Upload
                fs = FileSystemStorage()
                filename = fs.save(uploaded_image.name, uploaded_image)
                file_path = fs.path(filename)
                original_image_url = fs.url(filename)
                img = cv2.imread(file_path)
            
            elif camera_data:
                # Handle Camera Capture (Base64)
                format, imgstr = camera_data.split(';base64,') 
                ext = format.split('/')[-1]
                data = base64.b64decode(imgstr)
                
                filename = f"camera_{uuid.uuid4()}.{ext}"
                file_path = os.path.join(settings.MEDIA_ROOT, filename)
                
                # Ensure MEDIA_ROOT exists
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
                
                with open(file_path, 'wb') as f:
                    f.write(data)
                
                original_image_url = settings.MEDIA_URL + filename
                img = cv2.imread(file_path)

            if img is not None:
                output_filename = f"processed_{filename}"
                output_path = os.path.join(settings.MEDIA_ROOT, output_filename)
                
                # Ensure MEDIA_ROOT exists
                os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

                if action == 'compress':
                    scale = 1.0
                    if quality == 'medium':
                        scale = 0.5
                    elif quality == 'low':
                        scale = 0.25
                    elif quality == 'normal':
                        scale = 1.0
                    
                    if scale != 1.0:
                        height, width = img.shape[:2]
                        new_width = int(width * scale)
                        new_height = int(height * scale)
                        img = cv2.resize(img, (new_width, new_height))
                    
                    cv2.imwrite(output_path, img)

                elif action == 'grayscale':
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    cv2.imwrite(output_path, gray)

                processed_image_url = settings.MEDIA_URL + output_filename
            

    return render(request, 'image_processing/index.html', {
        'form': form,
        'processed_image_url': processed_image_url,
        'original_image_url': original_image_url
    })
