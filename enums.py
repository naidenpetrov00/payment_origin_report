from enum import Enum


class PaymentType(Enum):
    SalarySolder = "Плащане от запор на заплата"
    BankSolder = "Плащане от запор на банкова сметка"
    PensionSolder = "Запор на пенсия"
    VoluntaryPayment = "Доброволно плащане"
    ThirdPartyVoluntaryPayment = "Доброволно плащане от трето лице"


class PersonType(Enum):
    Company = "Юридическо"
    Male = "Мъж"
    FeMale = "Жена"
