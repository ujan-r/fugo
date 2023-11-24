__all__ = ['Size', 'Quality']

from enum import Enum, auto


class Size(Enum):
    UNISON = 0
    SECOND = 1
    THIRD = 2
    FOURTH = 3
    FIFTH = 4
    SIXTH = 5
    SEVENTH = 6
    OCTAVE = 7

    # Replace compound intervals with their simple equivalents.
    @classmethod
    def _missing_(cls, value: int):
        return cls(value % 7 or 7)


class Quality(Enum):
    PERFECT = auto()
    MAJOR = auto()
    MINOR = auto()
    DIMINISHED = auto()
    AUGMENTED = auto()
