# -------------------------------------------------------------------------------------------------------------------- #
# File Name    : UI.py
# Project Name : Mortgage-Loan-Calculator
# Author       : Yogyui (SeungHee Lee)
# Organization :
# Description  : 주택담보대출 상환액 계산 GUI
# [Revision History]
# >> 2022.04.20 - First Commit
# -------------------------------------------------------------------------------------------------------------------- #
import pandas as pd
from typing import Union
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets import QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton, QRadioButton, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy
from Calculator import MortgageLoanCalculator, RepaymentType


class MortgageLoanCalculatorWindow(QMainWindow):
    _df_calc_result: Union[pd.DataFrame, None] = None

    def __init__(self):
        super().__init__()
        self._calculator = MortgageLoanCalculator()
        self._editPrincipal = QLineEdit()  # 대출 원금
        self._spinInterest = QDoubleSpinBox()  # 대출 금리 (퍼센트)
        self._spinPeriod = QSpinBox()  # 대출 기간
        self._radioPeriodYear = QRadioButton('년')
        self._radioPeriodMonth = QRadioButton('개월')
        self._spinGracePeriod = QSpinBox()  # 이자 거치 기간
        self._radioGracePeriodYear = QRadioButton('년')
        self._radioGracePeriodMonth = QRadioButton('개월')
        self._comboRepaymentType = QComboBox()  # 이자 상환 방식
        self._btnCalculate = QPushButton('계산')
        self._tableResult = QTableWidget()
        self.initControl()
        self.initLayout()
        self.setWindowTitle('주택담보대출 계산기')
        self.resize(600, 600)

    def initLayout(self):
        central = QWidget()
        self.setCentralWidget(central)

        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(4, 4, 4, 4)
        vbox.setSpacing(4)

        grbox = QGroupBox('파라미터')
        grbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        vbox_gr = QVBoxLayout(grbox)
        vbox_gr.setContentsMargins(4, 6, 4, 4)
        vbox_gr.setSpacing(4)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(4)
        lbl = QLabel('대출금액')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._editPrincipal)
        vbox_gr.addWidget(wgt)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(4)
        lbl = QLabel('연이자율')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._spinInterest)
        lbl = QLabel('%')
        lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        hbox.addWidget(lbl)
        vbox_gr.addWidget(wgt)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(4)
        lbl = QLabel('대출 기간')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._spinPeriod)
        hbox.addWidget(self._radioPeriodYear)
        self._radioPeriodYear.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        hbox.addWidget(self._radioPeriodMonth)
        self._radioPeriodMonth.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        vbox_gr.addWidget(wgt)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(4)
        lbl = QLabel('이자 거치 기간')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._spinGracePeriod)
        hbox.addWidget(self._radioGracePeriodYear)
        self._radioGracePeriodYear.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        hbox.addWidget(self._radioGracePeriodMonth)
        self._radioGracePeriodMonth.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        vbox_gr.addWidget(wgt)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(4)
        lbl = QLabel('상환 방식')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._comboRepaymentType)
        vbox_gr.addWidget(wgt)
        vbox.addWidget(grbox)

        vbox.addWidget(self._btnCalculate)
        vbox.addWidget(self._tableResult)

    def initControl(self):
        self._editPrincipal.setValidator(QIntValidator())  # 숫자만 입력할 수 있도록 validator 설정
        # self._editPrincipal.setAlignment(Qt.AlignRight)
        self._editPrincipal.setText(str(self._calculator.principal))
        self._spinInterest.setRange(0, 100)
        self._spinInterest.setDecimals(2)
        self._spinInterest.setValue(self._calculator.interest_rate_percentage)
        period = self._calculator.period_month
        self._spinPeriod.setRange(0, 2147483647)
        self._radioPeriodYear.setChecked(True)
        self._spinPeriod.setValue(period // 12)
        self._radioPeriodYear.clicked.connect(self.onClickRadioPeriod)
        self._radioPeriodMonth.clicked.connect(self.onClickRadioPeriod)
        grace_period = self._calculator.grace_period_month
        self._spinGracePeriod.setRange(0, 2147483647)
        self._spinGracePeriod.setValue(grace_period // 12)
        self._radioGracePeriodYear.setChecked(True)
        self._radioGracePeriodYear.clicked.connect(self.onClickRadioGracePeriod)
        self._radioGracePeriodMonth.clicked.connect(self.onClickRadioGracePeriod)
        self._comboRepaymentType.addItems(['원리금균등', '원금균등', '만기일시'])
        self._btnCalculate.clicked.connect(self.onClickBtnCalculate)
        self._tableResult.verticalHeader().hide()

    def onClickRadioPeriod(self):
        # value =
        pass

    def onClickRadioGracePeriod(self):
        pass

    def onClickBtnCalculate(self):
        self._calculator.principal = int(self._editPrincipal.text())
        self._calculator.interest_rate_percentage = self._spinInterest.value()
        if self._radioPeriodYear.isChecked():
            self._calculator.period_month = self._spinPeriod.value() * 12
        else:
            self._calculator.period_month = self._spinPeriod.value()
        if self._radioGracePeriodYear.isChecked():
            self._calculator.grace_period_month = self._spinGracePeriod.value() * 12
        else:
            self._calculator.grace_period_month = self._spinGracePeriod.value()
        if self._comboRepaymentType.currentIndex() == 0:  # 원리금균등
            self._calculator.repayment_type = RepaymentType.EqualPrincipalInterest
        elif self._comboRepaymentType.currentIndex() == 1:  # 원금균등
            self._calculator.repayment_type = RepaymentType.EqualPrincipal
        else:
            pass
        self._df_calc_result = self._calculator.calculate()
        self.drawTable()

    def drawTable(self):
        self._tableResult.clear()
        self._tableResult.clearContents()
        columns = list(self._df_calc_result.columns)
        self._tableResult.setColumnCount(len(columns))
        self._tableResult.setHorizontalHeaderLabels(columns)
        self._tableResult.setRowCount(len(self._df_calc_result))
        values = self._df_calc_result.values
        for r in range(self._tableResult.rowCount()):
            for c in range(self._tableResult.columnCount()):
                item = QTableWidgetItem(str(values[r][c]))
                self._tableResult.setItem(r, c, item)


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from PyQt5.QtCore import QCoreApplication

    QApplication.setStyle('fusion')
    app = QCoreApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    mainWnd = MortgageLoanCalculatorWindow()
    mainWnd.show()
    app.exec_()
