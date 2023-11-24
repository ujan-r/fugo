__all__ = ['Size', 'Quality']

from enum import Enum, auto


class Size(Enum):
    # fmt: off
    UNISON  = 0
    SECOND  = 1
    THIRD   = 2
    FOURTH  = 3
    FIFTH   = 4
    SIXTH   = 5
    SEVENTH = 6
    OCTAVE  = 7
    # fmt: on

    # Replace compound intervals with their simple equivalents.
    @classmethod
    def _missing_(cls, value: int):
        return cls(value % 7 or 7)

    def __invert__(self):
        return Size(7 - self.value)


class Quality(Enum):
    # fmt: off
    DIMINISHED = auto()
    MINOR      = auto()
    PERFECT    = auto()
    MAJOR      = auto()
    AUGMENTED  = auto()
    # fmt: on
