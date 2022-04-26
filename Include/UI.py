# -------------------------------------------------------------------------------------------------------------------- #
# File Name    : UI.py
# Project Name : Mortgage-Loan-Calculator
# Author       : Yogyui (SeungHee Lee)
# Organization :
# Description  : 주택담보대출 상환액 계산 GUI
# [Revision History]
# >> 2022.04.20 - First Commit
# -------------------------------------------------------------------------------------------------------------------- #
import platform
import pandas as pd
from typing import Union
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QMainWindow, QWidget, QMessageBox, QFileDialog
from PyQt5.QtWidgets import QComboBox, QLineEdit, QSpinBox, QDoubleSpinBox, QPushButton, QRadioButton, QLabel
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QTabWidget
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGroupBox, QSizePolicy
from Calculator import MortgageLoanCalculator, RepaymentType, RoundType
from Common import money_string_to_readable_text


class MortgageLoanCalculatorWindow(QMainWindow):
    _df_calc_result: Union[pd.DataFrame, None] = None

    def __init__(self):
        super().__init__()
        self._calculator = MortgageLoanCalculator()
        self._editPrincipal = QLineEdit()  # 대출 원금
        self._last_valid_text: str = ''
        self._lbl_readable = QLabel()
        self._spinInterest = QDoubleSpinBox()  # 대출 금리 (퍼센트)
        self._spinPeriod = QSpinBox()  # 대출 기간
        self._radioPeriodYear = QRadioButton('년')
        self._radioPeriodMonth = QRadioButton('개월')
        self._spinGracePeriod = QSpinBox()  # 이자 거치 기간
        self._radioGracePeriodYear = QRadioButton('년')
        self._radioGracePeriodMonth = QRadioButton('개월')
        self._comboRepaymentType = QComboBox()  # 이자 상환 방식
        self._radioFloatRoundOff = QRadioButton('반올림')
        self._radioFloatRoundUp = QRadioButton('올림')
        self._radioFloatRoundDown = QRadioButton('버림')
        self._btnCalculate = QPushButton('계산')
        self._btnSaveCsv = QPushButton('저장 (CSV)')
        self._tabWidget = QTabWidget()
        self._tableResult1 = QTableWidget()
        self._tableResult2 = QTableWidget()
        self.initControl()
        self.initLayout()
        self.setWindowTitle('주택담보대출 계산기')
        self.setWindowIcon(QIcon("./Resource/application.ico"))
        self.resize(600, 800)

    def initLayout(self):
        central = QWidget()
        self.setCentralWidget(central)

        vbox = QVBoxLayout(central)
        vbox.setContentsMargins(4, 4, 4, 4)
        vbox.setSpacing(6)

        grbox = QGroupBox('조건')
        grbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        vbox_gr = QVBoxLayout(grbox)
        vbox_gr.setContentsMargins(4, 6, 4, 4)
        vbox_gr.setSpacing(6)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(6)
        lbl = QLabel('대출금액')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._editPrincipal)
        lbl = QLabel('원')
        lbl.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        hbox.addWidget(lbl)
        vbox_gr.addWidget(wgt)
        vbox_gr.addWidget(self._lbl_readable)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(6)
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
        hbox.setSpacing(6)
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
        hbox.setSpacing(6)
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
        hbox.setSpacing(6)
        lbl = QLabel('상환 방식')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._comboRepaymentType)
        vbox_gr.addWidget(wgt)
        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(6)
        lbl = QLabel('소수점')
        lbl.setFixedWidth(110)
        hbox.addWidget(lbl)
        hbox.addWidget(self._radioFloatRoundOff)
        self._radioFloatRoundOff.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        hbox.addWidget(self._radioFloatRoundUp)
        self._radioFloatRoundUp.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        hbox.addWidget(self._radioFloatRoundDown)
        self._radioFloatRoundDown.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.MinimumExpanding)
        hbox.addWidget(QWidget())
        vbox_gr.addWidget(wgt)
        vbox.addWidget(grbox)

        wgt = QWidget()
        hbox = QHBoxLayout(wgt)
        hbox.setContentsMargins(0, 0, 0, 0)
        hbox.setSpacing(6)
        hbox.addWidget(self._btnCalculate)
        hbox.addWidget(self._btnSaveCsv)
        hbox.addWidget(QWidget())
        vbox.addWidget(wgt)

        vbox.addWidget(self._tabWidget)

    def initControl(self):
        # self._editPrincipal.setValidator(QIntValidator())  # 숫자만 입력할 수 있도록 validator 설정
        # self._editPrincipal.setAlignment(Qt.AlignRight)
        self._editPrincipal.textChanged.connect(self.onEditPrincipalTextChanged)
        self._editPrincipal.setText(str(self._calculator.principal))
        self._lbl_readable.setAlignment(Qt.AlignRight)
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
        if self._calculator.repayment_type == RepaymentType.EqualPrincipalInterest:  # 원리금균등
            self._comboRepaymentType.setCurrentIndex(0)
        elif self._calculator.repayment_type == RepaymentType.EqualPrincipal:  # 원금균등
            self._comboRepaymentType.setCurrentIndex(1)
        else:
            self._comboRepaymentType.setCurrentIndex(2)
        if self._calculator.round_floating == RoundType.Off:
            self._radioFloatRoundOff.setChecked(True)
        elif self._calculator.round_floating == RoundType.Up:
            self._radioFloatRoundUp.setChecked(True)
        else:
            self._radioFloatRoundDown.setChecked(True)

        self._btnCalculate.clicked.connect(self.onClickBtnCalculate)
        self._btnCalculate.setIcon(QIcon("./Resource/calculator.png"))
        self._btnCalculate.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._btnSaveCsv.clicked.connect(self.onClickBtnSaveCsv)
        self._btnSaveCsv.setIcon(QIcon("./Resource/excel.png"))
        self._btnSaveCsv.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self._tabWidget.setTabPosition(QTabWidget.South)
        self._tableResult1.verticalHeader().hide()
        self._tableResult1.setAlternatingRowColors(True)
        styleSheet = "QTableWidget {alternate-background-color: #eeeeee; background-color: white;}"
        self._tableResult1.setStyleSheet(styleSheet)
        self._tabWidget.addTab(self._tableResult1, '테이블 1')
        self._tableResult2.verticalHeader().hide()
        self._tableResult2.setAlternatingRowColors(True)
        styleSheet = "QTableWidget {alternate-background-color: #eeeeee; background-color: white;}"
        self._tableResult2.setStyleSheet(styleSheet)
        self._tabWidget.addTab(self._tableResult2, '테이블 2')

    def onClickRadioPeriod(self):
        pass

    def onClickRadioGracePeriod(self):
        pass

    def onEditPrincipalTextChanged(self, text: str):
        pos = self._editPrincipal.cursorPosition()
        try:
            if len(text) == 0:
                value = 0
            else:
                value = int(text.replace(',', ''))
            self._editPrincipal.setText('{:,}'.format(value))
            self._last_valid_text = self._editPrincipal.text()
        except Exception:
            self._editPrincipal.setText(self._last_valid_text)
        self._editPrincipal.setCursorPosition(pos)

        self._lbl_readable.clear()
        try:
            value = int(self._editPrincipal.text().replace(',', ''))
            self._lbl_readable.setText(money_string_to_readable_text(value) + '원')
        except Exception:
            pass

    def onClickBtnCalculate(self):
        try:
            self._calculator.principal = int(self._editPrincipal.text().replace(',', ''))
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
                self._calculator.repayment_type = RepaymentType.Bullet
            if self._radioFloatRoundOff.isChecked():
                self._calculator.round_floating = RoundType.Off
            elif self._radioFloatRoundUp.isChecked():
                self._calculator.round_floating = RoundType.Up
            else:
                self._calculator.round_floating = RoundType.Down

            self._df_calc_result = self._calculator.calculate()
        except Exception as e:
            QMessageBox.warning(self, "Warning", str(e))
            self._df_calc_result = None
        self.drawTable1()
        self.drawTable2()

    def drawTable1(self):
        self._tableResult1.clear()
        self._tableResult1.clearContents()
        if self._df_calc_result is not None:
            columns = list(self._df_calc_result.columns)
            self._tableResult1.setColumnCount(len(columns))
            self._tableResult1.setHorizontalHeaderLabels(columns)
            self._tableResult1.setRowCount(len(self._df_calc_result))
            values = self._df_calc_result.values
            for r in range(self._tableResult1.rowCount()):
                for c in range(self._tableResult1.columnCount()):
                    if c == 0:
                        item = QTableWidgetItem(str(values[r][c]))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    else:
                        item = QTableWidgetItem("{:,}".format(values[r][c]))
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    item.setFlags(Qt.ItemFlags(int(item.flags()) ^ Qt.ItemIsEditable))
                    self._tableResult1.setItem(r, c, item)
            hHeader = self._tableResult1.horizontalHeader()
            hHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)

    def drawTable2(self):
        self._tableResult2.clear()
        self._tableResult2.clearContents()
        if self._df_calc_result is not None:
            # 12행 단위로 끊어서 sub-sum
            lst_year = []
            lst_interest_year = []  # 납입이자 계
            lst_pricipal_year = []  # 납입원금 계
            lst_redisual = []  # 잔금

            year = 1
            for i in range(len(self._df_calc_result)):
                if (i + 1) % 12 == 0:
                    lst_year.append(year)
                    year += 1
                    lst_interest_year.append(self._df_calc_result.iloc[i]['납입이자계'])
                    lst_pricipal_year.append(self._df_calc_result.iloc[i]['납입원금계'])
                    lst_redisual.append(self._df_calc_result.iloc[i]['대출잔금'])

            # 대출 개월 수가 년단위로 딱 떨어지지 않을 경우 행 한개 추가
            if len(self._df_calc_result) % 12 != 0:
                lst_year.append(year)
                lst_interest_year.append(self._df_calc_result.iloc[-1]['납입이자계'])
                lst_pricipal_year.append(self._df_calc_result.iloc[-1]['납입원금계'])
                lst_redisual.append(self._df_calc_result.iloc[-1]['대출잔금'])

            df_result = pd.DataFrame((lst_year, lst_interest_year, lst_pricipal_year, lst_redisual)).T
            df_result.columns = ['납입연차', '납입이자계', '납입원금계', '잔금']

            columns = list(df_result.columns)
            self._tableResult2.setColumnCount(len(columns))
            self._tableResult2.setHorizontalHeaderLabels(columns)
            self._tableResult2.setRowCount(len(df_result))
            values = df_result.values
            for r in range(self._tableResult2.rowCount()):
                for c in range(self._tableResult2.columnCount()):
                    if c == 0:
                        item = QTableWidgetItem(str(values[r][c]))
                        item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    else:
                        item = QTableWidgetItem("{:,}".format(values[r][c]))
                        item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    item.setFlags(Qt.ItemFlags(int(item.flags()) ^ Qt.ItemIsEditable))
                    self._tableResult2.setItem(r, c, item)
            hHeader = self._tableResult2.horizontalHeader()
            hHeader.setSectionResizeMode(0, QHeaderView.ResizeToContents)


    def onClickBtnSaveCsv(self):
        if self._df_calc_result is None:
            QMessageBox.warning(self, "Warning", "계산 결과 없음")
        else:
            options = QFileDialog.Options()
            path, _ = QFileDialog.getSaveFileName(self, "CSV 파일로 저장", "결과", "CSV File (*.csv)", options=options)
            if path:
                if platform.system() == 'Windows':
                    self._df_calc_result.to_csv(path, index=False, encoding='cp949')
                else:
                    self._df_calc_result.to_csv(path, index=False, encoding='utf-8')
