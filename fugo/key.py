__all__ = ['Mode', 'Degree']

from enum import Enum, auto

from fugo import Interval


class Mode(Enum):
    parse = lambda s: tuple(Interval(i) for i in s.split())
    # fmt: off
    MAJOR = IONIAN  = parse('P1 M2 M3 P4 P5 M6 M7')
    DORIAN          = parse('P1 M2 m3 P4 P5 M6 m7')
    PHRYGIAN        = parse('P1 m2 m3 P4 P5 m6 m7')
    LYDIAN          = parse('P1 M2 M3 A4 P5 M6 M7')
    MIXOLYDIAN      = parse('P1 M2 M3 P4 P5 M6 m7')
    MINOR = AEOLIAN = parse('P1 M2 m3 P4 P5 m6 m7')
    LOCRIAN         = parse('P1 m2 m3 P4 d5 m6 m7')
    # fmt: on
    del parse

    @property
    def intervals(self) -> tuple[Interval, ...]:
        return self.value

    def __len__(self):
        return len(self.intervals)


class Degree(Enum):
    """Represent a scale degree."""

    # fmt: off
    TONIC        = auto()
    SUPERTONIC   = auto()
    MEDIANT      = auto()
    SUBDOMINANT  = auto()
    DOMINANT     = auto()
    SUBMEDIANT   = auto()
    LEADING_TONE = auto()
    SUBTONIC     = auto()
    SEVENTH      = auto()

    FIRST   = TONIC
    SECOND  = SUPERTONIC
    THIRD   = MEDIANT
    FOURTH  = SUBDOMINANT
    FIFTH   = DOMINANT
    SIXTH   = SUBMEDIANT
    # fmt: on

    @classmethod
    def _missing_(cls, degree: int):
        if degree < 1:
            raise ValueError(f'invalid scale degree ({degree!r})')

        i = degree - 1
        degrees = [
            cls.FIRST,
            cls.SECOND,
            cls.THIRD,
            cls.FOURTH,
            cls.FIFTH,
            cls.SIXTH,
            cls.SEVENTH,
        ]
        return degrees[i]
