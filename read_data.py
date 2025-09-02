import os
import pandas as pd
from pandas import DataFrame

from config import (
    ARRIVED_SUM_COL,
    CASE_NUMBER_COL,
    DOCUMENTS_FOLDER_PATH,
    PERSON_COL,
    PRINCIPAL_COL,
    PRINCIPAL_VAT_COL,
    REASON_COL,
    RESULT_COL,
    TYPE_COL,
)


def read_documents() -> DataFrame:
    frames = []

    for filename in os.listdir(DOCUMENTS_FOLDER_PATH):
        file_path = os.path.join(DOCUMENTS_FOLDER_PATH, filename)
        print(f"Processing file: {filename}")
        df = pd.read_excel(file_path)
        # for index, row in df.iterrows():

        frames.append(
            pd.DataFrame(
                {
                    PRINCIPAL_COL: df[PRINCIPAL_COL],
                    PRINCIPAL_VAT_COL: df[PRINCIPAL_VAT_COL],
                    ARRIVED_SUM_COL: df[ARRIVED_SUM_COL],
                    CASE_NUMBER_COL: df[CASE_NUMBER_COL],
                    PERSON_COL: df[PERSON_COL],
                    REASON_COL: df[REASON_COL],
                    TYPE_COL: df[TYPE_COL],
                    RESULT_COL: None,
                }
            )
        )

    return pd.concat(frames, ignore_index=True)
