# 0331
import shutil
import os
from PyQt5.QtWidgets import *

# # path
# org_path = r'D:\Test\test.jpg'
# c_path = r'D:\Copy\test.jpg'

class Auto(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.resize(400, 300)
        self.setWindowTitle("UI")
        
        # path input
        self.org_path = QLineEdit()
        self.org_path.setText('원본/삭제할 파일 경로')

        self.result_path = QLineEdit()
        self.result_path.setText('복사할 경로')

        # make button
        copy_button = QPushButton("Copy")
        move_button = QPushButton("Move")
        remove_button = QPushButton("Remove")
        close_button = QPushButton("Close")

        # line layout
        line_lay = QVBoxLayout()
        line_lay.addWidget(self.org_path)
        line_lay.addWidget(self.result_path)

        # btn layout
        btn_lay = QHBoxLayout()
        btn_lay.addWidget(copy_button)
        btn_lay.addWidget(move_button)
        btn_lay.addWidget(remove_button)
        btn_lay.addWidget(close_button)

        # UI Layout
        main_lay = QVBoxLayout()
        main_lay.addLayout(line_lay)
        main_lay.addLayout(btn_lay)

        print(type(self.org_path.text()))

        # event
        self.setLayout(main_lay)
        copy_button.clicked.connect(self.copy)
        move_button.clicked.connect(self.move)
        remove_button.clicked.connect(self.remove)
        close_button.clicked.connect(self.close)

    # copy
    def copy(self):
        shutil.copyfile(self.org_path.text(), self.result_path.text())
        print('copy done')

    # move
    def move(self):
        shutil.move(self.org_path.text(), self.result_path.text())
        print('move done')

    # remove
    def remove(self):
        os.remove(self.org_path.text())
        print('remove done')

if __name__ == '__main__':
    app = QApplication([])
    dialog = Auto() # call class
    dialog.show() # class show. 
    app.exec_()
    print("program done")