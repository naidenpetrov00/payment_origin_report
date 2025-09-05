import os
import pandas as pd
from pandas import DataFrame

from config import (
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
    STATUS,
    SUM,
    TYPE_PERSON_COL,
)
from enums import PersonType


def read_documents() -> DataFrame:
    frames = []

    for filename in os.listdir(DOCUMENTS_FOLDER_PATH):
        file_path = os.path.join(DOCUMENTS_FOLDER_PATH, filename)
        print(f"Processing file: {filename}")
        df = pd.read_excel(file_path)

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
                TYPE_PERSON_COL: None,
                CLAIMANT_COL: df[CLAIMANT_COL],
                CLAIMANT_VAT_COL: df[CLAIMANT_VAT_COL],
                DEBTOR_COL: df[DEBTOR_COL],
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
    return cleaned_df


def detect_person_type(vat):
    type = "No Data"
    vat = str(vat)
    if len(vat) == 9:
        type = PersonType.Company.value
    elif len(vat) == 10:
        type = (
            PersonType.FeMale.value if int(vat[-1]) % 2 == 0 else PersonType.Male.value
        )
    return type
