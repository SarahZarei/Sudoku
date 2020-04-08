import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from random import randint

btnsStyle = "background-color: #ff6600; border-radius: 10px;"
font1 = QFont('Times', 14, QFont.Bold)
font2 = QFont('Times', 10, QFont.Bold)

class Sudoku(QWidget):
    def __init__(self):
        super(Sudoku, self).__init__()
        
        self.setWindowTitle('Sudoku')
        self.setFixedSize(500, 600)
        self.counter = 0

        fileNumber = randint(1, 20)
        selectedFile = open('files/k' + str(fileNumber) + '.txt', 'r')
        readFile = selectedFile.read()

        self.cells = []
        rows = readFile.split('\n')
        for row in rows:
            self.cells.append(row.split(' '))

        v_layout = QVBoxLayout()
        hLayoutTop = QHBoxLayout()
        gLayout = QGridLayout()
        hLayoutBottom = QHBoxLayout()

        btnCheck = QPushButton()
        btnCheck.setText('Check Game')
        btnCheck.setFixedSize(120, 40)
        btnCheck.setFont(font2)
        btnCheck.clicked.connect(self.check)
        btnCheck.setStyleSheet(btnsStyle)
        hLayoutTop.addWidget(btnCheck, alignment= Qt.AlignRight)

        obj_validator = QIntValidator(1, 9)
        self.tb = [[QLineEdit() for i in range(9)] for j in range(9)]
        for i in range(9):
            for j in range(9):
                self.tb[i][j].setAlignment(Qt.AlignCenter)
                self.tb[i][j].setFixedSize(50, 50)
                self.tb[i][j].setFont(font1)
                self.tb[i][j].setMaxLength(1)
                self.tb[i][j].setValidator(obj_validator)

                if self.cells[i][j] != '0':
                    self.tb[i][j].setText(self.cells[i][j])
                    self.tb[i][j].setReadOnly(True)
                self.tb[i][j] = self.tb[i][j]
                gLayout.addWidget(self.tb[i][j], i, j)
        
        self.btnColorMode = QPushButton()
        self.btnColorMode.setText('dark mode')
        self.btnColorMode.setFixedSize(120, 40)
        self.btnColorMode.setFont(font2)
        self.btnColorMode.clicked.connect(self.on_click)
        self.btnColorMode.setStyleSheet(btnsStyle)
        hLayoutBottom.addWidget(self.btnColorMode, alignment= Qt.AlignLeft)

        self.lblText = QLabel()
        self.lblText.setStyleSheet('color: #ff6600;')
        self.lblText.setFont(font1)
        hLayoutBottom.addWidget(self.lblText)
        
        v_layout.addLayout(hLayoutTop)
        v_layout.addLayout(gLayout)
        v_layout.addLayout(hLayoutBottom)
        self.setLayout(v_layout)

        self.mode_checker('dark')
        self.show()

    def on_click(self):
        self.counter += 1
        if self.counter % 2 == 1:
            self.mode = 'light'
            self.mode_checker(self.mode)
        else:
            self.mode = 'dark'
            self.mode_checker(self.mode)  

    def check(self):
        ok = True
        # row check
        for row in range(9):
            for i in range(9):
                for j in range(9):
                    if self.tb[row][i].text() == self.tb[row][j].text() and self.tb[row][i].text() != '' and \
                            self.cells[row][i] == '0' and i != j:
                        if self.mode == 'light' or self.mode == 'dark':
                            self.tb[row][i].setStyleSheet('background-color: #ee2737')
                            ok = False

        for col in range(9):
            for i in range(9):
                for j in range(9):
                    if self.tb[i][col].text() == self.tb[j][col].text() and self.tb[i][col].text() != '' and \
                            self.cells[i][col] == '0' and i != j:
                        if self.mode == 'light' or self.mode == 'dark':
                            self.tb[i][col].setStyleSheet('background-color: #ee2737')
                            ok = False

        for row in range(0, 9, 3):
            for col in range(0, 9, 3):
                for i in range(row, row+3):
                    for j in range(col, col + 3):
                        for k in range(row, row + 3):
                            for l in range(col, col + 3):
                                if self.tb[i][j].text() == self.tb[k][l].text() and \
                                        self.tb[i][j].text() != '' and self.cells[i][j] == '0' and(j != l or i != k):
                                    self.tb[i][j].setStyleSheet('background-color: #ffe033')
                                    ok = False

        if all(self.tb[i][col].text() != '' for i in range(9) for j in range(9)) and ok:
            self.lblText.setText('YOU Win!')
            # msg = QMessageBox()
            # msg.setText('win')
            # msg.exec()
            # exit()

    def mode_checker(self, modePTR):
        
        self.mode = modePTR
        if self.mode == 'dark':
            self.btnColorMode.setText('Light Mode')
            self.setStyleSheet('background-color: #171717')
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j] == '0':
                        self.tb[i][j].setStyleSheet('color: 171717; background-color: #999999;')
                    if self.cells[i][j] != '0':
                        self.tb[i][j].setStyleSheet('color: #ececec; background-color: #444444;')

        elif self.mode == 'light':
            self.btnColorMode.setText('Dark Mode')
            self.setStyleSheet('background-color: #ffffff')
            for i in range(9):
                for j in range(9):
                    if self.cells[i][j] == '0':
                        self.tb[i][j].setStyleSheet('color: 171717; background-color: #ebe9dd')
                    if self.cells[i][j] != '0':
                        self.tb[i][j].setStyleSheet('color: #171717; background-color: #e9e1bb;')
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Sudoku()
    sys.exit(app.exec_())

