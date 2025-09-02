from __future__ import annotations
from dataclasses import dataclass
import pandas as pd


class Spec:
    def is_satisfied_by(self, row: pd.Series) -> bool:
        raise NotImplementedError

    def __and__(self, other: "Spec") -> "Spec":
        return And(self, other)

    def __or__(self, other: "Spec") -> "Spec":
        return Or(self, other)

    def __invert__(self) -> "Spec":
        return Not(self)


@dataclass
class And(Spec):
    a: Spec
    b: Spec

    def is_satisfied_by(self, row):
        return self.a.is_satisfied_by(row) and self.b.is_satisfied_by(row)


@dataclass
class Or(Spec):
    a: Spec
    b: Spec

    def is_satisfied_by(self, row):
        return self.a.is_satisfied_by(row) or self.b.is_satisfied_by(row)


@dataclass
class Not(Spec):
    a: Spec

    def is_satisfied_by(self, row):
        return not self.a.is_satisfied_by(row)
