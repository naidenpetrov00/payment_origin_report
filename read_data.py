import os
import pandas as pd
from pandas import DataFrame

from config import (
    ARRIVED_SUM_COL,
    CASE_NUMBER_COL,
    DOCUMENTS_FOLDER_PATH,
    PRINCIPAL_COL,
)


def read_documents() -> DataFrame:
    data = []

    for filename in os.listdir(DOCUMENTS_FOLDER_PATH):
        file_path = os.path.join(DOCUMENTS_FOLDER_PATH, filename)
        print(f"Processing file: {filename}")
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            print(row.to_dict())

        data.append(
            df[
                [
                    PRINCIPAL_COL,
                    ARRIVED_SUM_COL,
                    CASE_NUMBER_COL,
                ]
            ]
        )

    return pd.concat(data, ignore_index=True)
