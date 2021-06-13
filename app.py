from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QFormLayout, QGroupBox,
QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox, QWidget, QMainWindow, QColorDialog,  QFileDialog, QStatusBar, 
QVBoxLayout)
from PyQt5.QtCore import QDir
from PyQt5.QtGui import QPixmap, QColor
import qrcode
import os
import sys
import random
import string

class QR_UI(QDialog):
    def __init__(self, parent=None):
        super(QR_UI, self).__init__(parent)
        self.__createFormGroupBox()
        self.resize(300, 300)
        self.photo_max_size = 240
        self.defaultLocation = QDir().currentPath()
        self.fillColor = "#000"
        self.backgroundColor = "#fff"
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.addButton("Close", QDialogButtonBox.RejectRole)
        self.buttonBox.rejected.connect(self.reject)
        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.formGroupBox)

        self.statusbar = QStatusBar();
        self.statusbar.setStyleSheet("color: green");
        self.statusbar.showMessage("Nadeera Sampath");
        #self.mainLayout.addWidget(self.statusbar);


        self.mainLayout.addWidget(self.buttonBox)
        self.setLayout(self.mainLayout)
        self.setWindowTitle("QR Code Generator V.1.0")
        
    def __createFormGroupBox(self):
        self.formGroupBox = QGroupBox("QR Code Generator")
        self.layout = QFormLayout()

        self.qrtext = QLineEdit()
        self.layout.addRow(QLabel("Text:"), self.qrtext)

        self.fillColorPickerButton = QPushButton('Change')
        self.fillColorPickerButton.setStyleSheet("background-color: #000; color: #fff;")
        self.fillColorPickerButton.setToolTip('Change QR code fill color')
        self.fillColorPickerButton.clicked.connect(self.__onClickFillColorPicker)
        self.fillColorPickerButton.setObjectName("fillColorPickerButton")
        self.layout.addRow(QLabel("Fill color:"), self.fillColorPickerButton)


        self.backgroundColorPickerButton = QPushButton('Change')
        self.backgroundColorPickerButton.setStyleSheet("background-color: #fff; color: #000;")
        self.backgroundColorPickerButton.setToolTip('Change QR code background color')
        self.backgroundColorPickerButton.clicked.connect(self.__onClickBackgroundColorPicker)
        self.backgroundColorPickerButton.setObjectName("backgroundColorPickerButton")
        self.layout.addRow(QLabel("Background color:"), self.backgroundColorPickerButton)

        self.saveLocationPicker = QPushButton(QDir().currentPath())
        self.saveLocationPicker.setStyleSheet("background-color: #fff; color: #000;")
        self.saveLocationPicker.setToolTip('Save location path')
        self.saveLocationPicker.clicked.connect(self.__onClickSaveLocationPicker)
        self.saveLocationPicker.setObjectName("saveLocationPicker")
        self.layout.addRow(QLabel("Save path:"), self.saveLocationPicker)

        self.generateButton = QPushButton('Generate')
        self.generateButton.setToolTip('Generate QR')
        self.generateButton.clicked.connect(self.__generateQR)
        self.layout.addRow(self.generateButton)

        self.image_holder = QLabel('')
        self.preview_image = QPixmap('')
        self.image_holder.setPixmap(self.preview_image)
        
        self.layout.addRow(self.image_holder)
        self.formGroupBox.setLayout(self.layout)



    def __generateQR(self):
        if self.qrtext.text() == "":
            self.msg = QMessageBox()
            self.msg.setText("Error")
            self.msg.setInformativeText('Please insert some text')
            self.msg.setWindowTitle("Color Error")
            self.msg.show()
        else:    
            self.qrcode = self.qrtext.text()
            self.qr = qrcode.QRCode(version=1, box_size=10, border=4)
            self.qr.add_data(self.qrcode)
            self.qr.make(fit=True)
            self.created = self.qr.make_image(fill_color=self.fillColor, back_color=self.backgroundColor)
            self.randomFileName = self.__uniqueid(5)
            defualtSaveLocation = self.defaultLocation
            self.qr_file = os.path.join(defualtSaveLocation, self.qrcode + ".jpg")
            self.img_file = open(self.qr_file, 'wb')
            self.created.save(self.img_file, 'JPEG')
            self.img_file.close()
            self.__onShowQRCode(self.qr_file)

    def __uniqueid(self, length):
        letters = string.ascii_lowercase
        return ''.join(random.choice(letters) for i in range(length))


    def __onShowQRCode(self, filepath):
        self.preview_image = QPixmap(filepath)
        self.image_holder.setPixmap(self.preview_image)


    def __onClickFillColorPicker(self):
        selectedColor = QColorDialog.getColor()
        self.fillColorPickerButton.setStyleSheet("background-color:"+selectedColor.name()+";")
        self.fillColor = selectedColor.name()


    def __onClickBackgroundColorPicker(self):
        selectedColor = QColorDialog.getColor()
        self.backgroundColorPickerButton.setStyleSheet("background-color:"+selectedColor.name()+";")
        self.backgroundColor = selectedColor.name()


    def __onClickSaveLocationPicker(self):
        selected_path = str(QFileDialog.getExistingDirectory())
        self.defaultLocation = selected_path
        self.saveLocationPicker.setText('{}'.format(selected_path))

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    qr_window = QR_UI()
    qr_window.exec_()
    #sys.exit(app.exec_())

