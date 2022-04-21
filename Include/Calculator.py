# -------------------------------------------------------------------------------------------------------------------- #
# File Name    : Calculator.py
# Project Name : Mortgage-Loan-Calculator
# Author       : Yogyui (SeungHee Lee)
# Organization :
# Description  : 주택담보대출 상환액 계산 알고리즘 구현
# [Revision History]
# >> 2022.04.20 - First Commit
# -------------------------------------------------------------------------------------------------------------------- #
import os
import time
import math
import numpy as np
import pandas as pd
from enum import IntEnum, unique, auto
import xml.etree.ElementTree as ET
from Common import ensurePathExist, writeXmlFile


@unique
class RepaymentType(IntEnum):
    # 상환방식
    EqualPrincipal = auto()  # 원금균등상환 - 매달 원금 동일하게 상환, 이자는 매달 줄어듬, 매달 상환액 변동
    EqualPrincipalInterest = auto()  # 원리금균등상환 - 원금+이자 매월 상환액 동일
    Bullet = auto()  # 만기일시상환 - 원금 상환 없음, 이자만 납입


@unique
class RoundType(IntEnum):
    Off = auto()  # 반올림
    Up = auto()  # 올림
    Down = auto()  # 버림


class MortgageLoanCalculator:
    _principal: int  # 대출 원금
    _interest_rate_percentage: float  # 대출 금리 (년, 퍼센트)
    _period_month: int  # 대출 기간 (개월)
    _grace_period_month: int  # 이자 거치 기간 (개월)
    _repayment_type: RepaymentType  # 대출 상환 방식
    _round_floating: RoundType  # 소수점 처리 방식

    def __init__(self):
        self._principal = 100000000
        self._interest_rate_percentage = 4.
        self._period_month = 360
        self._grace_period_month = 0
        self._repayment_type = RepaymentType.EqualPrincipalInterest
        self._round_floating = RoundType.Off
        curpath = os.path.dirname(os.path.abspath(__file__))
        self._config_xml_path = os.path.join(os.path.dirname(curpath), 'Config/config.xml')
        self.loadConfig()

    def calculate(self) -> pd.DataFrame:
        tm_start = time.perf_counter()

        lst_sequence = []  # 납입회차
        lst_repay_total = []  # 월 상환금
        lst_repay_principal = []  # 월 납입원금
        lst_repay_interest = []  # 월 납입이자
        lst_principal_sum = []  # 납입원금 합
        lst_interest_sum = []  # 납입이자 합
        lst_residual = []  # 월 잔금

        interest_rate_month = self._interest_rate_percentage / 100 / 12
        sequence = 1  # 회차
        residual = self._principal  # 잔금
        principal_sum = 0  # 원금 납입계
        interest_sum = 0  # 이자 납입계

        if self._repayment_type == RepaymentType.EqualPrincipalInterest:  # 원리금균등상환
            print("[원리금 균등 상환]")
            # 월 균등 상환액 산출 (https://meaningone.tistory.com/632)
            temp = math.pow(1 + interest_rate_month, self._period_month - self._grace_period_month)
            repayment_month = round(self._principal * interest_rate_month * temp / (temp - 1))  # 소수점 반올림
            print("월 상환금액: {:,}".format(repayment_month))
            # 이터레이션
            for i in range(self._period_month):
                interest = residual * interest_rate_month
                if self._round_floating == RoundType.Off:  # 반올림
                    interest = int(np.round(interest))
                elif self._round_floating == RoundType.Up:  # 올림
                    interest = int(np.ceil(interest))
                else:  # 버림
                    interest = int(np.trunc(interest))
                interest_sum += interest
                if i in range(self._grace_period_month):  # 이자거치기간일 경우
                    principal = 0
                elif i == self._period_month - 1:
                    principal = residual
                    residual = 0
                else:
                    principal = repayment_month - interest
                    residual -= principal
                principal_sum += principal

                lst_repay_interest.append(interest)
                lst_repay_principal.append(principal)
                lst_principal_sum.append(principal_sum)
                lst_interest_sum.append(interest_sum)
                lst_repay_total.append(interest + principal)
                lst_residual.append(residual)
                lst_sequence.append(sequence)
                sequence += 1
        elif self._repayment_type == RepaymentType.EqualPrincipal:  # 원금균등상환
            print("[원금 균등 상환]")
            # 이터레이션
            principal_div = self._principal / (self._period_month - self._grace_period_month)
            if self._round_floating == RoundType.Off:  # 반올림
                principal_div = int(np.round(principal_div))
            elif self._round_floating == RoundType.Up:  # 올림
                principal_div = int(np.ceil(principal_div))
            else:  # 버림
                principal_div = int(np.trunc(principal_div))
            print("월 상환원금: {:,}".format(principal_div))
            for i in range(self._period_month):
                interest = residual * interest_rate_month
                if self._round_floating == RoundType.Off:  # 반올림
                    interest = int(np.round(interest))
                elif self._round_floating == RoundType.Up:  # 올림
                    interest = int(np.ceil(interest))
                else:  # 버림
                    interest = int(np.trunc(interest))
                interest_sum += interest
                if i in range(self._grace_period_month):  # 이자거치기간일 경우
                    principal = 0
                elif i == self._period_month - 1:
                    principal = residual
                    residual = 0
                else:
                    principal = principal_div
                    residual -= principal
                principal_sum += principal

                lst_repay_interest.append(interest)
                lst_repay_principal.append(principal)
                lst_principal_sum.append(principal_sum)
                lst_interest_sum.append(interest_sum)
                lst_repay_total.append(interest + principal)
                lst_residual.append(residual)
                lst_sequence.append(sequence)
                sequence += 1
        elif self._repayment_type == RepaymentType.Bullet:  # 만기일시상환
            print("[만기 일시 상환]")
            # 이터레이션
            interest = residual * interest_rate_month
            if self._round_floating == RoundType.Off:  # 반올림
                interest = int(np.round(interest))
            elif self._round_floating == RoundType.Up:  # 올림
                interest = int(np.ceil(interest))
            else:  # 버림
                interest = int(np.trunc(interest))
            print("월 납입이자: {:,}".format(interest))
            for i in range(self._period_month):
                interest_sum += interest
                if i == self._period_month - 1:
                    principal = residual
                    residual = 0
                else:
                    principal = 0
                    residual -= principal
                principal_sum += principal

                lst_repay_interest.append(interest)
                lst_repay_principal.append(principal)
                lst_principal_sum.append(principal_sum)
                lst_interest_sum.append(interest_sum)
                lst_repay_total.append(interest + principal)
                lst_residual.append(residual)
                lst_sequence.append(sequence)
                sequence += 1

        df_result = pd.DataFrame(
            (lst_sequence, lst_repay_total,
             lst_repay_interest, lst_interest_sum,
             lst_repay_principal, lst_principal_sum, lst_residual)
        ).T
        print("총 납입이자: {:,}".format(lst_interest_sum[-1]))
        df_result.columns = ['납입회차', '월상환금', '납입이자', '납입이자계', '납입원금', '납입원금계', '대출잔금']

        elapsed = time.perf_counter() - tm_start
        print(f"계산 시간: {elapsed * 1000} msec")

        self.saveConfig()
        return df_result

    def onValueChanged(self):
        pass

    def loadConfig(self):
        if os.path.isfile(self._config_xml_path):
            try:
                root = ET.parse(self._config_xml_path).getroot()
            except ET.ParseError:
                return

            node = root.find('principal')
            if node is not None:
                self._principal = int(node.text)

            node = root.find('interest')
            if node is not None:
                self._interest_rate_percentage = float(node.text)

            node = root.find('period')
            if node is not None:
                self._period_month = int(node.text)

            node = root.find('grace')
            if node is not None:
                self._grace_period_month = int(node.text)

            node = root.find('repayment')
            if node is not None:
                try:
                    self._repayment_type = RepaymentType(int(node.text))
                except Exception:
                    pass

            node = root.find('round_float')
            if node is not None:
                try:
                    self._round_floating = RoundType(int(node.text))
                except Exception:
                    pass

    def saveConfig(self):
        if os.path.isfile(self._config_xml_path):
            try:
                root = ET.parse(self._config_xml_path).getroot()
            except ET.ParseError:
                root = ET.Element('CalcParams')
        else:
            root = ET.Element('CalcParams')

        node = root.find('principal')
        if node is None:
            node = ET.Element('principal')
            root.append(node)
        node.text = str(self._principal)

        node = root.find('interest')
        if node is None:
            node = ET.Element('interest')
            root.append(node)
        node.text = str(self._interest_rate_percentage)

        node = root.find('period')
        if node is None:
            node = ET.Element('period')
            root.append(node)
        node.text = str(self._period_month)

        node = root.find('grace')
        if node is None:
            node = ET.Element('grace')
            root.append(node)
        node.text = str(self._grace_period_month)

        node = root.find('repayment')
        if node is None:
            node = ET.Element('repayment')
            root.append(node)
        node.text = str(self._repayment_type.value)

        node = root.find('round_float')
        if node is None:
            node = ET.Element('round_float')
            root.append(node)
        node.text = str(self._round_floating.value)

        ensurePathExist(os.path.dirname(self._config_xml_path))
        writeXmlFile(root, self._config_xml_path)

    @property
    def principal(self) -> int:
        return self._principal

    @principal.setter
    def principal(self, value: int):
        self._principal = value
        self.onValueChanged()

    @property
    def interest_rate_percentage(self) -> float:
        return self._interest_rate_percentage

    @interest_rate_percentage.setter
    def interest_rate_percentage(self, value: float):
        self._interest_rate_percentage = value
        self.onValueChanged()

    @property
    def period_month(self) -> int:
        return self._period_month

    @period_month.setter
    def period_month(self, value: int):
        self._period_month = value
        self.onValueChanged()

    @property
    def grace_period_month(self) -> int:
        return self._grace_period_month

    @grace_period_month.setter
    def grace_period_month(self, value):
        self._grace_period_month = value
        self.onValueChanged()

    @property
    def repayment_type(self) -> RepaymentType:
        return self._repayment_type

    @repayment_type.setter
    def repayment_type(self, value: RepaymentType):
        self._repayment_type = value
        self.onValueChanged()

    @property
    def round_floating(self) -> RoundType:
        return self._round_floating

    @round_floating.setter
    def round_floating(self, value: RoundType):
        self._round_floating = value
        self.onValueChanged()
