import cv2
import serial

arduino = serial.Serial('COM8', 9600)  # Replace 'COM8' with your Arduino's port

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

cap = cv2.VideoCapture(0)

while True:
    
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    num_eyes = 0
    eye_distance = 0.0

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        eyes = eye_cascade.detectMultiScale(roi_gray, minNeighbors=5)

        eye_centers = []

        for (ex, ey, ew, eh) in eyes:
            eye_center_x = x + ex + ew // 2
            eye_center_y = y + ey + eh // 2
            vertical_distance = abs(eye_center_y - (y + h // 2))
            max_vertical_distance = h // 6

            if vertical_distance <= max_vertical_distance:
                cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
                cv2.putText(frame, 'Eye', (x + ex, y + ey - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                eye_centers.append((eye_center_x, eye_center_y))

        num_eyes = len(eye_centers)
        if num_eyes == 2:
            eye1_x, eye1_y = eye_centers[0]
            eye2_x, eye2_y = eye_centers[1]
            eye_distance = ((eye2_x - eye1_x) ** 2 + (eye2_y - eye1_y) ** 2) ** 0.5
            cv2.putText(frame, f'Eye Distance: {eye_distance:.2f}', (x, y - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.putText(frame, f'Number of Eyes: {num_eyes}', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imshow('Eye Detection', frame)

    # Check conditions and send signals to Arduino
    if num_eyes == 2 :
        data_to_send = b'off'
        arduino.write(data_to_send + b'\r')  # Sending 'off' signal if conditions met
        print(f"Sent: {data_to_send}")
    elif num_eyes < 2:
        data_to_send = b'on'
        arduino.write(data_to_send + b'\r')  # Sending 'on' signal if conditions met
        print(f"Sent: {data_to_send}")

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

