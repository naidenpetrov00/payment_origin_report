from dataclasses import dataclass
from typing import Any
import pandas as pd

from config import RESULT_COL
from spec import Spec


@dataclass
class Rule:
    when: Spec
    value: str


def apply_rules(row: pd.Series, rules: list[Rule], default=None):
    chosen = default
    for rule in rules:
        if rule.when.is_satisfied_by(row):
            chosen = rule.value if not callable(rule.value) else rule.value(row)
            return chosen
