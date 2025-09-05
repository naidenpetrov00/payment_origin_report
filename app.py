import os
from config import RESULT_COL, RESULTS_FOLDER_PATH, output_path
from enums import PaymentType
from helpers import generate_categories
from predicates import Predicates
from read_data import read_documents
from rules_engine import Rule, apply_rules
from datetime import datetime

df = read_documents()
p = Predicates()

rules = [
    Rule(
        when=(p.person_equal_principal & ~p.contains_any_of_the_solder_words),
        value=PaymentType.VoluntaryPayment.value,
    ),
    Rule(
        when=(p.pincipal_contains_any_of_the_pension_words),
        value=PaymentType.PensionSolder.value,
    ),
    Rule(
        when=(p.principal_with_EIK | p.pincipal_contains_any_of_thewords),
        value=PaymentType.SalarySolder.value,
    ),
    Rule(
        when=(
            (
                p.contains_any_of_the_solder_words
                #  & p.person_equal_principal
            )
            | (p.principal_equal_easypay & p.contains_any_of_the_easypay_solder_word)
        ),
        value=PaymentType.BankSolder.value,
    ),
    Rule(
        when=(
            (p.person_not_equal_principal & p.principal_with_EGN & p.person_with_EGN) |
            (p.person_not_equal_principal
            & (p.reason_contains_part_or_full_person | p.reason_contains_person_vat)
            & ~p.contains_any_of_the_solder_words)
        ),
        value=PaymentType.ThirdPartyVoluntaryPayment.value,
    ),
]

for index, row in df.iterrows():
    result = apply_rules(row, rules, default="DEFAULT")
    df.at[index, RESULT_COL] = result


os.makedirs(RESULTS_FOLDER_PATH, exist_ok=True)
today_str = datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
output_filename = f"Analyse_{today_str}.xlsx"
output_path = os.path.join(RESULTS_FOLDER_PATH, output_filename)

df.to_excel(output_path, index=False)

generate_categories(df, output_path)

print(f"Results written to {output_path}")
