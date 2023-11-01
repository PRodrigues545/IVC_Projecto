import cv2
import numpy as np

hmin = 43
hmax = 99
smin = 61
smax = 160
vmin = 44
vmax = 141


#funcao responsavel pela segmentacao
def update_segmentation(image_hsv):
    if hmin < hmax:
        ret, mask_hmin = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmin-1,
                                       maxval=1, type=cv2.THRESH_BINARY)
        ret, mask_hmax = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmax,
                                      maxval=1, type=cv2.THRESH_BINARY_INV)
        mask_h = mask_hmin * mask_hmax
    else:
        ret, mask_hmin = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmin,
                                       maxval=1, type=cv2.THRESH_BINARY)
        ret, mask_hmax = cv2.threshold(src=image_hsv[:, :, 0], thresh=hmax-1,
                                       maxval=1, type=cv2.THRESH_BINARY_INV)
        mask_h = cv2.bitwise_or(mask_hmin, mask_hmax)


    ret, mask_smin = cv2.threshold(src=image_hsv[:, :, 1],
                                   thresh=smin, maxval=1, type=cv2.THRESH_BINARY)
    ret, mask_smax = cv2.threshold(src=image_hsv[:, :, 1],
                                   thresh=smax, maxval=1, type=cv2.THRESH_BINARY_INV)
    mask_s = mask_smin * mask_smax


    ret, mask_vmin = cv2.threshold(src=image_hsv[:, :, 2],
                                   thresh=vmin, maxval=1, type=cv2.THRESH_BINARY)
    ret, mask_vmax = cv2.threshold(src=image_hsv[:, :, 1],
                                   thresh=vmax, maxval=1, type=cv2.THRESH_BINARY_INV)
    mask_v = mask_vmin * mask_vmax


    # cv2.imshow("Mask H min", mask_hmin*255)
    # cv2.imshow("Mask H max", mask_hmax * 255)
    #cv2.imshow("Mask H", mask_h * 255)
    #cv2.imshow("Mask S min", mask_smin * 255)
    #cv2.imshow("Mask S max", mask_smax * 255)
    #cv2.imshow("Mask S", mask_s * 255)
    # cv2.imshow("Mask V min", mask_vmin * 255)
    # cv2.imshow("Mask V max", mask_vmax * 255)
    #cv2.imshow("Mask V", mask_v * 255)
    mask = mask_s * mask_h * mask_v
    #cv2.imshow("Mask", mask *255)

    contours, hierarchy = cv2.findContours(image=mask,
                                           mode=cv2.RETR_TREE,
                                           method=cv2.CHAIN_APPROX_NONE)

    mask_filtered = np.zeros(mask.shape, np.uint8)
    for i in range (len(contours)):
        contour = contours[i]
        contour_area = cv2.contourArea(contour)
        if contour_area > 100:
            cv2.drawContours(image=mask_filtered, contours=contours,
                             contourIdx=i, color=1,thickness=-1)
    cv2.imshow("Mask Filtered", mask_filtered * 255)
    return mask_filtered


#Encontrar o centro da mascara
def find_center(mask):

    contours, hierarchy = cv2.findContours(image=mask,
                                           mode=cv2.RETR_TREE,
                                           method=cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0:
        contour = max(contours, key=cv2.contourArea)

        M = cv2.moments(contour)
        if M['m00'] != 0:
            Cx = int(np.round(M['m10'] / M['m00']))
            Cy = int(np.round(M['m01'] / M['m00']))
            return Cx, Cy
    return None

#Criacao de trackbars
def trackbar():
    def on_change_hmin(val):
        global hmin
        hmin = val

    def on_change_hmax(val):
        global hmax
        hmax = val

    def on_change_smin(val):
        global smin
        smin = val

    def on_change_smax(val):
        global smax
        smax = val

    def on_change_vmin(val):
        global vmin
        vmin = val

    def on_change_vmax(val):
        global vmax
        vmax = val

    cv2.namedWindow("Image")
    cv2.createTrackbar("Hmin", "Image", hmin, 180, on_change_hmin)
    cv2.createTrackbar("Hmax", "Image", hmax, 180, on_change_hmax)
    cv2.createTrackbar("Smin", "Image", smin, 255, on_change_smin)
    cv2.createTrackbar("Smax", "Image", smax, 255, on_change_smax)
    cv2.createTrackbar("Vmin", "Image", vmin, 255, on_change_vmin)
    cv2.createTrackbar("Vmax", "Image", vmax, 255, on_change_vmax)