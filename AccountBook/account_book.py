from PyQt5.QtWidgets import *
import pandas as pd
# import test # __name__=="__main__" 테스트

# 0417 기본 xlsx 틀 만들기 
# 0418 - UI  
# 0419 - 사용자 입력(input, output) 및 total 계산 
# 0420 - 각종 예외처리, (가능하면 1. 시각화 및 2. 행 추가 가능하게) 
# 0421 - 시각화 

class QPushButton(QPushButton):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class QLineEdit(QLineEdit):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class QTableWidget(QTableWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

class Account(QDialog):
    def __init__(self):
        QDialog.__init__(self) # QDialog 상속
        self.resize(500, 120)
        self.setWindowTitle("가계부 입력")

        # Content, Income, Expand
        content_label = QLabel("내역")
        income_label = QLabel("수입")
        expense_label = QLabel("지출")

        self.content = QLineEdit()
        self.income = QLineEdit()
        self.expense = QLineEdit()

        # check, cancel
        check_btn = QPushButton("확인")
        cancel_btn = QPushButton('취소')

        # table
        self.table = QTableWidget()

        # label 레이아웃
        label_lay = QHBoxLayout()
        label_lay.addWidget(content_label)
        label_lay.addWidget(income_label)
        label_lay.addWidget(expense_label)

        # text 레이아웃
        text_lay = QHBoxLayout()
        text_lay.addWidget(self.content)
        text_lay.addWidget(self.income)
        text_lay.addWidget(self.expense)

        # button 레이아웃
        btn_lay = QHBoxLayout()
        btn_lay.addWidget(check_btn)
        btn_lay.addWidget(cancel_btn)

        # UI layout
        main_lay = QVBoxLayout() # QV - 수직, QH - 수평
        main_lay.addLayout(label_lay)
        main_lay.addLayout(text_lay)
        main_lay.addLayout(btn_lay)
        main_lay.addWidget(self.table)

        self.setLayout(main_lay)
        check_btn.clicked.connect(self.main)
        cancel_btn.clicked.connect(self.close)

        # table
        self.table.setRowCount(1)
        self.table.setColumnCount(3)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        for i in range(1):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(str(i+j)))

    # 엑셀에 쓰기
    def main(self):
        global df

        df = pd.DataFrame({"Content": [],
                           "Income": [],
                           "Expense": [],
                           "Total": []}) # total 이전 값 - expense / + income
        
        # 원 df 딕셔너리 형태로 변환 후 input 받기
        self.dict_df = df.to_dict()
        
        try: # 예외 - 값이 아예 입력이 안 된 경우(ValueError)
            # dict_df['Content'] = str(self.content.text())
            self.dict_df['Income'] = int(self.income.text())                
            self.dict_df['Expense'] = int(self.expense.text())
        except:
            print("값 입력 아예 안 된 오류 발생")
            self.dict_df['Income'] = 0           
            self.dict_df['Expense'] = 0
        finally:
            self.dict_df['Content'] = str(self.content.text())

        # total
        self.dict_df["Total"] = 0

        # 지금 if, elif 동시 처리되는 중.. (수입을 받은 경우, 지출은 계산되지 않음)
        # 예외 (-값 들어오거나)
        if self.dict_df['Income'] < 0 or self.dict_df['Expense'] < 0:
            total = 0
            print("마이너스 값 입력되는 오류 발생") 
            pass
        # 수입, 지출 동시에 받은 경우
        elif self.dict_df['Income'] != 0 and self.dict_df['Expense'] != 0:
            total = self.dict_df["Income"] - self.dict_df["Expense"]
            self.dict_df['Total'] = int(total)
        # 수입을 받은 경우 
        elif self.dict_df['Income'] != 0:
            total = self.dict_df["Income"] + self.dict_df["Total"]
            self.dict_df['Total'] = int(total)
        # 지출을 받은 경우
        elif self.dict_df['Expense'] != 0:
            total = self.dict_df["Total"] - self.dict_df['Expense']
            self.dict_df['Total'] = int(total)
        else:
            pass

        # print
        print("딕셔너리: {0}".format(self.dict_df))
        print("내역: {0}".format(self.dict_df["Content"]))
        print(self.dict_df['Content'])

        # 다시 dataframe으로 변환 후 to_excel
        result_df = pd.DataFrame([self.dict_df])
        print(result_df)
        result_df.to_excel("Account Book.xlsx", encoding='enc_kr')
        

    # 데이터프레임 갱신 및 현재 내역 조회 (qt table)

if __name__ == "__main__":
    app = QApplication([])
    dialog = Account()
    dialog.show()
    app.exec_() # 이벤트 루프(UI) 생성하는 코드
    print("DONE")