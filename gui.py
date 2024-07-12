import switch
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class CameraThread(QThread):
    change_pixmap_signal = pyqtSignal(object)
    
    def run(self):
        self.cam = switch.cam_switch()
        self.cam.stream(self.change_pixmap_signal)
        
    def stop(self):
        self.cam.running = False
        self.quit()
        self.wait()
        
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.camera_thread = CameraThread()
        
    def initUI(self):
        self.setWindowTitle('Camera Modes')
        
        layout = QVBoxLayout()
        self.toggle_camera = QPushButton('Turn Camera On', self)
        self.toggle_camera.setCheckable(True)
        self.toggle_camera.clicked.connect(self.toggle_camera_func)
        
        self.default_mode = QRadioButton('Default', self)
        self.gray_mode = QRadioButton('Gray', self)
        self.red_mode = QRadioButton ('Red', self)
        self.mask_mode = QRadioButton ('Mask', self)
        
        self.default_mode.setChecked(True)
        
        layout.addWidget(self.toggle_camera)
        layout.addWidget(self.default_mode)
        layout.addWidget(self.gray_mode)
        layout.addWidget(self.red_mode)
        layout.addWidget(self.mask_mode)
        
        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)
        self.setLayout(layout)
        
        self.default_mode.clicked.connect(lambda: self.change_mode('default'))
        self.gray_mode.clicked.connect(lambda: self.change_mode('gray'))
        self.red_mode.clicked.connect(lambda: self.change_mode('red'))
        self.mask_mode.clicked.connect(lambda: self.change_mode('mask'))
        
    @pyqtSlot()
    def toggle_camera_func(self):
        if self.toggle_camera.isChecked():
            self.toggle_camera.setText('Turn Camera Off')
            self.camera_thread.start()
            self.camera_thread.change_pixmap_signal.connect(self.update_image)
        else:
            self.toggle_camera.setText('Turn Camera On')
            self.camera_thread.stop()
            
    def change_mode(self,mode):
        switch.cam_switch.set_mode(mode)
        
    @pyqtSlot(object)
    def update_image(self, cv_img):
        qt_img = switch.convert(cv_img)
        self.image_label.setPixmap(qt_img)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())