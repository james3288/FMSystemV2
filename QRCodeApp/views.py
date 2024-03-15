from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from fmsLogin.models import Items
import cv2 
import qrcode 
import numpy as np 

# Create your views here.
def scan_qr_code(request):
    # Initialize the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        if not ret:
            continue

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Use OpenCV to detect QR codes in the frame
        detector = cv2.QRCodeDetector()
        data, vertices, _ = detector.detectAndDecode(gray)

        if data:
            # Draw a bounding box around the QR code
            for i in range(4):
                cv2.line(frame, tuple(vertices[i][0]), tuple(vertices[(i + 1) % 4][0]), (0, 255, 0), 3)

            # Display the QR code data on the frame
            cv2.putText(frame, data, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Encode the data as a QR code and save it as an image
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)
            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save('qrcode.png')

            # Release the camera and return the QR code data
            cap.release()
            return JsonResponse({'data': data})

        # Display the camera frame
        cv2.imshow('QR Code Scanner', frame)

        # Exit the loop when the user presses the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()


    context     = my_context()
    return render(request, 'QRCodeApp/qrcode.html',context)

def QrCodePage(request):
    context     = my_context()

    if 'user_id' in request.session:     
        return render(request,'QRCodeApp/qrcode.html',context)
    else:
        return redirect('/login/')  

def my_context():
    items = Items()    
    context = {
                'facilities': items.Facilities(),
                'borrowed': items.Borrowed(),
                'repaired': len(items.Repaired()),
                'vacant': items.Vacant(),
                #'activities': items.Recent_Activities(),
                'supplier_price_update': items.Supplier_Price_Update(),         
                'selected': '',
                'defective': items.Defective(),
                }    
    
    return context