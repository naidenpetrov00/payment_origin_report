from enum import Enum


class PaymentType(Enum):
    SalarySolder = "Плащане от запор на заплата"
    BankSolder = "Плащане от запор на банкова сметка"
    VoluntaryPayment = "Доброволно плащане от „трето лице“"
