# -------------------------------------------------------------------------------------------------------------------- #
# File Name    : Calculator.py
# Project Name : Mortgage-Loan-Calculator
# Author       : Yogyui (SeungHee Lee)
# Organization :
# Description  : 주택담보대출 상환액 계산 알고리즘 구현
# reference: https://best79.com/loan/1/100000000/4/360
# https://search.naver.com/search.naver?where=nexearch&sm=top_sug.pre&fbm=0&acr=1&acq=%EB%8C%80%EC%B6%9C+%EC%9D%B4%EC%9E%90&qdt=0&ie=utf8&query=%EB%8C%80%EC%B6%9C+%EC%9D%B4%EC%9E%90%EA%B3%84%EC%82%B0%EA%B8%B0
# [Revision History]
# >> 2022.04.20 - First Commit
# -------------------------------------------------------------------------------------------------------------------- #
import math
import pandas as pd
from enum import IntEnum, unique, auto


@unique
class RepaymentType(IntEnum):
    # 상환방식
    EqualPrincipal = auto()  # 원금균등상환 - 매달 원금 동일하게 상환, 이자는 매달 줄어듬, 매달 상환액 변동
    EqualPrincipalInterest = auto()  # 원리금균등상환 - 원금+이자 매월 상환액 동일


class MortgageLoanCalculator:
    _principal: int  # 대출 원금
    _interest_rate_percentage: float  # 대출 금리 (년, 퍼센트)
    _period_month: int  # 대출 기간 (개월)
    _grace_period_month: int  # 이자 거치 기간 (개월)
    _repayment_type: RepaymentType  # 대출 상환 방식
    # TODO: 일의 자리 버림, 십의 자리 버림 옵션

    def __init__(self):
        self._principal = 100000000
        self._interest_rate_percentage = 4.
        self._period_month = 360
        self._grace_period_month = 0
        self._repayment_type = RepaymentType.EqualPrincipalInterest

    def calculate(self) -> pd.DataFrame:
        lst_sequence = []  # 납입회차
        lst_repay_total = []  # 월 상환금
        lst_repay_principal = []  # 월 납입원금
        lst_repay_interest = []  # 월 납입이자
        lst_principal_sum = []  # 납입원금 합
        lst_interest_sum = []  # 납입이자 합
        lst_residual = []  # 월 잔금

        if self._repayment_type == RepaymentType.EqualPrincipalInterest:  # 원리금균등상환
            print("[원리금 균등 상환]")
            # (1) 월 균등 상환액 산출 (https://meaningone.tistory.com/632)
            interest_rate_month = self._interest_rate_percentage / 100 / 12
            temp = math.pow(1 + interest_rate_month, self._period_month - self._grace_period_month)
            repayment_month = round(self._principal * interest_rate_month * temp / (temp - 1))  # 소수점 반올림
            print(f"월 상환금액: {repayment_month}")
            # (2) 이터레이션
            sequence = 1
            residual = self._principal
            principal_sum = 0
            interest_sum = 0
            for i in range(self._grace_period_month):  # 이자 거치 기간 = 원금상환없음, 이자만 납입
                interest = int(residual * interest_rate_month)
                interest_trunc = interest - interest % 10
                principal = 0
                principal_sum += principal
                interest_sum += interest_trunc
                lst_repay_interest.append(interest_trunc)
                lst_repay_principal.append(principal)
                lst_principal_sum.append(principal_sum)
                lst_interest_sum.append(interest_sum)
                lst_repay_total.append(interest_trunc + principal)
                lst_residual.append(residual)
                lst_sequence.append(sequence)
                sequence += 1

            for i in range(self._period_month - self._grace_period_month):
                interest = int(residual * interest_rate_month)
                interest_trunc = interest - interest % 10
                interest_sum += interest_trunc
                if residual >= repayment_month:  # 잔금이 월 상환액보다 클 경우
                    principal = repayment_month - interest_trunc
                    residual -= principal
                else:
                    principal = residual
                    residual = 0
                principal_sum += principal
                lst_repay_interest.append(interest_trunc)
                lst_repay_principal.append(principal)
                lst_principal_sum.append(principal_sum)
                lst_interest_sum.append(interest_sum)
                lst_repay_total.append(interest_trunc + principal)
                lst_residual.append(residual)
                lst_sequence.append(sequence)
                sequence += 1
        else:
            pass
        df_result = pd.DataFrame(
            (lst_sequence, lst_repay_total,
             lst_repay_interest, lst_interest_sum,
             lst_repay_principal, lst_principal_sum, lst_residual)
        ).T
        df_result.columns = ['납입회차', '월상환금', '납입이자', '납입이자계', '납입원금', '납입원금계', '대출잔금']
        self.saveConfig()
        return df_result

    def onValueChanged(self):
        pass

    def loadConfig(self):
        pass

    def saveConfig(self):
        pass

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
