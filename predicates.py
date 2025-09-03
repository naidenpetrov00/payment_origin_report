from dataclasses import dataclass
from rapidfuzz import fuzz

import pandas as pd
from config import (
    PERSON_COL,
    PRINCIPAL_COL,
    PRINCIPAL_VAT_COL,
    REASON_COL,
    WORD_FOR_PENSION,
    WORDS_FOR_EASYPAY_SOLDER,
    WORDS_FOR_PRINCIPAL_SOLDER,
    WORDS_FOR_SOLDER,
)
from spec import Spec


class Predicates:
    def __init__(self):
        self.pincipal_contains_any_of_the_pension_words = (
            ColContainsAnyWordCaseInsensitiveNotTrimmed(PRINCIPAL_COL, WORD_FOR_PENSION)
        )
        self.principal_with_EGN = ColIdentifierIsEGN(PRINCIPAL_COL)
        self.pincipal_contains_any_of_thewords = (
            ColContainsAnyWordSeparatedWithWhiteSpace(
                PRINCIPAL_COL, WORDS_FOR_PRINCIPAL_SOLDER
            )
        )
        self.principal_with_EIK = ColIdentifierIsEIK(PRINCIPAL_VAT_COL)
        self.person_equal_principal = ColNameFuzzMatch(PERSON_COL, PRINCIPAL_COL)
        self.person_not_equal_principal = ColNe(PERSON_COL, PRINCIPAL_COL)
        self.reason_contains_part_or_full_person = ColNamePartialMatch(
            REASON_COL, PERSON_COL
        )
        self.contains_any_of_the_solder_words = ColContainsAnyWord(
            REASON_COL, WORDS_FOR_SOLDER
        )
        self.contains_any_of_the_easypay_solder_word = ColContainsAnyWord(
            REASON_COL, WORDS_FOR_EASYPAY_SOLDER
        )
        self.principal_equal_easypay = ColEqualsValue(PRINCIPAL_COL, "Изипей АД")


@dataclass
class ColEq(Spec):
    col1: str
    col2: str

    def is_satisfied_by(self, row):
        return str(row[self.col1]).casefold() == str(row[self.col2]).casefold()


@dataclass
class ColNe(Spec):
    col1: str
    col2: str

    def is_satisfied_by(self, row):
        return str(row[self.col1]).casefold() != str(row[self.col2]).casefold()


@dataclass
class ColNamePartialMatch(Spec):
    col1: str
    col2: str

    def is_satisfied_by(self, row):
        text1 = str(row[self.col1]).casefold().replace(" ", "")
        text2 = str(row[self.col2]).casefold().strip()

        words2 = text2.split()

        if len(words2) >= 2:
            first, last = words2[0], words2[-1]
            return first in text1 and last in text1

        return words2[0] in text1 if words2 else False


@dataclass
class ColNameFuzzMatch(Spec):
    col1: str
    col2: str

    def is_satisfied_by(self, row):
        score = fuzz.token_sort_ratio(
            row[self.col1].casefold(), row[self.col2].casefold()
        )
        print(f"{row[self.col1]} - {row[self.col2]}")
        print(score)
        return score >= 60


@dataclass
class ColContainsAnyWord(Spec):
    col1: str
    words: list[str]

    def is_satisfied_by(self, row):
        col_value_cleaned = str(row[self.col1]).casefold().replace(" ", "")
        return any(
            word.casefold().replace(" ", "") in col_value_cleaned for word in self.words
        )


@dataclass
class ColContainsAnyWordCaseInsensitiveNotTrimmed(Spec):
    col1: str
    words: list[str]

    def is_satisfied_by(self, row):
        col_value_cleaned = str(row[self.col1])
        return any(word in col_value_cleaned for word in self.words)


@dataclass
class ColContainsAnyWordRaw(Spec):
    col1: str
    words: list[str]

    def is_satisfied_by(self, row):
        return any(word in row[self.col1] for word in self.words)


@dataclass
class ColContainsAnyWordSeparatedWithWhiteSpace(Spec):
    col1: str
    words: list[str]

    def is_satisfied_by(self, row):
        col_value_cleaned = str(row[self.col1]).casefold()
        tokens = col_value_cleaned.split()
        words_cleaned = [w.casefold() for w in self.words]
        return any(word in tokens for word in words_cleaned)


@dataclass
class ColContainsColCaseSensitiveTrimmed(Spec):
    col1: str
    col2: str

    def is_satisfied_by(self, row):
        return str(row[self.col2]).casefold().replace(" ", "") in str(
            row[self.col1]
        ).casefold().replace(" ", "")


@dataclass
class ColEqualsValue(Spec):
    col: str
    value: object

    def is_satisfied_by(self, row):
        return row[self.col] == self.value


@dataclass
class Always(Spec):
    def is_satisfied_by(self, row):
        return True


@dataclass
class ColIdentifierIsEIK(Spec):
    col: str

    def is_satisfied_by(self, row):
        val = row[self.col]

        # if pd.isna(val):
            # return True

        s = str(val).strip()
        return len(s) == 9 or len(s) == 13


@dataclass
class ColIdentifierIsEGN(Spec):
    col: str

    def is_satisfied_by(self, row):
        val = row[self.col]

        if pd.isna(val):
            return True

        s = str(val).strip()
        return len(s) == 10
