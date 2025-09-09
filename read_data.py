import os
import pandas as pd
from pandas import DataFrame
from datetime import date

from config import (
    AGE_GROUP_COL,
    ARRIVED_SUM_COL,
    CASE_NUMBER_COL,
    CLAIMANT_COL,
    CLAIMANT_VAT_COL,
    DEBTOR_COL,
    DOCUMENTS_FOLDER_PATH,
    PDI_STATUS_COL,
    PERSON_COL,
    PERSON_VAT_COL,
    PRINCIPAL_COL,
    PRINCIPAL_VAT_COL,
    REASON_COL,
    RECIEVED_AT,
    REMAINING_SUM_COL,
    RESULT_COL,
    SENDER_BIC,
    STATUS,
    SUM,
    TYPE_PERSON_COL,
)
from enums import AgeGroupType, PersonType


def read_documents() -> DataFrame:
    frames = []

    for filename in os.listdir(DOCUMENTS_FOLDER_PATH):
        file_path = os.path.join(DOCUMENTS_FOLDER_PATH, filename)
        print(f"Processing file: {filename}")
        df = pd.read_excel(
            file_path,
            dtype={
                PRINCIPAL_VAT_COL: str,
                PERSON_VAT_COL: str,
                CLAIMANT_VAT_COL: str,
            },
        )

        # cleaned_df = df.dropna(subset=[PRINCIPAL_COL, PERSON_COL])
        cleaned_df = pd.DataFrame(
            {
                RECIEVED_AT: df[RECIEVED_AT],
                CASE_NUMBER_COL: df[CASE_NUMBER_COL],
                ARRIVED_SUM_COL: df[ARRIVED_SUM_COL],
                SUM: df[SUM],
                PRINCIPAL_COL: df[PRINCIPAL_COL],
                PRINCIPAL_VAT_COL: df[PRINCIPAL_VAT_COL],
                PERSON_COL: df[PERSON_COL],
                PERSON_VAT_COL: df[PERSON_VAT_COL],
                SENDER_BIC: df[SENDER_BIC],
                TYPE_PERSON_COL: None,
                AGE_GROUP_COL: None,
                DEBTOR_COL: df[DEBTOR_COL],
                CLAIMANT_COL: df[CLAIMANT_COL],
                CLAIMANT_VAT_COL: df[CLAIMANT_VAT_COL],
                REASON_COL: df[REASON_COL],
                REMAINING_SUM_COL: df[REMAINING_SUM_COL],
                PDI_STATUS_COL: df[PDI_STATUS_COL],
                STATUS: df[STATUS],
                RESULT_COL: None,
            }
        )
        cleaned_df = clean_data(cleaned_df)

        frames.append(cleaned_df)

    return pd.concat(frames, ignore_index=True)


def clean_data(cleaned_df: DataFrame) -> DataFrame:
    cleaned_df.dropna(subset=[PRINCIPAL_COL, PERSON_COL], inplace=True)
    cleaned_df[[ARRIVED_SUM_COL, SUM]] = (
        cleaned_df[[ARRIVED_SUM_COL, SUM]]
        .astype(str)
        .replace(r"[^\d.,-]", "", regex=True)
        .replace(",", ".", regex=False)
        .apply(pd.to_numeric, errors="coerce")
    )
    cleaned_df = cleaned_df[cleaned_df[PRINCIPAL_COL].astype(str).str.strip() != ""]
    cleaned_df = cleaned_df[cleaned_df[PERSON_COL].astype(str).str.strip() != ""]
    cleaned_df[TYPE_PERSON_COL] = cleaned_df[PERSON_VAT_COL].apply(detect_person_type)
    cleaned_df[AGE_GROUP_COL] = cleaned_df[PERSON_VAT_COL].apply(
        detect_person_age_group
    )
    return cleaned_df


def detect_person_age_group(vat):
    if len(vat) != 10 or not vat.isdigit():
        return AgeGroupType.NoType.value

    age = get_age(vat)

    if age < 0:
        return AgeGroupType.NoType.value
    elif age < 18:
        return AgeGroupType.MINORS.value
    elif age <= 25:
        return AgeGroupType.YOUNG_ADULTS.value
    elif age <= 35:
        return AgeGroupType.EARLY_ADULTS.value
    elif age <= 50:
        return AgeGroupType.MIDDLE_AGED.value
    elif age <= 65:
        return AgeGroupType.PRE_RETIREMENT.value
    else:
        return AgeGroupType.RETIREES.value


def get_age(vat):
    year = int(vat[0:2])
    month = int(vat[2:4])
    day = int(vat[4:6])

    if 1 <= month <= 12:
        year += 1900
    elif 21 <= month <= 32:
        year += 1800
        month -= 20
    elif 41 <= month <= 52:
        year += 2000
        month -= 40
    else:
        return 0

    try:
        birth_date = date(year, month, day)
    except ValueError:
        return 0

    today = date.today()
    age = (
        today.year
        - birth_date.year
        - ((today.month, today.day) < (birth_date.month, birth_date.day))
    )

    return age


def detect_person_type(vat):
    type = "No Data"
    vat = str(vat)
    if len(vat) == 9:
        type = PersonType.Company.value
    elif len(vat) == 10:
        type = (
            PersonType.FeMale.value if int(vat[8]) % 2 == 0 else PersonType.Male.value
        )
    return type
