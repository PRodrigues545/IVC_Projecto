import cv2
import segmentation

cap = cv2.VideoCapture()

def camara_loop():
    if not cap.isOpened():
        cap.open(0)
        _, image = cap.read()
        #cv2.imshow("Image", image)
    else:
        ret, image = cap.read()

        if not ret:
            print("Error capturing frame.")

        else:
            image = image[:, ::-1, :]
            cv2.imshow("Image", image)
            # window_size = cv2.getWindowImageRect("Image")
            image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

            mask = segmentation.update_segmentation(image_hsv)

            center = segmentation.find_center(mask)
            if center is not None:
                center_x = center[0]

                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                cv2.circle(image, center, 5, (0, 255, 0), -1)
                #cv2.imshow("Result", image)
                return center_x
