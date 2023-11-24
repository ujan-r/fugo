__all__ = ['Accidental', 'LetterName']

from enum import Enum


class LetterName(Enum):
    C = 0
    D = 2
    E = 4
    F = 5
    G = 7
    A = 9
    B = 11

    def __init__(self, steps_above_C: int):
        self.steps_above_C = steps_above_C

    def __repr__(self):
        return f'LetterName.{self.name}'

    @classmethod
    def from_string(cls, /, letter: str) -> 'LetterName':
        try:
            return cls[letter.strip().upper()]
        except KeyError:
            raise ValueError(f'invalid letter: {letter!r}') from None


class Accidental(Enum):
    # fmt: off
    DOUBLE_FLAT  = -2
    FLAT         = -1
    NATURAL      =  0
    SHARP        = +1
    DOUBLE_SHARP = +2
    # fmt: on

    def __init__(self, offset: int):
        self.offset = offset

    @classmethod
    def from_string(cls, /, accidental: str) -> 'Accidental':
        mapping = {
            '𝄫': cls.DOUBLE_FLAT,
            'bb': cls.DOUBLE_FLAT,
            '♭': cls.FLAT,
            'b': cls.FLAT,
            '♮': cls.NATURAL,
            '': cls.NATURAL,
            '♯': cls.SHARP,
            '#': cls.SHARP,
            '𝄪': cls.DOUBLE_SHARP,
            'x': cls.DOUBLE_SHARP,
        }

        try:
            return mapping[accidental.strip()]
        except KeyError:
            raise ValueError(f'invalid accidental: {accidental!r}') from None
