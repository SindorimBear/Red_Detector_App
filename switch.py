import cv2 as cv
import numpy as np
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt 

class cam_switch:
    mode = 'default'
    running = True
    
    def __init__(self):
        self.cap = cv.VideoCapture(0)
        self.width = 640
        self.height = 480
        
    @staticmethod
    def set_mode(new_mode):
        cam_switch.mode = new_mode
        
    def stream(self, change_pixmap_signal):
        while self.running:
            ret, img = self.cap.read()
            if not ret:
                print("Camera read error")
                break
            frame = cv.resize(img, (self.width, self.height))
            
            if cam_switch.mode == "default": #기본 카메라 설정 
                processed_frame = cv.cvtColor(img, cv.COLOR_BGR2RGB)
            elif cam_switch.mode == 'gray': #흑백처리
                processed_frame = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
                processed_frame = cv.cvtColor(processed_frame, cv.COLOR_GRAY2RGB)
            elif cam_switch.mode == 'red':  #빨간색 색상 영역 검출
                processed_frame = self.process_red(img)
            elif cam_switch.mode == 'mask':  #마스킹 처리되는 부분 검출
                processed_frame = self.get_red_mask(img)
                if processed_frame.ndim == 2: 
                    processed_frame = cv.cvtColor(processed_frame, cv.COLOR_GRAY2RGB)
                print(f"Red mask area: {np.sum(processed_frame != 0)}")
                
            change_pixmap_signal.emit(processed_frame)
            
    def process_red(self, img):
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = self.red_mask(img_hsv)
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        area = sum(cv.contourArea(contour) for contour in contours if cv.contourArea(contour) > 500)
        cv.drawContours(img, contours, -1, (0, 255, 0), 3)
        print(f"Total Red Area: {area}")
        return cv.cvtColor(img, cv.COLOR_BGR2RGB)
    
    def get_red_mask(self, img):
        img_hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        mask = self.red_mask(img_hsv)
        return mask
    
    def red_mask(self, img_hsv):
        lower_hsv1 = np.array([0,120,180])
        upper_hsv1 = np.array([10,255,255])
        mask1 = cv.inRange(img_hsv, lower_hsv1, upper_hsv1)
        
        lower_hsv2 = np.array([170,120,70])
        upper_hsv2 = np.array([180,255,255])
        mask2 = cv.inRange(img_hsv, lower_hsv2, upper_hsv2)
        
        return mask1 + mask2
    
    def stop(self): #카메라 끄기
        self.running = False
        self.cap.release()
    
def convert(cv_img):
    if cv_img.ndim == 2:
        cv_img = cv.cvtColor(cv_img, cv.COLOR_GRAY2RGB)
    elif cv_img.shape[2] == 1:
        cv_img = cv.cvtColor(cv_img, cv.COLOR_GRAY2RGB)
    
    h, w, ch = cv_img.shape
    bytes_per_line = ch * w
    convert_Qt = QImage(cv_img.data, w, h, bytes_per_line, QImage.Format_RGB888)
    p = convert_Qt.scaled(640, 480, Qt.KeepAspectRatio)
    return QPixmap.fromImage(p)
                        
