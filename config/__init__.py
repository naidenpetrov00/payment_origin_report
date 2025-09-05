import os


DOCUMENTS_FOLDER_PATH = os.path.abspath("./documents")
RESULTS_FOLDER_PATH = os.path.abspath("./results")
PLOTS_PATH = os.path.abspath("./plots")
output_path = ""

RECIEVED_AT = "Получени на"
CASE_NUMBER_COL = "Дело"
ARRIVED_SUM_COL = "Пристигнала сума"
SUM = "Сума"
PRINCIPAL_COL = "Наредител"
PRINCIPAL_VAT_COL = "Наредител ЕГН/ЕИК"
PERSON_COL = "Лице"
TYPE_PERSON_COL = "Вид Лице"
PERSON_VAT_COL = "Лице ЕГН/ЕИК"
CLAIMANT_COL = "Взискатели"
CLAIMANT_VAT_COL = "Взискател ЕИК"
DEBTOR_COL = "Длъжници"
REASON_COL = "Основание"
REMAINING_SUM_COL = "Оставаща сума"
PDI_STATUS_COL = "ПДИ Статус"
STATUS = "Статус"
RECIEVED_AT = "Получени на"
RESULT_COL = "Резултат"

WORDS_FOR_SOLDER = [
    "ЗАПОР",
    "ZAPOR",
    "ПОЛУЧЕН ПРЕВОД",
    "СЛУЖ",
    "ЧАСТИЧНО",
    "ЧАСТ",
    "ЦЯЛОСТНО",
    "СПЕСТЕНА",
    "СЕКВ",
    "СПЕСТЕН",
    "СПЕСТЯВАНИЯ",
    "ЧЛ.446",
    "МРЗ",
]

WORDS_FOR_EASYPAY_SOLDER = [
    "ПРЕВОД",
    "ПРИХВАЩАНЕ",
]

WORDS_FOR_PRINCIPAL_SOLDER = [
    "АД",
    "ЕАД",
    "ООД",
    "ЕООД",
    "EOOD",
    "EOODCO",
    "ОБЩИНА",
    "ЕТ",
    "КД",
    "КДА",
    "БЮДЖЕТ",
    "ОП",
    "ПГ",
    "ДГ",
    "СУ",
    "ДП",
    "ТПК",
    "БД",
    "НМУ",
    "УМБА",
]

WORD_FOR_PENSION = [
    "НОИ",
    "НАЦИОНАЛЕН ОСИГУРИТЕЛЕН ИНСТИТУТ",
    "НАЦИОНАЛЕН ОСИГ ИНСТИТУТ Г",
    "СУСО",
    "РУСО",
    "ДОО",
    "ПЕНСИИ",
    "НАЦИОНАЛЕН ОСИГ",
]
