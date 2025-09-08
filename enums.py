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


class AgeGroupType(Enum):
    MINORS = "Непълнолетни <18"
    YOUNG_ADULTS = "Млади пълнолетни 18-25"
    EARLY_ADULTS = "Млади възрастни 26-35"
    MIDDLE_AGED = "Средна възраст 36-50"
    PRE_RETIREMENT = "Предпенсионна възраст 51-65"
    RETIREES = "Пенсионери 65+"
    NoType = " "
