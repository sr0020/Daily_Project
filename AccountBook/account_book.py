from PyQt5.QtWidgets import *
import pandas as pd

# 0417 기본 xlsx 틀 만들기 
# 0418 - UI  
# 0419 - 사용자 입력(input, output) 및 total 계산 
# 0420 - 각종 예외처리, (가능하면 1. 시각화 및 2. 행 추가 가능하게) 
# 0421 - 시각화 
# 0603-0604 - 완성

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
        super().__init__()
        self.df = pd.DataFrame({"Content": [],
                                "Income": [],
                                "Expense": [],
                                "Total": []}) 

        QDialog.__init__(self) # QDialog 상속
        self.resize(600, 300)
        self.setWindowTitle("가계부 입력")

        # Content, Income, Expense 입력받을 리스트
        self.content_list = []
        self.income_list = []
        self.expense_list = []
        self.total_list = []

        # Content, Income, Expense
        content_label = QLabel("내역")
        income_label = QLabel("수입")
        expense_label = QLabel("지출")

        self.content_input = QLineEdit()
        self.income_input = QLineEdit()
        self.expense_input = QLineEdit()

        # check, cancel
        check_btn = QPushButton("확인")
        cancel_btn = QPushButton('취소')
        # check_btn.clicked.connect(self.show_table)

        # table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["내역", "수입", "지출", "결과"])

        # label 레이아웃
        label_lay = QHBoxLayout()
        label_lay.addWidget(content_label)
        label_lay.addWidget(income_label)
        label_lay.addWidget(expense_label)

        # text 레이아웃
        text_lay = QHBoxLayout()
        text_lay.addWidget(self.content_input)
        text_lay.addWidget(self.income_input)
        text_lay.addWidget(self.expense_input)

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
        check_btn.clicked.connect(self.main) # clicked 함수 현재 두 개 
        cancel_btn.clicked.connect(self.close)

    # 테이블 및 엑셀에 쓰기
    def main(self):

        # 1. 테이블에서 현재 내역 조회 (qt table)
        content = self.content_input.text()
        income = self.income_input.text()
        expense = self.expense_input.text()
        total = self.total_list[-1] + int(income) - int(expense) if self.total_list else int(income) - int(expense) # total

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        self.table.setItem(row_count, 0, QTableWidgetItem(content))
        self.table.setItem(row_count, 1, QTableWidgetItem(income))
        self.table.setItem(row_count, 2, QTableWidgetItem(expense))
        self.table.setItem(row_count, 3, QTableWidgetItem(str(total)))  # 최종 결과값

        # 2. 엑셀에 쓰기 (여러 줄)

        # 원 df 딕셔너리 형태로 변환 후 input 받기
        self.dict_df = self.df.to_dict()

        try: # 예외 - 값이 아예 입력이 안 된 경우(ValueError)
            self.dict_df['Income'] = int(self.income_input.text())               
            self.dict_df['Expense'] = int(self.expense_input.text())
        except:
            print("값 입력 아예 안 된 오류 발생")
            self.dict_df['Income'] = 0           
            self.dict_df['Expense'] = 0
        finally:
            self.dict_df['Content'] = str(self.content_input.text())

        # total
        self.dict_df["Total"] = 0

        # 예외 (마이너스 값 들어오는 경우)
        if self.dict_df['Income'] < 0 or self.dict_df['Expense'] < 0:
            total = 0
            print("마이너스 값 입력되는 오류 발생") 
            pass

        # total 값 계산
        if self.total_list: # index error 방지
            total = self.total_list[-1] + self.dict_df["Income"] - self.dict_df["Expense"]
            self.dict_df['Total'] = int(total)
        else:
            total = self.dict_df["Income"] - self.dict_df['Expense']
            self.dict_df['Total'] = int(total)

        # 수입, 지출 동시에 받은 경우
        # elif self.dict_df['Income'] != 0 and self.dict_df['Expense'] != 0:
        # # 수입을 받은 경우 
        # elif self.dict_df['Income'] != 0:
        #     total = self.dict_df["Income"] + self.dict_df["Total"]
        #     self.dict_df['Total'] = int(total)
        # # 지출을 받은 경우
        # elif self.dict_df['Expense'] != 0:
        #     total = self.dict_df["Income"] - self.dict_df['Expense']
        #     self.dict_df['Total'] = int(total)
        #     self.dict_df['Total'] = int(total)
        # else:
        #     pass

        # 리스트의 각 인덱스(셀)에 input 값 받기
        self.content_list.append(content)
        self.income_list.append(income)
        self.expense_list.append(expense)
        self.total_list.append(total)
        
        print(self.content_list, self.income_list, self.expense_list, self.total_list)
        # print
        # print("딕셔너리: {0}".format(self.dict_df))
        # print("내역: {0}".format(self.dict_df["Content"]))
        # print(self.dict_df['Content'])

        # 다시 dataframe으로 변환 후 to_excel
        result_df = pd.DataFrame([self.dict_df])
        self.df = self.df.append(result_df, ignore_index=True)

        print(self.df)
        print(type(self.df))

        # to_excel
        self.df.to_excel("Account Book.xlsx", encoding='enc_kr')

        # clear
        self.content_input.clear()
        self.income_input.clear()
        self.expense_input.clear()
        
if __name__ == "__main__":
    app = QApplication([])
    dialog = Account()
    dialog.show()
    app.exec_() # 이벤트 루프(UI) 생성하는 코드
    print("DONE")